from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from api.models.user_model import UserModel

from api.views.user_view import UserView


class UserViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.__create_data()

    def __create_data(self):
        UserModel.objects.create(id=1, name='test1', mail_address='test1@example.com', deleted=0)
        UserModel.objects.create(id=2, name='test2', mail_address='test2@example.com', deleted=0)
        UserModel.objects.create(id=3, name='test3', mail_address='test3@example.com', deleted=1)

    def test_get_all_user(self):
        view = UserView.as_view({'post': 'get'})
        request = self.factory.post('http://localhost:8000/api/users/get/')
        response = view(request)
        self.assertEqual(len(response.data), 3)

    def test_get_active_user(self):
        view = UserView.as_view({'post': 'get'})
        data = {
            'selector': {
                'deleted': 0
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for user in response.data:
            self.assertNotEqual(user['name'], 'test3')

    def test_get_user_specified_name(self):
        view = UserView.as_view({'post': 'get'})
        data = {
            'selector': {
                'name': 'test1'
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'test1')

    def test_get_user_specified_name_in(self):
        view = UserView.as_view({'post': 'get'})
        data = {
            'selector': {
                'name__in': ['test1', 'test2']
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for user in response.data:
            self.assertNotEqual(user['name'], 'test3')

    def test_set_user(self):
        view = UserView.as_view({'post': 'set'})
        data = {
            'data': {
                'id': 1,
                'name': 'test4',
                'mail_address': 'test4@example.com'
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/set/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['name'], 'test4')
        self.assertEqual(response.data['mail_address'], 'test4@example.com')

    def test_set_user_duplicate_mail_address(self):
        view = UserView.as_view({'post': 'set'})
        data = {
            'data': {
                'id': 1,
                'name': 'test4',
                'mail_address': 'test2@example.com'
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/set/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['error'], 'MUTATE_VALIDATE_ERORR')

    def test_add_user(self):
        view = UserView.as_view({'post': 'add'})
        data = {
            'data': {
                'name': 'test4',
                'mail_address': 'test4@example.com'
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['name'], 'test4')
        self.assertEqual(response.data['mail_address'], 'test4@example.com')

    def test_add_user_duplicate_email_address(self):
        view = UserView.as_view({'post': 'add'})
        data = {
            'data': {
                'name': 'test4',
                'mail_address': 'test1@example.com'
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['error'], 'MUTATE_VALIDATE_ERORR')