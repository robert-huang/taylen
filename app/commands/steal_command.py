import logging
import re

import requests
from discord import Message, Forbidden, HTTPException

from app.slack.slack_client import SlackClient

logger = logging.getLogger('default')

help_message = """```
Takes the <emoji> give and adds it to the current server with the <name> given.

Usage: 
> .steal <emoji> <name>

Examples:
> .steal :MikuStare: kt_stare
```"""


class StealCommand:
    @staticmethod
    async def handle_discord(message: Message, url: str, name: str):
        logger.info(f"[url={url}] [name={name}]")
        if re.match(r'<:[A-Za-z0-9_]+:[0-9]+>', url):
            url = f"https://cdn.discordapp.com/emojis/{url[1:-1].split(':')[2]}.png"

        elif re.match(r'<a:[A-Za-z0-9_]+:[0-9]+>', url):
            url = f"https://cdn.discordapp.com/emojis/{url[1:-1].split(':')[2]}.gif"
        else:
            return await message.channel.send('Is that even an emoji?')

        response = requests.get(url)
        if response.status_code != 200:
            return await message.channel.send(f'Failed to download that emoji: {response.reason}')

        try:
            await message.guild.create_custom_emoji(name=name, image=response.content)
        except Forbidden:
            return await message.channel.send('Please give me more permissions..')
        except HTTPException as e:
            return await message.channel.send(f'I tried my best but: {e}')

        await message.add_reaction('✅')

    @staticmethod
    def handle_slack(client: SlackClient, event: dict):
        logger.info("")
