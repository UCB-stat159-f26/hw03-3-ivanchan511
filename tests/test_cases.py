import pytest
import pandas as pd
from bs4 import BeautifulSoup
from tenplayer_plot.private_func import normalize_player_name, js_to_df

def test_normalize_player_name():
	assert normalize_player_name("serena williams") == "SerenaWilliams"
	assert normalize_player_name("Serena Williams") == "SerenaWilliams"
	assert normalize_player_name("SerenaWilliams") == "SerenaWilliams"
	assert normalize_player_name("rafael nadal") == "RafaelNadal"

def test_js_to_df():
	with open("tests/js_for_testing/FemalePlayerCareer.js") as file:
		female_df = js_to_df(file)

	with open("tests/js_for_testing/MalePlayerCareer.js") as file:
		male_df = js_to_df(file)

	assert isinstance(female_df, pd.DataFrame)
	assert isinstance(male_df, pd.DataFrame)