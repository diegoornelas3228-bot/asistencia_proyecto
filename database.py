import sqlite3

def conectar():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect("asistencia_sistema.db")

def inicializar_db():
    """Crea las tablas con la corrección de zona horaria para México."""
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
    
    # IMPORTANTE: Se añade 'localtime' para ajustar la hora a México/Jalisco
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            fecha DATE DEFAULT (DATE('now', 'localtime')),
            hora_entrada TIME DEFAULT (TIME('now', 'localtime')),
            estado TEXT DEFAULT 'Presente',
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')
    conexion.commit()
    conexion.close()
    print("✅ Base de datos inicializada con zona horaria local.")

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
        print(f"Error al registrar: {e}")
        return False

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
    """Calcula el porcentaje de asistencia (meta de 20 días)."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM asistencias WHERE usuario_id = ?", (usuario_id,))
        total = cursor.fetchone()[0]
        conn.close()
        
        meta = 20
        porcentaje = min(int((total / meta) * 100), 100)
        return porcentaje, total
    except:
        return 0, 0

def obtener_estadisticas_globales():
    """Consulta para la gráfica comparativa."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT u.username, COUNT(a.id) 
            FROM usuarios u
            LEFT JOIN asistencias a ON u.id = a.usuario_id
            GROUP BY u.id
        ''')
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print(f"Error en estadísticas: {e}")
        return []

if __name__ == "__main__":
    inicializar_db()