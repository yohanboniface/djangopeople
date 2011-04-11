from django.contrib.gis import admin
from djangopeople.models import Country, CountrySite, Region, DjangoPerson, PortfolioSite
from olwidget.admin import GeoModelAdmin

class CountryAdmin(GeoModelAdmin):
    list_display = ('name',)
    map_fields = ['polygon']

class CountrySiteAdmin(admin.ModelAdmin):
    pass

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)

class DjangoPersonAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_views')
    raw_id_fields = ('user',)

class PortfolioSiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Country, CountryAdmin)
admin.site.register(CountrySite, CountrySiteAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(DjangoPerson, DjangoPersonAdmin)
admin.site.register(PortfolioSite, PortfolioSiteAdmin)
