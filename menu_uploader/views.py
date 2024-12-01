from django.shortcuts import render
from django.http import JsonResponse
from pdf_processing import format_menu_to_csv
from menu_uploader.models import Restaurant, Menu, RestaurantMenu, upload_menu


# Create your views here.
def upload_menu(request):
    
    if request.method == 'POST':
        request_data = request.POST
        
        menu_text = request_data.get('menu_text')
        restaurant_name = request_data.get('restaurant_name')
        restaurant_id = request_data.get('restaurant_id')
        
        menu_list = format_menu_to_csv(menu_text)
        
        # Insert processed menu into database
        data = {
            'Food': menu_list[0],
            'Price': menu_list[1],
            'Dish_Type': menu_list[2],
            'Allergens': menu_list[3],
            'Restaurant_Name': restaurant_name
        }
        
    
        
        
        
        
        
        return JsonResponse({'message': 'Menu uploaded successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    
    
    
    

