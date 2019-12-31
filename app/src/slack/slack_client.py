import slack
from django.conf import settings

client = slack.WebClient(token=settings.SLACK_API_TOKEN)
