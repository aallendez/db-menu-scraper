from rest_framework import serializers
from .models import Restaurant, Menu, Cuisine, FoodItem, SummarizedAvgPrices

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class SummarizedAvgPricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummarizedAvgPrices
        fields = ['restaurant_id', 'restaurant_name', 'avg_food_price', 'max_food_price', 'min_food_price']
