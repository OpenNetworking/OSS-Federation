from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from oss.apps.issuer.models import Issuer, Color, Address
from oss.apps.issuer.forms import (IssuerCreationForm, ColorCreationForm,
                                   AddressInputForm)

import config
# Create your tests here.

class WebsiteViewTest(TestCase):

    def setUp(self):
        # create a issuer
        user = User.objects.create_user(username='test',
                                        password='test',
                                        email='test@test.com')
        issuer = Issuer(user=user, register_url='http://test.com')
        issuer.save()
        issuer.active()
        address = Address(address='addr_test_color',
                          issuer=issuer)

        address.save()
        color = Color(color_id=1,
                      color_name='color_test',
                      address=address,
                      issuer=issuer)
        color.save()

        user2 = User.objects.create_user(username='test2',
                                         password='test2',
                                         email='test2@test2.com')
        issuer2 = Issuer(user=user2, register_url='http://test2.com')
        issuer2.save()
        issuer2.active()
        address = Address(address='addr_test2_color',
                          issuer=issuer2)

        address.save()
        color = Color(color_id=2,
                      color_name='color_test2',
                      address=address,
                      issuer=issuer2)
        color.save()

    def tearDown(self):
        Issuer.objects.all().delete()
        User.objects.all().delete()
        Color.objects.all().delete()

    def test_home_view(self):

        # no login
        response = self.client.get('/website/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             '/website/login/?next=/website/')

        # login
        user = User.objects.get(username='test')
        response = self.client.login(username='test', password='test')
        self.assertTrue(response)
        response = self.client.get('/website/')
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['issuer'], Issuer)
        self.assertEquals(response.context['issuer'].pk, user.issuer.pk)

    def test_signup_view(self):

        # test GET
        response = self.client.get('/website/signup/')
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['user_form'],
                              UserCreationForm)
        self.assertIsInstance(response.context['issuer_form'],
                              IssuerCreationForm)


        # test POST
        response = self.client.post('/website/signup/',
                                    {'username': 'test',
                                     'password1': 'password',
                                     'password2': 'password',
                                     'register_url': 'http://test.com'})
        self.assertEquals(response.status_code, 200)

        # miss required fields
        response = self.client.post('/website/signup/', {})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'username',
                             'This field is required.')
        self.assertFormError(response, 'user_form', 'password1',
                             'This field is required.')
        self.assertFormError(response, 'user_form', 'password2',
                             'This field is required.')
        self.assertFormError(response, 'issuer_form', 'register_url',
                             'This field is required.')

        # duplicate username
        response = self.client.post('/website/signup/',
                                    {'username': 'test',
                                     'password1': 'password',
                                     'password2': 'password',
                                     'register_url': 'http://test.com'})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'username',
                             'A user with that username already exists.')

        # two password didn't match
        response = self.client.post('/website/signup/',
                                    {'username': 'test',
                                     'password1': 'password',
                                     'password2': 'password2',
                                     'register_url': 'http://test.com'})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'password2',
                             "The two password fields didn't match.")

    def test_add_color_view(self):

        # no login

        # get
        response = self.client.get('/website/add_color/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             '/website/login/?next=/website/add_color/')

        # post
        response = self.client.post('/website/add_color/',
                                    {'color_name': 'test_color',
                                     'address': 'test_color'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response,
                             '/website/login/?next=/website/add_color/')

        # login
        response = self.client.login(username='test', password='test')
        self.assertTrue(response)

        # get
        response = self.client.get('/website/add_color/')
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['color_form'],
                              ColorCreationForm)
        self.assertIsInstance(response.context['address_form'],
                              AddressInputForm)

        # post
        response = self.client.post('/website/add_color/',
                                    {'color_name': 'test_color',
                                     'address': 'test_color'})
        self.assertRedirects(response, '/website/')
        color = Color.objects.get(color_name='test_color')
        user = User.objects.get(username='test')
        self.assertEquals(config.AUTO_CONFIRM_COLOR_REGISTRATION,
                          color.is_confirmed)
        self.assertEquals(color.issuer.pk, user.issuer.pk)

        # duplicate username
        response = self.client.post('/website/add_color/',
                                    {'color_name': 'test_color',
                                     'address': 'test_color'})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'color_form', 'color_name',
                             'Color with this Color name already exists.')
        # miss required fields
        response = self.client.post('/website/add_color/', {})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'color_form', 'color_name',
                             'This field is required.')
        self.assertFormError(response, 'address_form', 'address',
                             'This field is required.')

    def test_website_issuer_update_view(self):

        # no login
        response = self.client.get('/website/update/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/website/login/?next=/website/update/')

        response = self.client.post('/website/update/')
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/website/login/?next=/website/update/')

        # login
        response = self.client.login(username='test', password='test')
        self.assertTrue(response)

        # get
        response = self.client.get('/website/update/')
        self.assertEquals(response.status_code, 200)

        # post
        response = self.client.post('/website/update/',
                                    {'register_url': 'http://www.test2.com/'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/website/')
        issuer = Issuer.objects.get(user__username='test')
        self.assertEquals(issuer.register_url, 'http://www.test2.com/')

        response = self.client.post('/website/update/', {})
        self.assertFormError(response, 'form', 'register_url',
                             'This field is required.')

        response = self.client.post('/website/update/',
                                    {'register_url': 'http://www.test2.com/'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/website/')
        issuer = Issuer.objects.get(user__username='test')
        self.assertEquals(issuer.register_url, 'http://www.test2.com/')

    def test_color_detail_view(self):

        # no login
        color = Color.objects.get(color_name='color_test2')
        color_detail_url = '/website/color/{0}/detail/'
        url = color_detail_url.format(color.pk)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
        redirect_url = '/website/login/?next={0}'.format(url)
        self.assertRedirects(response, redirect_url)

        # login
        response = self.client.login(username='test', password='test')
        self.assertTrue(response)

        # get not my color
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

        # get my color
        color = Color.objects.get(color_name='color_test')
        url = color_detail_url.format(color.pk)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(repr(color), repr(response.context['color']))

