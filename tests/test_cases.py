import pytest
import pandas as pd
from tenplayer_plot.private_func import normalize_player_name, js_to_df, identify_gender, organize_player_df, calculate_age_difference

# Open the two test data file for our test cases
with open("tests/js_for_testing/FemalePlayerCareer.js") as file:
	female_js = file.read()
	female_df = js_to_df(female_js)

with open("tests/js_for_testing/MalePlayerCareer.js") as file:
	male_js = file.read()
	male_df = js_to_df(male_js)

## Test our helper functions for get_player_data()
def test_normalize_player_name():
	assert normalize_player_name("serena williams") == "SerenaWilliams"
	assert normalize_player_name("Serena Williams") == "SerenaWilliams"
	assert normalize_player_name("SerenaWilliams") == "SerenaWilliams"
	assert normalize_player_name("rafael nadal") == "RafaelNadal"

def test_js_to_df():
	assert isinstance(female_df, pd.DataFrame)
	assert isinstance(male_df, pd.DataFrame)

	assert len(female_df) == 3
	assert len(male_df) == 3

def test_identify_gender():
	assert identify_gender(female_df) == "F"
	assert identify_gender(male_df) == "M"

def test_organize_player_df():
	female_org = organize_player_df(female_df)
	male_org = organize_player_df(male_df)

	assert list(female_org.columns) == ["match_date", "win/loss", "opponent_name", "opponent_dob"]
	assert list(male_org.columns) == ["match_date", "win/loss", "opponent_name", "opponent_age_at_match"]

	assert female_org.attrs["gender"] == "F"
	assert male_org.attrs["gender"] == "M"

def test_calculate_age_difference():
	female_org = organize_player_df(female_df)
	male_org = organize_player_df(male_df)

	# Random DOB for testing purposes
	female_result = calculate_age_difference(female_org, pd.Timestamp("1981-09-26"))
	male_result = calculate_age_difference(male_org, pd.Timestamp("1980-01-01"))

	# Check that age columns are in the result DataFrame
	assert "player_age_at_match" in female_result.columns
	assert "opponent_age_at_match" in female_result.columns
	assert "age_difference" in female_result.columns

	# Check female opponent age calculation
	assert round(female_result.iloc[0]["opponent_age_at_match"], 2) == 18.78

	# Check male opponent age is unchanged
	assert round(male_result.iloc[0]["opponent_age_at_match"], 6) == 22.264203

	# Check age difference calculation
	assert round(female_result.iloc[0]["age_difference"], 2) == -4.68
	