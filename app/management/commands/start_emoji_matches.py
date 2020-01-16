import time
from random import shuffle
from typing import Dict

from constance import config
from django.core.management.base import BaseCommand

from app.models import Emoji, EmojiMatch
from app.slack.slack_client import client
from app.util import chunker


class Command(BaseCommand):
    def handle(self, *args, **options):
        emojis: Dict[str, int] = {}
        for emoji in Emoji.objects.order_by('?').all():
            if emoji.losing_matches.count() > 0:
                continue
            emojis[emoji] = emoji.winning_matches.count()
        sorted_by_matches = sorted(emojis.items(), key=lambda item: item[1])
        emojis_fighting = [emoji for emoji, _ in sorted_by_matches][:config.EMOJIS_BRACKET_NUMBER_OF_MATCHES * 2]
        shuffle(emojis_fighting)

        for first, second in chunker(emojis_fighting, 2):
            response = client.chat_postMessage(channel='#emoji-fight', text=f':{first.name}: :vs: :{second.name}:')
            match = EmojiMatch(first=first, second=second, slack_ts=response['ts'], slack_channel=response['channel'])
            client.react(response, first.name)
            time.sleep(config.EMOJIS_BRACKET_TIME_BETWEEN_REACTIONS)
            client.react(response, second.name)
            match.save()
