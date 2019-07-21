from multiprocessing import cpu_count

bind = 'unix:/src/Citadel.sock'
max_requests = 1000
worker_class = 'sync'
workers = cpu_count() + 1
reload = True
name = 'Citadel'
errorlog = '/var/log/gunicorn-error.log'
loglevel = 'critical'
