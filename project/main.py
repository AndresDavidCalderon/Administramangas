from fastapi import FastAPI
from .mangas import mangaRouter
from .users import usuarioRouter
from .prestamos import prestamoRouter

app = FastAPI(
    title="Administramangas",
    description="API para administrar un inventario de mangas, de una biblioteca",
)
app.include_router(mangaRouter)
app.include_router(usuarioRouter)
app.include_router(prestamoRouter)
