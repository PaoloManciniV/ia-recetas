# ============================================================
#  models/usuario.py  -->  Tabla "usuarios"
# ============================================================
# Guarda las cuentas de los usuarios. Ojo: la contraseña NO se
# guarda tal cual, se guarda encriptada (hashed_password).
# ============================================================

from sqlalchemy import Column, Integer, String
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    # email: debe ser único (no puede haber dos cuentas con el mismo correo)
    email = Column(String(120), unique=True, index=True, nullable=False)

    # contraseña encriptada (nunca la original)
    hashed_password = Column(String(255), nullable=False)
