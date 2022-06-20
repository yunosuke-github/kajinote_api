from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.utils import DataError
from django.core.exceptions import ValidationError

from .base_view import BaseView
from ..enums.error_code import ErrorCode
from ..models.housework_model import HouseworkModel
from ..models.housework_history_model import HouseworkHistoryModel
from ..serializers.housework_serializer import HouseworkSerializer
from ..serializers.housework_history_serializer import HouseworkHistorySerializer


class HouseworkHistoryView(viewsets.ModelViewSet, BaseView):
    queryset = HouseworkHistoryModel.objects.all()
    serializer_class = HouseworkHistorySerializer

    @action(detail=False, methods=['post'])
    def get(self, request, pk=None):
        selector, errors = self.get_selector(request, HouseworkHistoryModel)
        if len(errors) > 0:
            return Response(data=errors, status=400)
        housework_histories = HouseworkHistoryModel.objects.filter(**selector)
        data = HouseworkHistorySerializer(housework_histories, many=True).data
        return Response(data)

    @action(detail=False, methods=['post'])
    def add(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to add.'}, status=400)
        try:
            housework_history = HouseworkHistorySerializer().create(request.data['data'])
        except DataError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[1]}
            return Response(data=error, status=400)
        except ValidationError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[0]}
            return Response(data=error, status=400)
        return Response(data=housework_history, status=201)

    @action(detail=False, methods=['post'])
    def set(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to set.'}, status=400)
        try:
            housework_history = HouseworkHistorySerializer().update(request.data['data'])
        except DataError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[1]}
            return Response(data=error, status=400)
        except ValidationError as e:
            error = {'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': e.args[0]}
            return Response(data=error, status=400)
        return Response(data=housework_history, status=201)

    @action(detail=False, methods=['post'])
    def remove(self, request, pk=None):
        if 'data' not in request.data.keys():
            return Response(data={'error': ErrorCode.DATA_NONE.name, 'detail': 'Please specify the data to remove.'}, status=400)
        if not 'housework_history_id' in request.data['data'].keys():
            return Response(data={'error': ErrorCode.MUTATE_VALIDATE_ERORR.name, 'detail': 'Please specify the data.housework_hisotry_id to remove.'}, status=400)
        HouseworkHistoryModel().objects.filter(request.data['data']['housework_history_id']).delete()
        return Response(status=204)
