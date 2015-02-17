from django.core.exceptions import ImproperlyConfigured

from .base import *

def get_env_var(key):
    try:
        return os.environ[key]
    except KeyError:
        raise ImproperlyConfigured(
            'Environment variable {key} required.'.format(key=key)
        )

DEBUG = False
TEMPLATE_DEBUG = False

STATIC_URL = '/static/'


SECRET_KEY = get_env_var('DJANGO_SECRET_KEY')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alliance_staffsite_nginx',
        'USER': get_env_var('DJANGO_DEFAULT_DATABASE_USER'),
        'PASSWORD': get_env_var('DJANGO_DEFAULT_DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    },
    'website': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alliance_website_nginx',
        'USER': get_env_var("DJANGO_WEBSITE_DATABASE_USER"),
        'PASSWORD': get_env_var('DJANGO_WEBSITE_DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
     },
}

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media')

