from django.db import models

from .base_model import BaseModel
from .user_model import UserModel


class LoginSessionModel(BaseModel):

    class Meta:
        db_table = 'login_session'

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=False)
    token = models.CharField(max_length=32, null=False, blank=False)
