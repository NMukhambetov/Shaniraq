from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.comment import Comment
from ..schemas.shanyrak import ShanyrakRead, ShanyrakCreate, ShanyrakUpdate
from ..crud.shanyrak import shanyrak_crud
from ..auth import get_current_user

router = APIRouter(prefix="/shanyraks", tags=["Shanyraqs"])

@router.post("/", response_model=ShanyrakRead, status_code=status.HTTP_201_CREATED)
def create_new_shanyrak(
    shanyrak: ShanyrakCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return shanyrak_crud.create_shanyrak(db, shanyrak, user_id=current_user.user_id)

@router.get("/{shanyrak_id}", response_model=ShanyrakRead)
def read_shanyrak(shanyrak_id: int, db: Session = Depends(get_db)):
    db_shanyrak = shanyrak_crud.get_shanyrak(db, shanyrak_id)
    if not db_shanyrak:
        raise HTTPException(status_code=404, detail="Shanyrak not found")

    return {
        "shanyrak_id": db_shanyrak.shanyrak_id,
        "type": db_shanyrak.type,
        "price": db_shanyrak.price,
        "address": db_shanyrak.address,
        "area": db_shanyrak.area,
        "rooms_count": db_shanyrak.rooms_count,
        "description": db_shanyrak.description,
        "user_id": db_shanyrak.user_id,
        "total_comments": len(db_shanyrak.comments)
    }
@router.patch("/{shanyrak_id}", response_model=ShanyrakRead)
def update_shanyrak(
    shanyrak_id: int,
    updates: ShanyrakUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_shanyrak = shanyrak_crud.get_shanyrak(db, shanyrak_id)
    if not db_shanyrak or db_shanyrak.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shanyrak_crud.update_shanyrak(db, shanyrak_id, updates)

@router.delete("/{shanyrak_id}")
def delete_shanyrak(
    shanyrak_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_shanyrak = shanyrak_crud.get_shanyrak(db, shanyrak_id)
    if not db_shanyrak or db_shanyrak.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return shanyrak_crud.delete_shanyrak(db, shanyrak_id)