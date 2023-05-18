from django import forms
from .models import CustomUser

class CustomUser_Form(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['studentid', 'username', 'school', 'sports', 'major', 'idcard']