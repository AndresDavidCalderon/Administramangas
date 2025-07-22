from pydantic import BaseModel
from fastapi import APIRouter, Response, status

usuarioRouter = APIRouter(prefix="/usuarios")

class Usuario(BaseModel):
    nombre: str
    email: str

usuarios: list[Usuario] = []

@usuarioRouter.post("/add", status_code=201)
def agregar_usuario(usuario: Usuario, response: Response):
    if any(u.email == usuario.email for u in usuarios):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Usuario ya existe"}
    usuarios.append(usuario)
    return {"message": "Usuario agregado correctamente"}

@usuarioRouter.patch("/update/{email}")
def actualizar_usuario(email: str, nuevo_usuario: Usuario, response: Response):
    usuario_existente = next(filter(lambda u: u.email == email, usuarios), None)
    if usuario_existente is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Usuario no encontrado"}

    usuarios[usuarios.index(usuario_existente)] = nuevo_usuario
    return {"message": "Usuario actualizado"}

def obtener_usuario_por_email(email: str) -> Usuario | None:
    for u in usuarios:
        if u.email == email:
            return u
    return None

def lista_usuarios():
    return usuarios
