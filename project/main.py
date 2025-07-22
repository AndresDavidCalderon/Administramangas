import uvicorn
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

# Codigo de apoyo para correr la aplicacion desde VSCode, permitiendo breakpoints y debugging.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)