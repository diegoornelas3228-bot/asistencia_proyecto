import sqlite3

def conectar():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect("asistencia_sistema.db")

def inicializar_db():
    """Crea las tablas necesarias para el proyecto."""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT DEFAULT 'estudiante'
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            fecha DATE DEFAULT (DATE('now')),
            hora_entrada TIME DEFAULT (TIME('now')),
            estado TEXT DEFAULT 'Presente',
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conexion.commit()
    conexion.close()

def registrar_asistencia_db(usuario_id):
    """Inserta un registro de asistencia."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO asistencias (usuario_id) VALUES (?)", (usuario_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- ESTAS SON LAS FUNCIONES QUE FALTABAN ---

def obtener_historial_db(usuario_id):
    """Recupera las asistencias de un usuario específico."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT fecha, hora_entrada, estado FROM asistencias WHERE usuario_id = ?", (usuario_id,))
        datos = cursor.fetchall()
        conn.close()
        return datos
    except:
        return []

def calcular_rendimiento_db(usuario_id):
    """Calcula el porcentaje de asistencia (basado en un ideal de 20 clases)."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM asistencias WHERE usuario_id = ?", (usuario_id,))
        total = cursor.fetchone()[0]
        conn.close()
        
        meta = 20  # Suponemos 20 días de clase
        porcentaje = min(int((total / meta) * 100), 100)
        return porcentaje, total
    except:
        return 0, 0

if __name__ == "__main__":
    inicializar_db()