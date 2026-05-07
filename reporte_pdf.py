import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from database import obtener_historial_db

def generar_pdf(usuario_id):
    """Genera un PDF y lo guarda automáticamente en la carpeta de Descargas."""
    try:
        # 1. Detectar la ruta de la carpeta "Downloads" de tu usuario
        ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # 2. Definir el nombre del archivo dentro de esa carpeta
        nombre_archivo = os.path.join(ruta_descargas, f"Reporte_Asistencia_Usuario_{usuario_id}.pdf")

        # 3. Crear el PDF
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        c.setTitle(f"Reporte de Asistencia - Usuario {usuario_id}")
        
        # Estilo del Encabezado
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, f"SISTEMA DE ASISTENCIA - UDG")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Reporte del Usuario ID: {usuario_id}")
        c.line(100, 720, 500, 720)

        # Dibujar historial
        datos = obtener_historial_db(usuario_id)
        y = 690
        c.setFont("Helvetica-Bold", 11)
        c.drawString(100, y, f"{'FECHA':<15} | {'HORA':<15} | {'ESTADO'}")
        y -= 20
        c.setFont("Helvetica", 10)

        for fecha, hora, estado in datos:
            if y < 50: # Crear nueva página si se llena
                c.showPage()
                y = 750
            c.drawString(100, y, f"{fecha:<15} | {hora:<15} | {estado}")
            y -= 15

        c.save()
        print(f"✅ Reporte guardado con éxito en: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return False