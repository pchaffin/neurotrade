import os
import pandas as pd
import joblib
from datetime import datetime

# === CONFIGURACIÓN ===
DATA_PATH = os.path.join('..', 'data', 'ethusdt_1h_dataset.csv')
MODEL_PATH = os.path.join('..', 'models', 'modelo_v4_eth.joblib')
SIGNALS_PATH = os.path.join('..', 'signals', 'buy_signals.csv')

# === Cargar datos ===
df = pd.read_csv(DATA_PATH)
df = df.dropna()

# === Columnas usadas por el modelo ===
#columnas_usadas = ['rsi', 'macd', 'macd_signal', 'bb_bbh', 'bb_bbl', 'sma_20', 'sma_50', 'ema_20', 'ema_50']

columnas_usadas = [
    'rsi', 'macd', 'macd_signal',
    'bb_middle', 'bb_upper', 'bb_lower',
    'ema_20', 'ema_50',
    'sma_20', 'sma_50'
]

# === Último ejemplo para predecir ===
ultimo = df.iloc[-1:]
X = ultimo[columnas_usadas]

# === Cargar modelo ===
model = joblib.load(MODEL_PATH)

# === Hacer predicción ===
pred = model.predict(X)[0]
prob = model.predict_proba(X)[0][1]

# === Registrar señal si hay BUY ===
if pred == 1:
    signal = {
        'timestamp': ultimo['timestamp'].values[0],
        'datetime': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        'symbol': 'ETH/USDT',
        'signal': 'BUY',
        'confidence': round(prob, 4),
        'amount_usdt': 10
    }
    df_signal = pd.DataFrame([signal])
    file_exists = os.path.isfile(SIGNALS_PATH)
    df_signal.to_csv(SIGNALS_PATH, mode='a', index=False, header=not file_exists)
    print("📈 Señal de compra registrada:", signal)
else:
    print("📉 Sin señal de compra.")
