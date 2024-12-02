from django.urls import path
from .views import RestaurantView, MenuUploadView, BrowserPromptView

urlpatterns = [
    path('restaurants/', RestaurantView.as_view(), name='restaurants'),
    path('menus/upload/', MenuUploadView.as_view(), name='menu-upload'),
    path('browser-prompt/', BrowserPromptView.as_view(), name='browser-prompt'),
]
