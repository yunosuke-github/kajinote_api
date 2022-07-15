from django.db import models

from .base_model import BaseModel


class UserModel(BaseModel):

    class Meta:
        db_table = 'user'

    name = models.CharField(max_length=32, null=False, blank=False)
    password = models.CharField(max_length=32, null=False, blank=False)
    mail_address = models.EmailField(null=False, blank=False)
