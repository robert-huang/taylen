from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slack', views.slack, name="slack"),
    path('ping', views.ping, name="ping"),
    path('start-emoji-match', views.start_emoji_matches, name="start_emoji_matches"),
    path('conclude-emoji-matches', views.conclude_emoji_matches, name="conclude_emoji_matches"),
]
