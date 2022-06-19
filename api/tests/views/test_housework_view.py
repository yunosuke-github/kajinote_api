from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.models.user_model import UserModel
from api.models.house_model import HouseModel
from api.models.housework_model import HouseworkModel

from api.views.housework_view import HouseworkView


class HouseViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.__create_data()

    def __create_data(self):
        UserModel.objects.create(id=1, name='test1', mail_address='test1@example.com', deleted=0)
        HouseModel.objects.create(id=1, name='house1', description='description1', create_user_id=1, deleted=0)
        HouseworkModel.objects.create(id=1, name='housework1', point=1, house_id=1, deleted=0)
        HouseworkModel.objects.create(id=2, name='housework2', point=2, house_id=1, deleted=0)
        HouseworkModel.objects.create(id=3, name='housework3', point=3, house_id=1, deleted=1)

    def test_get_all_housework(self):
        view = HouseworkView.as_view({'post': 'get'})
        request = self.factory.post('http://localhost:8000/api/houseworks/get/')
        response = view(request)
        self.assertEqual(len(response.data), 3)

    def test_get_active_housework(self):
        view = HouseworkView.as_view({'post': 'get'})
        data = {
            'selector': {
                'deleted': 0
            }
        }
        request = self.factory.post('http://localhost:8000/api/houseworks/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for housework in response.data:
            self.assertNotEqual(housework['name'], 'housework3')

    def test_get_housework_specified_id(self):
        view = HouseworkView.as_view({'post': 'get'})
        data = {
            'selector': {
                'id': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/houseworks/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'housework1')

    def test_get_house_specified_id_in(self):
        view = HouseworkView.as_view({'post': 'get'})
        data = {
            'selector': {
                'id__in': [1, 2]
            }
        }
        request = self.factory.post('http://localhost:8000/api/houseworks/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for housework in response.data:
            self.assertNotEqual(housework['id'], 3)

    def test_set_housework(self):
        view = HouseworkView.as_view({'post': 'set'})
        data = {
            'data': {
                'id': 1,
                'name': 'housework5',
                'point': 5
            }
        }
        request = self.factory.post('http://localhost:8000/api/houseworks/set/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['name'], 'housework5')
        self.assertEqual(response.data['point'], 5)

    def test_add_housework(self):
        view = HouseworkView.as_view({'post': 'add'})
        data = {
            'data': {
                'name': 'housework6',
                'point': 6,
                'house_id': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/houseworks/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['name'], 'housework6')
        self.assertEqual(response.data['point'], 6)
        self.assertEqual(response.data['house_id'], 1)
