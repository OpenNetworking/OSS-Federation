from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from oss.apps.issuer.models import Issuer, Color
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


    def tearDown(self):
        Issuer.objects.all().delete()
        User.objects.all().delete()

    def test_home_view(self):

        # no login
        response = self.client.get('/website/')
        self.assertEquals(response.status_code, 302)

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
        self.assertRedirects(response,
                             '/website/login/?next=/website/add_color/')

        # post
        response = self.client.post('/website/add_color/',
                                    {'color_name': 'test_color',
                                     'address': 'test_color'})
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


