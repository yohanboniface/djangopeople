import re

from django.http import get_host
from django.shortcuts import redirect

multislash_re = re.compile('/{2,}')


class NoDoubleSlashes:
    """
    123-reg redirects djangopeople.com/blah to djangopeople.net//blah - this
    middleware eliminates multiple slashes from incoming requests.
    """
    def process_request(self, request):
        if '//' in request.path:
            new_path = multislash_re.sub('/', request.path)
            return redirect(new_path)
        else:
            return None


class RemoveWWW(object):
    def process_request(self, request):
        host = get_host(request)
        if host and host.startswith('www.'):
            newurl = "%s://%s%s" % (request.is_secure() and 'https' or 'http',
                                    host[len('www.'):], request.path)
            if request.GET:
                newurl += '?' + request.GET.urlencode()
            return redirect(newurl, permaent=True)
        else:
            return None
