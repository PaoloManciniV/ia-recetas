# ============================================================
#  auth.py  -->  Seguridad: contraseñas y tokens (JWT)
# ============================================================
# Aquí está toda la "magia" del login:
#   - Encriptar contraseñas (nunca se guardan en texto plano)
#   - Crear y leer los tokens JWT (el "pase" que identifica al usuario)
#   - Una función que averigua QUÉ usuario está haciendo la petición
# ============================================================

import os
from datetime import datetime, timedelta, timezone

import bcrypt   # para encriptar contraseñas
import jwt      # para crear/leer los tokens JWT (librería PyJWT)
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario

# ------------------------------------------------------------
# Configuración. La SECRET_KEY se usa para "firmar" los tokens.
# En producción DEBE venir del .env y ser larga y secreta.
# ------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "clave-de-desarrollo-cambiar-en-produccion")
ALGORITMO = "HS256"
TOKEN_EXPIRA_MINUTOS = 60   # el token dura 1 hora


# ------------------------------------------------------------
# Contraseñas: nunca guardamos la real, guardamos una versión
# encriptada (hash). Al iniciar sesión, comparamos hashes.
# ------------------------------------------------------------
def encriptar_password(password: str) -> str:
    # Convertimos el texto a bytes, lo encriptamos y lo devolvemos como texto
    hash_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_password(password: str, password_encriptada: str) -> bool:
    # Devuelve True si la contraseña coincide con la encriptada
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_encriptada.encode("utf-8"),
    )


# ------------------------------------------------------------
# Tokens JWT: el "pase" que el usuario recibe al iniciar sesión.
# Lo manda en cada petición para demostrar quién es.
# ------------------------------------------------------------
def crear_token(usuario_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRA_MINUTOS)
    datos = {
        "sub": str(usuario_id),   # "sub" = a quién pertenece el token
        "exp": expira,            # cuándo expira
    }
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITMO)


# Esquema de seguridad: le dice a FastAPI que espere un token tipo
# "Bearer" en las peticiones. También activa el botón "Authorize" en /docs.
security = HTTPBearer()


# ------------------------------------------------------------
# get_current_user(): dependencia que protege los endpoints.
# Lee el token, lo valida y devuelve el usuario dueño del token.
# Si el token es inválido, corta con un error 401 (no autorizado).
# Tus compañeros la usarán en recetas y calificaciones igual que aquí.
# ------------------------------------------------------------
def get_current_user(
    credenciales: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    token = credenciales.credentials   # el texto del token
    error_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado. Inicia sesión de nuevo.",
    )

    # Intentamos leer el token
    try:
        datos = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITMO])
        usuario_id = datos.get("sub")
    except Exception:
        raise error_401

    if usuario_id is None:
        raise error_401

    # Buscamos al usuario en la base de datos
    usuario = db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()
    if usuario is None:
        raise error_401

    return usuario
