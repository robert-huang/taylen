import sys

from django.apps import AppConfig


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        if 'runserver' in sys.argv or 'taylen.wsgi' in sys.argv:
            # Import locally to avoid cyclical dependency.
            from app.src.discord import discord_client
            # discord_client.start()
