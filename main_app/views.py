from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Menu, FoodItem, RestaurantCuisine, Cuisine, RestaurantMenu
from .serializers import RestaurantSerializer, MenuSerializer, FoodItemSerializer
from .ai_ops import format_menu_data, filter_query, extract_text_from_pdf, save_menu_to_db
from rest_framework.permissions import AllowAny

# Upload Menu
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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetAllRestaurants(APIView):
    def get_queryset(self):
        return Restaurant.objects.all()

    def get(self, request):
        try:
            restaurants = self.get_queryset()
            serializer = RestaurantSerializer(restaurants, many=True)
            return Response({"restaurants": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class GetAllMenuVersionsFromRestaurant(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            restaurant_id = request.data.get('restaurant_id')
            menu_versions = Menu.objects.filter(
                restaurantmenu__restaurant_id__id=restaurant_id
            ).order_by('-creation_date')
            serializer = MenuSerializer(menu_versions, many=True)
            
            return Response({"menu_versions": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class GetMenuVersion(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        if request.method == "OPTIONS":
            return Response(status=status.HTTP_200_OK)
        
        try:
            menu_version_id = request.data.get('menu_version_id')
            menu_version = Menu.objects.get(menu_version_id=menu_version_id)
            serializer = MenuSerializer(menu_version)
            return Response({"menu_version": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        


class HandleUserQuery(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            query = request.data.get('query')
            results = filter_query(query)
            
            return Response({"results": results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





