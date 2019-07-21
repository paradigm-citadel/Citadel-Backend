import os

env = os.environ.get('DJANGO_ENVIRONMENT', None)
if env == 'dev':
    from .docker_dev import *
elif env == 'prod':
    from .docker_prod import *
else:
    from .no_docker import *
