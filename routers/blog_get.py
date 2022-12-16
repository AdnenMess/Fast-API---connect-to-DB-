from enum import Enum
from typing import Optional

from fastapi import APIRouter, status, Response

router = APIRouter(prefix='/blog', tags=['blog'])


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@router.get("/type/{types}")
def get_blog(types: BlogType):
    return {"message": f"blog type {types}"}


@router.get('/all')
def get_all_blogs(page=1, page_size: Optional[int] = None):
    return {"message": f"All {page_size} blogs on page {page}"}


@router.get('/{ID}', response_description="The list of available blogs")
def get_blog_id(ID: int, response: Response):
    if ID > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog {ID} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with id {ID}"}
