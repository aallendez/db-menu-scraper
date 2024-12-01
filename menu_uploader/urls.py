from django.urls import path
from .views import upload_menu

urlpatterns = [
    path('', upload_menu.as_view(), name='upload-menu'),
]