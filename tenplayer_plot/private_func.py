import requests
import json
import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

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

# For Main Function `plot_player_data`
def check_dataframe(player_df):
	""" Check input DataFrame have the required columns"""
	required_columns = ["match_date", "win/loss", "player_age_at_match", "age_difference"]
	
	# Check if there's missing required columns
	missing_columns = [col for col in required_columns 
					   if col not in player_df.columns]

	# Raise warning for missing columns
	if missing_columns:
		raise ValueError(f"Missing required columns: {missing_columns}")

def create_plot():
	""" Initialize the figure and axes."""
	return plt.subplots(figsize=(12, 7.5))

def plot_win_loss_results(player_df, ax):
	""" Add separate scatter points for wins and losses."""
	results = [
		("W", "deepskyblue", "Match won"),
		("L", "indigo", "Match lost")
	]

	for outcome, color, label in results:
		subset = player_df.loc[player_df["win/loss"] == outcome]
		ax.scatter(subset["player_age_at_match"], subset["age_difference"],
				   c=color, s=10, label=label, zorder=0)

	# Add the horizontal line at age_difference = 0
	ax.axhline(0, color = "dimgray", linewidth = 0.6, zorder = 1)

## Sub-helper Function for format_axes
def give_min_max(player_df, column):
	""" Return the minimum and maximum of a given DataFrame Column"""
	col_min = player_df[column].min()
	col_max = player_df[column].max()
	return col_min, col_max

def format_axes(ax, player_df):
	""" Set axis ticks, and limits."""
	age_min, age_max = give_min_max(player_df, "player_age_at_match")
	diff_min, diff_max = give_min_max(player_df, "age_difference")
	
	x_min = np.floor(age_min / 2) * 2
	x_max = np.ceil(age_max / 2) * 2

	y_min = np.floor(diff_min / 5) * 5
	y_max = np.ceil(diff_max / 5) * 5

	ax.set_xticks(np.arange(x_min, x_max + 1, 2))
	ax.set_yticks(np.arange(y_min, y_max + 1, 10))

	ax.set_xlim(x_min - 0.5, x_max + 0.5)
	ax.set_ylim(y_min, y_max)

	ax.xaxis.tick_top()
	ax.xaxis.set_label_position("top")

	ax.tick_params(axis = 'x', colors = 'dimgray')
	ax.tick_params(axis = 'y', colors = 'dimgray')

def format_legend_grid(ax):
	""" Set axis legend, and grid."""
	ax.grid(True, axis = "both", color = "lightgray", linewidth = 1, alpha = 1.0)
	ax.set_axisbelow(True)

	## No Borders
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines["left"].set_visible(False)
	
	ax.spines["bottom"].set_color("lightgray")
	ax.spines["bottom"].set_linewidth(0.8)

	# Legend on the top
	ax.legend(loc = "upper center", bbox_to_anchor = (0.5, 1.125), ncol = 2, frameon = False)

def format_y_labels(ax):
	def format_temp(x, pos):
	    if x > 0:
	        return f"+{int(x)} Years"
	    elif x == 0:
	        return "Same age"
	    else:
	        return f"{int(x)} Years"

	ax.yaxis.set_major_formatter(FuncFormatter(format_temp))

def add_axis_labels(ax):
	## axis additional labels
	ax.text(0.01, 1.06,
	        "Player’s age:",
	        transform = ax.transAxes,
	        fontsize = 9,
	        ha = "left",
		    color = "dimgray")

	ax.text(-0.08, 1.00,
	        "Opponent’s\nAge\nDifference:",
	        transform = ax.transAxes,
	        fontsize = 9,
	        ha = "left",
		    color = "dimgray")

def add_title(ax, player_df, player_name = ""):
	""" Add a title using the player's name (if provided) and career age range."""
	age_min, age_max = give_min_max(player_df, "player_age_at_match")
	age_min = int(np.floor(age_min))
	age_max = int(np.ceil(age_max))

	if player_name:
		title = f"{player_name}'s Professional Matches, Age {age_min} to {age_max}"
	else:
		title = f"Player Professional Matches, Age {age_min} to {age_max}"
	
	ax.set_title(title,
			 fontsize = 12,
			 fontweight = "bold",
			 pad = 50)