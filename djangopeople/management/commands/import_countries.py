from django.core.management.base import LabelCommand
from djangopeople.importers import import_countries

class Command(LabelCommand):
    """ Import country data from the GeoNames XML """
    
    def handle_label(self, label, **options):
        with open(label) as f:
            import_countries(f)

