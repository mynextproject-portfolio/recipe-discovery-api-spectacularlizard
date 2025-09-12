from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory recipe storage with sample data
recipes_db = {
    1: {
        "id": 1,
        "title": "Classic Spaghetti Carbonara",
        "description": "A traditional Italian pasta dish with eggs, cheese, and pancetta",
        "ingredients": [
            "400g spaghetti",
            "200g pancetta or guanciale",
            "4 large eggs",
            "100g Pecorino Romano cheese",
            "Black pepper",
            "Salt"
        ],
        "instructions": [
            "Cook spaghetti in salted boiling water until al dente",
            "Fry pancetta until crispy",
            "Whisk eggs with grated cheese and black pepper",
            "Combine hot pasta with pancetta",
            "Remove from heat and quickly mix in egg mixture",
            "Serve immediately with extra cheese"
        ],
        "prep_time": 15,
        "cook_time": 15,
        "servings": 4
    },
    2: {
        "id": 2,
        "title": "Chicken Tikka Masala",
        "description": "Creamy and flavorful Indian curry with tender chicken pieces",
        "ingredients": [
            "1kg chicken breast, cubed",
            "2 cups basmati rice",
            "400ml coconut milk",
            "400g canned tomatoes",
            "2 tbsp tikka masala paste",
            "1 onion, diced",
            "3 garlic cloves",
            "1 tsp ginger paste",
            "Fresh cilantro"
        ],
        "instructions": [
            "Marinate chicken in yogurt and spices for 30 minutes",
            "Cook rice according to package instructions",
            "Grill chicken pieces until cooked through",
            "Sauté onion, garlic, and ginger",
            "Add tomatoes and tikka masala paste",
            "Simmer with coconut milk for 10 minutes",
            "Add grilled chicken and cook for 5 minutes",
            "Garnish with cilantro and serve with rice"
        ],
        "prep_time": 45,
        "cook_time": 30,
        "servings": 6
    },
    3: {
        "id": 3,
        "title": "Chocolate Chip Cookies",
        "description": "Soft and chewy homemade chocolate chip cookies",
        "ingredients": [
            "2¼ cups all-purpose flour",
            "1 tsp baking soda",
            "1 tsp salt",
            "1 cup butter, softened",
            "¾ cup granulated sugar",
            "¾ cup brown sugar",
            "2 large eggs",
            "2 tsp vanilla extract",
            "2 cups chocolate chips"
        ],
        "instructions": [
            "Preheat oven to 375°F (190°C)",
            "Mix flour, baking soda, and salt in a bowl",
            "Cream butter and sugars until light and fluffy",
            "Beat in eggs and vanilla",
            "Gradually blend in flour mixture",
            "Stir in chocolate chips",
            "Drop spoonfuls onto ungreased baking sheets",
            "Bake for 9-11 minutes until golden brown"
        ],
        "prep_time": 20,
        "cook_time": 11,
        "servings": 24
    }
}

@app.get("/ping")
def ping():
    """Health check endpoint for service verification"""
    return "pong"

@app.get("/recipes")
def get_all_recipes():
    """Get all recipes from the in-memory storage"""
    return list(recipes_db.values())

@app.get("/recipes/{recipe_id}")
def get_recipe_by_id(recipe_id: int):
    """Get a specific recipe by ID"""
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipes_db[recipe_id]
