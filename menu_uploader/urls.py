from django.urls import path
from .views import upload_menu

urlpatterns = [
    path('upload-menu/', upload_menu, name='upload-menu'),
]
