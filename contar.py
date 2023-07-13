import os
import pandas as pd
from datetime import datetime, timedelta

# Ruta de la carpeta que contiene los archivos CSV
carpeta = '/home/manu/Contar-asistencia-teams/csv/csv_miercoles'

# Crear un diccionario para almacenar el recuento de cada persona
recuento_personas_tiempo = {}
recuento_personas_total = {}

# Contador de Excels recorridos
excels_recorridos = 0

# Recorrer todos los archivos en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.csv'):  # Asegurarse de que solo se procesen archivos CSV
        ruta_archivo = os.path.join(carpeta, archivo)
        
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(ruta_archivo)
        
        # Incrementar el contador de Excels recorridos
        excels_recorridos += 1
        
        # Verificar la existencia de las columnas necesarias
        if 'ParticipantDisplayName' in df.columns and 'SessionStartTime' in df.columns and 'SessionEndTime' in df.columns:
            # Convertir las columnas de fecha y hora a objetos datetime
            df['SessionStartTime'] = pd.to_datetime(df['SessionStartTime'])
            df['SessionEndTime'] = pd.to_datetime(df['SessionEndTime'])
            
            # Calcular la duración de cada sesión
            df['Duration'] = df['SessionEndTime'] - df['SessionStartTime']
            
            # Agrupar por persona y sumar la duración de las sesiones
            group_by_persona = df.groupby('ParticipantDisplayName')
            duracion_total = group_by_persona['Duration'].sum()
            
            # Filtrar por duración mayor o igual a 90 minutos
            duracion_mas_90 = duracion_total[duracion_total >= timedelta(minutes=90)]
            
            # Contar las apariciones de más de 90 minutos por persona
            for persona, duracion in duracion_mas_90.items():
                recuento_personas_tiempo[persona] = recuento_personas_tiempo.get(persona, 0) + 1
        
        # Contar las apariciones totales por persona
        conteo_total = df['ParticipantDisplayName'].value_counts()
        
        # Actualizar el recuento global de cada persona
        for persona, count in conteo_total.items():
            recuento_personas_total[persona] = recuento_personas_total.get(persona, 0) + count

# Ordenar las personas por el número de apariciones en orden descendente
personas_tiempo_ordenadas = sorted(recuento_personas_tiempo.items(), key=lambda x: x[1], reverse=True)
personas_total_ordenadas = sorted(recuento_personas_total.items(), key=lambda x: x[1], reverse=True)

# Crear un DataFrame para guardar los resultados
data = {
    'Alumno': [persona for persona, _ in personas_tiempo_ordenadas],
    'Asistencia': [count_tiempo for _, count_tiempo in personas_tiempo_ordenadas]
}

# Crear el DataFrame y guardarlo en un archivo CSV
df_resultado = pd.DataFrame(data)
df_resultado.to_csv("AsistenciaMiercoles.csv", index=False)
