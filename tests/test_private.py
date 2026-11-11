import pytest
from tenplayer_plot.private_func import normalize_player_name

def test_normalize_player_name():
	assert normalize_player_name("serena williams") == "SerenaWilliams"
	assert normalize_player_name("Serena Williams") == "SerenaWilliams"
	assert normalize_player_name("SerenaWilliams") == "SerenaWilliams"
	assert normalize_player_name("rafael nadal") == "RafaelNadal"