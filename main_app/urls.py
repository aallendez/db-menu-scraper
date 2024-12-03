from django.urls import path
from .views import MenuUploadView, GetAllRestaurants, CreateRestaurant, HandleUserQuery, GetAllMenuVersionsFromRestaurant, GetMenuVersion

urlpatterns = [
    path('upload-menu/', MenuUploadView.as_view(), name='menu-upload'),
    path('get-all-restaurants/', GetAllRestaurants.as_view(), name='get-all-restaurants'),
    path('create-restaurant/', CreateRestaurant.as_view(), name='create-restaurant'),
    path('q/', HandleUserQuery.as_view(), name='q'),
    path('get-all-menu-versions-from-restaurant/', GetAllMenuVersionsFromRestaurant.as_view(), name='get-all-menu-versions-from-restaurant'),
    path('get-menu-version/', GetMenuVersion.as_view(), name='get-menu-version'),
]
