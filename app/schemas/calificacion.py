# ============================================================
#  schemas/calificacion.py  -->  Datos de entrada/salida de calificaciones
# ============================================================

from pydantic import BaseModel, Field


# Lo que el usuario envía para calificar una receta
class CalificacionCrear(BaseModel):
    estrellas: int = Field(..., ge=1, le=5, description="Puntuación de 1 a 5 estrellas")


# Lo que la API devuelve
class CalificacionRespuesta(BaseModel):
    id: int
    estrellas: int
    receta_id: int
    usuario_id: int

    class Config:
        from_attributes = True