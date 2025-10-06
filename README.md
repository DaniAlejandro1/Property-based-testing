# CRUD de Usuarios con FastAPI

Un prototipo funcional que implementa un CRUD completo de usuarios con FastAPI y pruebas basadas en propiedades.


---

## 🧩 Prerrequisitos

- Python 3.8 o superior  
- `pip` (gestor de paquetes de Python)  
- `git`

---

## ⚙️ Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/DaniAlejandro1/Property-based-testing
cd Property-based-testing
```
2. Crear entorno virtual
🪟 Opción A: Windows (PowerShell)
```powershell
Copiar código
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate
```
# Si PowerShell da error de ejecución, ejecutar primero:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
# 🪟 Opción B: Windows (Command Prompt)

# Crear entorno virtual
### Activar entorno virtual
```
python -m venv venv

venv\Scripts\activate.bat
```
### 🐧 Opción C: Linux/MacOS

```bash
Copiar código
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate
```
### 3. Instalar dependencias
```bash
Copiar código
# Instalar todas las dependencias
pip install -r requirements.txt

# Si hay problemas con bcrypt en Windows, usar:
pip install -r requirements.txt --only-binary=all

# O instalar manualmente las dependencias:
pip install fastapi==0.104.1 uvicorn==0.24.0 pydantic==2.5.0 hypothesis==6.88.0 pytest==7.4.3 pytest-asyncio==0.21.1 passlib[bcrypt]==1.7.4
```

# Desarrollo con auto-reload
```
uvicorn app.main:app --reload
```
### 🧪 Ejecutar pruebas
```bash

pytest
```



# 🧠 Pruebas basadas en propiedades implementadas
- Creación y recuperación: Un usuario creado con datos válidos debe ser recuperable

- Idempotencia de actualización: Actualizar múltiples veces con los mismos datos no cambia el resultado

- Idempotencia de eliminación: Eliminar usuarios inexistentes es idempotente

- Unicidad de email: No se pueden crear dos usuarios con el mismo email

- Consistencia de listado: La lista de usuarios es consistente con las operaciones CRUD