from pydantic import BaseModel
from fastapi import Response, status, APIRouter

mangaRouter = APIRouter(prefix="/mangas")

class Manga(BaseModel):
    title: str
    author: str
    usuario_ultimo_prestamo: str = None

class MangaCreado(BaseModel):
    title: str
    author: str

inventario:list[Manga]=[]

# Añade un manga. Por defecto, va al catalogo.
@mangaRouter.post("/add")
def anadir_manga(manga:MangaCreado,response:Response):
    response.status_code= status.HTTP_201_CREATED
    inventario.append(Manga(**manga.model_dump()))


@mangaRouter.get("/list")
def listar_mangas(catalogo: bool = False):
    """Devuelve la lista de mangas en el inventario."""
    if catalogo:
        return [manga for manga in inventario if manga.usuario_ultimo_prestamo is None]
    return inventario

# Configura el inventario por defecto con algunos mangas.
def configurar_por_defecto():
    global inventario
    inventario = [
        Manga(title="Attack on titan", author="Hajime Isayama"),
        Manga(title="Death Note", author="Tsugumi Ohba"),
        Manga(title="One Piece", author="Eiichiro Oda")
    ] # Algunos mangas de ejemplo, los unittest cuentan con ellos.

# Elimina un manga del inventario, por titulo.
@mangaRouter.delete("/delete/{title}")
def eliminar_manga(title: str, response: Response):
    global inventario
    aeliminar = list(filter(lambda x: x.title==title, inventario))
    if len(aeliminar) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Manga no encontrado"}
    inventario.remove(aeliminar[0])
    response.status_code = status.HTTP_200_OK

configurar_por_defecto()