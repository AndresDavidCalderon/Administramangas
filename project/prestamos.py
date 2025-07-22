from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from .users import obtener_usuario_por_email
from .mangas import buscar_manga

prestamoRouter = APIRouter(prefix="/prestamos")

class Prestamo(BaseModel):
    titulo_manga: str
    email_usuario: str
    fecha: str  

prestamos: list[Prestamo] = []

@prestamoRouter.post("/add")
def crear_prestamo(prestamo: Prestamo, response: Response):
    usuario = obtener_usuario_por_email(prestamo.email_usuario)
    if not usuario:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Usuario no encontrado"}

    manga = buscar_manga(prestamo.titulo_manga)
    if not manga:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Manga no encontrado"}

    if manga.usuario_ultimo_prestamo is not None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Manga ya prestado"}

    manga.usuario_ultimo_prestamo = prestamo.email_usuario
    prestamos.append(prestamo)
    return {"message": "Préstamo registrado"}

@prestamoRouter.patch("/devolver/{titulo}")
def devolver_manga(titulo: str, response: Response):
    manga = buscar_manga(titulo)
    if not manga:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Manga no encontrado"}

    if manga.usuario_ultimo_prestamo is None:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Manga no está prestado"}

    manga.usuario_ultimo_prestamo = None
    return {"message": "Manga devuelto"}


@prestamoRouter.patch("/renovar")
def renovar_prestamo(email_usuario: str, titulo_manga: str, fecha: str, response: Response):
    usuario = obtener_usuario_por_email(email_usuario)
    if not usuario:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Usuario no encontrado"}

    manga = buscar_manga(titulo_manga)
    if not manga:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Manga no encontrado"}

    if manga.usuario_ultimo_prestamo != email_usuario:
        response.status_code = status.HTTP_409_CONFLICT
        return {"message": "Manga no está prestado a este usuario"}

    for prestamo in prestamos:
        if prestamo.titulo_manga == titulo_manga and prestamo.email_usuario == email_usuario:
            prestamo.fecha = fecha
            return {"message": "Préstamo renovado"}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"message": "Préstamo no encontrado"}