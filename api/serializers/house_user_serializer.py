from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..enums.house_user_status import HouseUserStatus
from ..models.user_model import UserModel
from ..models.house_model import HouseModel
from ..models.house_user_model import HouseUserModel
from ..serializers.user_serializer import UserSerializer
from ..serializers.house_serializer import HouseSerializer


class HouseUserSerializer(serializers.ModelSerializer):

    house = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = HouseUserModel
        fields = (
            'id',
            'house',
            'user',
            'status',
            'admin_flg'
        )

    def get_user(self, obj):
        try:
            return UserSerializer(UserModel.objects.get(id=obj.user_id)).data
        except:
            return None

    def get_house(self, obj):
        try:
            return HouseSerializer(HouseModel.objects.get(id=obj.house_id)).data
        except:
            return None

    def create(self, validate_data):
        if 'house_id' not in validate_data.keys():
            raise ValidationError('name key does not exist.')
        if 'user_id' not in validate_data.keys():
            raise ValidationError('description key does not exist.')

        if not UserModel.objects.filter(id=validate_data['user_id'], deleted=0).exists():
            raise ValidationError('user_id does not exists.')
        if not HouseModel.objects.filter(id=validate_data['house_id'], deleted=0).exists():
            raise ValidationError('house_id does not exists.')

        if HouseUserModel.objects.filter(house_id=validate_data['house_id'], 
            user_id=validate_data['user_id'], deleted=0).exists():
            raise ValidationError('The user is already registered in the specified house.')

        validate_data['status'] = HouseUserStatus.INVITING.id
        validate_data['admin_flg'] = 0
        house_user = HouseUserModel.objects.create(**validate_data)
        return HouseUserSerializer(house_user).data
