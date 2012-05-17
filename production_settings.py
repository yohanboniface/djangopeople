from default_settings import *

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(),
}

SECRET_KEY = os.environ['SECRET_KEY']

STATICFILES_STORAGE = 's3storage.S3HashedFilesStorage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', '')

STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
