from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_article
from db.database import get_db
from schemas import ArticleBase, ArticleDisplay
from auth.oauth2 import oauth2_scheme

router = APIRouter(prefix='/article', tags=['article'])


# Create article
@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.create_article(db, request)


# Get specific article
@router.get('/{ids}', response_model=ArticleDisplay)
def get_article(ids: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return db_article.get_article(db, ids)
