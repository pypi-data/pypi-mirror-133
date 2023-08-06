from django.urls import path
from .views import test, setting

app_name = 'dbmanager'

urlpatterns = [
    path('setting/', setting, name='setting'),
    path('', test, name='test'),
]
