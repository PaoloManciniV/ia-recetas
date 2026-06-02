# ============================================================
#  database.py  -->  Configuración de la base de datos
# ============================================================
# Aquí creamos la "conexión" a la base de datos usando SQLAlchemy.
# SQLAlchemy es una librería que nos deja trabajar con tablas de la
# base de datos como si fueran clases de Python (más fácil que escribir SQL).
# ============================================================

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ------------------------------------------------------------
# DATABASE_URL: la dirección de la base de datos.
#
# Se lee desde el archivo .env (variables de entorno).
# Si no existe, usamos SQLite por defecto: un simple archivo
# llamado "recetas.db" que se crea solo. Así el proyecto FUNCIONA
# de una vez sin tener que instalar MySQL en tu computador.
#
# Cuando el equipo lo despliegue con Docker + MySQL, solo cambian
# esta variable en el .env (ya dejé el ejemplo en .env.example).
# ------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./recetas.db")

# SQLite necesita este parámetro extra para funcionar con FastAPI.
# MySQL/PostgreSQL NO lo necesitan, por eso lo ponemos condicional.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# El "engine" es el motor que se conecta a la base de datos.
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# SessionLocal: una "fábrica" de sesiones. Cada vez que entra una
# petición a la API, abrimos una sesión para hablar con la BD.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: clase de la que heredan TODOS nuestros modelos (las tablas).
Base = declarative_base()


# ------------------------------------------------------------
# get_db(): función que entrega una sesión de base de datos y se
# asegura de cerrarla al terminar. FastAPI la usa con "Depends".
# Tus compañeros van a reutilizar esto en todos los routers.
# ------------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db        # entrega la sesión al endpoint
    finally:
        db.close()      # la cierra cuando el endpoint termina
