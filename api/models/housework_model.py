from django.db import models

from .base_model import BaseModel
from .house_model import HouseModel


class HouseworkModel(BaseModel):

    class Meta:
        db_table = 'housework'

    name = models.CharField(max_length=32, null=False, blank=False)
    point = models.IntegerField(null=False, blank=False)
    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE, null=False)
