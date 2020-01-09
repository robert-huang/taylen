from django.core.management.base import BaseCommand

from app.models import EmojiMatch
from app.src.slack.slack_client import client


class Command(BaseCommand):
    def handle(self, *args, **options):
        winning_emojis = []
        for match in EmojiMatch.objects.filter(winner=None).all():
            reactions = client.reactions_get(channel=match.slack_channel, timestamp=match.slack_ts)['message'][
                'reactions']
            reaction_to_count = {}
            for reaction in reactions:
                reaction_to_count[reaction['name']] = reaction['count']

            first_votes = reaction_to_count[match.first.name]
            second_votes = reaction_to_count[match.second.name]
            match.first_votes = first_votes
            match.second_votes = second_votes

            if first_votes > second_votes:
                match.winner = match.first
                match.loser = match.second
            else:
                match.winner = match.second
                match.loser = match.first

            winning_emojis.append(match.winner.name)
            match.save()

        text = 'Winners: '
        for emoji in winning_emojis:
            text += f':{emoji}: '
        client.chat_postMessage(channel='#emoji-fight', text=text)
