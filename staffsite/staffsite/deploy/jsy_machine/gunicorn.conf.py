import os

# machine related configuration
VENV_PATH = '/root/.virtualenvs/alliance/bin/'
PROJECT_PATH = '/root/OSS-Federation/staffsite/'

bind = '127.0.0.1:8080'
workers = (os.sysconf('SC_NPROCESSORS_ONLN') * 2) + 1

command = VENV_PATH + 'gunicorn'
pythonpath = PROJECT_PATH + 'staffsite'
accesslog = PROJECT_PATH + 'log/gunicorn_access.log'
errorlog = PROJECT_PATH + 'log/gunicorn_error.log'
