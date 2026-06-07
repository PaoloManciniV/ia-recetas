# ============================================================
#  models/receta.py  -->  Tabla "recetas"
# ============================================================
# Guarda cada receta generada por el LLM para un usuario.
# La receta se almacena como JSON en un campo de texto.
# ============================================================

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)

    # nombre del plato, ej: "Tortilla de patatas"
    nombre = Column(String(200), nullable=False)

    # respuesta completa del LLM guardada como JSON string
    contenido_json = Column(Text, nullable=False)

    # fecha y hora en que se generó (se llena sola)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # a qué usuario pertenece esta receta
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)