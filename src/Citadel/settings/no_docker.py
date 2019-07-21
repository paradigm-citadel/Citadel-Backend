import envvars

from .base import *

# Load environment variables from .env file
envvars.load(os.path.join(BASE_DIR, '.env'))

DEBUG = True
SECRET_KEY = 'abracodabra'

INSTALLED_APPS.append('silk')
INSTALLED_APPS.append('django_seed')
MIDDLEWARE.append('silk.middleware.SilkyMiddleware')

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Email account credentials
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

# Citadel second backend url (for transactions loading)
SECOND_BACKEND_URL=os.environ['SECOND_BACKEND_URL']

# Currency rates source
CURRENCY_RATE_API_KEY=os.environ['CURRENCY_RATE_API_KEY']