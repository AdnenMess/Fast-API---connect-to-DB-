from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import DbArticle
from schemas import ArticleBase


def create_article(db: Session, request: ArticleBase):
    new_article = DbArticle(
        title=request.title,
        content=request.content,
        published=request.published,
        user_id=request.creator_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def get_article(db: Session, ids: int):
    article = db.query(DbArticle).filter(DbArticle.id == ids).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {ids} not found")
    return article
