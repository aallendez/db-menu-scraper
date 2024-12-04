# Menu Relational Database Management System

## Overview

A menu relational database management system designed to enable users to upload menus and perform queries, allowing text-based search results to be viewed. The system uses Django REST API and OpenAI's LLM to extract data from menu PDFs, which is then parsed into JSON format. This JSON data is subsequently processed by Django's admin API and stored in a relational MySQL database structured in third normal form, using main and transitive tables. The database is hosted on an AWS server located in Michigan, USA, as part of a one-year free trial.

## Key Features

1. **AI-Powered PDF Processing**: Extract text and format it into structured data.
2. **Database Integration**: Save processed data to a database.
3. **Indexing for Performance**: Optimized queries using database indexes.

## Technologies Used

- **Django REST API**: Web framework to create the web application and handle user interaction.
- **Python**: Programming language Django is built on.
- **React**: Front-end integration.
- **OpenAI API**: AI model to process text extracted from PDFs.
- **MySQL**: Relational database system.
- **AWS**: For database hosting.

## Folder Structure

- **main_app**: Back-end logic.
- **MenuScraper**: Root folder.
- **Rest_api**: API folder.

## Setup Instructions

1. Navigate to the `database_project` folder.
2. Run the following command:

   ```bash
   python3 manage.py runserver
   ```

3. Test the API endpoints

## API Documentation

There are two ways to interact with the API:

1. Using the Django Admin interface
2. Using the API endpoints

Below, you can find the API endpoints, their descriptions, and the expected input and output for each endpoint.

1. **Upload Menu**
    - **Endpoint**: `/upload_menu/`
    - **Description**: Handles uploading of menus from restaurants.
    - **Method**: POST
    - **Input**: PDF file as well as restaurant ID.
        ````
        curl -k --tlsv1.2 -X POST http://127.0.0.1:8000/api/upload-menu/ \
        -H "Content-Type: multipart/form-data" \
        -F "file=@menu.pdf" \
        -F "restaurant_id=4"
        ````
    - **Output**: Menu version ID.

2. **Get all restaurants**
    - **Endpoint**: `/get_all_restaurants/`
    - **Description**: Retrieves all restaurants from the database.
    - **Method**: GET
    - **Input**: None
    - **Output**: See below.
        ```
        {
            "restaurants": [
                {
                    "id": 1,
                    "name": "Pizza Place",
                    "location": "Downtown",
                    "url": "https://pizzaplace.com"
                }
            ]
        }```

3. **Create restaurant**
    - **Endpoint**: `/create_restaurant/`
    - **Description**: Creates a new restaurant.
    - **Method**: POST
    - **Input**: 
        ```
        {
            "name": "Burger Bistro",
            "cuisine_id": 2,
            "location": "City Center",
            "schedule": "Mon-Fri 10:00-22:00, Sat-Sun 10:00-23:00",
            "url": "https://burgerbistro.com"
        }   
        ```
    - **Output**: Created restaurant message along with restaurant ID.

4. **Get all menu versions from restaurant**
    - **Endpoint**: `/get-menus-restaurant/`
    - **Description**: Retrieves all menu versions from a restaurant.
    - **Method**: GET
    - **Input**: 
        ```
        {
            "restaurant_id": 1
        }
        ```
    - **Output**: 
        ````
        {
            "menu_versions": [
                {
                    "menu_version_id": 101,
                    "items": [...]
                }
            ]
        }
        ````

5. **Get menu version**
    - **Endpoint**: `/get-menu-version/`
    - **Description**: Retrieves a specific menu version from a restaurant.
    - **Method**: POST
    - **Input**: 
        ```
        {
            "menu_version_id": 101
        }
        ```
    - **Output**: 
        ````
        {
            "menu_version": {
                "menu_version_id": 9,
                "creation_date": "2024-12-04T18:13:44.098280Z",
                "menu_text": "....."
            }
        }
        ````

6. **Filter foods by dietary restrictions**
    - **Endpoint**: `/filter-foods/`
    - **Description**: Filters foods by dietary restrictions.
    - **Method**: POST
    - **Input**: 
        ```
        {
            "restrictions": ["Tree Nut", "Shellfish"]
        }
        ```
    - **Output**: 
        {
            "results": [
                {
                    "food_name": "Passion Jazz Dry Italian SW3",
                    "food_description": "",
                    "food_price": 0.0,
                    "ingredients": [
                        "vodka",
                        "passion fruit",
                        ...
                    ],
                    "restaurants": [
                        {
                            "name": "London Stakehouse",
                            "location": "Ciudad Deportiva Real Madrid",
                            "url": "https://stakehouse.com"
                        }
                    ]
                },...
            ]
        }

7. **Get summarized avg prices**
    - **Endpoint**: `/get-summarized-avg-prices/`
    - **Description**: Gets summarized report of the prices of the menu items in the restaurant (including avg, min and max price). This is a materialized view that is updated every 1 hour with the latest menu versions.
    - **Method**: POST
    - **Input**: 
        ```
        {
            "restaurant_id": 9
        }
        ```
    - **Output**: See below.