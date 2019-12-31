import difflib
import itertools
import logging
import re

from discord import Message
from slack import WebClient

logger = logging.getLogger('default')

help_message = """```
Posts a full size image of a users avatar. This uses a fuzzy search
so you can @ the user, type their name, or type their nickname.

Usage: 
> .avatar <user query>

Examples:
> .avatar @tso
> .avatar tso
> .avatar great nickname
```"""


class AvatarCommand:
    @staticmethod
    async def handle_discord(message: Message, query: str):
        logger.info(f"[query={query}]")
        if re.match(r'<@![0-9]+>', query):
            query = str(query[3:-1])

        guild_members = message.guild.members
        search_criteria = [[member.name, str(member.id), member.display_name] for member in guild_members]
        flattened = list(itertools.chain(*search_criteria))
        match = difflib.get_close_matches(query, flattened, n=1, cutoff=0)
        i = flattened.index(match[0])
        await message.channel.send(guild_members[i // 3].avatar_url_as(static_format='png'))

    @staticmethod
    def handle_slack(client: WebClient, event: dict):
        logger.info("")
