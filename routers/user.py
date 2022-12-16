from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import db_user
from db.database import get_db
from schemas import UserBase, UserDisplay

router = APIRouter(prefix='/user', tags=['user'])


# Create user
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# readr all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# read one user
@router.get('/{ids}', response_model=UserDisplay)
def get_user(ids: int, db: Session = Depends(get_db)):
    return db_user.get_user(db, ids)


# Update user
@router.put('/{ids}/update')
def update_user(ids: int, request: UserBase, db: Session = Depends(get_db)):
    return db_user.update_user(db, ids, request)


# Delete user
@router.delete('/delete/{ids}')
def delete_user(ids: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, ids)
