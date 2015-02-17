import os

# virtualenv path
VENV_PATH = "/path/to/venv"

# project path
PROJECT_PATH = "/path/to/project"

# need to same as nginx.conf upstream server
bind = 'IP:PORT'

workers = (os.sysconf('SC_NPROCESSORS_ONLN') * 2) + 1
command = VENV_PATH + 'gunicorn'
pythonpath = PROJECT_PATH + 'staffsite'
accesslog = PROJECT_PATH + 'log/gunicorn_access.log'
errorlog = PROJECT_PATH + 'log/gunicorn_error.log'
