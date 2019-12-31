import logging

from slack import WebClient

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
    def handle_slack(client: WebClient, event: dict):
        logger.info("")
        client.chat_postMessage(
            text='ping',
            channel=event['channel']
        )
