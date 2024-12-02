import os
import pdfplumber
from openai import OpenAI

# Initialize OpenAI client with the loaded API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


# AI PDF Processing
def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    print(text)
    return text

def format_menu_data(pdf_path):
    """Format menu text into structured data using OpenAI API."""
    menu_text = extract_text_from_pdf(pdf_path)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """
                        You are an assistant made to format menu text into structured data. You will be given a string of text that contains a restaurant menu.
                        Your job is to format the text into a list of lists, where each inner list contains the fields of a menu item.
                """
            },
            {
                "role": "user",
                "content":  f"""
                                Format the following menu into structured data:\n\n{menu_text}.
                                Return the response as a list of dicts, where each element is a dict of the fields of a menu item.
                                1. Return the food name as the first element of the dict.
                                2. Return the price as the second element of the dict.
                                3. Return the dish type as the third element of the dict. Choose from: Appetizers, Mains, Desserts, Sides, Drinks
                                4. Return the allergens as the fourth element of the dict, set them as a list of allergens. Choose from: Dairy, Gluten, Vegan, Vegetarian, Eggs, Shellfish, Tree Nuts, Peanuts, Fish, Soy
                                5. Return the ingredients as the fifth element of the dict, set them as a list of ingredients.
                                A a list in the full response would look like this: 
                                [
                                    {{
                                        'Food': 'food name',
                                        'Price': 'price',
                                        'Dish_Type': 'dish type',
                                        'Allergens': ['allergen1', 'allergen2', 'allergen3'],
                                        'Ingredients': ['ingredient1', 'ingredient2', 'ingredient3']
                                    }},
                                    ...
                                ]
                            """
            }
        ]
    )
    
    

    # Parse the response into a list of menu items
    structured_data = response.choices[0].message.content
    menu_items = []
    
    for line in structured_data.strip().splitlines():
        # Convert each line into a list of fields
        fields = [field.strip() for field in line.split(",")]
        menu_items.append(fields)
    
    return menu_items


# AI Query Processing

def filter_query(criteria):
    # Mock filter logic
    return [{"name": "Italian Bistro", "location": "Main St"}]
