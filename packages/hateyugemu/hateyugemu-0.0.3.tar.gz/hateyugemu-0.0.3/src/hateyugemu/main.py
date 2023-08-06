import os
import sys
import json
import random
import pandas as pd
from .notify import LINENotifyBot
from .utils import *

args = parse_user_option()

def generate_topic(data):
	idx = random.randint(0, len(data) - 1)
	topic = {'Topic': data.loc[idx]['Topic'], 
			'Notes': data.loc[idx]['Notes'], 
			'A': data.loc[idx]['A'], 
			'B': data.loc[idx]['B'], 
			'C': data.loc[idx]['C'], 
			'D': data.loc[idx]['D'], 
			'E': data.loc[idx]['E'], 
			'F': data.loc[idx]['F'],
			'G': data.loc[idx]['G'],
			'H': data.loc[idx]['H']}
	print_topic(topic)
	return idx, topic


def generate_act():
	acts = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
	for act in random.sample(acts, len(acts)):
		yield act


def start_round(topic, players, bots, act):
	for player in random.sample(players, len(players)):
		try:
			os.system('clear')
			action = next(act)

			if not args.skip:
				print("Press enter to view " + player + "'s action")
				input()

			action_msg = action + ": " + topic[action]

			if not args.skip:
				print(action_msg, end = "\n\n")

			if bots[player] is not None:
				bots[player].send(msg = get_topic_string(topic) + player + "のお題は↓\n" + action_msg)

			if not args.skip:
				print("Press enter if you finish checking your action...")
				input()
		except StopIteration:
			break


def setup_bot():
	bots = {k: LINENotifyBot(token = v) if v != "" else None for k, v in setup().items()}
	return bots


def setup():
	if args.newname:
		players = {}
		input_str = input("Enter number of players: ")
		try: 
			n = int(input_str)
		except Exception as e:
			print(e)
			print("Number of players should be an integer.")
			raise e

		for i in range(n):
			name = input("Player " + str(i + 1) + ": ")
			while name == "":
				print("Name should not be empty.")
				name = input("Player " + str(i + 1) + ": ")
			token = input("LINE Notify token of player " + str(i + 1) + ": ")
			players[name] = token

		return players
	else:
		path = os.path.join(os.path.dirname(__file__), 'data', 'tokens.txt')
		if os.path.exists(path):
			with open(path, 'r') as f:
				data = f.read()
			return json.loads(data)
		else:
			raise Exception(f"Could not load existing tokens data from {path}. Use the --newname option to create new users or create a tokens.txt file.")


def main(path, bots):
	# Initialize player
	players = bots.keys()

	# Prepare topics
	topic_data = pd.read_csv(path)
	topic_data = topic_data.fillna({'Notes': "-"})

	# Welcoming
	os.system('clear')
	show_banner()
	show_players(players)
	print("Press enter to continue or enter q to quit...")
	sys.exit() if input() == 'q' else os.system('clear')

	# Main game loop
	while len(topic_data) > 0:
		# Generate new topic		
		os.system('clear')
		idx, topic = generate_topic(topic_data)
		topic_data = topic_data.drop([idx])
		input("Press enter to view your actions...")

		# Check actions
		start_round(topic, players, bots, generate_act())
		os.system('clear')

		# Vote
		print_topic(topic)
		print("Start voting...", end = "\n\n")

		# Go to new topic
		if input("Press enter to go to the next topic or enter q to quit...") == 'q':
			sys.exit()

	print("No more topics left...")


if __name__ == '__main__':
	main('data/topics.csv', setup_bot())