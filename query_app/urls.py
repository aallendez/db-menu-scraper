from django.urls import path
from .views import get_restaurant_by_id

urlpatterns = [
    path('get-restaurant-by-id/<int:restaurant_id>/', get_restaurant_by_id, name='get_restaurant_by_id')
]
