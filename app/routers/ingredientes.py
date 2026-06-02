# ============================================================
#  routers/ingredientes.py  -->  CRUD de ingredientes (protegido)
# ============================================================
# Las 5 operaciones del CRUD. AHORA todas piden iniciar sesión:
# cada usuario solo ve y maneja SUS propios ingredientes.
#
# El truco está en este parámetro que se repite en cada endpoint:
#     usuario: Usuario = Depends(get_current_user)
# Eso obliga a mandar un token válido y nos dice quién es el usuario.
#
# Este archivo es el EJEMPLO que el equipo copia para recetas y
# calificaciones. ¡Mismo patrón!
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ingrediente import Ingrediente
from app.models.usuario import Usuario
from app.schemas.ingrediente import IngredienteCrear, IngredienteRespuesta
from app.auth import get_current_user

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])


# ------------------------------------------------------------
# CREAR (CREATE)
# ------------------------------------------------------------
@router.post("/", response_model=IngredienteRespuesta)
def crear_ingrediente(
    datos: IngredienteCrear,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    nuevo = Ingrediente(
        nombre=datos.nombre,
        cantidad=datos.cantidad,
        unidad=datos.unidad,
        usuario_id=usuario.id,   # lo guardamos a nombre del usuario logueado
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# ------------------------------------------------------------
# LISTAR TODOS (READ) -> solo los del usuario logueado
# ------------------------------------------------------------
@router.get("/", response_model=list[IngredienteRespuesta])
def listar_ingredientes(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    return db.query(Ingrediente).filter(Ingrediente.usuario_id == usuario.id).all()


# ------------------------------------------------------------
# VER UNO (READ por id)
# ------------------------------------------------------------
@router.get("/{ingrediente_id}", response_model=IngredienteRespuesta)
def ver_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    ingrediente = (
        db.query(Ingrediente)
        .filter(Ingrediente.id == ingrediente_id, Ingrediente.usuario_id == usuario.id)
        .first()
    )
    if ingrediente is None:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente


# ------------------------------------------------------------
# ACTUALIZAR (UPDATE)
# ------------------------------------------------------------
@router.put("/{ingrediente_id}", response_model=IngredienteRespuesta)
def actualizar_ingrediente(
    ingrediente_id: int,
    datos: IngredienteCrear,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    ingrediente = (
        db.query(Ingrediente)
        .filter(Ingrediente.id == ingrediente_id, Ingrediente.usuario_id == usuario.id)
        .first()
    )
    if ingrediente is None:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")

    ingrediente.nombre = datos.nombre
    ingrediente.cantidad = datos.cantidad
    ingrediente.unidad = datos.unidad

    db.commit()
    db.refresh(ingrediente)
    return ingrediente


# ------------------------------------------------------------
# BORRAR (DELETE)
# ------------------------------------------------------------
@router.delete("/{ingrediente_id}")
def borrar_ingrediente(
    ingrediente_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    ingrediente = (
        db.query(Ingrediente)
        .filter(Ingrediente.id == ingrediente_id, Ingrediente.usuario_id == usuario.id)
        .first()
    )
    if ingrediente is None:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")

    db.delete(ingrediente)
    db.commit()
    return {"mensaje": "Ingrediente eliminado correctamente"}
