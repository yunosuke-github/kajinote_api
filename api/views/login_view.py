import secrets
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DataError
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from api.models.login_session_model import LoginSessionModel

from .base_view import BaseView
from ..enums.error_code import ErrorCode
from ..models.user_model import UserModel
from ..serializers.user_serializer import UserSerializer


class LoginView(viewsets.ModelViewSet, BaseView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    @action(detail=False, methods=['post'])
    def doLogin(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to set.'}, status=400)
        if 'mail_address' not in request.data['data'].keys():
            raise ValidationError('mail_address key does not exist.')
        if 'password' not in request.data['data'].keys():
            raise ValidationError('password key does not exist.')
        try:
            user = UserModel.objects.get(
                    mail_address=request.data['data']['mail_address'],
                    password=request.data['data']['password'],
                    deleted=0
                )
        except UserModel.DoesNotExist as e:
            return Response(data={'error': ErrorCode.DOES_NOT_EXISTS.name, 'detail': 'User does not exists.'}, status=400)
        LoginSessionModel.objects.filter(user_id=user.id).delete()
        login_session = LoginSessionModel.objects.create(
            user_id=user.id,
            token=secrets.token_hex(16),
        )
        res_data = {'user_id': login_session.user_id, 'token': login_session.token}
        return Response(data=res_data, status=200)
