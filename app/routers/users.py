from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import UserRead, UserCreate, UserUpdate
from ..crud.user import user_crud
from ..auth  import get_current_user

router = APIRouter(prefix="/auth/users", tags=["Auth"])

@router.post("/", response_model=UserRead, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_crud.create_user(db, user)

@router.patch("/me")
def update_my_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    updated_user = user_crud.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/me", response_model=UserRead)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    return current_user