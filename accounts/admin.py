from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.CustomUser)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'studentid',
        'username',
        'is_staff',
        'date_joined',
        'last_login',
    )
    
    fields = ['studentid', 'username', 'school', 'sports', 'major', 'profile', 'idprofile', 'info_1', 'info_2','idcard', 'is_staff', 'is_superuser',] # detail화면 내 나열순서

    search_fields = ['studentid']