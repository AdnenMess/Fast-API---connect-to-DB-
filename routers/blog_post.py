from fastapi import APIRouter, Query, Body
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix='/blog', tags=['blog'])


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]


@router.post('/new/{ids}')
def create_blog(blog: BlogModel, ids: int, version: int = 1):
    return {
        "id": ids,
        "data": blog,
        "version": version
        }


@router.post('/new/{ids}/comment')
def create_comment(blog: BlogModel,
                   ids: int,
                   comment_id: int = Query(None,
                                           title='Id of the comment',
                                           description='Some description for comment_id',
                                           alias='commentID',
                                           deprecated=True),
                   content: str = Body(...)
                   ):
    return {
        'blog': blog,
        'id': ids,
        'comment_id': comment_id,
        'content': content
    }
