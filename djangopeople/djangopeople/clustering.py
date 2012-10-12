from django.core.cache import cache

from .models import DjangoPerson


class Cluster(object):

    # Must contain a %d fo the zoom level
    CACHE_KEY = "clusters_for_%d"

    ZOOM_LEVELS = {
        0: {
            "step": 70,  # Grid step
            "min": 20  # Min markers in a cluster to display it
        },
        1: {
            "step": 50,
            "min": 10
        },
        2: {
            "step": 45,
            "min": 5
        },
        3: {
            "step": 30,
            "min": 3
        },
        4: {
            "step": 15,
            "min": 2
        },
        5: {
            "step": 5,
            "min": 2
        },
    }

    def get_points(self):
        return DjangoPerson.objects.values('id', 'latitude', 'longitude')

    def mass_populate_cache(self):
        """Runs server-side clustering for each zoom level."""
        points = self.get_points()
        for zoom_level in self.ZOOM_LEVELS.iterkeys():
            self.populate_cache(points, zoom_level)

    def populate_cache(self, points, zoom_level):
        """
        Runs the server-side clustering and cache it for front usage.
        Poor man algorithm:
        - divide the world in a grids, sized according to zoom level
        - for each point, calculate the closest grid node
        - take a "random" point in the cluster to set the center
        (For better rendering, these clusters could be reclustered,
        as they are now not numerous. But it's not done right now.)
        """
        simple_cluster = {}
        for point in points:
            lat = point['latitude']
            lng = point['longitude']
            grid_point = (
                lat - lat % self.ZOOM_LEVELS[zoom_level]['step'],
                lng - lng % self.ZOOM_LEVELS[zoom_level]['step'],
            )
            if not grid_point in simple_cluster:
                simple_cluster[grid_point] = {}
                simple_cluster[grid_point]['points'] = []
            simple_cluster[grid_point]['points'].append(point)
            # Ungrid the cluster center artificially
            simple_cluster[grid_point]['lat'] = lat
            simple_cluster[grid_point]['lng'] = lng
        geojson = {'type': 'FeatureCollection', 'features': []}
        for cluster in simple_cluster.itervalues():
            if len(cluster['points']) < self.ZOOM_LEVELS[zoom_level]['min']:
                continue
            feature = self.make_feature(cluster)
            geojson['features'].append(feature)
        cache.set(self.CACHE_KEY % zoom_level, geojson)
        return geojson

    def make_feature(self, cluster):
        lat = cluster['lat']
        lng = cluster['lng']
        feature = {'type': 'Feature', 'properties': {}}
        feature['geometry'] = {
            "type": "Point",
            "coordinates": [lng, lat]
        }
        feature['properties']['len'] = len(cluster['points'])
        return feature

    def get_for_zoom(self, zoom_level):
        clusters = cache.get(self.CACHE_KEY % int(zoom_level))
        if not clusters:
            points = self.get_points()
            clusters = self.populate_cache(points, zoom_level)
        return clusters
