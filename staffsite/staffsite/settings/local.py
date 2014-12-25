from .dev import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alliance_staffsite',
        'USER': 'oss_alliance',
        'PASSWORD': 'oss_alliance',
        'HOST': 'localhost',
        'PORT': '',
    },
    'website': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alliance_website',
        'USER': 'oss_alliance',
        'PASSWORD': 'oss_alliance',
        'HOST': 'localhost',
        'PORT': '',
     },
    'chart_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chart',
        'USER': 'oss_alliance',
        'PASSWORD': 'oss_alliance',
    }
}
