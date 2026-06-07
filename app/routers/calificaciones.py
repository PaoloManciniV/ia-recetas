# ============================================================
#  routers/calificaciones.py  -->  Calificar recetas (1-5 estrellas)
# ============================================================
# Funcionalidad 5:
#   POST   /recetas/{id}/calificar  -> calificar una receta
#   GET    /recetas/{id}/calificacion -> ver mi calificación
#   PUT    /recetas/{id}/calificar  -> actualizar mi calificación
#
# Mismo patrón: Depends(get_current_user) protege todos los endpoints.
# Un usuario NO puede calificar la misma receta dos veces (constraint en BD).
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.receta import Receta
from app.models.calificacion import Calificacion
from app.models.usuario import Usuario
from app.schemas.calificacion import CalificacionCrear, CalificacionRespuesta
from app.auth import get_current_user

router = APIRouter(prefix="/recetas", tags=["Calificaciones"])


# ------------------------------------------------------------
# FUNCIONALIDAD 5: Calificar una receta
# ------------------------------------------------------------
@router.post("/{receta_id}/calificar", response_model=CalificacionRespuesta)
def calificar_receta(
    receta_id: int,
    datos: CalificacionCrear,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    # Verificamos que la receta exista y pertenezca al usuario
    receta = (
        db.query(Receta)
        .filter(Receta.id == receta_id, Receta.usuario_id == usuario.id)
        .first()
    )
    if receta is None:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    # ¿Ya calificó esta receta?
    ya_calificada = (
        db.query(Calificacion)
        .filter(
            Calificacion.receta_id == receta_id,
            Calificacion.usuario_id == usuario.id,
        )
        .first()
    )
    if ya_calificada:
        raise HTTPException(
            status_code=400,
            detail="Ya calificaste esta receta. Usa PUT para actualizarla.",
        )

    nueva = Calificacion(
        estrellas=datos.estrellas,
        receta_id=receta_id,
        usuario_id=usuario.id,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


# ------------------------------------------------------------
# FUNCIONALIDAD 5: Ver mi calificación de una receta
# ------------------------------------------------------------
@router.get("/{receta_id}/calificacion", response_model=CalificacionRespuesta)
def ver_calificacion(
    receta_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    calificacion = (
        db.query(Calificacion)
        .filter(
            Calificacion.receta_id == receta_id,
            Calificacion.usuario_id == usuario.id,
        )
        .first()
    )
    if calificacion is None:
        raise HTTPException(status_code=404, detail="Aún no has calificado esta receta")
    return calificacion


# ------------------------------------------------------------
# FUNCIONALIDAD 5: Actualizar mi calificación
# ------------------------------------------------------------
@router.put("/{receta_id}/calificar", response_model=CalificacionRespuesta)
def actualizar_calificacion(
    receta_id: int,
    datos: CalificacionCrear,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    calificacion = (
        db.query(Calificacion)
        .filter(
            Calificacion.receta_id == receta_id,
            Calificacion.usuario_id == usuario.id,
        )
        .first()
    )
    if calificacion is None:
        raise HTTPException(
            status_code=404,
            detail="No has calificado esta receta todavía. Usa POST primero.",
        )

    calificacion.estrellas = datos.estrellas
    db.commit()
    db.refresh(calificacion)
    return calificacion