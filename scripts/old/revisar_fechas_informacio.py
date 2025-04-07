import pandas as pd
import os

# Ruta al archivo
file_path = os.path.join('data', 'ethusdt_1h_labeled_v4.csv')

# Cargar el archivo
df = pd.read_csv(file_path)

# Asegurar que 'timestamp' esté en formato datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Ver rango de fechas
print("📅 Primer timestamp:", df['timestamp'].min())
print("📅 Último timestamp:", df['timestamp'].max())

# Cantidad total de filas
print("🔢 Total de filas:", len(df))
