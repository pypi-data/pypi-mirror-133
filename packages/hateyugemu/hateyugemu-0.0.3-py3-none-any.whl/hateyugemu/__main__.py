import os
from .main import main, setup_bot
from .settings import init_tokens_settings, init_topics_settings


tokens_path = os.path.join(os.path.dirname(__file__), 'data', 'tokens.txt')
topics_path = os.path.join(os.path.dirname(__file__), 'data', 'topics.csv')


if not os.path.exists(tokens_path):
	print("Tokens settings file is missing. Initializing settings...")	
	init_tokens_settings()

elif input("Update tokens? [y/n]  ") == 'y':
	init_tokens_settings()


if not os.path.exists(topics_path):
	print("Topics settings file is missing. Initializing settings...")	
	init_topics_settings()

elif input("Update topics? [y/n]  ") == 'y':
	init_topics_settings()


if os.path.exists(topics_path):
	with open(topics_path, 'r') as f:
		line_count = 0
		for line in f:
			if line != '\n':
				line_count += 1
	if line_count < 3:
		print("Need at least 3 topics to start. Initializing settings...")
		init_topics_settings()


main(topics_path, setup_bot())