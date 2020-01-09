from django.core.management.base import BaseCommand

from app.models import EmojiMatch
from app.src.slack.slack_client import client


class Command(BaseCommand):
    def handle(self, *args, **options):
        for match in EmojiMatch.objects.filter(winner=None).all():
            reactions = client.reactions_get(channel=match.slack_channel, timestamp=match.slack_ts)['message'][
                'reactions']
            reaction_to_count = {}
            for reaction in reactions:
                reaction_to_count[reaction['name']] = reaction['count']

            if reaction_to_count[match.first.name] > reaction_to_count[match.second.name]:
                match.winner = match.first
                match.loser = match.second
            else:
                match.winner = match.second
                match.loser = match.first

            match.save()
