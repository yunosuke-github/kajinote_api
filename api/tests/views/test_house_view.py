from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from api.models.user_model import UserModel
from api.models.house_model import HouseModel

from api.views.house_view import HouseView


class HouseViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.__create_data()

    def __create_data(self):
        UserModel.objects.create(id=1, name='user1', mail_address='user1@example.com', deleted=0)
        UserModel.objects.create(id=2, name='user2', mail_address='user2@example.com', deleted=1)
        HouseModel.objects.create(id=1, name='house1', description='description1', create_user_id=1, deleted=0)
        HouseModel.objects.create(id=2, name='house2', description='description1', create_user_id=2, deleted=0)
        HouseModel.objects.create(id=3, name='house3', description='description1', create_user_id=1, deleted=1)

    def test_get_all_house(self):
        view = HouseView.as_view({'post': 'get'})
        request = self.factory.post('http://localhost:8000/api/houses/get/')
        response = view(request)
        self.assertEqual(len(response.data), 3)

    def test_get_active_house(self):
        view = HouseView.as_view({'post': 'get'})
        data = {
            'selector': {
                'deleted': 0
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for user in response.data:
            self.assertNotEqual(user['name'], 'house3')

    def test_get_house_specified_id(self):
        view = HouseView.as_view({'post': 'get'})
        data = {
            'selector': {
                'id': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'house1')

    def test_get_house_specified_id_in(self):
        view = HouseView.as_view({'post': 'get'})
        data = {
            'selector': {
                'name__in': ['house1', 'house2']
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for user in response.data:
            self.assertNotEqual(user['name'], 'house3')

    def test_get_house_specified_create_user_id(self):
        view = HouseView.as_view({'post': 'get'})
        data = {
            'selector': {
                'create_user_id': 1,
                'deleted': 0,
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'house1')

    def test_set_house(self):
        view = HouseView.as_view({'post': 'set'})
        data = {
            'data': {
                'id': 1,
                'name': 'house4',
                'description': 'description4'
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/set/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['name'], 'house4')
        self.assertEqual(response.data['description'], 'description4')

    def test_add_house(self):
        view = HouseView.as_view({'post': 'add'})
        data = {
            'data': {
                'name': 'house4',
                'description': 'description4',
                'create_user_id': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['name'], 'house4')
        self.assertEqual(response.data['description'], 'description4')
        self.assertEqual(response.data['create_user']['id'], 1)
        self.assertEqual(response.data['create_user']['name'], 'user1')

    def test_add_house_unspecified_user_id(self):
        view = HouseView.as_view({'post': 'add'})
        data = {
            'data': {
                'name': 'house4',
                'description': 'description4'
            }
        }
        request = self.factory.post('http://localhost:8000/api/houses/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['error'], 'MUTATE_VALIDATE_ERORR')

    def test_add_user_duplicate_email_address(self):
        view = HouseView.as_view({'post': 'add'})
        data = {
            'data': {
                'name': 'test4',
                'mail_address': 'test1@example.com'
            }
        }
        request = self.factory.post('http://localhost:8000/api/users/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['error'], 'MUTATE_VALIDATE_ERORR')