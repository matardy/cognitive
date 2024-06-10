from sqlalchemy.orm import Session
from schemas.user import User, UserCreate
from repository.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.db = db

    async def create_user(self, user_create: UserCreate):
        return await self.user_repository.create_user(user_create=user_create)