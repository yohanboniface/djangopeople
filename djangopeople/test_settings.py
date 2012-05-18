from default_settings import *  # noqa

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
BASE_PATH = os.path.join(OUR_ROOT, os.pardir)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djangopeople',
        'USER': 'postgres',
    },
}
