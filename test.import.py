from database import importar_alumnos_desde_excel

# Asegúrate de que el archivo 'lista_alumnos.xlsx' esté en la misma carpeta
if importar_alumnos_desde_excel("lista_alumnos.xlsx"):
    print("¡Éxito! Ahora puedes intentar loguearte con cualquiera de esos usuarios.")
else:
    print("Hubo un fallo en la importación.")