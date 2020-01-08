import re

from discord import Message
from pyparsing import ParseException

from app.src.commands.avatar_command import AvatarCommand
from app.src.commands.help_command import HelpCommand
from app.src.commands.mmr_command import MmrCommand
from app.src.commands.ping_command import PingCommand
from app.src.commands.pong_command import PongCommand
from app.src.commands.splitwise_command import SplitwiseCommand
from app.src.commands.steal_command import StealCommand
from app.src.discord import discord_grammar
from app.src.slack import slack_grammar
from app.src.slack.slack_client import client

shared_cmd_map = {
    '.ping': PingCommand(),
    '.pong': PongCommand(),
    '.help': HelpCommand(),
    '.mmr': MmrCommand()
}

discord_cmd_map = {
    **shared_cmd_map,
    '.steal': StealCommand(),
    '.avatar': AvatarCommand()
}

slack_cmd_map = {
    **shared_cmd_map,
    '.sw': SplitwiseCommand(),
}


async def handle_discord(message: Message):
    try:
        parsed = discord_grammar.grammar.parseString(message.content, True)
        await discord_cmd_map[parsed[0]].handle_discord(message, *parsed[1:])
    except ParseException:
        pass


def handle_slack(event):
    text: str = event['text']
    try:
        parsed = slack_grammar.grammar.parseString(text, True)
        slack_cmd_map[parsed[0]].handle_slack(client, event, *parsed[1:])
    except ParseException:
        if re.match(r'\.[a-zA-Z]+( .*)?', text):
            client.react(event, 'confused-lump')
