from django.contrib import admin
from .models import Profile, Message

# Register your models here.

#class Profile_Admin(admin.ModelAdmin):
    
#    list_display = ('username', 'school', 'sports')  #list화면
    
class Message_Admin(admin.ModelAdmin):
    
    list_display = ('profile', 'text')  #list화면

#admin.site.register(Profile, Profile_Admin)
admin.site.register(Profile)
admin.site.register(Message, Message_Admin)