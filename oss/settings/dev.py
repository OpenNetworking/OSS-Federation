from .base import *


DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            },
    'chart_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'chart',
        'USER': 'root',
        'PASSWORD': 'wclab12345',
    }
}

DATABASE_ROUTERS = [
    'oss.apps.chart.ChartRouter.ChartRouter'
]
