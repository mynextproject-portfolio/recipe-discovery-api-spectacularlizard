import sys
from copy import deepcopy
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
import main  # noqa: E402  # isort: skip


@pytest.fixture(autouse=True)
def reset_state():
    """Ensure each test starts with the original in-memory data."""
    initial_recipes = deepcopy(main.recipes_db)
    initial_next_id = main.next_recipe_id
    yield
    main.recipes_db.clear()
    main.recipes_db.update(deepcopy(initial_recipes))
    main.next_recipe_id = initial_next_id


@pytest.fixture
def client():
    return TestClient(main.app)


def test_ping(client):
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == "pong"


def test_get_all_recipes(client):
    response = client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert isinstance(recipes, list)
    assert len(recipes) == len(main.recipes_db)
    assert {recipe["id"] for recipe in recipes} == set(main.recipes_db.keys())


def test_get_recipe_by_id(client):
    response = client.get("/recipes/1")
    assert response.status_code == 200
    recipe = response.json()
    assert recipe["id"] == 1
    assert recipe["title"] == main.recipes_db[1]["title"]


def test_get_recipe_not_found(client):
    response = client.get("/recipes/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_create_recipe(client):
    new_recipe = {
        "title": "Summer Harvest Salad",
        "ingredients": ["lettuce", "tomatoes", "cucumbers", "vinaigrette"],
        "steps": ["Chop vegetables", "Toss with dressing"],
        "prepTime": "10 minutes",
        "cookTime": "0 minutes",
        "difficulty": "Easy",
        "cuisine": "Mediterranean",
    }
    expected_id = main.next_recipe_id

    response = client.post("/recipes", json=new_recipe)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] == expected_id
    for key, value in new_recipe.items():
        assert created[key] == value

    stored = client.get(f"/recipes/{expected_id}")
    assert stored.status_code == 200
    assert stored.json()["title"] == new_recipe["title"]


def test_update_recipe(client):
    updated_recipe = {
        "title": "Classic Spaghetti Carbonara (Updated)",
        "ingredients": ["spaghetti", "pancetta", "eggs", "pecorino", "pepper"],
        "steps": ["Boil pasta", "Cook pancetta", "Mix eggs and cheese", "Combine all"],
        "prepTime": "12 minutes",
        "cookTime": "14 minutes",
        "difficulty": "Medium",
        "cuisine": "Italian",
    }

    response = client.put("/recipes/1", json=updated_recipe)
    assert response.status_code == 200
    recipe = response.json()
    assert recipe["id"] == 1
    assert recipe["title"] == updated_recipe["title"]

    fetched = client.get("/recipes/1")
    assert fetched.status_code == 200
    assert fetched.json()["title"] == updated_recipe["title"]


def test_update_recipe_not_found(client):
    updated_recipe = {
        "title": "Nonexistent Recipe",
        "ingredients": ["item"],
        "steps": ["do something"],
        "prepTime": "1 minute",
        "cookTime": "1 minute",
        "difficulty": "Easy",
        "cuisine": "Fusion",
    }

    response = client.put("/recipes/404", json=updated_recipe)
    assert response.status_code == 404
    assert response.json()["detail"] == "Recipe not found"


def test_search_recipes_case_insensitive_and_partial_matches(client):
    carbonara = client.get("/recipes/search", params={"q": "carbonara"})
    assert carbonara.status_code == 200
    carbonara_results = carbonara.json()
    assert len(carbonara_results) == 1
    assert carbonara_results[0]["id"] == 1

    chicken = client.get("/recipes/search", params={"q": "CHICKEN"})
    assert chicken.status_code == 200
    chicken_results = chicken.json()
    assert len(chicken_results) == 1
    assert chicken_results[0]["id"] == 2

    partial = client.get("/recipes/search", params={"q": "choco"})
    assert partial.status_code == 200
    partial_results = partial.json()
    assert len(partial_results) == 1
    assert partial_results[0]["id"] == 3


def test_search_recipes_returns_empty_for_missing_or_blank_query(client):
    missing_query = client.get("/recipes/search")
    assert missing_query.status_code == 200
    assert missing_query.json() == []

    blank_query = client.get("/recipes/search", params={"q": "   "})
    assert blank_query.status_code == 200
    assert blank_query.json() == []


def test_happy_path_crud_and_search_cycle(client):
    create_payload = {
        "title": "Roasted Veggie Bowl",
        "ingredients": ["sweet potatoes", "broccoli", "quinoa", "olive oil"],
        "steps": ["Roast veggies", "Cook quinoa", "Assemble bowl"],
        "prepTime": "15 minutes",
        "cookTime": "30 minutes",
        "difficulty": "Easy",
        "cuisine": "American",
    }

    create_response = client.post("/recipes", json=create_payload)
    assert create_response.status_code == 201
    created_recipe = create_response.json()
    recipe_id = created_recipe["id"]

    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == create_payload["title"]

    search_response = client.get("/recipes/search", params={"q": "Veggie"})
    assert search_response.status_code == 200
    search_results = search_response.json()
    assert any(recipe["id"] == recipe_id for recipe in search_results)

    updated_payload = {**create_payload, "title": "Roasted Veggie Bowl Deluxe"}
    update_response = client.put(f"/recipes/{recipe_id}", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["title"] == updated_payload["title"]

    verify_response = client.get(f"/recipes/{recipe_id}")
    assert verify_response.status_code == 200
    assert verify_response.json()["title"] == updated_payload["title"]

