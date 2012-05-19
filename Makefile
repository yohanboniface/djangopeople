proj = djangopeople
settings = --settings=$(proj).settings
test_settings = --settings=$(proj).test_settings

test:
	django-admin.py test $(test_settings) --failfast --noinput
run:
	django-admin.py runserver $(settings)
db:
	django-admin.py syncdb $(settings) --noinput && django-admin.py fix_counts $(settings)
shell:
	django-admin.py shell $(settings)
