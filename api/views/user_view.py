from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DataError
from django.core.exceptions import ValidationError

from .base_view import BaseView
from ..enums.error_code import ErrorCode
from ..models.user_model import UserModel
from ..serializers.user_serializer import UserSerializer


class UserView(viewsets.ModelViewSet, BaseView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def get(self, request, pk=None):
        selector, errors = self.get_selector(request, UserModel)
        if len(errors) > 0:
            return Response(data=errors, status=400)
        users = UserModel.objects.filter(**selector)
        data = UserSerializer(users, many=True).data
        return Response(data)

    @action(detail=False, methods=['post'])
    def add(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to add.'}, status=400)
        try:
            user = UserSerializer().create(request.data['data'])
        except DataError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[1]}
            return Response(data=error, status=400)
        except ValidationError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[0]}
            return Response(data=error, status=400)
        return Response(data=user, status=201)

    @action(detail=False, methods=['post'])
    def set(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to set.'}, status=400)
        try:
            user = UserSerializer().update(request.data['data'])
        except DataError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[1]}
            return Response(data=error, status=400)
        except ValidationError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[0]}
            return Response(data=error, status=400)
        return Response(data=user, status=201)