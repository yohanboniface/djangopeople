from django.conf import settings

SERVICES = (
    # shortname, name, icon
    ('flickr', 'Flickr', settings.STATIC_URL + 'img/services/flickr.png'),
    ('delicious', 'del.icio.us', settings.STATIC_URL + 'img/services/delicious.png'),
    ('magnolia', 'Ma.gnolia.com', settings.STATIC_URL + 'img/services/magnolia.png'),
    ('twitter', 'Twitter', settings.STATIC_URL + 'img/services/twitter.png'),
    ('facebook', 'Facebook', settings.STATIC_URL + 'img/services/facebook.png'),
    ('linkedin', 'LinkedIn', settings.STATIC_URL + 'img/services/linkedin.png'),
    ('pownce', 'Pownce', settings.STATIC_URL + 'img/services/pownce.png'),
    ('djangosnippets', 'djangosnippets.org', settings.STATIC_URL + 'img/services/django.png'),
    ('djangosites', 'DjangoSites.org', settings.STATIC_URL + 'img/services/django.png'),
)
SERVICES_DICT = dict([(r[0], r) for r in SERVICES])

IMPROVIDERS = (
    # shortname, name, icon
    ('aim', 'AIM', settings.STATIC_URL + 'img/improviders/aim.png'),
    ('yim', 'Y!IM', settings.STATIC_URL + 'img/improviders/yim.png'),
    ('gtalk', 'GTalk', settings.STATIC_URL + 'img/improviders/gtalk.png'),
    ('msn', 'MSN', settings.STATIC_URL + 'img/improviders/msn.png'),
    ('jabber', 'Jabber', settings.STATIC_URL + 'img/improviders/jabber.png'),
    ('django', '#django IRC', settings.STATIC_URL + 'img/services/django.png'),
)
IMPROVIDERS_DICT = dict([(r[0], r) for r in IMPROVIDERS])

# Convenience mapping from fields to machinetag (namespace, predicate)
MACHINETAGS_FROM_FIELDS = dict(
    [('service_%s' % shortname, ('services', shortname))
     for shortname, name, icon in SERVICES] + 
    [('im_%s' % shortname, ('im', shortname))
     for shortname, name, icon in IMPROVIDERS] + [
        ('privacy_search', ('privacy', 'search')),
        ('privacy_email', ('privacy', 'email')),
        ('privacy_im', ('privacy', 'im')),
        ('privacy_irctrack', ('privacy', 'irctrack')),
    ]
)
