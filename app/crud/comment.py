from sqlalchemy.orm import Session
from ..models.comment import Comment
from ..schemas.comment import CommentCreate, CommentRead, CommentListResponse

class CommentCRUD:

    def get_comment(self, db: Session, comment_id: int):
        return db.query(Comment).filter(Comment.comment_id == comment_id).first()

    def get_comments_by_shanyrak(self, db: Session, shanyrak_id: int, skip: int = 0, limit: int = 100):
        comments = db.query(Comment).filter(Comment.shanyrak_id == shanyrak_id).offset(skip).limit(limit).all()
        return CommentListResponse(comments=[CommentRead.model_validate(c) for c in comments])

    def create_comment(self, db: Session, comment: CommentCreate, shanyrak_id: int, author_id: int):
        db_comment = Comment(
            content=comment.content,
            shanyrak_id=shanyrak_id,
            author_id=author_id
        )
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment # Not ideal — better to use Pydantic

    def update_comment(self, db: Session, comment_id: int, updates: CommentCreate):
        db_comment = self.get_comment(db, comment_id)
        if not db_comment:
            return None

        for key, value in updates.model_dump(exclude_unset=True).items():
            setattr(db_comment, key, value)

        db.commit()
        db.refresh(db_comment)
        return CommentRead.model_validate(db_comment)

    def delete_comment(self, db: Session, comment_id: int):
        db_comment = self.get_comment(db, comment_id)
        if not db_comment:
            return None

        db.delete(db_comment)
        db.commit()
        return {"message": "Comment deleted successfully"}

comment_crud = CommentCRUD()