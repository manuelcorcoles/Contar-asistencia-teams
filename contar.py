import os
import pandas as pd
from datetime import datetime, timedelta

# Ruta de la carpeta que contiene los archivos CSV
carpeta = '/home/manu/Contar-asistencia-teams/csv'

# Crear un diccionario para almacenar el recuento de cada persona
recuento_personas_tiempo = {}
recuento_personas_total = {}

# Contador de Excels recorridos
excels_recorridos = 0

# Recorrer todos los archivos en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith('.csv'):  # Asegurarse de que solo se procesen archivos CSV
        ruta_archivo = os.path.join(carpeta, archivo)
        
        # Incrementar el contador de Excels recorridos
        excels_recorridos += 1
        
        # Leer el archivo CSV en un DataFrame
        df = pd.read_csv(ruta_archivo)
        
        # Verificar la existencia de las columnas 'SessionStartTime' y 'SessionEndTime'
        if 'SessionStartTime' in df.columns and 'SessionEndTime' in df.columns:
            # Convertir las columnas de fecha y hora a objetos datetime
            df['SessionStartTime'] = pd.to_datetime(df['SessionStartTime'])
            df['SessionEndTime'] = pd.to_datetime(df['SessionEndTime'])
            
            # Calcular la diferencia de tiempo entre 'SessionStartTime' y 'SessionEndTime'
            df['TimeDifference'] = df['SessionEndTime'] - df['SessionStartTime']
            
            # Filtrar las filas con una diferencia de tiempo mayor a 1.5 horas (90 minutos)
            df_filtrado = df[df['TimeDifference'] > timedelta(minutes=90)]
            
            # Obtener la columna 'ParticipantDisplayName' del DataFrame filtrado
            column_name = 'ParticipantDisplayName'
            if column_name in df_filtrado.columns:
                # Contar la aparición de cada persona en el DataFrame filtrado
                conteo_tiempo = df_filtrado[column_name].value_counts()
                
                # Actualizar el recuento global de cada persona
                for persona, count in conteo_tiempo.items():
                    recuento_personas_tiempo[persona] = recuento_personas_tiempo.get(persona, 0) + count
        
        # Contar la aparición de cada persona sin tener en cuenta el tiempo
        conteo_total = df[column_name].value_counts()
        
        # Actualizar el recuento global de cada persona
        for persona, count in conteo_total.items():
            recuento_personas_total[persona] = recuento_personas_total.get(persona, 0) + count

# Ordenar las personas por el número de apariciones en orden descendente
personas_tiempo_ordenadas = sorted(recuento_personas_tiempo.items(), key=lambda x: x[1], reverse=True)
personas_total_ordenadas = sorted(recuento_personas_total.items(), key=lambda x: x[1], reverse=True)

# Imprimir el número de Excels recorridos
print(f'Número de Excels recorridos: {excels_recorridos}')

# Imprimir el número de apariciones de más de 90 minutos y de menos para cada persona
for persona, count_tiempo in personas_tiempo_ordenadas:
    count_total = recuento_personas_total.get(persona, 0)
    print(f'{persona}: {count_tiempo}/{count_total}')

# Imprimir el número total de apariciones sin tener en cuenta el tiempo
print('Total de apariciones sin tener en cuenta el tiempo:')
for persona, count in personas_total_ordenadas:
    # Evitar imprimir las apariciones nuevamente si ya se imprimieron en el bloque anterior
    if persona not in recuento_personas_tiempo:
        print(f'{persona}: {count} veces')
