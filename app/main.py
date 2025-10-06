from fastapi import FastAPI, HTTPException, status
from app.schemas import User, UserCreate, UserUpdate
from app.database import db
from typing import List

app = FastAPI(
    title="User CRUD API",
    description="Un prototipo funcional de CRUD de usuarios con pruebas basadas en propiedades",
    version="1.0.0"
)

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    # Verificar si el email ya existe
    existing_user = await db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = await db.create_user(user)
    return new_user

@app.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100):
    users = await db.get_all_users()
    return users[skip:skip + limit]

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = await db.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@app.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user_update: UserUpdate):
    # Convertir el modelo Pydantic a dict y eliminar campos None
    update_data = user_update.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )
    
    # Verificar si el email ya existe (si se está actualizando el email)
    if 'email' in update_data and update_data['email']:
        existing_user = await db.get_user_by_email(update_data['email'])
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    updated_user = await db.update_user(user_id, update_data)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    success = await db.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None

@app.get("/")
async def root():
    return {"message": "User CRUD API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}