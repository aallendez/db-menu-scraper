from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Menu
from .serializers import RestaurantSerializer, MenuSerializer
from .ai_operations import process_pdf, filter_query

class RestaurantView(APIView):
    def get(self, request):
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuUploadView(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        restaurant_id = request.data.get('restaurant_id')
        try:
            processed_data = process_pdf(file)
            menu = Menu.objects.create(
                restaurant_id=restaurant_id,
                pdf_file=file,
                processed_data=processed_data,
            )
            return Response({"id": menu.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BrowserPromptView(APIView):
    def get(self, request):
        criteria = request.query_params.get("criteria")
        results = filter_query(criteria)
        return Response(results)

# Create your views here.
def upload_menu(request):
    
    if request.method == 'POST':
        request_data = request.POST
        
        menu_text = request_data.get('menu_text')
        restaurant_name = request_data.get('restaurant_name')
        restaurant_id = request_data.get('restaurant_id')
        
        menu_list = format_menu_data(menu_text)
        
        # Insert processed menu into database
        data = {
            'Food': menu_list['Food'],
            'Price': menu_list['Price'],
            'Dish_Type': menu_list['Dish_Type'],
            'Allergens': menu_list['Allergens'],
            'Ingredients': menu_list['Ingredients']
        }
        
        return JsonResponse({'message': 'Menu uploaded successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
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