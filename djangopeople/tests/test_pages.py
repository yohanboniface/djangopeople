from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.core import mail
from django.core.urlresolvers import reverse
from django.middleware.common import CommonMiddleware
from django.test import TestCase
from django.test.client import RequestFactory

from django_openidauth.models import associate_openid
from django_openidconsumer.util import OpenID

from djangopeople.models import DjangoPerson, Country
from djangopeople.views import signup, openid_whatnext


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

    def _get_signup_data(self):
        # Helper method to get a dict of valid signup data, minus a password.
        return {
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

        data = self._get_signup_data()
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

        data = self._get_signup_data()
        data['username'] = 'meh'
        data['email'] = 'other@example.com'
        request = prepare_request(factory.post(url, data))
        response = signup(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                         reverse('user_profile', args=['meh']))
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(DjangoPerson.objects.count(), 2)

    def test_signup_sets_location(self):
        """ Check that signup sets the location field correctly. """
        data = self._get_signup_data()
        data['password1'] = 'secret'
        data['password2'] = 'secret'
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(302, response.status_code)
        user = User.objects.all()[0]
        self.assertEqual(1, len(user.djangoperson_set.all()))
        person = user.djangoperson_set.all()[0]
        self.assertAlmostEqual(2, person.location.x, 0)
        self.assertAlmostEqual(45, person.location.y, 0)

    def test_whatnext(self):
        """Redirection after a successful openid login"""
        url = reverse('openid_whatnext')

        # No openid -> homepage
        response = self.client.get(url)
        self.assertRedirects(response, reverse('index'))

        # Anonymous user, openid -> signup
        factory = RequestFactory()
        request = prepare_request(factory.get(url))
        response = openid_whatnext(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('signup'))

        user = User.objects.create_user('testuser', 'foo@example.com', 'pass')
        profile = DjangoPerson.objects.create(
            user=user,
            country=Country.objects.get(pk=1),
            latitude=44,
            longitude=2,
            location_description='Somewhere',
        )
        associate_openid(user, 'http://foo.example.com/')

        # Anonymous user, openid + assoc. with an existing user -> profile
        response = openid_whatnext(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'],
                         reverse('user_profile', args=['testuser']))

        # Authenticated user -> openid associations
        self.client.login(username='testuser', password='pass')
        request = prepare_request(factory.get(url))
        request.session = self.client.session
        response = openid_whatnext(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], reverse('openid_associations'))
