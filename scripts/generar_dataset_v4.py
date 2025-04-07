import pandas as pd
import os
from datetime import datetime

# Cargar el dataset con indicadores
df = pd.read_csv('../data/ethusdt_1h_dataset.csv')

# Asegurar orden por fecha
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df.sort_values('timestamp').reset_index(drop=True)

# Crear columna target
target = []
lookahead = 3  # 3 horas hacia adelante
threshold = 0.04  # 4% de subida

for i in range(len(df)):
    if i + lookahead >= len(df):
        target.append(0)
        continue

    precio_actual = df.loc[i, 'close']
    futuros = df.loc[i+1:i+lookahead, 'high']
    suba_max = (futuros.max() - precio_actual) / precio_actual

    if suba_max >= threshold:
        target.append(1)
    else:
        target.append(0)

df['target'] = target

# Filtrar columnas para guardar dataset final
features = [
    'timestamp', 'open', 'high', 'low', 'close', 'volume',
    'rsi', 'macd', 'macd_signal',
    'sma_20', 'sma_50',
    'bb_middle', 'bb_upper', 'bb_lower',
    'ema_20', 'ema_50',
    'target'
]

df_final = df[features].dropna()

# Guardar CSV final
os.makedirs('../data', exist_ok=True)
output_path = '../data/ethusdt_1h_dataset.csv'
df_final.to_csv(output_path, index=False)

# Log de confirmación
print(f"[{datetime.now()}] ✅ Dataset v4 generado con {len(df_final)} filas.")
print(f"📁 Guardado en: {output_path}")
print(f"🔍 Ejemplos con target=1: {df_final['target'].sum()}")
