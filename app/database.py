from typing import Dict, List, Optional
from app.schemas import User, UserCreate
import bcrypt

class Database:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self._next_id = 1
        self._passwords: Dict[int, bytes] = {}

    def _hash_password(self, password: str) -> bytes:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def _verify_password(self, password: str, hashed: bytes) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)

    async def create_user(self, user: UserCreate) -> User:
        user_id = self._next_id
        self._next_id += 1
        
        # Crear usuario sin password
        db_user = User(
            id=user_id,
            email=user.email,
            name=user.name,
            role=user.role,
            is_active=True
        )
        
        self.users[user_id] = db_user
        self._passwords[user_id] = self._hash_password(user.password)
        
        return db_user

    async def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    async def get_all_users(self) -> List[User]:
        return list(self.users.values())

    async def update_user(self, user_id: int, user_update: dict) -> Optional[User]:
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        
        # Actualizar campos
        for field, value in user_update.items():
            if value is not None:
                if field == 'password':
                    self._passwords[user_id] = self._hash_password(value)
                else:
                    setattr(user, field, value)
        
        return user

    async def delete_user(self, user_id: int) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            if user_id in self._passwords:
                del self._passwords[user_id]
            return True
        return False

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if not user:
            return None
        
        hashed_password = self._passwords.get(user.id)
        if not hashed_password or not self._verify_password(password, hashed_password):
            return None
        
        return user

# Instancia global de la base de datos
db = Database()