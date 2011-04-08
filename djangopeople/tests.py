from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core import mail
from django.core.urlresolvers import reverse
from django.middleware.common import CommonMiddleware
from django.test import TestCase
from django.test.client import RequestFactory

from django_openidconsumer.util import OpenID

from djangopeople.models import DjangoPerson, Country
from djangopeople.views import signup


def prepare_request(request, openid=True):
    """
    Given a raw request coming from a RequestFactory, process it
    using the middleware and (if openid is True) attach an openid to it
    """
    if openid:
        request.openid = OpenID('http://foo.example.com/', 1302206357)
    for m in (CommonMiddleware, SessionMiddleware):
        m().process_request(request)
    return request


class DjangoPeopleTest(TestCase):

    def test_simple_pages(self):
        """Simple pages with no action"""
        names = ['index', 'about', 'recent']
        for name in names:
            url = reverse(name)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'username': 'foo',
                'password': 'bar'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        User.objects.create_user('foo', 'test@example.com', 'bar')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 404)  # Missing DjangoPerson
        self.assertEqual(len(response.redirect_chain), 1)

        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertTrue('log in' in response.content)

        self.client.logout()
        data['next'] = reverse('about')
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('<h1>About Django People</h1>' in response.content)

    def test_recover_account(self):
        url = reverse('recover')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected = '<label for="id_username">Username'
        self.assertTrue(expected in response.content)

        data = {'username': 'foo'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('That was not a valid username' in response.content)

        user = User.objects.create_user('foo', 'test@example.com', 'bar')
        DjangoPerson.objects.create(user=user,
                                    country=Country.objects.get(pk=1),
                                    latitude=0,
                                    longitude=0,
                                    location_description='Somewhere')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('An e-mail has been sent' in response.content)
        self.assertEqual(len(mail.outbox), 1)

        content = mail.outbox[0].body
        url = content.split('\n\n')[2]
        url = url.replace('http://djangopeople.net', '')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.redirect_chain), 1)
        self.assertTrue('<h1>Change your password</h1>' in response.content)

    def test_signup(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'testuser',
            'email': 'foo@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'latitude': '45',
            'longitude': '2',
            'country': 'FR',
            'location_description': 'Somewhere',
            'privacy_search': 'public',
            'privacy_email': 'private',
            'privacy_im': 'private',
            'privacy_irctrack': 'public',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

        data['password1'] = 'secret'
        data['password2'] = 'othersecret'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)

        data['password2'] = 'secret'
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.redirect_chain), 1)

        # Logged in users go back to the homepage
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.client.session.flush()

        # Registration with an OpenID shouldn't ask for a password
        factory = RequestFactory()
        request = prepare_request(factory.get(url))
        response = signup(request)
        response.render()
        self.assertTrue('foo.example.com' in response.content)

        del data['password1']
        del data['password2']
        data['username'] = 'meh'
        data['email'] = 'other@example.com'
        request = prepare_request(factory.post(url, data))
        response = signup(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                         reverse('user_profile', args=['meh']))
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(DjangoPerson.objects.count(), 2)
