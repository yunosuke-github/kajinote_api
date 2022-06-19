from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.models.user_model import UserModel
from api.models.house_model import HouseModel
from api.models.house_user_model import HouseUserModel

from api.views.house_user_view import HouseUserView


class HouseUserViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.__create_data()

    def __create_data(self):
        UserModel.objects.create(id=1, name='user1', mail_address='user1@example.com', deleted=0)
        UserModel.objects.create(id=2, name='user2', mail_address='user2@example.com', deleted=0)
        UserModel.objects.create(id=3, name='user3', mail_address='user3@example.com', deleted=0)
        HouseModel.objects.create(id=1, name='house1', description='description1', create_user_id=1, deleted=0)
        HouseModel.objects.create(id=2, name='house2', description='description1', create_user_id=1, deleted=0)
        HouseUserModel.objects.create(id=1, user_id=1, house_id=1, status=1, admin_flg=0)
        HouseUserModel.objects.create(id=2, user_id=2, house_id=1, status=2, admin_flg=0)
        HouseUserModel.objects.create(id=3, user_id=3, house_id=1, status=3, admin_flg=1)
        HouseUserModel.objects.create(id=4, user_id=1, house_id=2, status=3, admin_flg=1)

    def test_get_all_house_user(self):
        view = HouseUserView.as_view({'post': 'get'})
        request = self.factory.post('http://localhost:8000/api/house_users/get/')
        response = view(request)
        self.assertEqual(len(response.data), 4)

    def test_get_house_user_specified_house_id(self):
        view = HouseUserView.as_view({'post': 'get'})
        data = {
            'selector': {
                'house_id': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/house_users/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 3)
        for house_user in response.data:
            self.assertEqual(house_user['house']['id'], 1)

    def test_add_house_user(self):
        view = HouseUserView.as_view({'post': 'add'})
        data = {
            'data': {
                'house_id': 2,
                'user_id': 2
            }
        }
        request = self.factory.post('http://localhost:8000/api/house_users/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['house']['id'], 2)
        self.assertEqual(response.data['status'], 1)
        self.assertEqual(response.data['admin_flg'], 0)
