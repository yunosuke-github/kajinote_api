from django.db import models

from .base_model import BaseModel
from .user_model import UserModel
from .house_model import HouseModel
from .housework_model import HouseworkModel


class HouseworkHistoryModel(BaseModel):

    class Meta:
        db_table = 'housework_history'

    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE, null=False)
    housework = models.ForeignKey(HouseworkModel, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
    point = models.IntegerField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    approve_flg = models.SmallIntegerField(default=0)
