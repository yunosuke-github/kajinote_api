from django.db import models

from .base_model import BaseModel
from .user_model import UserModel


class HouseModel(BaseModel):

    class Meta:
        db_table = 'house'

    name = models.CharField(max_length=32, null=False, blank=False)
    description = models.CharField(max_length=300, null=True, blank=True)
    create_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
