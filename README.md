# CRUD de Usuarios con FastAPI

Un prototipo funcional que implementa un CRUD completo de usuarios con FastAPI y pruebas basadas en propiedades.

## Características

- ✅ CRUD completo de usuarios (Create, Read, Update, Delete)
- ✅ Validación de datos con Pydantic
- ✅ Pruebas unitarias convencionales
- ✅ Pruebas basadas en propiedades con Hypothesis
- ✅ Base de datos en memoria
- ✅ Hashing seguro de contraseñas con bcrypt

## Instalación

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd crud-users-fastapi

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
uvicorn app.main:app --reload

# La API estará disponible en http://localhost:8000
# Documentación automática en http://localhost:8000/docs