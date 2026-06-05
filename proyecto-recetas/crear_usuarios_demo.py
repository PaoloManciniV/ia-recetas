# ============================================================
#  crear_usuarios_demo.py  -->  Crea cuentas de prueba en la app
# ============================================================
# Script OPCIONAL. Sirve para tener cuentas listas el dia de la
# sustentacion sin tener que registrarlas a mano una por una.
#
# Crea 4 usuarios en la base de datos: Paolo, Maria, Roberto y Harley.
# Cada uno con la contrasena "demo1234" (cambienla si quieren).
#
# Como usarlo (con el servidor APAGADO):
#     python crear_usuarios_demo.py
# ============================================================

from app.database import SessionLocal, Base, engine
from app.models.usuario import Usuario
from app.auth import encriptar_password

# Nos aseguramos de que las tablas existan antes de insertar
Base.metadata.create_all(bind=engine)

# Lista de cuentas que vamos a crear: (correo, contrasena)
USUARIOS_DEMO = [
    ("paolo@recetas.com",   "demo1234"),
    ("maria@recetas.com",   "demo1234"),
    ("roberto@recetas.com", "demo1234"),
    ("harley@recetas.com",  "demo1234"),
]


def crear_usuarios():
    # Abrimos una sesion con la base de datos
    db = SessionLocal()
    try:
        for correo, password in USUARIOS_DEMO:
            # Si la cuenta ya existe, la saltamos (para no duplicar)
            ya_existe = db.query(Usuario).filter(Usuario.email == correo).first()
            if ya_existe:
                print(f"  - {correo}: ya existia, se omite")
                continue

            # Creamos el usuario con la contrasena encriptada
            usuario = Usuario(
                email=correo,
                hashed_password=encriptar_password(password),
            )
            db.add(usuario)
            print(f"  + {correo}: creado")

        db.commit()   # guardamos todos los cambios de una vez
        print("Listo. Cuentas de demostracion creadas.")
    finally:
        db.close()    # cerramos la sesion siempre


# Esto hace que el script solo corra cuando lo ejecutas directamente
if __name__ == "__main__":
    crear_usuarios()
