from django.db import models
from menu_uploader.models import Restaurant, Menu

# Create your models here.

# Restaurant Queries
def get_all_restaurants():
    return Restaurant.objects.all()

def get_restaurant_by_id(restaurant_id):
    return Restaurant.objects.get(restaurant_id=restaurant_id)

def get_restaurant_by_name(restaurant_name):
    return Restaurant.objects.filter(restaurant_name__icontains=restaurant_name)

def get_restaurant_by_cuisine(cuisine_name):
    return Restaurant.objects.filter(cuisine_name__icontains=cuisine_name)

def get_restaurant_by_location(location):
    return Restaurant.objects.filter(location__icontains=location)


# Menu Queries
def get_all_menus():
    return Menu.objects.all()

def get_menu_by_id(menu_id):
    return Menu.objects.get(menu_id=menu_id)

def get_latest_menu_by_restaurant_id(restaurant_id):
    return Menu.objects.filter(restaurant_id=restaurant_id).order_by('-menu_version_id').first()