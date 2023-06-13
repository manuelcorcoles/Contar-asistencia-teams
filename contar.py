import os
import pandas as pd
from collections import defaultdict

directorio = "/home/manu/Contar-asistencia-teams"  # Reemplaza con la ruta correcta

alumnos = defaultdict(int)  # Diccionario para contar la asistencia de cada alumno

# Recorre todos los archivos CSV en el directorio
for archivo in os.listdir(directorio):
    if archivo.endswith(".csv"):
        ruta_archivo = os.path.join(directorio, archivo)

        try:
            # Leer el archivo CSV y extraer los datos relevantes
            df = pd.read_csv(ruta_archivo, encoding='utf-16', delimiter='\t', skiprows=7)
            
            # Verificar si el archivo contiene la columna "Full Name"
            if "Full Name" in df.columns:
                asistencia_alumnos = df["Full Name"].value_counts().to_dict()
                
                # Actualizar el recuento de asistencia de cada alumno
                for alumno, count in asistencia_alumnos.items():
                    alumnos[alumno] += count
            else:
                print(f"El archivo no contiene la columna 'Full Name': {ruta_archivo}")
        except Exception as e:
            print(f"Error al procesar el archivo: {ruta_archivo}")
            print(f"Detalle del error: {str(e)}")

# Imprimir el recuento de asistencia para cada alumno
for alumno, count in alumnos.items():
    print(f"{alumno}: {count}")
