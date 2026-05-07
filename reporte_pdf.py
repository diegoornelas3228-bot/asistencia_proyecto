from fpdf import FPDF
import sqlite3
from datetime import datetime
from tkinter import messagebox

class ReporteAsistencia(FPDF):
    def header(self):
        # Título principal del reporte 
        self.set_font('Helvetica', 'B', 16)
        self.cell(0, 10, 'UNIVERSIDAD DE GUADALAJARA', 0, 1, 'C')
        self.set_font('Helvetica', 'B', 12)
        self.cell(0, 10, 'Sistema de Gestión de Asistencia - Reporte General', 0, 1, 'C')
        
        # Fecha de generación 
        self.set_font('Helvetica', 'I', 10)
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Generado el: {fecha_actual}', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        # Pie de página con numeración 
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generar_pdf():
    try:
        pdf = ReporteAsistencia()
        pdf.add_page()
        
        # Estilo de encabezados de tabla 
        pdf.set_fill_color(200, 220, 255) # Azul claro para el encabezado
        pdf.set_font('Helvetica', 'B', 12)
        
        pdf.cell(30, 10, 'ID User', 1, 0, 'C', True)
        pdf.cell(60, 10, 'Fecha', 1, 0, 'C', True)
        pdf.cell(50, 10, 'Hora', 1, 0, 'C', True)
        pdf.cell(50, 10, 'Estado', 1, 1, 'C', True)

        # Conexión a la base de datos
        conn = sqlite3.connect('asistencia_sistema.db')
        cursor = conn.cursor()
        
        # CORRECCIÓN DE COLUMNAS: 
        # Seleccionamos usuario_id, fecha, hora_entrada y estado de la tabla 'asistencias'
        cursor.execute("SELECT usuario_id, fecha, hora_entrada, estado FROM asistencias")
        registros = cursor.fetchall()

        pdf.set_font('Helvetica', '', 12)
        for fila in registros:
            pdf.cell(30, 10, str(fila[0]), 1, 0, 'C') # id
            pdf.cell(60, 10, str(fila[1]), 1, 0, 'C') # fecha
            pdf.cell(50, 10, str(fila[2]), 1, 0, 'C') # hora
            pdf.cell(50, 10, str(fila[3]), 1, 1, 'C') # estado

        conn.close()
        
        nombre_archivo = "reporte_asistencia.pdf"
        pdf.output(nombre_archivo)
        
        messagebox.showinfo("Reporte Listo", f"El archivo '{nombre_archivo}' ha sido generado con éxito.")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

if __name__ == "__main__":
    generar_pdf()