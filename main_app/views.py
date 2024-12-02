from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Menu, FoodItem, RestaurantCuisine, Cuisine
from .serializers import RestaurantSerializer, MenuSerializer, FoodItemSerializer
from .ai_ops import format_menu_data, filter_query, extract_text_from_pdf, save_menu_to_db
from rest_framework.permissions import AllowAny

# Upload Menu
class MenuUploadView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
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
        try:
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


class HandleUserQuery(APIView):
    def post(self, request):
        try:
            query = request.data.get('query')
            results = filter_query(query)
            
            return Response({"results": results}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





