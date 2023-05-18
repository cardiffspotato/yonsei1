from django.urls import path
from . import views

app_name='profile'

urlpatterns = [
    path('<str:sports>/<str:school>', views.Profile_list, name='list'),
    path('<str:sports>/<str:school>/<int:profile_id>', views.Profile_detail, name='detail'),
    path('<str:sports>/<str:school>/<int:profile_id>/sendmessage', views.SendMessage, name='sendmessage'),
    path('<str:sports>/<str:school>/<int:profile_id>/deletemessage', views.DeleteMessage, name='deletemessage'),
]
