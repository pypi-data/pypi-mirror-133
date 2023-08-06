import argparse

def show_banner():
	banner = """
=================================================\n\n
                 はぁって言うゲーム\n\n
=================================================\n\n
	"""	
	print(banner)


def show_players(players):
	player_list = "Players: "
	for i, name in enumerate(players):
		player_list += name
		if not i == len(players) - 1:
			player_list += " / "
	player_list += "\n\n"

	print(player_list)


def parse_user_option():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--newname', action='store_true', help='define new players for this game (new players will not be saved after the game)')
	parser.add_argument('-s', '--skip', action='store_true', help='skip through the process where the assigned action of each player will be displayed on the screen in turns')
	return parser.parse_args()


def print_topic(topic):
	print("====================================", end="\n\n")
	print("Topic:", topic['Topic'], end="\n\n")
	print("Notes:", topic['Notes'], end="\n\n")
	print("Act A:", topic['A'], end="\n\n")
	print("Act B:", topic['B'], end="\n\n")
	print("Act C:", topic['C'], end="\n\n")
	print("Act D:", topic['D'], end="\n\n")
	print("Act E:", topic['E'], end="\n\n")
	print("Act F:", topic['F'], end="\n\n")
	print("Act G:", topic['G'], end="\n\n")
	print("Act H:", topic['H'], end="\n\n")
	print("====================================", end="\n\n")


def get_topic_string(topic):
	return f"""\n
=======================\n
テーマ: {topic['Topic']}\n
指示: {topic['Notes']}\n
A: {topic['A']}\n
B: {topic['B']}\n
C: {topic['C']}\n
D: {topic['D']}\n
E: {topic['E']}\n
F: {topic['F']}\n
G: {topic['G']}\n
H: {topic['H']}\n
=======================\n\n
"""