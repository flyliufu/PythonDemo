from django.urls import path
from . import views

app_name = 'zeus'
urlpatterns = [
    path('token', views.token, name='token'),
    path('test', views.test, name='test')
]
