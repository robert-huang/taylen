import logging

from app.slack.slack_client import SlackClient
from . import ping_command, pong_command, splitwise_command, steal_command, avatar_command, mmr_command, record_command

logger = logging.getLogger('default')

slack_help_message = """```
To know more about a given command use `.help <command>`

Commands:
- .help
- .ping
- .pong
- .sw <amount> <direction> <user> <description...> 
- .mmr <query> <filters...>
- .record <emoji>
```"""

discord_help_message = """```
To know more about a given command use `.help <command>`

Commands:
- .help
- .ping
- .pong
- .steal <emoji> <name>
- .avatar <query>
. .mmr <query> <filters...>
```"""

help_messages = {
    'help': 'Are you serious?',
    'ping': ping_command.help_message,
    'pong': pong_command.help_message,
    'sw': splitwise_command.help_message,
    'steal': steal_command.help_message,
    'avatar': avatar_command.help_message,
    'mmr': mmr_command.help_message,
    'record': record_command.help_message,
}


class HelpCommand:
    @staticmethod
    async def handle_discord(message, command: str = None):
        logger.info(f"[command={command}]")
        text = help_messages.get(command, discord_help_message)
        await message.channel.send(text)

    @staticmethod
    def handle_slack(client: SlackClient, event: dict, command: str = None):
        logger.info(f"[command={command}]")
        text = help_messages.get(command, slack_help_message)
        client.post_message(event, text)
