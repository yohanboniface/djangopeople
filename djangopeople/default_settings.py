# Django settings for djangopeoplenet project.
import os

from django.core.urlresolvers import reverse_lazy

OUR_ROOT = os.path.realpath(os.path.dirname(__file__))

TEST_RUNNER = 'djangopeople.runner.DiscoveryRunner'
TEST_DISCOVERY_ROOT = os.path.join(OUR_ROOT, os.pardir)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# OpenID settings
OPENID_REDIRECT_NEXT = reverse_lazy('openid_whatnext')
LOGIN_URL = reverse_lazy('login')

# Tagging settings
FORCE_LOWERCASE_TAGS = True

AUTH_PROFILE_MODULE = 'djangopeople.DjangoPerson'
RECOVERY_EMAIL_FROM = 'example@example.com'

ADMINS = ()
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(OUR_ROOT, 'media')

# Absolute path to the directory where static media will be collected.
STATIC_ROOT = os.path.join(OUR_ROOT, 'static')

STATICFILES_STORAGE = ('django.contrib.staticfiles.storage.'
                       'CachedStaticFilesStorage')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# Password used by the IRC bot for the API
API_PASSWORD = 'API-PASSWORD-GOES-HERE'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'djangopeople.djangopeople.middleware.RemoveWWW',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'djangopeople.django_openidconsumer.middleware.OpenIDMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'djangopeople.djangopeople.middleware.NoDoubleSlashes',
)

ROOT_URLCONF = 'djangopeople.urls'

TEMPLATE_DIRS = ()

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'djangopeople.django_openidconsumer',
    'djangopeople.django_openidauth',
    'raven.contrib.django',
    'djangosecure',
    'djangopeople.djangopeople',
    'djangopeople.machinetags',
    'tagging',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'raven': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'sentry.errors': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
