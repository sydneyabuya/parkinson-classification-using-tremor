from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello)
    
]

from .views import home, result

urlpatterns = [
    path('', home, name='home'),
    path('result/', result, name='result')
]
