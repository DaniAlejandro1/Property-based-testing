import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserCreate, UserRole

client = TestClient(app)

def test_create_user():
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword",
        "role": UserRole.USER
    }
    
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data

def test_get_user():
    # Primero crear un usuario
    user_data = {
        "email": "get@example.com",
        "name": "Get User",
        "password": "password",
        "role": UserRole.USER
    }
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Luego obtenerlo
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == user_data["email"]

def test_get_nonexistent_user():
    response = client.get("/users/9999")
    assert response.status_code == 404

def test_get_all_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_user():
    # Crear usuario
    user_data = {
        "email": "update@example.com",
        "name": "Update User",
        "password": "password",
        "role": UserRole.USER
    }
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Actualizar usuario
    update_data = {"name": "Updated Name", "role": UserRole.ADMIN}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["role"] == UserRole.ADMIN

def test_delete_user():
    # Crear usuario
    user_data = {
        "email": "delete@example.com",
        "name": "Delete User",
        "password": "password",
        "role": UserRole.USER
    }
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]
    
    # Eliminar usuario
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    # Verificar que fue eliminado
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404