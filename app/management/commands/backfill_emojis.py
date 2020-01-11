from django.core.management.base import BaseCommand

from app.models import Emoji
from app.src.slack.slack_client import client

foo = ":+1::ok_hand::cry::stuck_out_tongue::-1::disappointed::100::fire::heart::chart_with_downwards_trend::question::wave::slightly_smiling_face::sunglasses::heart_eyes::yum::tired_face::thinking_face::face_with_rolling_eyes::smirk::triumph::triumph::triumph::weary::zany_face::nerd_face::ghost::alien::heart_eyes_cat::male-police-officer::skin-tone-6::flushed::hankey::middle_finger::clap::eyes::heart::man_in_business_suit_levitating::sweat_drops:"
bar = ":crab::peach::eggplant::sushi::beers::japan::love_hotel:"
baz = ":new_moon_with_face::game_die::cd::put_litter_in_its_place::cancer::wavy_dash::100::jp::kr::us::flag-ca:"
boop = ":uk:"
meep = ":shinto_shrine: :japanese_ogre: :japanese_castle: :japanese_goblin: :dagger_knife: :crossed_swords:"


class Command(BaseCommand):
    def handle(self, *args, **options):
        emojis = client.emoji_list()['emoji']
        for emoji in emojis:
            if 'alias:' in emojis[emoji]:
                continue

            if Emoji.objects.filter(name=emoji).count() == 0:
                e = Emoji(name=emoji)
                e.save()

        requested_emojis = foo.split(':') + bar.split(':') + baz.split(':') + boop.split(':') + meep.split(':')
        for emoji in requested_emojis:
            if emoji == '':
                continue

            if Emoji.objects.filter(name=emoji).count() == 0:
                e = Emoji(name=emoji)
                e.save()
