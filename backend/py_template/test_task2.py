import requests

url = "http://127.0.0.1:8080/entry"
headers = {"Content-Type": "application/json"}

# Test Adding a Recipe
recipe_data = {
    "type": "recipe",
    "name": "Sussy Salad",
    "requiredItems": [
        {"name": "Mayonaise", "quantity": 1},
        {"name": "Lettuce", "quantity": 3}
    ]
}

response = requests.post(url, json=recipe_data, headers=headers)
print("Recipe Test Response:", response.status_code, response.json() if response.content else "No content")

# Test Adding an Ingredient
ingredient_data = {
    "type": "ingredient",
    "name": "Egg",
    "cookTime": 6
}

response = requests.post(url, json=ingredient_data, headers=headers)
print("Ingredient Test Response:", response.status_code, response.json() if response.content else "No content")
