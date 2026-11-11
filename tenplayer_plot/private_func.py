import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

def normalize_player_name(player_name):
	""" Normalize a player's name for URL."""
	# Check if input is a string
	if not isinstance(player_name, str):
		raise TypeError("Player name must be a string.")

	# Check for empty string
	if not player_name.strip():
		raise TypeError("Player name can't be empty string.")
	
	if " " in player_name:
		return "".join(word.capitalize() for word in player_name.split())
	else:
		return player_name

def fetch_player_js(player_name):
	"""Download a player's career JS file."""
	# Build the url
	url = f"https://www.tennisabstract.com/jsmatches/{player_name}Career.js"

	# Retrieve the file
	response = requests.get(url)

	# Raise error for invalid name
	if response.status_code == 404:
		raise ValueError(f"Player '{player_name}' not found.")

	#Check that it has match data var
	if "var morematchmx" not in response.text:
		raise ValueError("Invalid career JS file, no Match Record.")
	
	return response.text

def js_to_df(js_file):
	""" Parse JS content into a pandas DataFrame."""
	matches = js_file.read()
	
	ranges = matches.split("=", 1)[1].strip()
	ranges = ranges.removesuffix(";").strip()
	
	matches_list = json.loads(ranges)
	return pd.DataFrame(matches_list)

def get_player_dob(player_name):
	"""Retrieve a player's date of birth from Tennis Abstract."""
	url = (f"https://www.tennisabstract.com/cgi-bin/wplayer-classic.cgi?p={name}")

	response = requests.get(url)

	# Fetch the DOB, looking specifically at the section where it contains the DOB
	soup = BeautifulSoup(response.text, "html.parser")
	bio = soup.find(id="biog")
	if bio is None:
		raise ValueError("Player biography not found.")

	dob = re.search(r"\((\d{1,2}-[A-Za-z]{3}-\d{4})\)", bio.get_text())

	return pd.to_datetime(dob.group(1), format="%d-%b-%Y")
	