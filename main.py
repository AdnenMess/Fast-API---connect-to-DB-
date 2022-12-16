from db.database import engine
from routers import blog_get, article
from routers import blog_post
from routers import user
from db import models

from fastapi import FastAPI

app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{names}",
         tags=['hello'],
         summary="Retrieve all names",
         description="This api call simulates fetching all blogs")
async def say_hello(names: str):
    return {"message": f"Hello {names}"}

models.Base.metadata.create_all(engine)
