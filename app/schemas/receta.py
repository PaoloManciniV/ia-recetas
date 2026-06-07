# ============================================================
#  schemas/receta.py  -->  Datos de entrada/salida de recetas
# ============================================================

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Lo que la API devuelve al listar o ver una receta
class RecetaRespuesta(BaseModel):
    id: int
    nombre: str
    contenido_json: str
    creado_en: datetime
    calificacion_promedio: Optional[float] = None  # se calcula al vuelo

    class Config:
        from_attributes = True


# Lo que devuelve la generación: el JSON estructurado del LLM
class RecetaGenerada(BaseModel):
    nombre: str
    ingredientes: list[str]
    pasos: list[str]
    tiempo_minutos: int
    dificultad: str   # "fácil", "media" o "difícil"