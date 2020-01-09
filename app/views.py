import json
import logging
import uuid
from random import shuffle
from typing import Dict

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app.models import Emoji, EmojiMatch
from app.src.bot import handle_slack
from app.src.slack.slack_client import client
from app.src.util.chunker import chunker

logger = logging.getLogger('default')


def ping(request: HttpRequest):
    return HttpResponse("pong")


def start_emoji_matches(request: HttpRequest):
    logger.info(f"[request.body=${request.body}")
    if request.body != settings.SLACK_EVENTS_TOKEN:
        raise HttpResponseForbidden

    emojis: Dict[str, int] = {}
    for emoji in Emoji.objects.all():
        if emoji.losing_matches.count() > 0:
            continue
        emojis[emoji] = emoji.winning_matches.count()
    emojis_fighting = [emoji for emoji, matches_won in sorted(emojis.items(), key=lambda item: item[1])][:20]
    shuffle(emojis_fighting)

    for first, second in chunker(emojis_fighting, 2):
        response = client.chat_postMessage(channel='#emoji-fight', text=f'Fight: :{first.name}: vs :{second.name}:')
        match = EmojiMatch(first=first, second=second, slack_ts=response['ts'], slack_channel=response['channel'])
        client.react(response, first.name)
        client.react(response, second.name)
        match.save()

    return HttpResponse("ok")


def conclude_emoji_matches(request: HttpRequest):
    logger.info(f"[request.body=${request.body}")
    if request.body != settings.SLACK_EVENTS_TOKEN:
        raise HttpResponseForbidden

    for match in EmojiMatch.objects.filter(winner=None).all():
        reactions = client.reactions_get(channel=match.slack_channel, timestamp=match.slack_ts)['message']['reactions']
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

    return HttpResponse("ok")


@csrf_exempt
def slack(request: HttpRequest):
    logger.info(f"[request.body=${request.body}]")
    body = json.loads(request.body)
    if body['token'] != settings.SLACK_EVENTS_TOKEN:
        raise HttpResponseForbidden
    if body.get('type') == 'url_verification':
        return HttpResponse(body['challenge'])

    # Events are often sent multiple times from slack, so we avoid double
    # processing by using redis. I should probably be using something like
    # https://redis.io/commands/setnx but this is fine for now. Possibly not
    # correct though.
    event_id = body['event_id']
    uid = uuid.uuid4()
    if cache.get_or_set(event_id, lambda: uid, stale_cache_timeout=0) != uid:
        return JsonResponse({'ok': True})

    event = body.get('event')
    if event.get('type') == 'message':
        handle_slack(event)

    return JsonResponse({'ok': True})
