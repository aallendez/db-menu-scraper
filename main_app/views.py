from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Menu, FoodItem
from .serializers import RestaurantSerializer, MenuSerializer, FoodItemSerializer
from .ai_ops import format_menu_data, filter_query, extract_text_from_pdf, save_menu_to_db

# Upload Menu
class MenuUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        restaurant_id = request.data.get('restaurant_id')

        try:
            # Step 1: Extract menu text from PDF
            menu_text = extract_text_from_pdf(file)

            # Step 2: Save menu to the database
            menu = save_menu_to_db(menu_text, restaurant_id)

            return Response({"menu_id": menu.menu_version_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllRestaurants(APIView):
    def get(self, request):
        try:
            restaurants = Restaurant.objects.all()
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response({"restaurants": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CreateRestaurant(APIView):
    def post(self, request):
        try:
            serializer = RestaurantSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"restaurant": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HandleUserQuery(APIView):
    def post(self, request):
        try:
            query = request.data.get('query')
            results = filter_query(query)
            return Response({"results": results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





# Restaurant Queries
def get_all_restaurants():
    return Restaurant.objects.all()

def get_restaurant_by_id(request, restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    return JsonResponse(restaurant)

def get_restaurant_by_name(restaurant_name):
    return Restaurant.objects.filter(restaurant_name__icontains=restaurant_name)

def get_restaurant_by_cuisine(cuisine_name):
    return Restaurant.objects.filter(cuisine_name__icontains=cuisine_name)

def get_restaurant_by_location(location):
    return Restaurant.objects.filter(location__icontains=location)

def get_restaurant_average_price(restaurant_id):
    menus = Menu.objects.filter(restaurant_id=restaurant_id)
    total_price = 0
    for menu in menus:
        for food_item in menu.food_items.all():
            total_price += food_item.food_price
    return total_price / menus.count()

# Menu Queries
def get_all_menus():
    return Menu.objects.all()

def get_menu_by_id(menu_id):
    return Menu.objects.get(menu_id=menu_id)

def get_latest_menu_by_restaurant_id(restaurant_id):
    return Menu.objects.filter(restaurant_id=restaurant_id).order_by('-menu_version_id').first()