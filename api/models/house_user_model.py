from django.db import models

from ..enums.house_user_status import HouseUserStatus
from .base_model import BaseModel
from .user_model import UserModel
from .house_model import HouseModel


class HouseUserModel(BaseModel):

    class Meta:
        db_table = 'house_user'

    house = models.ForeignKey(HouseModel, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
    status = models.IntegerField(null=False)
    admin_flg = models.SmallIntegerField(default=0)
