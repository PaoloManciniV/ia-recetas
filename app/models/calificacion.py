# ============================================================
#  models/calificacion.py  -->  Tabla "calificaciones"
# ============================================================
# Guarda la calificación (1 a 5 estrellas) que un usuario
# le da a una receta generada. Una receta solo puede tener
# UNA calificación por usuario.
# ============================================================

from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.database import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id = Column(Integer, primary_key=True, index=True)

    # puntuación de 1 a 5 estrellas
    estrellas = Column(Integer, nullable=False)

    # a qué receta pertenece
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)

    # quién la calificó
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    # un usuario no puede calificar la misma receta dos veces
    __table_args__ = (
        UniqueConstraint("receta_id", "usuario_id", name="uq_calificacion_receta_usuario"),
    )