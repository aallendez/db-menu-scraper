from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def upload_menu(request):
    
    if request.method == 'POST':
        request_data = request.POST
        
        
        
        
        
        
        return JsonResponse({'message': 'Menu uploaded successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)