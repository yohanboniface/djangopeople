from django.contrib.gis.geos import Point
from django.test import TestCase

class SignupFormTestCase(TestCase):

    def setUp(self):
        from djangopeople.models import Country
        super(SignupFormTestCase, self).setUp()
        
        # Some data will already have been loaded through fixtures. Grab
        # a couple of them for use in the tests.
        self.country = Country.objects.all()[0]

    @property
    def form_class(self):
        # Avoid import-time dependency, so tests fail if this is not
        # importable, rather than breaking completely.
        from djangopeople.forms import SignupForm
        return SignupForm

    def test_point(self):
        """When a valid latitude and longitude are set, the clean() method
        on the form should set a ``point`` key in cleaned_data, corresponding
        to a Point we can set on the DjangoPeople instance.
        """
        longitude = -73.153152465821
        latitude = -51.449727928453
        form_data = {
            'username': u'testuser',
            'first_name': u'Test',
            'last_name': u'User',
            'email': u'test@test.com',
            'password1': u'test',
            'password2': u'test',
            'latitude': str(latitude).decode('ascii'),
            'longitude': str(longitude).decode('ascii'),
            'country': self.country.iso_code,
            'location_description': u'Location Description',
            'privacy_search': u'public',
            'privacy_email': u'public',
            'privacy_im': u'public',
            'privacy_irctrack': u'public',
        }
        form = self.form_class(form_data)
        self.assertTrue(form.is_valid(), form.errors)
        expected = Point(longitude, latitude)
        self.assertEqual(expected, form.cleaned_data['point'])
