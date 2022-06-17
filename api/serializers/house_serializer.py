from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models.user_model import UserModel
from ..models.house_model import HouseModel
from ..serializers.user_serializer import UserSerializer


class HouseSerializer(serializers.ModelSerializer):

    create_user = serializers.SerializerMethodField()

    class Meta:
        model = HouseModel
        fields = (
            'id',
            'name',
            'description',
            'create_user'
        )

    def get_create_user(self, obj):
        try:
            return UserSerializer(UserModel.objects.get(id=obj.create_user_id)).data
        except:
            return None

    def create(self, validate_data):
        if 'name' not in validate_data.keys():
            raise ValidationError('name key does not exist.')
        if 'description' not in validate_data.keys():
            raise ValidationError('description key does not exist.')
        if 'create_user_id' not in validate_data.keys():
            raise ValidationError('create_user key does not exist.')

        if not UserModel.objects.filter(id=validate_data['create_user_id'], deleted=0).exists():
            raise ValidationError('create_user_id does not exists.')

        house = HouseModel.objects.create(**validate_data)
        return HouseSerializer(house).data

    def update(self, validate_data):
        if 'id' not in validate_data.keys():
            raise ValidationError('id key does not exist.')
        try:
            house = HouseModel.objects.get(id=validate_data['id'], deleted=0)
        except:
            raise ValidationError(f"house id={validate_data['id']} dose not exists.")
        if 'name' in validate_data.keys():
            house.name = validate_data['name']
        if 'description' in validate_data.keys():
            house.description = validate_data['description']
        house.save()
        return HouseSerializer(house).data