from mock import patch

from django.core.urlresolvers import reverse
from django.test import TestCase


class OpenIDTests(TestCase):
    @patch('openid.consumer.consumer.Consumer')
    def test_openid_begin(self, consumer):
        """
        OpenID initial negociation
        """
        url = reverse('openid_begin')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'openid_url': 'http://bruno.renie.fr'}

        auth = consumer.return_value.begin
        auth.return_value.redirectURL.return_value = 'http://www.myopenid.com/server'

        response = self.client.post(url, data)
        auth.assert_called_with('http://bruno.renie.fr')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response['Location'].startswith('http://www.myopenid.com/server')
        )
