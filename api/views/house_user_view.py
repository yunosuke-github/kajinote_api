from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DataError
from django.core.exceptions import ValidationError

from .base_view import BaseView
from ..enums.error_code import ErrorCode
from ..models.house_user_model import HouseUserModel
from ..serializers.house_user_serializer import HouseUserSerializer


class HouseUserView(viewsets.ModelViewSet, BaseView):
    queryset = HouseUserModel.objects.all()
    serializer_class = HouseUserSerializer

    @action(detail=False, methods=['post'])
    def get(self, request, pk=None):
        selector, errors = self.get_selector(request, HouseUserModel)
        if len(errors) > 0:
            return Response(data=errors, status=400)
        house_users = HouseUserModel.objects.filter(**selector)
        data = HouseUserSerializer(house_users, many=True).data
        return Response(data)

    @action(detail=False, methods=['post'])
    def add(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to add.'}, status=400)
        try:
            house_user = HouseUserSerializer().create(request.data['data'])
        except DataError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[1]}
            return Response(data=error, status=400)
        except ValidationError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[0]}
            return Response(data=error, status=400)
        return Response(data=house_user, status=201)

    @action(detail=False, methods=['post'])
    def remove(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to remove.'}, status=400)
        if 'user_id' not in request.data['data'].keys():
            return Response(data={'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': 'user_id not specified.'}, status=400)
        HouseUserModel().objects.filter(user_id=request.data['data']['user_id']).delete()
        return Response(status=204)