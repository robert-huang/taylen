import asyncio
import logging
import os
import threading

import discord
from discord import Message
from django.conf import settings

from app.bot import handle_discord

logger = logging.getLogger('default')

loop = asyncio.new_event_loop()
client = discord.Client(shard_count=2, loop=loop)


def send_message(guild, channel, msg):
    asyncio.run_coroutine_threadsafe(client.get_guild(guild).get_channel(channel).send(msg), loop)


@client.event
async def on_ready():
    logger.info(f"[user={client.user}] [shard_id={client.shard_id}]")


@client.event
async def on_message(message: Message):
    logger.info(f"[user={message.author}] [content={message.content}]")
    await handle_discord(message)


async def run_discord_bot():
    # Gunicorn/Heroku runs our workers on PIDs 10 and 11 always.
    client.shard_id = 11 - os.getpid()
    await client.start(settings.DISCORD_TOKEN)


def start():
    loop.create_task(run_discord_bot())
    thread = threading.Thread(target=lambda: loop.run_forever())
    thread.setDaemon(True)
    thread.start()
