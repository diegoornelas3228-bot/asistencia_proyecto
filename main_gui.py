import customtkinter as ctk
from tkinter import messagebox
from auth import verificar_login
# Importamos todas las funciones necesarias de la base de datos
from database import registrar_asistencia_db, obtener_historial_db, calcular_rendimiento_db

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Asistencia - UDG")
        self.geometry("400x500")

        # --- Interfaz de Login ---
        self.label_titulo = ctk.CTkLabel(self, text="Inicio de Sesión", font=("Arial", 20, "bold"))
        self.label_titulo.pack(pady=30)

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", width=250)
        self.entry_usuario.pack(pady=10)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250)
        self.entry_password.pack(pady=10)

        self.btn_login = ctk.CTkButton(self, text="Entrar", command=self.evento_login)
        self.btn_login.pack(pady=20)

    def evento_login(self):
        usuario = self.entry_usuario.get()
        pwd = self.entry_password.get()
        
        datos_usuario = verificar_login(usuario, pwd)

        if datos_usuario:
            self.abrir_panel_principal(datos_usuario[0]) 
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def abrir_panel_principal(self, id_usuario):
        """Crea el panel principal con estadísticas de asistencia."""
        self.withdraw()
        self.ventana_panel = ctk.CTkToplevel()
        self.ventana_panel.title("Panel Académico - UDG")
        self.ventana_panel.geometry("500x550")

        # --- SECCIÓN DE BIENVENIDA ---
        lbl = ctk.CTkLabel(self.ventana_panel, text="Panel de Control Escolar", font=("Arial", 20, "bold"))
        lbl.pack(pady=20)

        # --- SECCIÓN DE ESTADÍSTICAS ---
        porcentaje, total = calcular_rendimiento_db(id_usuario)
        
        # Color dinámico basado en reglas académicas
        color_estatus = "green" if porcentaje >= 80 else "orange"
        if porcentaje < 60: color_estatus = "red"

        self.lbl_stats = ctk.CTkLabel(
            self.ventana_panel, 
            text=f"Asistencias Registradas: {total} | Progreso: {porcentaje}%",
            font=("Arial", 14),
            text_color=color_estatus
        )
        self.lbl_stats.pack(pady=10)

        # Barra de progreso visual
        self.progreso = ctk.CTkProgressBar(self.ventana_panel, width=300)
        self.progreso.set(porcentaje / 100) 
        self.progreso.configure(progress_color=color_estatus)
        self.progreso.pack(pady=5)

        # --- BOTONES DE ACCIÓN ---
        self.btn_asistencia = ctk.CTkButton(
            self.ventana_panel, 
            text="MARCAR ENTRADA", 
            fg_color="green", 
            hover_color="darkgreen",
            command=lambda: self.marcar_asistencia(id_usuario)
        )
        self.btn_asistencia.pack(pady=20)

        self.btn_historial = ctk.CTkButton(
            self.ventana_panel,
            text="VER MI HISTORIAL",
            command=lambda: self.ver_historial(id_usuario)
        )
        self.btn_historial.pack(pady=10)

    def marcar_asistencia(self, id_usuario):
        """Registra la asistencia y notifica al usuario."""
        if registrar_asistencia_db(id_usuario):
            messagebox.showinfo("Éxito", "Asistencia registrada correctamente.")
            # Opcional: Podrías cerrar y abrir el panel para refrescar la barra, 
            # o dejarlo así para la entrega básica.
        else:
            messagebox.showerror("Error", "No se pudo conectar con la base de datos.")

    def ver_historial(self, id_usuario):
        """Ventana secundaria para ver registros pasados."""
        ventana_historial = ctk.CTkToplevel()
        ventana_historial.title("Mi Historial de Asistencia")
        ventana_historial.geometry("400x450")

        datos = obtener_historial_db(id_usuario)

        titulo = ctk.CTkLabel(ventana_historial, text="Últimos Registros", font=("Arial", 16, "bold"))
        titulo.pack(pady=10)

        txt_area = ctk.CTkTextbox(ventana_historial, width=350, height=300)
        txt_area.pack(pady=10)

        header = f"{'FECHA':<15} | {'HORA':<10} | {'ESTADO'}\n"
        separator = "-" * 40 + "\n"
        txt_area.insert("0.0", header + separator)

        if not datos:
            txt_area.insert("end", "\nNo hay registros todavía.")
        else:
            for fecha, hora, estado in datos:
                fila = f"{fecha:<15} | {hora:<10} | {estado}\n"
                txt_area.insert("end", fila)
        
        txt_area.configure(state="disabled") 

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()