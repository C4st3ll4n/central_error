import dj_database_url

from .settings import *

DEBUG = False

SECRET_KEY = "jz1jhrh&&3^k3i=0m1&h-+s8e0_jt3m!d0=lht6%m@p-s@3)$i"

ALLOWED_HOSTS.append('*')

DATABASES = {
    'default': dj_database_url.config()
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}
