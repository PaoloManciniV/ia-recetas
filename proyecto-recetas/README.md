# Generador de Recetas con Inventario

Proyecto final de Tecnologias Web. Aplicacion web que permite registrar los
ingredientes que tienes en casa y, a partir de ese inventario, generar recetas
con un modelo de lenguaje (LLM).

Este repositorio contiene la BASE del proyecto: ya trae el registro e inicio de
sesion de usuarios (funcionalidad 1), el CRUD de ingredientes (funcionalidad 2)
y una interfaz web. Las demas funcionalidades las completa el equipo (ver la
seccion "Pendientes").

---

## Como correr el proyecto (local)

No necesitas instalar MySQL ni XAMPP: por defecto usa SQLite (un archivo) que
se crea solo.

    # 1. (Opcional) crear un entorno virtual
    python -m venv venv
    venv\Scripts\activate           # En Mac/Linux:  source venv/bin/activate

    # 2. Instalar las dependencias
    pip install -r requirements.txt

    # 3. Copiar el archivo de variables de entorno
    copy .env.example .env          # En Mac/Linux:  cp .env.example .env

    # 4. Arrancar el servidor
    python -m uvicorn app.main:app --reload

Luego abre en el navegador:

- http://localhost:8000        -> la interfaz web (registrarse, iniciar sesion
  y administrar la despensa).
- http://localhost:8000/docs   -> documentacion automatica de la API (Swagger),
  para probar los endpoints directamente.

En /docs, para probar los endpoints protegidos: inicia sesion con
POST /usuarios/login, copia el access_token y pegalo en el boton "Authorize"
(arriba a la derecha).

---

## Como correr las pruebas

    pytest

Hay 6 pruebas que cubren registro, login, seguridad y el CRUD de ingredientes.

---

## Estructura del proyecto

    proyecto-recetas/
    |-- app/
    |   |-- main.py              # arranque + sirve la web y el favicon
    |   |-- database.py          # conexion a la base de datos
    |   |-- auth.py              # contrasenas y tokens JWT (login)
    |   |-- models/
    |   |   |-- usuario.py       # tabla "usuarios"
    |   |   |-- ingrediente.py   # tabla "ingredientes" (ligada al usuario)
    |   |-- routers/
    |   |   |-- usuarios.py      # registro e inicio de sesion
    |   |   |-- ingredientes.py  # CRUD de ingredientes (protegido)
    |   |-- schemas/
    |   |   |-- usuario.py
    |   |   |-- ingrediente.py
    |   |-- services/            # aqui ira llm_service.py (pendiente)
    |-- tests/
    |   |-- test_ingredientes.py # 6 pruebas
    |-- static/
    |   |-- index.html           # la interfaz web (la "cara" de la app)
    |   |-- favicon.ico          # icono de la pestana
    |-- crear_usuarios_demo.py   # script opcional: crea cuentas de prueba
    |-- .env.example
    |-- .gitignore
    |-- pytest.ini
    |-- requirements.txt
    |-- README.md

---

## Lo que YA esta hecho

- Estructura completa del proyecto
- Conexion a base de datos (SQLite local; MySQL listo para Docker)
- Funcionalidad 1: Registro e inicio de sesion con JWT (tabla usuarios)
- Funcionalidad 2: CRUD de ingredientes (ligado a cada usuario = inventario personal)
- Interfaz web con login, registro y administracion de la despensa
- Favicon visible
- 6 pruebas unitarias con pytest
- .env.example y .gitignore (protege las claves)

## Pendientes (para el equipo)

- Funcionalidad 3: Servicio LLM en app/services/llm_service.py + endpoint para
  generar una receta a partir del inventario (devolver JSON: nombre del plato,
  ingredientes, pasos, tiempo y dificultad). Crear tabla recetas.
- Funcionalidad 4: Ver recetas generadas (historial)
- Funcionalidad 5: Calificar receta (1 a 5 estrellas). Crear tabla calificaciones.
- Funcionalidad 6: Eliminar recetas del historial
- Agregar a la interfaz un boton "Generar receta" y mostrar las recetas
- Mas pruebas (generacion del prompt, parseo de la respuesta del LLM)
- Docker + Docker Compose (app + base de datos MySQL en contenedores)
- Despliegue en VPS con dominio y certificado SSL (HTTPS)
- Documento PDF (max 3 paginas): arquitectura, diagrama ER y capturas

Para recetas y calificaciones, copien el patron de ingredientes.py: el modelo,
el schema, el router con Depends(get_current_user) y registrarlo en main.py.
Es la misma receta.

---

## Equipo

La nota es individual y cada integrante debe tener minimo 10 commits con
mensajes descriptivos.

- Paolo Mancini   - (parte que hizo)
- Maria           - (parte que hizo)
- Roberto         - (parte que hizo)
- Harley          - (parte que hizo)
