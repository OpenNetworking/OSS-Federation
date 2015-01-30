"""
This is a setting file for my own machine.
"""
from .dev import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'alliance_website',
        'USER': 'oss_alliance',
        'PASSWORD': 'oss_alliance',
        'HOST': 'localhost',
        'PORT': '',
    }
}

