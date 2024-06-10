
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schemas.user import UserCreate
from sqlalchemy.orm import selectinload, Session
class UserRepository:
    def __init__(self, db: Session):
        self.db = db 
    
    async def create_user(self, user_create: UserCreate):
        # Verifica si el usuario ya existe en la base de datos
        stmt = select(User).filter(User.user_id == user_create.user_id)
        result = self.db.execute(stmt)
        existing_user = result.scalars().first()
        
        if existing_user:
            print(f"User already exists: {existing_user}")
            return existing_user
        
        # Si el usuario no existe, crea uno nuevo
        user = User(user_id=user_create.user_id)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        print(f"Created User: {user}")
        return user