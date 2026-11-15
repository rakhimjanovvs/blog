from fastapi import FastAPI

import models
from routers import blogs

app = FastAPI(title="blog")
app.include_router(blogs.router)