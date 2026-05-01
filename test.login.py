import sqlite3

def revisar_usuarios():
    conn = sqlite3.connect("asistencia_sistema.db")
    cursor = conn.cursor()
    
    # Esto nos dirá qué usuarios hay realmente grabados
    cursor.execute("SELECT username, password_hash FROM usuarios")
    usuarios = cursor.fetchall()
    
    print("--- Usuarios encontrados en la DB ---")
    for user in usuarios:
        print(f"Usuario: '{user[0]}' | Contraseña: '{user[1]}'")
    
    conn.close()

if __name__ == "__main__":
    revisar_usuarios()