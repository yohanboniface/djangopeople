from django.conf import settings


def tilestache_domain(request):
    return {
        "TILESTACHE_DOMAIN": settings.TILESTACHE_DOMAIN
    }
