import customtkinter as ctk
import reporte_pdf
from tkinter import messagebox
import matplotlib.pyplot as plt
from auth import verificar_login, registrar_usuario 
from database import (registrar_asistencia_db, obtener_historial_db, 
                      calcular_rendimiento_db, obtener_estadisticas_globales)

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Asistencia - UDG")
        self.centrar_ventana(self, 400, 550)

        # --- Interfaz de Login ---
        self.label_titulo = ctk.CTkLabel(self, text="Inicio de Sesión", font=("Arial", 22, "bold"))
        self.label_titulo.pack(pady=(40, 20))

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", width=280, height=35)
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=280, height=35)
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="ENTRAR", font=("Arial", 14, "bold"), 
                                       width=280, height=40, command=self.evento_login)
        self.btn_login.pack(pady=20)

        self.btn_registro_vista = ctk.CTkButton(
            self, text="¿No tienes cuenta? Regístrate", 
            fg_color="transparent", command=self.abrir_registro
        )
        self.btn_registro_vista.pack(pady=10)

    def centrar_ventana(self, ventana, ancho, alto):
        ventana.update_idletasks()
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def abrir_registro(self):
        ventana_reg = ctk.CTkToplevel(self)
        ventana_reg.title("Nuevo Registro")
        self.centrar_ventana(ventana_reg, 350, 450)
        
        ventana_reg.after(100, lambda: ventana_reg.focus_force()) 

        ctk.CTkLabel(ventana_reg, text="Crear Cuenta", font=("Arial", 18, "bold")).pack(pady=20)
        reg_user = ctk.CTkEntry(ventana_reg, placeholder_text="Nuevo Usuario", width=220)
        reg_user.pack(pady=10)
        reg_pass = ctk.CTkEntry(ventana_reg, placeholder_text="Contraseña", show="*", width=220)
        reg_pass.pack(pady=10)

        def ejecutar_registro():
            u, p = reg_user.get(), reg_pass.get()
            if u and p:
                if registrar_usuario(u, p):
                    messagebox.showinfo("Éxito", f"Usuario {u} creado correctamente.")
                    ventana_reg.destroy()
                else:
                    messagebox.showerror("Error", "El nombre de usuario ya existe.")
            else:
                messagebox.showwarning("Atención", "Por favor llena ambos campos.")

        ctk.CTkButton(ventana_reg, text="CONFIRMAR", width=220, command=ejecutar_registro).pack(pady=30)

    def evento_login(self):
        usuario, pwd = self.entry_usuario.get(), self.entry_password.get()
        datos_usuario = verificar_login(usuario, pwd)
        if datos_usuario:
            self.abrir_panel_principal(datos_usuario[0]) 
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_panel_principal(self, id_usuario):
        self.withdraw()
        self.ventana_panel = ctk.CTkToplevel()
        self.ventana_panel.title("Panel Académico - UDG")
        self.centrar_ventana(self.ventana_panel, 500, 700)
        
        self.ventana_panel.after(100, lambda: self.ventana_panel.focus_force())

        ctk.CTkLabel(self.ventana_panel, text="Panel de Control Escolar", font=("Arial", 22, "bold")).pack(pady=20)

        porcentaje, total = calcular_rendimiento_db(id_usuario)
        color_estatus = "green" if porcentaje >= 80 else "orange"
        if porcentaje < 60: color_estatus = "red"

        self.lbl_stats = ctk.CTkLabel(self.ventana_panel, text=f"Asistencias: {total} | Progreso: {porcentaje}%",
                                      font=("Arial", 16), text_color=color_estatus)
        self.lbl_stats.pack(pady=10)

        self.progreso = ctk.CTkProgressBar(self.ventana_panel, width=350, height=15)
        self.progreso.set(porcentaje / 100) 
        self.progreso.configure(progress_color=color_estatus)
        self.progreso.pack(pady=10)

        ctk.CTkButton(self.ventana_panel, text="MARCAR ENTRADA", fg_color="#27ae60",
                      width=300, height=45, command=lambda: self.marcar_asistencia(id_usuario)).pack(pady=20)
        
        ctk.CTkButton(self.ventana_panel, text="VER MI HISTORIAL", width=300,
                      command=lambda: self.ver_historial(id_usuario)).pack(pady=10)

        ctk.CTkButton(self.ventana_panel, text="VER ESTADÍSTICAS GLOBALES", fg_color="#2c3e50", width=300,
                      command=self.mostrar_grafica_global).pack(pady=10)

        # CORRECCIÓN AQUÍ: Se agregó 'lambda: ... (id_usuario)' para evitar el TypeError
        ctk.CTkButton(self.ventana_panel, text="DESCARGAR REPORTE PDF", fg_color="#A30000",
                      width=300, command=lambda: reporte_pdf.generar_pdf(id_usuario)).pack(pady=25)

    def marcar_asistencia(self, id_usuario):
        if registrar_asistencia_db(id_usuario):
            messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")
            # Opcional: refrescar las estadísticas tras marcar entrada
            porcentaje, total = calcular_rendimiento_db(id_usuario)
            color = "green" if porcentaje >= 80 else "orange"
            if porcentaje < 60: color = "red"
            self.lbl_stats.configure(text=f"Asistencias: {total} | Progreso: {porcentaje}%", text_color=color)
            self.progreso.set(porcentaje / 100)
            self.progreso.configure(progress_color=color)
        else:
            messagebox.showerror("Error", "No se pudo registrar.")

    def ver_historial(self, id_usuario):
        ventana_historial = ctk.CTkToplevel()
        ventana_historial.title("Mi Historial")
        self.centrar_ventana(ventana_historial, 450, 500)
        
        ventana_historial.after(100, lambda: ventana_historial.focus_force())

        datos = obtener_historial_db(id_usuario)
        txt_area = ctk.CTkTextbox(ventana_historial, width=400, height=350)
        txt_area.pack(pady=20)

        txt_area.insert("0.0", f"{'FECHA':<15} | {'HORA':<10} | {'ESTADO'}\n" + "-"*45 + "\n")
        for fecha, hora, estado in datos:
            txt_area.insert("end", f"{fecha:<15} | {hora:<10} | {estado}\n")
        txt_area.configure(state="disabled")

    def mostrar_grafica_global(self):
        datos = obtener_estadisticas_globales()
        if not datos:
            messagebox.showinfo("Info", "No hay datos para graficar.")
            return

        nombres = [d[0] for d in datos]
        totales = [d[1] for d in datos]

        plt.figure(num='Estadísticas del Sistema', figsize=(8, 5))
        plt.bar(nombres, totales, color='#3498db')
        plt.title('Asistencias Totales por Alumno')
        plt.xlabel('Estudiantes')
        plt.ylabel('Cantidad de Asistencias')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()