from django.core.management.base import NoArgsCommand

from ...clustering import Cluster


class Command(NoArgsCommand):
    help = "Re-runs the server-side clustering"

    def handle_noargs(self, **options):
        cluster = Cluster()
        cluster.mass_populate_cache()
