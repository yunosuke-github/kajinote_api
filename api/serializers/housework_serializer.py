from rest_framework import serializers
from django.core.exceptions import ValidationError

from ..models.house_model import HouseModel
from ..models.housework_model import HouseworkModel


class HouseworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = HouseworkModel
        fields = (
            'id',
            'name',
            'point',
            'house_id'
        )

    def create(self, validate_data):
        if 'name' not in validate_data.keys():
            raise ValidationError('name key does not exist.')
        if 'point' not in validate_data.keys():
            raise ValidationError('point key does not exist.')
        if 'house_id' not in validate_data.keys():
            raise ValidationError('house_id key does not exist.')

        if not HouseModel.objects.filter(id=validate_data['house_id'], deleted=0).exists():
            raise ValidationError('house_id does not exists.')
        if HouseworkModel.objects.filter(house_id=validate_data['house_id'], name=validate_data['name'], deleted=0).exists():
            raise ValidationError(f'housework name {validate_data["name"]} already exists.')

        housework = HouseworkModel.objects.create(**validate_data)

        return HouseworkSerializer(housework).data

    def update(self, validate_data):
        if 'id' not in validate_data.keys():
            raise ValidationError('id key does not exist.')
        try:
            housework = HouseworkModel.objects.get(id=validate_data['id'], deleted=0)
        except:
            raise ValidationError(f"housework id={validate_data['id']} dose not exists.")
        if 'name' in validate_data.keys():
            housework.name = validate_data['name']
        if 'point' in validate_data.keys():
            housework.point = validate_data['point']
        housework.save()
        return HouseworkSerializer(housework).data