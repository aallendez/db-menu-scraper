from django.urls import path
from .views import insert_restaurant

urlpatterns = [
    path('insert-restaurant/', insert_restaurant, name='insert_restaurant')
]