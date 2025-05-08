from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate, UserRead
from ..auth import get_password_hash


class UserCRUD:

    def get_user(self, db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    def get_all_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: UserCreate):
        db_user = User(
            user_email=user.user_email,
            phone=user.phone,
            hashed_password=get_password_hash(user.hashed_password),
            name=user.name,
            city=user.city
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return UserRead.model_validate(db_user)

    def update_user(self, db: Session, user_id: int, updates: UserUpdate):
        db_user = self.get_user(db, user_id)
        if not db_user:
            return None

        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_user, key, value)

        db.commit()
        db.refresh(db_user)
        return UserRead.model_validate(db_user)

    def delete_user(self, db: Session, user_id: int):
        db_user = self.get_user(db, user_id)
        if not db_user:
            return None
        db.delete(db_user)
        db.commit()
        return {"message": "User deleted successfully"}

user_crud = UserCRUD()