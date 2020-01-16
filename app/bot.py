import re

from discord import Message
from pyparsing import ParseException

from app.commands.avatar_command import AvatarCommand
from app.commands.help_command import HelpCommand
from app.commands.mmr_command import MmrCommand
from app.commands.ping_command import PingCommand
from app.commands.pong_command import PongCommand
from app.commands.record_command import RecordCommand
from app.commands.splitwise_command import SplitwiseCommand
from app.commands.steal_command import StealCommand
from app.discord import discord_grammar
from app.slack import slack_grammar
from app.slack.slack_client import client

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
    '.record': RecordCommand()
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
