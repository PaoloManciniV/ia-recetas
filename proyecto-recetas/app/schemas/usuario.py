# ============================================================
#  schemas/usuario.py  -->  Datos de entrada/salida de usuarios
# ============================================================

from pydantic import BaseModel, EmailStr


# Lo que se envía para registrarse o iniciar sesión
class UsuarioCrear(BaseModel):
    email: EmailStr   # EmailStr valida que sea un correo de verdad
    password: str


# Lo que la API devuelve de un usuario (¡nunca la contraseña!)
class UsuarioRespuesta(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True


# Lo que devuelve el login: el token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
