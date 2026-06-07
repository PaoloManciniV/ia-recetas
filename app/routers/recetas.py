# ============================================================
#  routers/recetas.py  -->  Generación, historial y eliminación
# ============================================================
# Funcionalidad 3: POST /recetas/generar  -> genera receta con LLM
# Funcionalidad 4: GET  /recetas/         -> historial de recetas
#                  GET  /recetas/{id}     -> ver una receta
# Funcionalidad 6: DELETE /recetas/{id}  -> eliminar del historial
#
# Mismo patrón que ingredientes.py: Depends(get_current_user)
# para que cada usuario solo vea y maneje SUS recetas.
# ============================================================

import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.receta import Receta
from app.models.calificacion import Calificacion
from app.models.ingrediente import Ingrediente
from app.models.usuario import Usuario
from app.schemas.receta import RecetaRespuesta, RecetaGenerada
from app.auth import get_current_user
from app.services.llm_service import generar_receta

router = APIRouter(prefix="/recetas", tags=["Recetas"])


# ------------------------------------------------------------
# Función auxiliar: añade el promedio de calificaciones a una receta
# ------------------------------------------------------------
def _con_promedio(receta: Receta, db: Session) -> RecetaRespuesta:
    promedio = (
        db.query(func.avg(Calificacion.estrellas))
        .filter(Calificacion.receta_id == receta.id)
        .scalar()
    )
    datos = RecetaRespuesta(
        id=receta.id,
        nombre=receta.nombre,
        contenido_json=receta.contenido_json,
        creado_en=receta.creado_en,
        calificacion_promedio=round(promedio, 1) if promedio else None,
    )
    return datos


# ------------------------------------------------------------
# FUNCIONALIDAD 3: Generar receta a partir del inventario
# ------------------------------------------------------------
@router.post("/generar", response_model=RecetaGenerada)
async def generar(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    # 1. Obtenemos los ingredientes del inventario del usuario
    ingredientes_db = (
        db.query(Ingrediente)
        .filter(Ingrediente.usuario_id == usuario.id)
        .all()
    )

    if not ingredientes_db:
        raise HTTPException(
            status_code=400,
            detail="Tu inventario está vacío. Agrega ingredientes primero.",
        )

    # Lista de nombres para el prompt: ["Tomate (3 unidad)", "Harina (500 g)", ...]
    nombres = [f"{i.nombre} ({i.cantidad} {i.unidad})" for i in ingredientes_db]

    # 2. Llamamos al LLM
    receta_dict = await generar_receta(nombres)

    # 3. Guardamos la receta en la base de datos
    nueva = Receta(
        nombre=receta_dict["nombre"],
        contenido_json=json.dumps(receta_dict, ensure_ascii=False),
        usuario_id=usuario.id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    # 4. Devolvemos el objeto estructurado al cliente
    return RecetaGenerada(**receta_dict)


# ------------------------------------------------------------
# FUNCIONALIDAD 4: Historial de recetas del usuario
# ------------------------------------------------------------
@router.get("/", response_model=list[RecetaRespuesta])
def listar_recetas(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    recetas = (
        db.query(Receta)
        .filter(Receta.usuario_id == usuario.id)
        .order_by(Receta.creado_en.desc())
        .all()
    )
    return [_con_promedio(r, db) for r in recetas]


# ------------------------------------------------------------
# FUNCIONALIDAD 4: Ver una receta específica
# ------------------------------------------------------------
@router.get("/{receta_id}", response_model=RecetaRespuesta)
def ver_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    receta = (
        db.query(Receta)
        .filter(Receta.id == receta_id, Receta.usuario_id == usuario.id)
        .first()
    )
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return _con_promedio(receta, db)


# ------------------------------------------------------------
# FUNCIONALIDAD 6: Eliminar receta del historial
# ------------------------------------------------------------
@router.delete("/{receta_id}")
def eliminar_receta(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    receta = (
        db.query(Receta)
        .filter(Receta.id == receta_id, Receta.usuario_id == usuario.id)
        .first()
    )
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    # Borramos también las calificaciones asociadas (integridad referencial)
    db.query(Calificacion).filter(Calificacion.receta_id == receta_id).delete()
    db.delete(receta)
    db.commit()
    return {"mensaje": "Receta eliminada correctamente"}