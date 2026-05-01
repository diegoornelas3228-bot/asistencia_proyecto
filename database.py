import sqlite3
import pandas as pd

def conectar():
    """Establece conexión con la base de datos SQLite."""
    return sqlite3.connect("asistencia_sistema.db")

def inicializar_db():
    """Crea las tablas necesarias para el proyecto."""
    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla 1: Usuarios (Estructura para alumnos y profesores)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT DEFAULT 'estudiante'
        )
    ''')

    # Tabla 2: Asistencias (Registro de eventos con fecha y hora automática)
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
    print("✅ Base de datos e infraestructura inicializadas.")

def registrar_asistencia_db(usuario_id):
    """Inserta un registro de asistencia con fecha y hora actual."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO asistencias (usuario_id) VALUES (?)", (usuario_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return False

def obtener_historial_db(usuario_id):
    """Obtiene los últimos 10 registros de asistencia del usuario."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT fecha, hora_entrada, estado 
            FROM asistencias 
            WHERE usuario_id = ? 
            ORDER BY id DESC LIMIT 10
        ''', (usuario_id,))
        
        registros = cursor.fetchall()
        conn.close()
        return registros
    except Exception as e:
        print(f"Error al consultar historial: {e}")
        return []

def calcular_rendimiento_db(usuario_id, total_clases_semestre=30):
    """Calcula el porcentaje de asistencia basado en un total de clases."""
    try:
        conn = conectar()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM asistencias WHERE usuario_id = ?", (usuario_id,))
        total_asistencias = cursor.fetchone()[0]
        conn.close()

        porcentaje = (total_asistencias / total_clases_semestre) * 100
        return round(porcentaje, 2), total_asistencias
    except Exception as e:
        print(f"Error al calcular porcentaje: {e}")
        return 0, 0
    
def importar_alumnos_desde_excel(ruta_archivo):
    """Lee un Excel y registra a los alumnos filtrando solo las columnas necesarias."""
    try:
        # 1. Leer el archivo Excel
        df = pd.read_excel(ruta_archivo)
        
        # 2. Filtrar columnas para que coincidan exactamente con la tabla 'usuarios'
        # Esto ignora cualquier otra columna que el profesor tenga en su Excel
        columnas_necesarias = ['username', 'password_hash', 'rol']
        
        # Verificamos que las columnas existan en el Excel
        if not all(col in df.columns for col in columnas_necesarias):
            print("❌ El Excel no tiene los encabezados correctos (username, password_hash, rol).")
            return False

        df_filtrado = df[columnas_necesarias]
        
        # 3. Conectar e insertar
        conn = conectar()
        df_filtrado.to_sql('usuarios', conn, if_exists='append', index=False)
        conn.close()
        
        print(f"✅ Se han importado {len(df_filtrado)} alumnos correctamente.")
        return True
    except Exception as e:
        print(f"❌ Error al importar desde Excel: {e}")
        return False

# Bloque principal para configurar todo
if __name__ == "__main__":
    inicializar_db()
    importar_alumnos_desde_excel("lista_alumnos.xlsx") 
    # Para probar la importación por primera vez, puedes descomentar la línea de abajo:
    # importar_alumnos_desde_excel("lista_alumnos.xlsx")