proj = djangopeople
settings = --settings=$(proj).settings
test_settings = --settings=$(proj).test_settings

test:
	django-admin.py test $(test_settings) --failfast --noinput
run:
	django-admin.py runserver $(settings)
