"""
Django settings for oss project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&oflv@17242og)e9j8*s!1^2*gxcqeaz@&fbnl+spfq=j=kn32'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminapp',
    'baseissuer',
    'chart',
    'alliance',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
)

ROOT_URLCONF = 'staffsite.urls'

WSGI_APPLICATION = 'staffsite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

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
        'USER': 'root',
        'PASSWORD': 'wclab12345',
    }
}

# Session settings
SESSION_SECURITY_EXPIRE_AFTER = 300
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/home/signin/'
LOGIN_REDIRECT_URL = '/home/index/'
LOGOUT_URL = 'home/logout/'


LOG_DIR = BASE_DIR
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/oss-federation.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'django.db.backends': {
            'handlers': ['file'],
            'propagate': False,
            'level': 'WARNING',
        },
        'adminapp': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'alliance': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'baseissuer': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
