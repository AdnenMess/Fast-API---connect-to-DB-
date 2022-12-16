class Optional:
pass# FASTAPI


We have to install `fastapi` and `uvicorn(light web server)`

```shell
pip install fastapi
pip install uvicorn
```

Then we have to install `BaselModel` from the library  `pydantic` (validation data modeling)

```shell
pip install pydandic
```

***
### GET method

1- **Path parameters**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get('/blog/{ids}')
def index(ids: int):
    return {"message": f"Bolg with id {ids}"}
```
***

2- **Predefined path**
```python
from enum import Enum

class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'
```
```python
@app.get('/blog/type/{type}')
def blog_type(type: BlogType):  
    return {"message": f"Blog type: {type}"}
```

***

3- **Query parameters**

Any function parameters not part of the path are considered as query parameters


```python
@ap.get('/blog/all')
def get_blogs(page = 1, page_size: Optional[int] = None):
    return {"message": f"All {page_size} blogs on page {page}"}
```
`http://127.0.0.1:8000/blog/all?page=2&page_size=5 , the query is after ? `

***
### Operation description

1- **Status Code**

```python
from fastapi import FastAPI, status, Response

app = FastAPI()

@app.get('/blog/{id}')
def get_blog_id(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": f"Blog {id} not found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"message": f"Blog with id {id}"}
```

***

2- **Tags**

tags allow to structure the documentation in a very nice way

```python
@app.get("/hello/{names}", tags=['hello'])
async def say_hello(names: str):
    return {"message": f"Hello {names}"}
```

***

3- **Summary and description**

```python
@app.get("/hello/{names}",
         tags=['hello'],
         summary="Retrieve all names",
         description="This api call simulates fetching all blogs")
async def say_hello(names: str):
    return {"message": f"Hello {names}"}
```

for the description we can use **docstrings** inside the function

***

4- **Response description**

```python
@app.get('/blog/{ID}', response_description="The list of available blogs")
```

***

### Routers

Routers allow to split our api on multiple files 

```python
from fastapi import APIRouter

my_router = APIRouter(prefix='/blog', tags=['blog'])

@my_router.get('/')
```
```python
from fastapi import FastAPI
from routers import blog

app = FastAPI()

app.include_router(blog.my_router)
```
***

### Post method

1- **Pydantic BaseModel**

```python
from pydantic import BaseModel
from typing import Optional


class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool]
```

FastAPI will convert the data:

```python
@router.post('/new/{ids}')
def create_blog(blog: BlogModel, ids: int, version: int = 1):
    return {"id": ids,
            "data": blog,
            "version": version }
```

***

2- **Parameter metadata**

Add title and description

```python
from fastapi import Query

comment_id: int = Query(None,
                        title='Id of the comment',
                        description='Some description for comment_id')
```

Add alias

```python
from fastapi import Query

comment_id: int = Query(None,
                        alias='commentID')
```

Add deprecation

```python
from fastapi import Query

comment_id: int = Query(None,
                        description=True)
```

result ==> 

```python
@router.post('/new/{ids}/comment')
def create_comment(blog: BlogModel,
                   ids: int,
                   comment_id: int = Query(None,
                                           title='Id of the comment',
                                           description='Some description for comment_id',
                                           alias='commentID',
                                           deprecated=True)
                   ):
    return {
        'blog': blog,
        'id': ids,
        'comment_id': comment_id
    }
```

***

### Connect the API to database

1- **Post method**

1. Import required libraries :
    ```shell
    pip install sqlalchemy
    pip install bcrypt
    pip install passlib
    ```
2. Create database definition `db\database.py` and run it in `main.py`
3. Create database models `db\models.py`
4. Create tables (functionality) to write to database `routers\user.py`
5. Create schemas `schemas.py`

        - Datafrom user: UserBase
        - Response to user: UserDisplay
6. Create API operation `routers\user.py`

***

2- **Get method**

**Read all elements**
```python
return db.query(DbUser).all()
```

**Read one element (base on id)**
```python
return db.query(DbUser).filter(DbUser.id==id).first()
```

3- **Update method**

```python
user = db.query(DbUser).filter(DbUser.id == id)
user.update({
   DbUser.username: request.username
   DbUser.email: request.email
})
db.commit()
```

***

4- **Delete method**

```python
user = db.query(DbUser).filter(DbUser.id == id).first()
db.delete(user)
db.commit()
```

***

5- **Connection with multi-tables**

if we have a relation of tables like this :

<img src="C:\Project\API\SecondAPIProject\db\Relationship.png"/>

1. Define relationship in models :

```python
class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("DbArticle", back_populates='user')


class DbArticle(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("DbUser", back_populates='items')
```
2. Add elements in schemas :

```python
class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
    

class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    
    class Config:
        orm_mode = True
```
3. Create functions :

```python
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
    return article
```
4. Create a router :

```python
router = APIRouter(prefix='/article', tags=['article'])

# Create article
@router.post('/', response_model=ArticleDisplay)
def create_article(request: ArticleBase, db: Session = Depends(get_db)):
    return db_article.create_article(db, request)

# Get specific article
@router.get('/{ids}', response_model=ArticleDisplay)
def get_article(ids: int, db: Session = Depends(get_db)):
    return db_article.get_article(db, ids)
```

***

### Exceptions

```python
raise HTTPException(status_code=satus.HTTP_404_NOT_FOUND, detail=f"User with id 
{id}" not found)
```

***


