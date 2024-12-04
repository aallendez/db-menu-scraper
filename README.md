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
        }
        ```

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
            "menu_version_id": 19
        }
        ```
    - **Output**: 
        ````
        {
            "menu_version": {
                "menu_version_id": 19,
                "creation_date": "2024-12-04T21:06:00.205035Z",
                "menu_text": "NUESTROS CLÁSICOS\nGuacamole clásico con pico de gallo y totopos. 11€\nColiflor a las brasas marinada con aceite de oliva, limón y flor de sal. 12€\nTostada de atún de la Almadraba, ponzu, mayo-chipotle, aguacate\ny puerro frito. 25€\nChicharrón de Angus con guacamole y salsa chiltepín-limón. 20€\nGaonera de solomillo de vaca Rubia gallega madurada sobre\ncostra de queso mozzarella, rúcula sobre tortilla de maíz amarillo. 20€\nGobernador con camarón rojo, costra de queso oaxaqueño,\npico de gallo y alioli de chipotle ahumado. 23€\nCostilla de Black Angus flambeada con Tequila Don Julio 70. 24€\nLubina salvaje a la Talla de 1kg, con guacamole, kimchi y frijoles.\n(Recomendado para 2/3pax) 70€\nPARA COMPARTIR O NO, A LA BRASA\nPuerro y cebolleta a la brasa con demiglace de chile habanero. 9€\nChoriqueso parrillero de ropa vieja. 16€\nHuevos rotos con huitlacoche, con lascas de jamón ibérico puro\nde bellota, crema de guacamole y frijoles charros. 22€\nArroz a la Tumbada de mariscos con frijoles . 24€\nCRUDOS Y FRESCOS\nOstra Guillardeau Nº2 con aguachile verde y salsa de habanero\nquemada. 5,5€ ud\nCeviche de lubina salvaje, tomate de árbol, maracuyá, coco\ny espuma de elote. 25€\nEnsaladilla rusa, tartar de atún, mahonesa de chile meco, piparras\nahumadas. 25€\nDE LA HUERTA\nEnsalada lechuga, aguacate y piñones con vinagreta. 14€\nEnsalada de Jitomates, melón, pepino y vainilla. 14€\nCogollos de Tudela a la brasa a modo de ensalada Cesar. 14€NUESTROS TACOS DE AUTOR. 2 unidades\nPescadilla a la Veracruzana (Quesadilla de Bonito), aguachile\nrojo y zanahoria escabechada. 18€\nTaco Baja de langostinos, lombarda, tzatziki enchipotlado. 20€\nCochinillo de Sepúlveda, ribeteado con pibil, guacamole y Xnipek. 20€\nJaiba con txangurro, piña asada y ensalada de hierbas. 23€\nDEL MAR A LA BRASA\nPulpo a la brasa con papas al ajillo y Xnipek. 28€\nVentresca de bonito zarandeada, mole de novia y spaguetti\nde calabacín. 32€\nLangostinos a la brasa con piperrada de chiles toreados. 35€\nNUESTRA SELECCIÓN DE CARNE\nSolomillo de vaca madurada, 250g, Ayshire Sashi, Finlandia. 30€\nEntraña, 300g. Black Angus con chimichurri MX. 32€\nRibeye Steak, Lomo alto sin hueso 500g Ayshire Sashi, Finlandia. 58€\nTomahawk Steak 1kg, Ayshire Sashi, Finlandia.\n(Recomendado para 2/3 pax) 95€\nGUARNICIONES\nPatatas gratinadas con queso oaxaqueño. 9€\nCamote asado con miel chile guajillo y con setas tatemadas. 9€\nPimientos rojos al carbón con pimientos del Padrón toreados. 12€\n********\nPOSTRES\nJericalla, Natilla de coco, jazmín y sorbete de maracuyá. 9€\nTarta inversa de queso, crema de maíz y helado de vainilla\nde Veracruz. 10€\nPiña asada con hierba luisa, tequila blanco Don Julio y helado de\nleche merengada. 10€\nTarta de chocolate de metate con chantilly. 12€\n10% iva incluido"
            },
            "food_items": [
                {
                    "food_id": 161,
                    "food_name": "Guacamole clásico con pico de gallo y totopos",
                    "food_description": "",
                    "food_price": "11.00"
                }, ...
            ]
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
        ```
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
        ```

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
    - **Output**: 
        ````
        {
            "restaurant_id": 9,
            "restaurant_name": "Bromfields",
            "avg_food_price": "12.3300",
            "max_food_price": "24.95",
            "min_food_price": "4.95"
        }
        ````
