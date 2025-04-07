import pandas as pd
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIGNALS_PATH = os.path.join(BASE_DIR, 'signals', 'signals_log.csv')
HISTORICAL_PATH = os.path.join(BASE_DIR, 'data', 'ethusdt_1h.csv')
OUTPUT_PATH = os.path.join(BASE_DIR, 'signals', 'validated_signals.csv')

# Parámetros
THRESHOLD = 0.04  # 4% mínimo de ganancia
WINDOW_START = 2  # Desde la 2da vela (hora)
WINDOW_END = 3    # Hasta la 3ra vela (hora)

# Carga de archivos
df_signals = pd.read_csv(SIGNALS_PATH, parse_dates=['datetime'])
df_hist = pd.read_csv(HISTORICAL_PATH, parse_dates=['timestamp'])
df_hist.set_index('timestamp', inplace=True)

# Validación de señales
results = []
for _, row in df_signals.iterrows():
    signal_time = row['datetime']
    entry_price = row['price_usdt']

    # Selecciona velas entre la 2da y 3ra posterior a la señal
    future_window = df_hist.loc[signal_time:].iloc[WINDOW_START:WINDOW_END + 1]

    success = False
    for _, future_row in future_window.iterrows():
        high = future_row['high']
        if high >= entry_price * (1 + THRESHOLD):
            success = True
            break

    row_dict = row.to_dict()
    row_dict['success'] = success
    results.append(row_dict)

# Guardar resultados
df_validated = pd.DataFrame(results)
df_validated.to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Validación completada. Resultados guardados en: {OUTPUT_PATH}")
print(df_validated['success'].value_counts())
