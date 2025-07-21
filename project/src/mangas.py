from pydantic import BaseModel
from fastapi import Response, status, APIRouter

inventario=[]

mangaRouter = APIRouter(prefix="/mangas")

class Manga(BaseModel):
    title: str
    author: str
    usuario_ultimo_prestamo: str = None

@mangaRouter.post("/add")
def anadir_manga(manga:Manga,response:Response):
    response.status_code= status.HTTP_201_CREATED
    inventario.append(manga)