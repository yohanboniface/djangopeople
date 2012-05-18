from django.core.urlresolvers import reverse
from django.test import TestCase


class OpenIDTests(TestCase):
    def test_openid_begin(self):
        """
        OpenID initial negociation
        """
        url = reverse('openid_begin')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'openid_url': 'http://bruno.renie.fr'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['Location'].startswith('http://www.myopenid.com/server')
        )
