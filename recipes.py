import requests
import json

def get_recipes(
    api_key, app_id, query, image_type='THUMBNAIL', 
    meal_type=None, cuisine_type=None, calorie_range=None, health_labels=None, excluded_ingredients=None
):
    url = f"https://api.edamam.com/search?q={query}&app_id={app_id}&app_key={api_key}" 

    opt_args = [
        meal_type,
        cuisine_type,
        calorie_range,
        health_labels,
        excluded_ingredients
    ]

    opt_query_params = [
        'mealType',
        'cuisineType',
        'calories',
        'health',
        'excluded'
    ]

    for (arg, param) in zip(opt_args, opt_query_params):
        if arg:
            url += '&' + param + '=' + arg

    response = requests.get(url)
    content = json.loads(response.content)
    
    #recipe_names = [recipe['recipe']['label'] for recipe in content['hits']]
    recipes = []
    for recipe in content['hits']:
        x = recipe['recipe']

        y = {
            "name": x['label'],
            "thumbnail": x['image'],
            "servings": x['yield'],
            "diets_label": x['dietLabels'],
            "health_labels": x['healthLabels'],
            "cautions": x['cautions'],
            "calories": x['calories'],
            "meal_type": x['mealType'],
            "dish_type": x['dishType']
        }

        ingredients = []
        for ingr in x['ingredients']:
            ingredients.append({
                "name": ingr['text'], 
                "grams": ingr['weight'],  # WEIGHT IS IN GRAMS
                "image": ingr['image']
            })
        
        y['ingredients'] = ingredients

        recipes.append(y)

    return json.dumps(recipes, indent=4)