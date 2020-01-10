import time
from random import shuffle
from typing import Dict

from django.core.management.base import BaseCommand

from app.models import Emoji, EmojiMatch
from app.src.slack.slack_client import client
from app.src.util.chunker import chunker


class Command(BaseCommand):
    def handle(self, *args, **options):
        emojis: Dict[str, int] = {}
        for emoji in Emoji.objects.order_by('?').all():
            if emoji.losing_matches.count() > 0:
                continue
            emojis[emoji] = emoji.winning_matches.count()
        emojis_fighting = [emoji for emoji, matches_won in sorted(emojis.items(), key=lambda item: item[1])][:20]
        shuffle(emojis_fighting)

        for first, second in chunker(emojis_fighting, 2):
            response = client.chat_postMessage(channel='#emoji-fight', text=f':{first.name}: vs :{second.name}:')
            match = EmojiMatch(first=first, second=second, slack_ts=response['ts'], slack_channel=response['channel'])
            client.react(response, first.name)
            time.sleep(0.25)
            client.react(response, second.name)
            match.save()
