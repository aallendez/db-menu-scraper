from django.db import models

class ProcessLog(models.Model):
    process_log_id = models.AutoField(primary_key=True)
    process_date = models.DateTimeField(auto_now_add=True)
    process_output = models.CharField(max_length=255)
    process_message = models.TextField()
    
    def __str__(self):
        return f"{self.process_name} - {self.process_date}"

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Menu(models.Model):
    menu_version_id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    menu_text = models.TextField()
    
    def __str__(self):
        return f"{self.menu_version_id} - {self.creation_date}"

class RestaurantMenu(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    menu_version_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.restaurant_id} - {self.menu_version_id}"
    
class Cuisine(models.Model):
    cuisine_id = models.AutoField(primary_key=True)
    cuisine_type = models.CharField(max_length=255)
    
    def __str__(self):
        return self.cuisine_type

class RestaurantCuisine(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    cuisine_id = models.ForeignKey(Cuisine, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.restaurant_id} - {self.cuisine_id}"
    
class DishType(models.Model):
    dish_type_id = models.AutoField(primary_key=True)
    dish_type = models.CharField(max_length=255)
    
    def __str__(self):
        return self.dish_type
    
class FoodItem(models.Model):
    food_id = models.AutoField(primary_key=True)
    food_name = models.CharField(max_length=255)
    food_description = models.TextField()
    food_price = models.FloatField()
    
    def __str__(self):
        return self.food_name
    
class MenuFoodItem(models.Model):
    menu_version_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    food_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.menu_version_id} - {self.food_id}"

class DishTypeFoodItem(models.Model):
    dish_type_id = models.ForeignKey(DishType, on_delete=models.CASCADE)
    food_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.dish_type_id} - {self.food_id}"
    
class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.ingredient_name

class FoodItemIngredient(models.Model):
    food_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.food_id} - {self.ingredient_id}"
    
class Allergen(models.Model):
    allergen_id = models.AutoField(primary_key=True)
    allergen_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.allergen_name

class FoodItemAllergen(models.Model):
    food_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    allergen_id = models.ForeignKey(Allergen, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.food_id} - {self.allergen_id}"