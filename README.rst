This is an attempt to bring djangopeople.net back online and up to date. Very
much a work in progress, the plan is to:

* Remove the lib/ folder in favor of pip requirements
* Migrate the geopy / lat-lng stuff to geodjango

Original README from Simon Willison:

This is an unmodified (except removal of secrets and API keys) dump of the
code now running on djangopeople.net - the vast majority of which was
developed between January and April 2008 by Simon Willison and Natalie Downe.

It originally ran on Django r7400, but has recently been updated for Django 1.1.

This code was not originally intended for public consumption, so there are
probably one or two eyebrow raising design decisions. In particular, the
machine tags stuff for user profiles was an ambitious experiment which I
wouldn't mind seeing the back of.

You'll want to place both /lib/ and the root of the repo on your PYTHONPATH, e.g.

PYTHONPATH=/path/to/repo/lib/:\
/path/to/repo/:\
$PYTHONPATH python /path/to/repo/djangopeoplenet/manage.py runserver

----------

TODO
cleanup imports


404s:
	je.gif
	aq.gif
