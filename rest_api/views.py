from rest_framework.response import Response
from rest_framework.decorators import api_view
from main_app.models import Restaurant
from main_app.views import GetAllRestaurants, CreateRestaurant, HandleUserQuery, MenuUploadView

# Menu Uploader Requests

@api_view(['POST'])
def insert_restaurant(request):
    try:
        return CreateRestaurant.as_view()(request)
    except Exception as e:
        return Response({"message": str(e)}, status=500)

@api_view(['POST'])
def upload_menu(request):
    try:
        return MenuUploadView.as_view()(request)
    except Exception as e:
        return Response({"message": str(e)}, status=500)


@api_view(['GET'])
def get_all_restaurants(request):
    try:
        return GetAllRestaurants.as_view()(request)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def handle_user_query(request):
    try:
        return HandleUserQuery.as_view()(request)
    except Exception as e:
        return Response({"error": str(e)}, status=500)