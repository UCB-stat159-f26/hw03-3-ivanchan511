# Once finished, will uncomment
from .private_func import normalize_player_name, fetch_player_js, js_to_df, get_player_dob, organize_player_df, calculate_age_difference

import pandas as pd

def get_player_data(player_name):
	"""Retrieve and clean a player's career match data, with an additional column of player age and age difference for later plotting."""
	# Validate and organize player_name if possible
	player_name = normalize_player_name(player_name)

	# Retrieve and Turn into DataFrame
	player_js = fetch_player_js(player_name)
	matches = js_to_df(player_js)

	# Retrieve Player DOB
	player_dob = get_player_dob(player_name)

	# Calculate Age and Age Difference
	matches = organize_player_df(matches).copy()
	matches = calculate_age_difference(matches, player_dob)
	# Return Final Cleaned DataFrame
	return matches


# 5. Calculate player and opponent ages and age difference
# 6. Clean and return DataFrame
def plot_player_data(df):
	"""Create a scatter plot of a player's career match results."""
	pass