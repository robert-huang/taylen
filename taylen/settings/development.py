from .common import *

SECRET_KEY = '0c(i&aa$a5gt8#2mc&#7mw7mw_59vy3@$or#fphd6tbf2esjjo'
DEBUG = True
ALLOWED_HOSTS = ['*']

SPLITWISE_CONSUMER_KEY = ''
SPLITWISE_CONSUMER_SECRET = ''
SPLITWISE_OUATH_TOKEN = ''
SPLITWISE_OUATH_TOKEN_SECRET = ''
SPLITWISE_GROUP_ID = ''
SLACK_API_TOKEN = ''
SLACK_EVENTS_TOKEN = ''
DISCORD_TOKEN = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = []
