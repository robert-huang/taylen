import urllib.parse as urlparse

import django_heroku

from .common import *

django_heroku.settings(locals(), logging=False)

ALLOWED_HOSTS = ['taylen.herokuapp.com', '.slack.com']
DEBUG = False

SPLITWISE_CONSUMER_KEY = os.environ['SPLITWISE_CONSUMER_KEY']
SPLITWISE_CONSUMER_SECRET = os.environ['SPLITWISE_CONSUMER_SECRET']
SPLITWISE_OUATH_TOKEN = os.environ['SPLITWISE_OUATH_TOKEN']
SPLITWISE_OUATH_TOKEN_SECRET = os.environ['SPLITWISE_OUATH_TOKEN_SECRET']
SPLITWISE_GROUP_ID = os.environ['SPLITWISE_GROUP_ID']

SLACK_API_TOKEN = os.environ["SLACK_API_TOKEN"]
SLACK_EVENTS_TOKEN = os.environ["SLACK_EVENTS_TOKEN"]

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

db_url = urlparse.urlparse(os.environ['DATABASE_URL'])
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_url.path[1:],
        'USER': db_url.username,
        'PASSWORD': db_url.password,
        'HOST': db_url.hostname,
        'PORT': db_url.port,
    }
}

CACHES = {
    'default': {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": os.environ['REDIS_URL'],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'default': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = 'same-origin'
