def normalize_player_name(player_name):
	""" Normalize a player's name for URL."""
	# Check if input is a string
	if not isinstance(player_name, str):
		raise TypeError("Player name must be a string.")

	# Check for empty string
	if not player_namestrip():
		raise TypeError("Player name can't be empty string.")
	
	if " " in player_name:
		return "".join(
        word.capitalize() for word in player_name.split()
    )
	else:
		return player_name