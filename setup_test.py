from auth import registrar_usuario
from database import inicializar_db

# 1. Creamos la base de datos
inicializar_db()

# 2. Creamos un usuario para probar el login
if registrar_usuario("diego", "12345"):
    print("👤 Usuario 'diego' creado exitosamente.")
else:
    print("⚠️ El usuario ya existe.")