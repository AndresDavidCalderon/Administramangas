from fastapi import FastAPI
from .mangas import mangaRouter

app = FastAPI(
    title="Administramangas",
    description="API para administrar un inventario de mangas, de una biblioteca",
)
app.include_router(mangaRouter)
