from django.core.management.base import BaseCommand

from app.models import Emoji
from app.src.slack.slack_client import client


class Command(BaseCommand):
    def handle(self, *args, **options):
        emojis = client.emoji_list()['emoji']
        for emoji in emojis:
            if 'alias:' in emojis[emoji]:
                continue
            e = Emoji(name=emoji)
            e.save()
