import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import UserRole

client = TestClient(app)

# Estrategias para generar datos de prueba
emails = st.text(
    alphabet=st.characters(whitelist_categories=["L", "N"]),
    min_size=3,
    max_size=10
).map(lambda s: f"{s.lower()}@example.com")
names = st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=['L', 'N', 'Zs']))
passwords = st.text(min_size=6, max_size=100)
roles = st.sampled_from([role.value for role in UserRole])

class TestPropertyBasedCRUD:
    
    @given(
        email=emails,
        name=names,
        password=passwords,
        role=roles
    )
    @settings(max_examples=5, suppress_health_check=[HealthCheck.too_slow])
    def test_create_user_property(self, email: str, name: str, password: str, role: str):
        """Propiedad: Un usuario creado con datos válidos debe ser recuperable"""
        
        # Sanitizar campos que podrían causar errores
        name = name.strip()
        if len(name) < 1 or len(password) < 6:
            return

        user_data = {
            "email": email,
            "name": name,
            "password": password,
            "role": role
        }

        # Crear usuario
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 201, f"Error al crear usuario: {create_response.text}"
        created_user = create_response.json()

        # Verificar propiedades del usuario creado
        assert created_user["email"] == email
        assert created_user["name"] == name
        assert created_user["role"] == role
        assert "id" in created_user

        # Recuperar usuario por ID
        user_id = created_user["id"]
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 200, f"Error al obtener usuario: {get_response.text}"
        retrieved_user = get_response.json()

        # Verificar que los datos coincidan
        assert retrieved_user["id"] == user_id
        assert retrieved_user["email"] == email
        assert retrieved_user["name"] == name
        assert retrieved_user["role"] == role

        # Limpiar: eliminar el usuario
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code in (200, 204)

    @given(
        original_name=names,
        updated_name=names,
        original_role=roles,
        updated_role=roles
    )
    @settings(max_examples=2, suppress_health_check=[HealthCheck.too_slow])
    def test_update_user_idempotence(self, original_name: str, updated_name: str, 
                                   original_role: str, updated_role: str):
        """Propiedad: Actualizar un usuario múltiples veces con los mismos datos no cambia el resultado"""
        if len(original_name) < 1 or len(updated_name) < 1:
            return
            
        # Crear usuario inicial
        user_data = {
            "email": f"test_{original_name}@example.com",
            "name": original_name,
            "password": "password123",
            "role": original_role
        }
        create_response = client.post("/users/", json=user_data)
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]
        
        try:
            # Primera actualización
            update_data_1 = {"name": updated_name, "role": updated_role}
            update_1_response = client.put(f"/users/{user_id}", json=update_data_1)
            assert update_1_response.status_code == 200
            user_after_first_update = update_1_response.json()
            
            # Segunda actualización con los mismos datos
            update_data_2 = {"name": updated_name, "role": updated_role}
            update_2_response = client.put(f"/users/{user_id}", json=update_data_2)
            assert update_2_response.status_code == 200
            user_after_second_update = update_2_response.json()
            
            # Propiedad: Los resultados deben ser idénticos
            assert user_after_first_update == user_after_second_update
            
        finally:
            # Limpiar
            client.delete(f"/users/{user_id}")
    
    @given(user_id=st.integers(min_value=1, max_value=1000))
    @settings(max_examples=20)
    def test_delete_nonexistent_user(self, user_id: int):
        """Propiedad: Eliminar un usuario que no existe debe ser idempotente"""
        # Verificar que el usuario no existe
        get_response = client.get(f"/users/{user_id}")
        if get_response.status_code == 404:
            # Propiedad: Eliminar un usuario que no existe debe devolver 404
            delete_response = client.delete(f"/users/{user_id}")
            assert delete_response.status_code == 404
    
    @given(
        email1=emails,
        email2=emails,
        name1=names,
        name2=names
    )
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
    def test_user_uniqueness(self, email1: str, email2: str, name1: str, name2: str):
        """Propiedad: No se pueden crear dos usuarios con el mismo email"""
        if len(name1) < 1 or len(name2) < 1:
            return
            
        # Usar el mismo email para ambos usuarios
        same_email = email1 if email1 == email2 else email1
        
        user_data_1 = {
            "email": same_email,
            "name": name1,
            "password": "password123",
            "role": "user"
        }
        
        user_data_2 = {
            "email": same_email,
            "name": name2,
            "password": "password456",
            "role": "user"
        }
        
        # Crear primer usuario
        response_1 = client.post("/users/", json=user_data_1)
        if response_1.status_code == 201:
            user_id = response_1.json()["id"]
            
            # Intentar crear segundo usuario con mismo email
            response_2 = client.post("/users/", json=user_data_2)
            
            # Propiedad: El segundo intento debe fallar
            assert response_2.status_code == 400
            assert "already registered" in response_2.json()["detail"].lower()
            
            # Limpiar
            client.delete(f"/users/{user_id}")

    