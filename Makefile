proj = djangopeople
settings = --settings=$(proj).settings
test_settings = --settings=$(proj).test_settings

test:
	django-admin.py test $(test_settings) --failfast --noinput
run:
	django-admin.py runserver 0.0.0.0:8888 $(settings)
db:
	django-admin.py syncdb $(settings) --noinput && django-admin.py fix_counts $(settings)
shell:
	django-admin.py shell $(settings)

dbshell:
	django-admin.py dbshell $(settings)

makemessages:
	cd $(proj) && django-admin.py makemessages -a $(settings)

compilemessages:
	cd $(proj) && django-admin.py compilemessages $(settings)

txpush:
	tx push -s

txpull:
	tx pull -a

tiles:
	gunicorn "TileStache:WSGITileServer('tilestache.cfg')" -b 0.0.0.0:8889