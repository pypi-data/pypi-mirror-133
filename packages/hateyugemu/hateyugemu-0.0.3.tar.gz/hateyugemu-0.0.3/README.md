# Hateyugemu
<a href="https://pypi.org/project/hateyugemu/"><img src="https://img.shields.io/pypi/v/hateyugemu" alt="pypi badge"></a>
<a href="https://github.com/kaiwinut/hateyugemu"><img src="https://img.shields.io/github/license/kaiwinut/hateyugemu?color=blue" alt="license badge"></a>
<a href="https://github.com/kaiwinut/hateyugemu"><img src="https://img.shields.io/github/release-date/kaiwinut/hateyugemu" alt="release date badge"></a>

A digital remake of [a popular board game](https://www.gentosha-edu.co.jp/book/index.php?book_no=378746&changeview=pc) in Japan that integrates [LINE Notify](https://notify-bot.line.me/en/) in order to send content to players.

## Usage
###### Step 1 
Create the following files before the game begins:

- [ ] A player list containing LINE Notify tokens, as shown in [tokens.txt](https://github.com/kaiwinut/hateyugemu/blob/main/src/hateyugemu/data/tokens.txt)
- [ ] A list of topics gathered from the Internet or created on your own, following the format in [topics.csv](https://github.com/kaiwinut/hateyugemu/blob/main/src/hateyugemu/data/topics.csv)

###### Step 2
Install the package and run the module (see the Notes section below for options you can specify)

`pip install hateyugemu`

`python3 -m hateyugemu`

The first time you run the program, it will ask you to update your tokens file and topics file. Provide the path to these file and your game will begin. 

###### Notes
You can leave the tokens as empty strings in the tokens file if you don't need to use LINE Notify to receive game content. Instead of making a new tokens list everytime the player changes, you can also use the `--newname` option to create new players (the new players **will NOT be saved after the game**). 

Also, if you are using LINE Notify to receive game content, you might wish to use the `--skip` option to skip through the process where the assigned action of each player will be displayed on the screen in turns.