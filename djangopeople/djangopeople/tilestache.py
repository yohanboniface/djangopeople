from TileStache.Goodies.Providers.PostGeoJSON import Provider as BaseProvider
from TileStache.Goodies.Providers.PostGeoJSON import (_p2p, SaveableResponse,
                                                      _connect, RealDictCursor,
                                                      shape2geometry,
                                                      _InvisibleBike, _copy)
from TileStache.Geography import getProjectionByName
from django.conf import settings


class Provider(BaseProvider):
    """
    Custom provider because we don't use PostGIS for now.
    """

    def __init__(self, layer):
        self.layer = layer
        self.mercator = getProjectionByName('spherical mercator')
        self.indent = 2
        self.precision = 6
        self.id_field = "people_id"

    def row2feature(self, row):
        """ Convert a database row dict to a feature dict."""
        feature = {'type': 'Feature', 'properties': _copy(row)}

        lat = feature['properties'].pop("latitude")
        lng = feature['properties'].pop("longitude")
        feature['geometry'] = {
            "type": "Point",
            "coordinates": [lng, lat]
        }
        feature['id'] = feature['properties'].pop("people_id")
        first_name = feature['properties'].pop("first_name").decode('utf-8')
        last_name = feature['properties'].pop("last_name").decode('utf-8')
        feature['properties']['name'] = u"%s %s" % (first_name, last_name)
        feature['properties'].update({
            "photo": "https://secure.gravatar.com/avatar/e9bd94b49ff9cf2ab370b5b3b346e8fc?s=40&d=mm",
            "iso_code": "fr"
            })

        return feature

    def renderTile(self, width, height, srs, coord):
        """ Render a single tile, return a SaveableResponse instance."""
        nw = self.layer.projection.coordinateLocation(coord)
        se = self.layer.projection.coordinateLocation(coord.right().down())

        database = settings.DATABASES['default']['NAME']
        user = settings.DATABASES['default']['USER']
        db = _connect(database=database, user=user).cursor(cursor_factory=RealDictCursor)

        query = ("""SELECT dj.id as people_id, latitude, longitude,"""
                 """ username, first_name, last_name, location_description"""
                 """ from djangopeople_djangoperson as dj"""
                 """ JOIN auth_user as au ON dj.user_id=au.id"""
                 """ WHERE latitude BETWEEN {0} AND {1} AND longitude BETWEEN {2} AND {3}""")
        query = query.format(
            se.lat,
            nw.lat,
            nw.lon,
            se.lon,
        )
        db.execute(query)
        rows = db.fetchall()

        db.close()

        response = {'type': 'FeatureCollection', 'features': []}

        for row in rows:
            feature = self.row2feature(row)
            response['features'].append(feature)

        return SaveableResponse(response, self.indent, self.precision)
