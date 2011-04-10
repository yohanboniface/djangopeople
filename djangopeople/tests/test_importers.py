from cStringIO import StringIO
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.test import TestCase

from djangopeople.models import Country

class ImportCountryTest(TestCase):
    """ Test that the country importer is working properly """

    def setUp(self):
        # Zap any countries that came in through fixtures
        super(ImportCountryTest, self).setUp()
        Country.objects.all().delete()

    def _import(self):
        from djangopeople.importers import import_countries
        fp = StringIO(COUNTRY_XML)
        import_countries(fp)

    def test_import_ok(self):
        """ Test that a straight import from the sample XML data creates
        countries' attributes
        """
        self._import()
        andorra, uae = Country.objects.all().order_by('iso_code')

        self.assertEqual(u'AD', andorra.iso_code)
        self.assertEqual(u'Andorra', andorra.name)

        self.assertEqual(u'AE', uae.iso_code)
        self.assertEqual(u'United Arab Emirates', uae.name)

    def test_import_polygon(self):
        """ Check that the polygon is imported correctly based on the
        data's bounding box.
        """
        from djangopeople.importers import bbox_to_mpoly
        self._import()
        andorra = Country.objects.get(iso_code=u'AD')
        expected = bbox_to_mpoly(42.658695, 1.780389, 42.435081, 1.422111)
        self.assertEqual(expected.coords, andorra.polygon.coords)

    def test_update(self):
        """ Test that if appropriate country records are present, then they
        are not updated from the feed.
        """
        self._import()
        andorra = Country.objects.get(iso_code=u'AD')
        andorra.name = u'Other Name'
        andorra.save()
        self._import()
        andorra = Country.objects.get(pk=andorra.pk)
        self.assertEqual(u'Other Name', andorra.name)

    def test_bbox_to_mpoly(self):
        """ Test that the bBox* values are converted properly to the
        appropriate MultiPolygon.
        """
        from djangopeople.importers import bbox_to_mpoly

        # Define where the edges of the bounding box lie.
        bbox_west = 2.0
        bbox_east = 4.0
        bbox_north = 5.0
        bbox_south = 1.0

        # MultiPolygons are made up from Polygons, which are in turn defined
        # by their corners. Longitude (east-west) is the first argument to
        # each point.
        expected_mpoly = MultiPolygon(
            Polygon([
                (2.0, 5.0), # north-west
                (4.0, 5.0), # north-east
                (4.0, 1.0), # south-east
                (2.0, 1.0), # south-west
                (2.0, 5.0), # north-west again, close the polygon
            ]))
        actual = bbox_to_mpoly(bbox_north, bbox_east, bbox_south, bbox_west)
        self.assertEqual(expected_mpoly.coords, actual.coords)


COUNTRY_XML = """
<geonames>
<country>
<countryCode>AD</countryCode>
<countryName>Andorra</countryName>
<isoNumeric>200</isoNumeric>
<isoAlpha3>AND</isoAlpha3>
<fipsCode>AN</fipsCode>
<continent>EU</continent>
<capital>Andorra la Vella</capital>

<areaInSqKm>468.0</areaInSqKm>
<population>84000</population>
<currencyCode>EUR</currencyCode>
<languages>ca</languages>
<geonameId>3041565</geonameId>
<bBoxWest>1.422111</bBoxWest>
<bBoxNorth>42.658695</bBoxNorth>
<bBoxEast>1.780389</bBoxEast>
<bBoxSouth>42.435081</bBoxSouth>

</country>
<country>
<countryCode>AE</countryCode>
<countryName>United Arab Emirates</countryName>
<isoNumeric>784</isoNumeric>
<isoAlpha3>ARE</isoAlpha3>
<fipsCode>AE</fipsCode>
<continent>AS</continent>
<capital>Abu Dhabi</capital>
<areaInSqKm>82880.0</areaInSqKm>

<population>4975593</population>
<currencyCode>AED</currencyCode>
<languages>ar-AE,fa,en,hi,ur</languages>
<geonameId>290557</geonameId>
<bBoxWest>51.58332824707031</bBoxWest>
<bBoxNorth>26.08415985107422</bBoxNorth>
<bBoxEast>56.38166046142578</bBoxEast>
<bBoxSouth>22.633329391479492</bBoxSouth>
</country>
</geonames>
"""
