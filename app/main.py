from fastapi import FastAPI
from . import models
from .database import engine
from .routes import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.routers)
app.include_router(user.routers)
app.include_router(auth.routers)
app.include_router(vote.routers)


@app.get("/")
async def root():
    return {"message": "Social media backend!!!"}


