# generar_senales_v4.py
import os
import pandas as pd
import joblib
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator, MACD
from ta.volatility import BollingerBands
from datetime import datetime

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, 'data', 'ethusdt_1h.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'modelo_rf_v4.pkl')
SIGNALS_PATH = os.path.join(BASE_DIR, 'signals', 'signals_v4.csv')

# Carga de datos
df = pd.read_csv(CSV_PATH)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Cálculo de indicadores si no existen
if 'rsi' not in df.columns:
    df['rsi'] = RSIIndicator(close=df['close']).rsi()
if 'macd' not in df.columns:
    df['macd'] = MACD(close=df['close']).macd()
if 'bb_upper' not in df.columns:
    bb = BollingerBands(close=df['close'])
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
if 'sma_20' not in df.columns:
    df['sma_20'] = SMAIndicator(close=df['close'], window=20).sma_indicator()
if 'sma_50' not in df.columns:
    df['sma_50'] = SMAIndicator(close=df['close'], window=50).sma_indicator()

# Eliminamos filas con NaNs
df.dropna(inplace=True)

# Features
features = ['rsi', 'macd', 'bb_upper', 'bb_lower', 'sma_20', 'sma_50']
X = df[features]

# Carga modelo
model = joblib.load(MODEL_PATH)

# Predicciones
df['predicted'] = model.predict(X)

# Filtramos señales de compra
signals = df[df['predicted'] == 1].copy()
signals = signals.reset_index()

# Creamos carpeta si no existe
os.makedirs(os.path.dirname(SIGNALS_PATH), exist_ok=True)

# Guardamos en CSV en formato append
signals_to_save = signals[['timestamp', 'predicted', 'close']]
signals_to_save['pair'] = 'ETH/USDT'
signals_to_save['usdt'] = 10
signals_to_save.rename(columns={'timestamp': 'datetime', 'predicted': 'buy_signal', 'close': 'price'}, inplace=True)
signals_to_save.to_csv(SIGNALS_PATH, mode='a', header=not os.path.exists(SIGNALS_PATH), index=False)

print(f"✅ Se generaron {len(signals_to_save)} señales de compra y se guardaron en: {SIGNALS_PATH}")
