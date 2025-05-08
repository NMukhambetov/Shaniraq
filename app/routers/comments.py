from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.comment import CommentCreate, CommentRead, CommentListResponse
from ..crud.comment import comment_crud
from ..auth  import get_current_user

router = APIRouter(prefix="/shanyraks/{shanyrak_id}/comments", tags=["Comments"])


@router.post("/", response_model=CommentRead)
def add_comment(
    shanyrak_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return comment_crud.create_comment(db, comment, shanyrak_id=shanyrak_id, author_id=current_user.user_id)

@router.get("/", response_model=CommentListResponse)
def list_comments(shanyrak_id: int, db: Session = Depends(get_db)):
    return comment_crud.get_comments_by_shanyrak(db, shanyrak_id)

@router.patch("/{comment_id}")
def edit_comment(
    shanyrak_id: int,
    comment_id: int,
    updates: CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_comment = comment_crud.get_comment(db, comment_id)
    if not db_comment or db_comment.author_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return comment_crud.update_comment(db, comment_id, updates)

@router.delete("/{comment_id}")
def remove_comment(
    shanyrak_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    db_comment = comment_crud.get_comment(db, comment_id)
    if not db_comment or db_comment.author_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return comment_crud.delete_comment(db, comment_id)