import logging

from app.src.slack.slack_client import SlackClient

logger = logging.getLogger('default')

help_message = """```
The bot will respond with pong.

Usage: 
> .ping
```"""


class PingCommand:
    @staticmethod
    async def handle_discord(message):
        logger.info("")
        await message.channel.send('pong')

    @staticmethod
    def handle_slack(client: SlackClient, event: dict):
        logger.info("")
        client.post_message(event, 'pong')
