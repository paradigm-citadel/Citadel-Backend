bind = 'unix:/src/Citadel.sock'
max_requests = 100
worker_class = 'sync'
workers = 1
reload = True
name = 'Citadel'
errorlog = '/var/log/gunicorn-error.log'
loglevel = 'warning'
