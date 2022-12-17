from severe import views as v
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
]

from .views import home, result

urlpatterns = [
    path('', home, name='home'),
    path('register', views.register, name='register'),
    path('result/', result, name='result')
]


