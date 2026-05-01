import sqlite3

def verificar_login(usuario, password):
    """
    Verifica las credenciales comparando el texto plano del Excel 
    con lo que el usuario escribe en la interfaz.
    """
    try:
        conn = sqlite3.connect("asistencia_sistema.db")
        cursor = conn.cursor()
        
        # Buscamos al usuario que coincida con el nombre Y la contraseña exacta
        cursor.execute("SELECT id, rol FROM usuarios WHERE username = ? AND password_hash = ?", (usuario, password))
        
        resultado = cursor.fetchone() 
        conn.close()
        return resultado
        
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return None