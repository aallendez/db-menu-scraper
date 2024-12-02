from django.urls import path
from .views import MenuUploadView, GetAllRestaurants, CreateRestaurant, HandleUserQuery

urlpatterns = [
    path('upload-menu/', MenuUploadView.as_view(), name='menu-upload'),
    path('get-all-restaurants/', GetAllRestaurants.as_view(), name='get-all-restaurants'),
    path('create-restaurant/', CreateRestaurant.as_view(), name='create-restaurant'),
    path('handle-user-query/', HandleUserQuery.as_view(), name='handle-user-query'),
]
