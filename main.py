from fastapi import FastAPI

from database import Base, engine
import models
from routers import blogs

Base.metadata.create_all(engine)

app = FastAPI(title="blog")
app.include_router(blogs.router)