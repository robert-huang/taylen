import logging

import requests

from app.src.slack.slack_client import SlackClient
from app.src.util.chunker import chunker

logger = logging.getLogger('default')

help_message = """```
Returns matching results from sc2ladder sorted by MMR.

Usage: 
> .mmr <query> <filters...>

Arguments:
- query: will match battlenet or sc2 in game names
- filters: can be server, race, or number of results. these can be in any order.

Examples:
> .mmr avilo
> .mmr avilo na terran 5
> .mmr showtime protoss 1 eu
> .mmr dark 1 kr z
```"""


class MmrCommand:
    @staticmethod
    async def handle_discord(message, query: str, filters: str):
        logger.info(f"[query={query}] [filters={filters}]")
        lines = mmr(query, filters.split(), discord_server_mapping, discord_race_mapping)
        for chunk in chunker(lines, 25):
            await message.channel.send(''.join(chunk))

    @staticmethod
    def handle_slack(client: SlackClient, event: dict, query: str, filters: str):
        logger.info(f"[query={query}] [filters={filters}]")
        lines = mmr(query, filters.split(), slack_server_mapping, slack_race_mapping)
        for chunk in chunker(lines, 25):
            client.post_message(event, ''.join(chunk))


discord_server_mapping = {
    'US': ':flag_us:',
    'EU': ':flag_eu:',
    'KR': ':flag_kr:',
}

discord_race_mapping = {
    'Zerg': '<:zerg:536337025901527053>',
    'Terran': '<:terran:536337048831787008>',
    'Protoss': '<:protoss:536337009363648515>',
    'Random': '<:random:536424834511536141>',
}

slack_server_mapping = {
    'US': ':flag-us:',
    'EU': ':flag-eu:',
    'KR': ':flag-kr:',
}

slack_race_mapping = {
    'Zerg': ':bug:',
    'Terran': ':gun:',
    'Protoss': ':alien:',
    'Random': ':question:',
}


def mmr(query, filters, server_mapping, race_mapping):
    url = f'http://sc2ladder.herokuapp.com/api/player?query={query}'
    race_filters = {
        'Zerg': ['z', 'Z', 'zerg', 'Zerg'],
        'Protoss': ['p', 'P', 'protoss', 'Protoss'],
        'Terran': ['t', 'T', 'terran', 'Terran'],
        'Random': ['r', 'R', 'random', 'Random'],
    }
    server_filters = {
        'US': ['na', 'NA', 'us', 'US'],
        'EU': ['eu', 'EU'],
        'KR': ['kr', 'KR'],
    }
    limit = 10
    for arg in filters:
        try:
            limit = int(arg)
        except ValueError:
            pass

    race_filter = None
    for race, value in race_filters.items():
        for v in value:
            if v in filters:
                race_filter = race

    server_filter = None
    for server, value in server_filters.items():
        for v in value:
            if v in filters:
                server_filter = server

    return sc2ladder_query(url, race_filter, server_filter, limit, server_mapping, race_mapping).splitlines(
        keepends=True)


def sc2ladder_query(url, race, server, limit, server_mapping, race_mapping):
    r = requests.get(url)
    players = r.json()

    if race:
        players = [x for x in players if x['race'] == race]
    if server:
        players = [x for x in players if x['region'] == server]

    content = f"Displaying {min(limit, len(players))}/{len(players)} matches:"
    for player in players[:limit]:
        name = f"{player['username'][:player['username'].index('#')]} ({player['bnet_id']})"
        server = server_mapping[player['region']]
        race = race_mapping[player['race']]
        clan = '' if not player['clan'] else f"[{player['clan']}]"
        content += f"\n{server} {race} {clan} {name}: {player['mmr']}"
    return content
