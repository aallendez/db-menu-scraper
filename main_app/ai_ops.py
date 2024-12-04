import os
import pdfplumber
import json
from openai import OpenAI
from .models import Menu, FoodItem, DishType, Ingredient, Allergen, FoodItemIngredient, FoodItemAllergen, DishTypeFoodItem, MenuFoodItem, RestaurantMenu, ProcessLog
import re

# Initialize OpenAI client with the loaded API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


# AI PDF Processing
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def format_menu_data(menu_text):
    """Format menu text into structured data using OpenAI API."""
    
    
    print("Formatting menu data...")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in formatting restaurant menu text into structured data."
            },
            {
                "role": "user",
                "content": f"Convert the following menu into a structured dictionary with the following structure: "
                           f"[{{'Food': 'dish name', "
                           f"'Price': 'float in euros', "
                           f"'Dish_Type': 'Appetizers, Mains, Desserts, Sides, Drinks', "
                           f"'Ingredients': ['ingredient1', 'ingredient2', ...], "
                           f"'Allergens': ['allergen1', 'allergen2', ...]}}].\n\n"
                           f"Menu:\n{menu_text}\n\n"
                           f"Instructions:\n"
                           f"- Allergens must be strictly chosen from the following list: Dairy, Gluten, Vegan, Vegetarian, Eggs, Shellfish, Tree Nuts, Peanuts, Fish, Soy.\n"
                           f"- If the menu specifies allergens, use them as provided.\n"
                           f"- If allergens are not mentioned, infer them based on the dish description where possible"
                           f"(e.g., cheese implies Dairy, pasta implies Gluten, seafood implies Fish, vegetarian dishes contain no meat or fish).\n"
                           f"- Ingredients should be inferred based on the dish description (e.g., 'Caesar Salad' implies lettuce, croutons, parmesan, Caesar dressing). Make the ingredients lower case\n"
                           f"- If no ingredients can be inferred or identified, use an empty array [] for ingredients.\n"
                           f"- Provide only the dictionary structure as output. Do not include explanations or extra text."
                           f"- Your answer will be parsed as JSON, so make sure it's valid JSON."
            }
        ]
    )
    

    try:
        print("Parsing AI response as JSON...")
        content = response.choices[0].message.content
        content = re.sub(r"(?<!\w)'(?!\w)", '"', content)  # Replace single quotes with double quotes for keys
        content = content.replace("'", '"')  # Replace all single quotes with double quotes
        
        print("Content: ", content)
        structured_data = json.loads(content)
        
        if not isinstance(structured_data, list):
            raise ValueError("AI response is not a list of dictionaries.")
        return structured_data
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        raise ValueError(f"Failed to parse AI response: {str(e)}")



def save_menu_to_db(pdf_path, restaurant_id):
    """
    Save a menu and its items to the database.
    """
    # Step 1: Create a new Menu instance
    print("Creating menu...")
    menu_text = extract_text_from_pdf(pdf_path)
    menu = Menu(menu_text=menu_text)
    menu.save()

    # Step 2: Link the menu to the restaurant
    print("Linking menu to restaurant...")
    RestaurantMenu.objects.create(restaurant_id_id=restaurant_id, menu_version_id=menu)

    # Step 3: Parse the structured menu data
    print("Parsing structured menu data...")
    try:
        structured_data = format_menu_data(menu_text)
    except ValueError as e:
        raise ValueError(f"Error processing menu data: {str(e)}")
    
    # Step 4: Save related data to the database
    print("Saving related data to the database...")
    for item in structured_data:
        try:
            print("Extracting fields...")
            # Extract fields
            food_name = item['Food']
            price = item['Price']
            dish_type_name = item['Dish_Type']
            allergens = item.get('Allergens', [])
            ingredients = item.get('Ingredients', [])

            print("Handling empty price...")
            # Handle empty price
            if price == '':
                price = 0.0  # Set a default value or handle as needed
            else:
                price = float(price)  # Convert to float if not empty
                
            print("Creating or getting FoodItem...")
            
            # Create or get FoodItem
            food_item, created = FoodItem.objects.get_or_create(
                food_name=food_name,
                defaults={
                    'food_description': "",
                    'food_price': price
                }
            )

            # Create or get DishType
            dish_type, _ = DishType.objects.get_or_create(dish_type=dish_type_name)

            # Link DishType and FoodItem
            DishTypeFoodItem.objects.get_or_create(
                food_id=food_item,
                dish_type_id=dish_type
            )

            # Create or get Ingredients and link them to the FoodItem
            for ingredient_name in ingredients:
                ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient_name)
                FoodItemIngredient.objects.get_or_create(food_id=food_item, ingredient_id=ingredient)

            # Create or get Allergens and link them to the FoodItem
            for allergen_name in allergens:
                allergen, _ = Allergen.objects.get_or_create(allergen_name=allergen_name)
                FoodItemAllergen.objects.get_or_create(food_id=food_item, allergen_id=allergen)

            # Link FoodItem to the Menu
            MenuFoodItem.objects.create(menu_version_id=menu, food_id=food_item)

        except KeyError as e:
            raise ValueError(f"Missing field in structured data: {str(e)}")

    return menu



# AI Query Processing

def filter_query(query):
    # Mock filter logic
    
    # Get ai educated guess 
    suggested_query = ai_suggested_query(query)
    
    
    
    
    ...
    
def ai_suggested_query(query):
    # Get ai educated guess 
    response = client.chat.completions.create(  
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in restaurant menus and customer queries. Your task is to suggest a more specific query based on a general query."
            },
            {
                "role": "user",
                "content": f"Suggest a more specific query based on the following general query: {query}"
            }
        ]
    )
    # Parse the response
    output = json.loads(response.choices[0].message.content)
    return output
    