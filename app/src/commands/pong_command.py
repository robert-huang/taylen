import logging

from app.src.slack.slack_client import SlackClient

logger = logging.getLogger('default')

help_message = """```
The bot will respond with ping.

Usage: 
> .pong
```"""


class PongCommand:
    @staticmethod
    async def handle_discord(message):
        logger.info("")
        await message.channel.send('ping')

    @staticmethod
    def handle_slack(client: SlackClient, event: dict):
        logger.info("")
        client.post_message(event, 'ping')
