# ============================================================
#  main.py  -->  El corazón de la aplicación (punto de arranque)
# ============================================================
# Aquí:
#   1. Creamos la app de FastAPI
#   2. Creamos las tablas en la base de datos
#   3. Conectamos los routers (usuarios e ingredientes)
#   4. Servimos la interfaz web (la página bonita) y el favicon
#
# Para correrlo:   python -m uvicorn app.main:app --reload
#   - Interfaz web:        http://localhost:8000
#   - Documentación API:   http://localhost:8000/docs
# ============================================================

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine

# Importamos los modelos para que SQLAlchemy "conozca" todas las tablas
# antes de crearlas. (usuarios e ingredientes)
from app.models import usuario, ingrediente  # noqa: F401
from app.routers import ingredientes, usuarios

# Crea las tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Generador de Recetas con Inventario",
    description="API del proyecto final de Tecnologías Web",
    version="0.2.0",
)

# Conectamos los routers (los endpoints de la API)
app.include_router(usuarios.router)
app.include_router(ingredientes.router)

# Servimos la carpeta /static (para el favicon y archivos de la web)
app.mount("/static", StaticFiles(directory="static"), name="static")


# ------------------------------------------------------------
# Página principal: la interfaz web (HTML bonito).
# Al entrar a http://localhost:8000 se abre esta página.
# ------------------------------------------------------------
@app.get("/")
def inicio():
    return FileResponse("static/index.html")


# ------------------------------------------------------------
# Favicon: el iconito de la pestaña del navegador.
# ------------------------------------------------------------
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("static/favicon.ico")
