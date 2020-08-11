from .settings import *

# Using in-memory database makes tests run faster.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
