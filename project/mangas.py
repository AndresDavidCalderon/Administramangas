from pydantic import BaseModel
from fastapi import Response, status, APIRouter

inventario=[]

mangaRouter = APIRouter(prefix="/mangas")

class Manga(BaseModel):
    title: str
    author: str
    usuario_ultimo_prestamo: str = None

class MangaCreado(BaseModel):
    title: str
    author: str

@mangaRouter.post("/add")
def anadir_manga(manga:MangaCreado,response:Response):
    response.status_code= status.HTTP_201_CREATED
    inventario.append(Manga(**manga.model_dump()))


@mangaRouter.get("/list")
def listar_mangas():
    return inventario