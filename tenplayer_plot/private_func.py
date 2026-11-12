import requests
import json
import pandas as pd
import re

# For Main Function `get_player_data`
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

def js_to_df(js_content):
	""" Parse JS content into a pandas DataFrame."""
	ranges = js_content.split("=", 1)[1].strip()
	ranges = ranges.removesuffix(";").strip()
	
	matches_list = json.loads(ranges)
	return pd.DataFrame(matches_list)

def get_player_dob(player_name):
	"""Retrieve a player's date of birth from Tennis Abstract."""
	name = normalize_player_name(player_name)
	url = f"https://www.tennisabstract.com/jsmatches/{name}.js"

	response = requests.get(url, timeout=30)

	dob_match = re.search(r"\bvar\s+dob\s*=\s*(\d{8})\s*;", response.text)
	
	if dob_match is None:
		raise ValueError("Player date of birth not found.")

	return pd.to_datetime(dob_match.group(1), format="%Y%m%d")

def identify_gender(player_df):
	""" Identify whether the player is female or male."""
	identifier = player_df.iloc[0, 16]

	# If it's DOB, which would be a string and 8 digits long --> Female
	if isinstance(identifier, str) and len(identifier) == 8 and identifier.isdigit():
		return "F"
	return "M"

def organize_player_df(player_df):
	""" Organize and Return Simplified Player Data with Neccessary Columns."""
	gender = identify_gender(player_df)
	match_data = player_df.iloc[:, [0, 4, 11, 16]].copy()

	# Rename columns
	columns = ["match_date", "win/loss", "opponent_name"]
	if gender == "F":
		columns.append("opponent_dob")
	else:
		columns.append("opponent_age_at_match")
	match_data.columns = columns

	# Convert Dates to datetime object
	match_data["match_date"] = pd.to_datetime(match_data["match_date"], format="%Y%m%d", errors="coerce")
	match_data.attrs["gender"] = gender
	return match_data


def calculate_age_difference(player_df, player_dob):
	""" Calculate player age and/or opponent age, along with age difference."""
	gender = player_df.attrs["gender"]

	# Calculate player_age_at_match
	player_df["player_age_at_match"] = (player_df["match_date"] - player_dob).dt.days / 365.2425

	if gender == "F":
		opponent_dob = pd.to_datetime(player_df["opponent_dob"], format="%Y%m%d", errors="coerce")
		player_df["opponent_age_at_match"] = (player_df["match_date"] - opponent_dob).dt.days / 365.2425
	else:
		player_df["opponent_age_at_match"] = pd.to_numeric(player_df["opponent_age_at_match"], errors="coerce")

	player_df["age_difference"] = player_df["player_age_at_match"] - player_df["opponent_age_at_match"] 
	
	return player_df