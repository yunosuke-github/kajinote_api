from django.contrib import admin

from .models.user_model import UserModel


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    fields = ['name', 'mail_address', 'deleted', 'created_at', 'created_by', 'updated_at', 'updated_by']
