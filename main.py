from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Pydantic model for Recipe request body
class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[str]
    prepTime: str
    cookTime: str
    difficulty: str
    cuisine: str

class Recipe(RecipeCreate):
    id: int

# In-memory recipe storage with sample data
recipes_db = {
    1: {
        "id": 1,
        "title": "Classic Spaghetti Carbonara",
        "ingredients": [
            "400g spaghetti",
            "200g pancetta or guanciale",
            "4 large eggs",
            "100g Pecorino Romano cheese",
            "Black pepper",
            "Salt"
        ],
        "steps": [
            "Cook spaghetti in salted boiling water until al dente",
            "Fry pancetta until crispy",
            "Whisk eggs with grated cheese and black pepper",
            "Combine hot pasta with pancetta",
            "Remove from heat and quickly mix in egg mixture",
            "Serve immediately with extra cheese"
        ],
        "prepTime": "15 minutes",
        "cookTime": "15 minutes",
        "difficulty": "Medium",
        "cuisine": "Italian"
    },
    2: {
        "id": 2,
        "title": "Chicken Tikka Masala",
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
        "steps": [
            "Marinate chicken in yogurt and spices for 30 minutes",
            "Cook rice according to package instructions",
            "Grill chicken pieces until cooked through",
            "Sauté onion, garlic, and ginger",
            "Add tomatoes and tikka masala paste",
            "Simmer with coconut milk for 10 minutes",
            "Add grilled chicken and cook for 5 minutes",
            "Garnish with cilantro and serve with rice"
        ],
        "prepTime": "45 minutes",
        "cookTime": "30 minutes",
        "difficulty": "Medium",
        "cuisine": "Indian"
    },
    3: {
        "id": 3,
        "title": "Chocolate Chip Cookies",
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
        "steps": [
            "Preheat oven to 375°F (190°C)",
            "Mix flour, baking soda, and salt in a bowl",
            "Cream butter and sugars until light and fluffy",
            "Beat in eggs and vanilla",
            "Gradually blend in flour mixture",
            "Stir in chocolate chips",
            "Drop spoonfuls onto ungreased baking sheets",
            "Bake for 9-11 minutes until golden brown"
        ],
        "prepTime": "20 minutes",
        "cookTime": "11 minutes",
        "difficulty": "Easy",
        "cuisine": "American"
    }
}

# Counter for generating unique IDs
next_recipe_id = 4

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

@app.post("/recipes", status_code=status.HTTP_201_CREATED, response_model=Recipe)
def create_recipe(recipe: RecipeCreate):
    """Create a new recipe"""
    global next_recipe_id
    
    # Create new recipe with generated ID
    new_recipe = {
        "id": next_recipe_id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "steps": recipe.steps,
        "prepTime": recipe.prepTime,
        "cookTime": recipe.cookTime,
        "difficulty": recipe.difficulty,
        "cuisine": recipe.cuisine
    }
    
    # Store in database
    recipes_db[next_recipe_id] = new_recipe
    next_recipe_id += 1
    
    return new_recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: RecipeCreate):
    """Update an existing recipe by ID"""
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    # Update recipe with new data
    updated_recipe = {
        "id": recipe_id,
        "title": recipe.title,
        "ingredients": recipe.ingredients,
        "steps": recipe.steps,
        "prepTime": recipe.prepTime,
        "cookTime": recipe.cookTime,
        "difficulty": recipe.difficulty,
        "cuisine": recipe.cuisine
    }
    
    recipes_db[recipe_id] = updated_recipe
    
    return updated_recipe

@app.delete("/recipes/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int):
    """Delete a recipe by ID"""
    if recipe_id not in recipes_db:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    del recipes_db[recipe_id]
    
    return None
