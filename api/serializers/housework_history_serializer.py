from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models.user_model import UserModel
from ..models.house_model import HouseModel
from ..models.housework_model import HouseworkModel
from ..models.housework_history_model import HouseworkHistoryModel
from ..models.house_user_model import HouseUserModel
from ..serializers.user_serializer import UserSerializer
from ..serializers.housework_serializer import HouseworkSerializer


class HouseworkHistorySerializer(serializers.ModelSerializer):

    housework = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = HouseworkHistoryModel
        fields = (
            'id',
            'house_id',
            'housework',
            'user',
            'point',
            'date',
            'approve_flg'
        )

    def get_user(self, obj):
        try:
            return UserSerializer(UserModel.objects.get(id=obj.user_id)).data
        except:
            return None

    def get_housework(self, obj):
        try:
            return HouseworkSerializer(HouseworkModel.objects.get(id=obj.housework_id)).data
        except:
            return None

    def create(self, validate_data):
        if 'house_id' not in validate_data.keys():
            raise ValidationError('house_id key does not exist.')
        if 'housework_id' not in validate_data.keys():
            raise ValidationError('housework_id key does not exist.')
        if 'user_id' not in validate_data.keys():
            raise ValidationError('user_id key does not exist.')
        if 'date' not in validate_data.keys():
            raise ValidationError('date key does not exist.')

        if not UserModel.objects.filter(id=validate_data['user_id'], deleted=0).exists():
            raise ValidationError('user_id does not exists.')
        if not HouseModel.objects.filter(id=validate_data['house_id'], deleted=0).exists():
            raise ValidationError('house_id does not exists.')
        if not HouseUserModel.objects.filter(user_id=validate_data['user_id'], house_id=validate_data['house_id'], deleted=0).exists():
            raise ValidationError('user_id is not registered in house_id.')
        if not HouseworkModel.objects.filter(id=validate_data['housework_id'], deleted=0).exists():
            raise ValidationError('housework_id does not exists.')

        housework = HouseworkModel.objects.get(id=validate_data['housework_id'])
        validate_data['point'] = housework.point
        validate_data['approve_flg'] = 0
        housework_history = HouseworkHistoryModel.objects.create(**validate_data)
        return HouseworkHistorySerializer(housework_history).data

    def update(self, validate_data):
        if 'id' not in validate_data.keys():
            raise ValidationError('id key does not exist.')
        if 'housework_id' in validate_data.keys():
            if not HouseworkModel.objects.filter(id=validate_data['housework_id'], deleted=0).exists():
                raise ValidationError('housework_id does not exists.')
        try:
            housework_history = HouseworkHistoryModel.objects.get(id=validate_data['id'], deleted=0)
        except:
            raise ValidationError(f"housework id={validate_data['id']} dose not exists.")
        if 'date' in validate_data.keys():
            housework_history.date = validate_data['date']
        if 'housework_id' in validate_data.keys():
            housework = HouseworkModel.objects.get(id=validate_data['housework_id'], deleted=0)
            housework_history.housework_id = housework.id
            housework_history.point = housework.point
        housework_history.save()
        return HouseworkHistorySerializer(housework_history).data
