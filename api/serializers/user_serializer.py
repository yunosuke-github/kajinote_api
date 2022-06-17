from rest_framework import serializers
from django.db.utils import DataError
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from ..models.user_model import UserModel


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = (
            'id',
            'name',
            'mail_address'
        )

    def create(self, validate_data):
        if 'name' not in validate_data.keys():
            raise ValidationError('name key does not exist.')
        if 'mail_address' not in validate_data.keys():
            raise ValidationError('mail_address key does not exist.')
        validate_email(validate_data['mail_address'])
        if UserModel.objects.filter(mail_address=validate_data['mail_address'], deleted=0).exists():
            raise ValidationError('Email address already exists.')
        user = UserModel.objects.create(**validate_data)
        return UserSerializer(user).data

    def update(self, validate_data):
        if 'id' not in validate_data.keys():
            raise ValidationError('id key does not exist.')
        try:
            user = UserModel.objects.get(id=validate_data['id'], deleted=0)
        except:
            raise ValidationError(f"user id={validate_data['id']} dose not exists.")
        if 'name' in validate_data.keys():
            user.name = validate_data['name']
        if 'mail_address' in validate_data.keys():
            if UserModel.objects.filter(mail_address=validate_data['mail_address'], deleted=0).exclude(id=user.id).exists():
                raise ValidationError('Email address already exists.')
            user.mail_address = validate_data['mail_address']
        user.save()
        return UserSerializer(user).data