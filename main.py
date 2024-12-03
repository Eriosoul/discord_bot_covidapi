import json
import os
import discord
from cogs.bot_patata import MyBot


def main():
    if os.path.exists('cogs/config.json'):
        with open('cogs/config.json') as f:
            config_data = json.load(f)
    else:
        template: dict = {'prefix!':'!', 'token': ""}
        with open('cogs/config.json', 'w') as f:
            json.dump(template, f)

    prefix: str = config_data["prefix!"]
    token: str = config_data["token"]
    intent = discord.Intents.all()

    bot = MyBot(prefix=prefix, token=token, intent=intent)
    bot.run(token)


if __name__ == '__main__':
    main()