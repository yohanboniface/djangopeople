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
AWS_QUERYSTRING_AUTH = False

STATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME

SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

# Run the site over SSL
MIDDLEWARE_CLASSES = (
    'sslify.middleware.SSLifyMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
) + MIDDLEWARE_CLASSES
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 2592000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
