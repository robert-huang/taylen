import logging

from slack import WebClient

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
    def handle_slack(client: WebClient, event: dict):
        logger.info("")
        client.chat_postMessage(
            text='pong',
            channel=event['channel']
        )
