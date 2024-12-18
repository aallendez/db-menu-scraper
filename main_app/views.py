from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Menu, FoodItem, RestaurantCuisine, Cuisine, RestaurantMenu, ProcessLog, FoodItemAllergen, SummarizedAvgPrices
from .serializers import RestaurantSerializer, MenuSerializer, FoodItemSerializer, SummarizedAvgPricesSerializer
from .ai_ops import format_menu_data, process_restriction_query, extract_text_from_pdf, save_menu_to_db
from rest_framework.permissions import AllowAny
import datetime

# Upload Menu
# Not inserting success process logs here because they will be automated by the database trigger
class MenuUploadView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        if request.method == "OPTIONS":
            return Response(status=status.HTTP_200_OK)
            
        file = request.FILES.get('file')
        restaurant_id = request.data.get('restaurant_id')

        try:
            menu = save_menu_to_db(file, restaurant_id)
            
            return Response({"menu_id": menu.menu_version_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            ProcessLog.objects.create(
                process_name="format_and_save_menu_data",
                process_date=datetime.datetime.now(),
                process_message=f"Error processing menu data for restaurant of ID {restaurant_id}: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Get all restaurants
# Not inserting process logs here because they will be automated by the database trigger
class GetAllRestaurants(APIView):
    def get_queryset(self):
        return Restaurant.objects.all()

    def get(self, request):
        try:
            restaurants = self.get_queryset()
            serializer = RestaurantSerializer(restaurants, many=True)
            
            return Response({"restaurants": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            ProcessLog.objects.create(
                process_name="get_all_restaurants",
                process_date=datetime.datetime.now(),
                process_message=f"Error retrieving all restaurants from DB: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Create restaurant
class CreateRestaurant(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.method == "OPTIONS":
            return Response(status=status.HTTP_200_OK)
            
        try:
            # Check if restaurant already exists
            name = request.data.get('name')
            if Restaurant.objects.filter(name=name).exists():
                return Response(
                    {"error": "Restaurant with this name already exists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                restaurant = serializer.save()
                
                # New code to handle cuisine
                cuisine_id = request.data.get('cuisine_id')
                if cuisine_id:
                    restaurant_cuisine = RestaurantCuisine.objects.create(
                        restaurant_id=restaurant,
                        cuisine_id=Cuisine.objects.get(cuisine_id=cuisine_id)
                    )
                
                
                return Response({"restaurant": serializer.data}, status=status.HTTP_201_CREATED)
            
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            error_message = str(e) if e else "Unknown error"
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
# Get all menu versions from restaurant
class GetAllMenuVersionsFromRestaurant(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        if request.method == "OPTIONS":
            return Response(status=status.HTTP_200_OK)
        
        try:
            restaurant_id = request.data.get('restaurant_id')
            menu_versions = Menu.objects.filter(
                restaurantmenu__restaurant_id__id=restaurant_id
            ).order_by('-creation_date')
            serializer = MenuSerializer(menu_versions, many=True)
            
            ProcessLog.objects.create(
                process_name="get_all_menu_versions_from_restaurant",
                process_date=datetime.datetime.now(),
                process_message=f"All menu versions correctly retrieved from DB for restaurant of ID {restaurant_id}",
                process_output=serializer.data
            )
            return Response({"menu_versions": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            ProcessLog.objects.create(
                process_name="get_all_menu_versions_from_restaurant",
                process_date=datetime.datetime.now(),
                process_message=f"Error retrieving all menu versions from DB for restaurant of ID {restaurant_id}: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
  
# Get menu version
class GetMenuVersion(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        if request.method == "OPTIONS":
            return Response(status=status.HTTP_200_OK)
        
        try:
            menu_version_id = request.data.get('menu_version_id')
            menu_version = Menu.objects.get(menu_version_id=menu_version_id)
            
            # Get all food items associated with this menu
            food_items = FoodItem.objects.filter(
                menufooditem__menu_version_id=menu_version
            )
            food_serializer = FoodItemSerializer(food_items, many=True)
            menu_serializer = MenuSerializer(menu_version)
            
            ProcessLog.objects.create(
                process_name="get_menu_version",
                process_date=datetime.datetime.now(),
                process_message=f"Menu version correctly retrieved from DB for ID {menu_version_id}",
                process_output=menu_serializer.data
            )
            return Response({
                "menu_version": menu_serializer.data,
                "food_items": food_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            ProcessLog.objects.create(
                process_name="get_menu_version",
                process_date=datetime.datetime.now(),
                process_message=f"Error retrieving menu version from DB for ID {menu_version_id}: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Handle user query for allergens
class HandleUserQuery(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Get the allergen restrictions from the request data
            restrictions = request.data.get('query')
            
            restrictions = process_restriction_query(restrictions)
            
            if not restrictions:
                raise ValueError("Allergen restrictions must be provided.")
            
            # Query to find all food items that DO contain any of the given allergens
            restricted_food_ids = FoodItemAllergen.objects.filter(
                allergen_id__allergen_name__in=restrictions
            ).values_list('food_id__food_id', flat=True)  # Use the correct foreign key lookup
            
            # Get all food items not in the restricted_food_ids
            food_items = FoodItem.objects.exclude(food_id__in=restricted_food_ids).prefetch_related(
                'fooditemingredient_set__ingredient_id',  # Prefetch ingredients
                'menufooditem_set__menu_version_id__restaurantmenu_set__restaurant_id'  # Prefetch restaurant info
            )
            
            # Restructure results to group by restaurant
            restaurant_foods = {}
            
            for food in food_items:
                food_data = {
                    "food_name": food.food_name,
                    "food_description": food.food_description,
                    "food_price": food.food_price,
                    "ingredients": [
                        ingredient.ingredient_id.ingredient_name
                        for ingredient in food.fooditemingredient_set.all()
                    ]
                }
                
                # Group by restaurant
                for menu in food.menufooditem_set.all():
                    for restaurant in menu.menu_version_id.restaurantmenu_set.all():
                        restaurant_key = restaurant.restaurant_id.name
                        if restaurant_key not in restaurant_foods:
                            restaurant_foods[restaurant_key] = {
                                "name": restaurant.restaurant_id.name,
                                "location": restaurant.restaurant_id.location,
                                "url": restaurant.restaurant_id.url,
                                "foods": []
                            }
                        restaurant_foods[restaurant_key]["foods"].append(food_data)
            
            results = list(restaurant_foods.values())
            
            # Log the process
            ProcessLog.objects.create(
                process_name="filter_foods_by_dietary_restrictions",
                process_date=datetime.datetime.now(),
                process_message=f"Foods successfully filtered by dietary restrictions: {restrictions}",
                process_output=str(results)
            )
            
            return Response({"results": results}, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Log the error
            ProcessLog.objects.create(
                process_name="filter_foods_by_dietary_restrictions",
                process_date=datetime.datetime.now(),
                process_message=f"Error filtering foods by dietary restrictions: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# Filter foods by dietary restrictions
class FilterFoodsByDietaryRestrictions(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            # Get the allergen restrictions from the request data
            restrictions = request.data.get('restrictions', [])
            
            if not restrictions:
                raise ValueError("Allergen restrictions must be provided.")
            
            # Query to find all food items that DO contain any of the given allergens
            restricted_food_ids = FoodItemAllergen.objects.filter(
                allergen_id__allergen_name__in=restrictions
            ).values_list('food_id__food_id', flat=True)  # Use the correct foreign key lookup
            
            # Get all food items not in the restricted_food_ids
            food_items = FoodItem.objects.exclude(food_id__in=restricted_food_ids).prefetch_related(
                'fooditemingredient_set__ingredient_id',  # Prefetch ingredients
                'menufooditem_set__menu_version_id__restaurantmenu_set__restaurant_id'  # Prefetch restaurant info
            )
            
            # Structure the result with the required details
            results = []
            for food in food_items:
                ingredients = [
                    ingredient.ingredient_id.ingredient_name
                    for ingredient in food.fooditemingredient_set.all()
                ]
                restaurants = [
                    {
                        "name": restaurant.restaurant_id.name,
                        "location": restaurant.restaurant_id.location,
                        "url": restaurant.restaurant_id.url
                    }
                    for menu in food.menufooditem_set.all()
                    for restaurant in menu.menu_version_id.restaurantmenu_set.all()
                ]
                results.append({
                    "food_name": food.food_name,
                    "food_description": food.food_description,
                    "food_price": food.food_price,
                    "ingredients": ingredients,
                    "restaurants": restaurants
                })
            
            # Log the process
            ProcessLog.objects.create(
                process_name="filter_foods_by_dietary_restrictions",
                process_date=datetime.datetime.now(),
                process_message=f"Foods successfully filtered by dietary restrictions: {restrictions}",
                process_output=str(results)
            )
            
            return Response({"results": results}, status=status.HTTP_200_OK)
        
        except Exception as e:
            # Log the error
            ProcessLog.objects.create(
                process_name="filter_foods_by_dietary_restrictions",
                process_date=datetime.datetime.now(),
                process_message=f"Error filtering foods by dietary restrictions: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Access to materialized view
class GetSummarizedAvgPrices(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            restaurant_id = request.data.get('restaurant_id')
            if not restaurant_id:
                raise ValueError("Restaurant ID must be provided")
            
            summarized_data = SummarizedAvgPrices.objects.get(restaurant_id=restaurant_id)
            serializer = SummarizedAvgPricesSerializer(summarized_data)
            
            ProcessLog.objects.create(
                process_name="get_summarized_avg_prices",
                process_date=datetime.datetime.now(),
                process_message=f"Successfully retrieved price summary for restaurant ID {restaurant_id}",
                process_output=serializer.data
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except SummarizedAvgPrices.DoesNotExist:
            return Response(
                {"error": f"No data found for restaurant ID {restaurant_id}"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            ProcessLog.objects.create(
                process_name="get_summarized_avg_prices",
                process_date=datetime.datetime.now(),
                process_message=f"Error retrieving price summary: {str(e)}",
                process_output=str(e)
            )
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)