from django.core.urlresolvers import reverse
from django.test import TestCase


class DjangoPeopleTest(TestCase):

    def test_index(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
