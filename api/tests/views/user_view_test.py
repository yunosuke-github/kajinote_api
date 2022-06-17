from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class UserViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_user(self):
        res = self.client.post('api/user/get/')
        print(res)