import sqlite3

conn = sqlite3.connect("asistencia_sistema.db")
cursor = conn.cursor()

# Consultamos los últimos 5 usuarios registrados
cursor.execute("SELECT id, username, rol FROM usuarios ORDER BY id DESC LIMIT 5")
usuarios = cursor.fetchall()

print("--- ÚLTIMOS USUARIOS EN LA BASE DE DATOS ---")
for u in usuarios:
    print(f"ID: {u[0]} | Usuario: {u[1]} | Rol: {u[2]}")

conn.close()