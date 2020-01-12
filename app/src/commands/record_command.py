import logging

from django.core.exceptions import ObjectDoesNotExist

from app.models import Emoji
from app.src.slack.slack_client import SlackClient

logger = logging.getLogger('default')

help_message = """```
The bot will respond with the given emoji's record

Usage: 
> .record <emoji>

Arguments:
- emoji: an emoji

Examples:
> .record :simple_smile:
```"""


class RecordCommand:
    @staticmethod
    async def handle_discord(message):
        logger.info("")

    @staticmethod
    def handle_slack(client: SlackClient, event: dict, emoji_name: str):
        logger.info(f"[emoji_name={emoji_name}]")
        try:
            emoji = Emoji.objects.get(name=emoji_name)
            client.post_message(event, emoji.record())
        except ObjectDoesNotExist:
            client.post_message(event, 'Could not found that emoji sry')
