from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('slack', views.slack, name="slack"),
    path('ping', views.ping, name="ping"),
]
