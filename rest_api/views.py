from rest_framework.response import Response
from rest_framework.decorators import api_view
from menu_uploader.models import Restaurant
from query_app.views import get_restaurant_by_id

# Menu Uploader Requests

@api_view(['POST'])
def insert_restaurant(request):
    print(request.data)
    
    name = request.data['name']
    cuisine = request.data['cuisine']
    location = request.data['location']
    
    try:
        restaurant = Restaurant(restaurant_name=name, cuisine_name=cuisine, location=location)
        restaurant.save()
    except Exception as e:
        return Response({"message": str(e)}, status=500)
    
    return Response({"message": "Restaurant inserted successfully"}, status=200)



# Query App Requests

@api_view(['GET'])
def get_restaurant_by_id(request, restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    return Response(restaurant, status=200)

