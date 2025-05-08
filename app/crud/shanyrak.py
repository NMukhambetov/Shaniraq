from sqlalchemy.orm import Session
from app.models.shanyrak import Shanyrak
from app.schemas.shanyrak import ShanyrakCreate, ShanyrakUpdate, ShanyrakRead

class ShanyrakCRUD:
    def get_shanyrak(self, db: Session, shanyrak_id: int):
        return db.query(Shanyrak).filter(Shanyrak.shanyrak_id == shanyrak_id).first()

    def create_shanyrak(self, db: Session, shanyrak: ShanyrakCreate, user_id: int):
        db_shanyrak = Shanyrak(**shanyrak.model_dump(), user_id=user_id)
        db.add(db_shanyrak)
        db.commit()
        db.refresh(db_shanyrak)
        return ShanyrakRead.model_validate(db_shanyrak)

    def update_shanyrak(self, db: Session, shanyrak_id: int, updates: ShanyrakUpdate):
        db_shanyrak = self.get_shanyrak(db, shanyrak_id)
        if not db_shanyrak:
            return None

        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_shanyrak, key, value)

        db.commit()
        db.refresh(db_shanyrak)
        return ShanyrakRead.model_validate(db_shanyrak)

    def delete_shanyrak(self, db: Session, shanyrak_id: int):
        db_shanyrak = self.get_shanyrak(db, shanyrak_id)
        if not db_shanyrak:
            return None
        db.delete(db_shanyrak)
        db.commit()
        return {"message": "Shanyrak deleted successfully"}

shanyrak_crud = ShanyrakCRUD()