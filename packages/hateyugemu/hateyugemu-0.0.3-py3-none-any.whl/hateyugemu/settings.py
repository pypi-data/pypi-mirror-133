import os

def init_tokens_settings():
	tokens_path = input("Enter path to tokens.txt: ")
	while not os.path.exists(tokens_path):
		print(f"Cannot find tokens file at {tokens_path}")
		tokens_path = input("Enter path to tokens.txt: ")

	with open(tokens_path, 'r') as f:
		tokens = f.read()

	tokens_settings_path = os.path.join(os.path.dirname(__file__), 'data', 'tokens.txt')
	with open(tokens_settings_path, 'w') as f:
		print(f"Writing to {tokens_settings_path}")
		print(tokens)
		f.write(tokens)

def init_topics_settings():
	topics_path = input("Enter path to topics.csv: ")
	while not os.path.exists(topics_path):
		print(f"Cannot find topics file at {topics_path}")
		topics_path = input("Enter path to topics.csv: ")

	with open(topics_path, 'r') as f:
		topics = f.read()

	topics_settings_path = os.path.join(os.path.dirname(__file__), 'data', 'topics.csv')
	with open(topics_settings_path, 'w') as f:
		print(f"Writing to {topics_settings_path}")
		print(topics)
		f.write(topics)