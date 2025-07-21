from fastapi import FastAPI
from .mangas import mangaRouter

app = FastAPI()
app.include_router(mangaRouter)
