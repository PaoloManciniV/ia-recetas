# ============================================================
#  models/ingrediente.py  -->  Tabla "ingredientes"
# ============================================================
# Un "modelo" es una clase de Python que representa una TABLA de
# la base de datos. Cada ingrediente pertenece a UN usuario
# (su inventario personal).
# ============================================================

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Ingrediente(Base):
    __tablename__ = "ingredientes"

    # id único de cada ingrediente (1, 2, 3, ...). Se genera solo.
    id = Column(Integer, primary_key=True, index=True)

    # nombre del ingrediente, ej: "Tomate". Obligatorio.
    nombre = Column(String(100), nullable=False)

    # cantidad disponible, ej: 3. Por defecto 1.
    cantidad = Column(Float, default=1)

    # unidad de medida, ej: "kg", "unidad". Por defecto "unidad".
    unidad = Column(String(30), default="unidad")

    # usuario_id: a qué usuario pertenece este ingrediente.
    # ForeignKey("usuarios.id") lo conecta con la tabla usuarios.
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
