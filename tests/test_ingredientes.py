# ============================================================
#  tests/test_ingredientes.py  -->  Pruebas con pytest
# ============================================================
# La rúbrica pide mínimo 6 pruebas. Aquí dejo 6 funcionando que
# cubren: registro, login, validación de seguridad y el CRUD.
# El equipo puede sumar más (generación del prompt, parseo del LLM).
#
# Para correr las pruebas:   pytest
# ============================================================

import os
import random

# Usamos una base de datos de PRUEBA aparte para no tocar la real.
# Esto debe ir ANTES de importar la app.
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from app.main import app

cliente = TestClient(app)


# Función de ayuda: registra un usuario, inicia sesión y devuelve
# el encabezado con el token para las pruebas protegidas.
def crear_usuario_y_token():
    email = f"prueba{random.randint(1, 1000000)}@test.com"
    cliente.post("/usuarios/registro", json={"email": email, "password": "clave1234"})
    respuesta = cliente.post("/usuarios/login", json={"email": email, "password": "clave1234"})
    token = respuesta.json()["access_token"]
    return {"Authorization": "Bearer " + token}


# Prueba 1: la interfaz web (ruta "/") responde
def test_inicio_responde():
    respuesta = cliente.get("/")
    assert respuesta.status_code == 200


# Prueba 2: un usuario se puede registrar
def test_registro_usuario():
    email = f"nuevo{random.randint(1, 1000000)}@test.com"
    respuesta = cliente.post("/usuarios/registro", json={"email": email, "password": "clave1234"})
    assert respuesta.status_code == 200
    assert respuesta.json()["email"] == email


# Prueba 3: el login devuelve un token
def test_login_devuelve_token():
    encabezado = crear_usuario_y_token()
    assert "Authorization" in encabezado
    assert encabezado["Authorization"].startswith("Bearer ")


# Prueba 4: sin token, el CRUD de ingredientes está bloqueado
def test_ingredientes_requiere_login():
    respuesta = cliente.get("/ingredientes/")   # sin token
    assert respuesta.status_code in (401, 403)


# Prueba 5: con token, se puede CREAR un ingrediente
def test_crear_ingrediente():
    encabezado = crear_usuario_y_token()
    respuesta = cliente.post(
        "/ingredientes/",
        json={"nombre": "Tomate", "cantidad": 3, "unidad": "unidad"},
        headers=encabezado,
    )
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["nombre"] == "Tomate"
    assert "id" in datos


# Prueba 6: pedir un ingrediente que NO existe devuelve error 404
def test_ingrediente_no_existe():
    encabezado = crear_usuario_y_token()
    respuesta = cliente.get("/ingredientes/99999", headers=encabezado)
    assert respuesta.status_code == 404
