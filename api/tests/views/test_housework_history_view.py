from django.test import TestCase
from rest_framework.test import APIRequestFactory
from api.models.user_model import UserModel
from api.models.house_model import HouseModel
from api.models.house_user_model import HouseUserModel
from api.models.housework_model import HouseworkModel
from api.models.housework_history_model import HouseworkHistoryModel

from api.views.housework_history_view import HouseworkHistoryView


class HouseworkHistoryViewTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.__create_data()

    def __create_data(self):
        UserModel.objects.create(id=1, name='test1', mail_address='test1@example.com', deleted=0)
        HouseModel.objects.create(id=1, name='house1', description='description1', create_user_id=1, deleted=0)
        HouseUserModel.objects.create(id=1, user_id=1, house_id=1, admin_flg=1, status=2, deleted=0)
        HouseworkModel.objects.create(id=1, name='housework1', point=1, house_id=1, deleted=0)
        HouseworkModel.objects.create(id=2, name='housework2', point=2, house_id=1, deleted=0)
        HouseworkHistoryModel.objects.create(id=1, user_id=1, house_id=1, housework_id=1, point=1, date='2022-06-01', approve_flg=0, deleted=0)
        HouseworkHistoryModel.objects.create(id=2, user_id=1, house_id=1, housework_id=2, point=2, date='2022-06-02', approve_flg=0, deleted=0)
        HouseworkHistoryModel.objects.create(id=3, user_id=1, house_id=1, housework_id=1, point=1, date='2022-06-03', approve_flg=0, deleted=1)

    def test_get_all_housework_history(self):
        view = HouseworkHistoryView.as_view({'post': 'get'})
        request = self.factory.post('http://localhost:8000/api/housework_histories/get/')
        response = view(request)
        self.assertEqual(len(response.data), 3)

    def test_get_active_housework_history(self):
        view = HouseworkHistoryView.as_view({'post': 'get'})
        data = {
            'selector': {
                'deleted': 0
            }
        }
        request = self.factory.post('http://localhost:8000/api/housework_histories/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 2)
        for housework_history in response.data:
            self.assertNotEqual(housework_history['id'], 3)

    def test_get_housework_history_specified_id(self):
        view = HouseworkHistoryView.as_view({'post': 'get'})
        data = {
            'selector': {
                'id': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/housework_histories/get/', data=data, format='json')
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)

    def test_set_housework_history(self):
        view = HouseworkHistoryView.as_view({'post': 'set'})
        data = {
            'data': {
                'id': 1,
                'housework_id': 2,
                'date': '2022-05-31',
                'approve_flg': 1
            }
        }
        request = self.factory.post('http://localhost:8000/api/housework_histories/set/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['housework']['id'], 2)
        self.assertEqual(response.data['point'], 2)
        self.assertEqual(response.data['date'], '2022-05-31')
        self.assertEqual(response.data['approve_flg'], 1)

    def test_set_housework_history_approve_flg_exception(self):
        view = HouseworkHistoryView.as_view({'post': 'set'})
        data = {
            'data': {
                'id': 1,
                'housework_id': 2,
                'date': '2022-05-31',
                'approve_flg': 2
            }
        }
        request = self.factory.post('http://localhost:8000/api/housework_histories/set/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['error'], 'MUTATE_VALIDATE_ERORR')

    def test_add_housework_history(self):
        view = HouseworkHistoryView.as_view({'post': 'add'})
        data = {
            'data': {
                'user_id': 1,
                'house_id': 1,
                'housework_id': 2,
                'date': '2022-06-04'
            }
        }
        request = self.factory.post('http://localhost:8000/api/housework_histories/add/', data=data, format='json')
        response = view(request)
        self.assertEqual(response.data['user']['id'], 1)
        self.assertEqual(response.data['housework']['id'], 2)
        self.assertEqual(response.data['house_id'], 1)
        self.assertEqual(response.data['point'], 2)
        self.assertEqual(response.data['approve_flg'], 0)
        self.assertEqual(response.data['date'], '2022-06-04')
