import sqlite3

def conectar():
    """Función auxiliar para conectar a la DB."""
    return sqlite3.connect("asistencia_sistema.db")

def verificar_login(usuario, password):
    """
    Verifica las credenciales en la tabla 'usuarios'.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Usamos 'password_hash' que es el nombre oficial en tu base de datos
        cursor.execute("SELECT id, username, rol FROM usuarios WHERE username = ? AND password_hash = ?", (usuario, password))
        
        resultado = cursor.fetchone() 
        conn.close()
        return resultado # Retorna (id, username, rol) o None
        
    except Exception as e:
        print(f"Error en la autenticación: {e}")
        return None

def registrar_usuario(username, password, rol="estudiante"):
    """
    Registra un nuevo usuario directamente desde la interfaz.
    """
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        # Insertamos usando la estructura limpia de la DB
        cursor.execute("INSERT INTO usuarios (username, password_hash, rol) VALUES (?, ?, ?)", 
                       (username, password, rol))
        
        conn.commit()
        conn.close()
        print(f"✅ Usuario '{username}' registrado con éxito en la base de datos.")
        return True
    except sqlite3.IntegrityError:
        print(f"❌ Error: El nombre de usuario '{username}' ya está ocupado.")
        return False
    except Exception as e:
        print(f"❌ Error al registrar usuario: {e}")
        return False