import slack
from django.conf import settings


class SlackClient(slack.WebClient):
    def post_message(self, event: dict, text: str):
        args = {
            'text': text,
            'channel': event['channel'],
        }
        if 'thread_ts' in event:
            args['thread_ts'] = event['thread_ts']

        self.chat_postMessage(**args)

    def react(self, event: dict, reaction: str):
        self.reactions_add(
            name=reaction,
            channel=event['channel'],
            timestamp=event['ts']
        )


client = SlackClient(token=settings.SLACK_API_TOKEN)
