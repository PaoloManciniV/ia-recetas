# ============================================================
#  schemas/ingrediente.py  -->  "Formularios" de entrada y salida
# ============================================================
# Los "schemas" (con Pydantic) definen QUÉ datos entran y QUÉ datos
# salen de la API. Sirven para validar automáticamente:
#   - Si alguien manda un nombre que no es texto -> FastAPI lo rechaza.
#
# Es distinto al "modelo": el modelo es la tabla de la BD,
# el schema es lo que viaja por la API (JSON).
# ============================================================

from pydantic import BaseModel


# Campos comunes que comparten la entrada y la salida
class IngredienteBase(BaseModel):
    nombre: str
    cantidad: float = 1
    unidad: str = "unidad"


# Lo que el usuario ENVÍA para crear un ingrediente.
# (No incluye "id" porque la base de datos lo genera sola.)
class IngredienteCrear(IngredienteBase):
    pass


# Lo que la API DEVUELVE. Aquí sí incluimos el "id".
class IngredienteRespuesta(IngredienteBase):
    id: int

    class Config:
        # Permite convertir un objeto de la BD (modelo) en este schema.
        from_attributes = True
