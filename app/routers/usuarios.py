# ============================================================
#  routers/usuarios.py  -->  Endpoints de registro e inicio de sesión
# ============================================================
#   POST /usuarios/registro  -> crear una cuenta nueva
#   POST /usuarios/login     -> iniciar sesión y recibir un token
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCrear, UsuarioRespuesta, Token
from app.auth import encriptar_password, verificar_password, crear_token

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# ------------------------------------------------------------
# REGISTRO: crear una cuenta nueva
# ------------------------------------------------------------
@router.post("/registro", response_model=UsuarioRespuesta)
def registrar(datos: UsuarioCrear, db: Session = Depends(get_db)):
    # 1. Revisar que el correo no esté ya registrado
    existe = db.query(Usuario).filter(Usuario.email == datos.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ese correo ya está registrado")

    # 2. Crear el usuario con la contraseña ENCRIPTADA
    nuevo = Usuario(
        email=datos.email,
        hashed_password=encriptar_password(datos.password),
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ------------------------------------------------------------
# LOGIN: iniciar sesión y recibir un token
# ------------------------------------------------------------
@router.post("/login", response_model=Token)
def iniciar_sesion(datos: UsuarioCrear, db: Session = Depends(get_db)):
    # 1. Buscar al usuario por su correo
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()

    # 2. Verificar que exista y que la contraseña sea correcta.
    #    (Damos el mismo mensaje en ambos casos por seguridad.)
    if usuario is None or not verificar_password(datos.password, usuario.hashed_password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

    # 3. Crear y devolver el token
    token = crear_token(usuario.id)
    return Token(access_token=token)
