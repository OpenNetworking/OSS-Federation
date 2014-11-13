from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .forms import IssuerCreationForm, ColorCreationForm, AddressInputForm
from .models import Issuer, Color, Address, ColorHistory, AddressHistory
# Create your tests here.

class IssuerViewTests(TestCase):

    def setUp(self):

        # create test data
        for i in range(10):
            issuer_name = 'issuer{0}'.format(i)
            issuer_password = '12345{0}'.format(i)
            issuer_register_url = 'http://google{0}.com.tw'.format(i)
            user = User.objects.create(username=issuer_name,
                                       password=issuer_password)
            Issuer.objects.create(user=user, register_url=issuer_register_url)

        issuer = Issuer.objects.get(pk=1)
        for i in range(10):
            color_name = 'color{0}'.format(i)
            address_name = 'address{0}'.format(i)
            address = Address(address=address_name, issuer=issuer)
            address.save()
            is_confirmed = True if i % 2 == 0 else False
            color = Color(color_id=i+1, color_name=color_name,
                          issuer=issuer, address=address,
                          is_confirmed=is_confirmed)
            color.save()


    def tearDown(self):
        Issuer.objects.all().delete()

    def test_issuer_create_view(self):
        # test GET
        response = self.client.get('/issuer/create/')
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['issuer_form'],
                              IssuerCreationForm)
        self.assertIsInstance(response.context['user_form'],
                              UserCreationForm)

        response = self.client.get('/issuer/create')
        self.assertEquals(response.status_code, 301)

        # test POST
        # good input
        response = self.client.post('/issuer/create/',
                                     {'username': 'test',
                                      'password1': 'password',
                                      'password2': 'password',
                                      'register_url': 'http://test.com'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'success')

        # miss required fileds
        response = self.client.post('/issuer/create/', {})
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
        response = self.client.post('/issuer/create/',
                                    {'username': 'test',
                                     'password1': 'password',
                                     'password2': 'password',
                                     'register_url': 'http://test.com'})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'username',
                             'A user with that username already exists.')

        # two password didn't match
        response = self.client.post('/issuer/create/',
                                    {'username': 'test',
                                     'password1': 'password',
                                     'password2': 'password2',
                                     'register_url': 'http://test.com'})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'user_form', 'password2',
                             "The two password fields didn't match.")



    def test_issuer_delete_view(self):
        response = self.client.get('/issuer/update/')
        self.assertEquals(response.status_code, 200)

    def test_issuer_detail_view(self):
        response = self.client.get('/issuer/1/detail/')
        self.assertEquals(response.status_code, 200)
        issuer = Issuer.objects.get(pk=1)
        self.assertEquals(repr(issuer), repr(response.context['issuer']))

        response = self.client.get('/issuer/1/detail')
        self.assertEquals(response.status_code, 301)
        response = self.client.get('/issuer/100/detail/')
        self.assertEquals(response.status_code, 404)
        response = self.client.get('/issuer/dd/detail/')
        self.assertEquals(response.status_code, 404)

    def test_add_color_view(self):
        # test GET
        response = self.client.get('/issuer/1/add_color/')
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['color_form'],
                              ColorCreationForm)
        self.assertIsInstance(response.context['address_form'],
                              AddressInputForm)

        response = self.client.get('/issuer/1/add_color')
        self.assertEquals(response.status_code, 301)
        response = self.client.get('/issuer/3001/add_color/')
        self.assertEquals(response.status_code, 404)
        response = self.client.get('/issuer/dd/add_color/')
        self.assertEquals(response.status_code, 404)

        # test POST
        response = self.client.post('/issuer/1/add_color/',
                                    {'color_name': 'test_color',
                                     'address': 'test_address'})
        self.assertEquals(response.status_code, 302)

        # miss fields
        response = self.client.post('/issuer/1/add_color/', {})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'color_form', 'color_name',
                             'This field is required.')
        self.assertFormError(response, 'address_form', 'address',
                             'This field is required.')

        # duplicate color name
        response = self.client.post('/issuer/1/add_color/',
                                    {'color_name': 'test_color',
                                     'address': 'test_address'})
        self.assertEquals(response.status_code, 200)
        self.assertFormError(response, 'color_form', 'color_name',
                             'Color with this Color name already exists.')


    def test_issuer_list_view(self):
        response = self.client.get('/issuer/issuer_list/')
        self.assertEquals(response.status_code, 200)
        issuer_list = map(lambda x: repr(x),
                          response.context['issuer_list'])
        self.assertQuerysetEqual(Issuer.objects.filter(user__is_active=True),
                                 issuer_list,
                                 ordered=False)
        response = self.client.get('/issuer/issuer_list')
        self.assertEquals(response.status_code, 301)

    def test_unconfirmed_issuer_list_view(self):
        response = self.client.get('/issuer/unconfirmed_issuer_list/')
        self.assertEquals(response.status_code, 200)
        issuer_list = map(lambda x: repr(x),
                          response.context['issuer_list'])
        self.assertQuerysetEqual(Issuer.objects.filter(user__is_active=False),
                                 issuer_list,
                                 ordered=False)
        response = self.client.get('/issuer/unconfirmed_issuer_list')
        self.assertEquals(response.status_code, 301)

    def test_color_list_view(self):
        response = self.client.get('/issuer/color_list/')
        self.assertEquals(response.status_code, 200)
        color_list = map(lambda x: repr(x),
                         response.context['color_list'])
        self.assertQuerysetEqual(Color.objects.filter(is_confirmed=True),
                                 color_list,
                                 ordered=False)

        response = self.client.get('/issuer/color_list')
        self.assertEquals(response.status_code, 301)

    def test_unconfirmed_color_list_view(self):
        response = self.client.get('/issuer/unconfirmed_color_list/')
        self.assertEquals(response.status_code, 200)
        color_list = map(lambda x: repr(x),
                         response.context['color_list'])
        self.assertQuerysetEqual(Color.objects.filter(is_confirmed=False),
                                 color_list,
                                 ordered=False)

        response = self.client.get('/issuer/unconfirmed_color_list')
        self.assertEquals(response.status_code, 301)




