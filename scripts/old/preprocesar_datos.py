import pandas as pd
import ta
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, 'data', 'ethusdt_1h.csv')
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed')
TRAIN_FILE = os.path.join(DATA_PROCESSED, 'ethusdt_1h_train.csv')
VAL_FILE = os.path.join(DATA_PROCESSED, 'ethusdt_1h_val.csv')

# Carga datos
df = pd.read_csv(DATA_RAW)
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

# Indicadores técnicos
df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
df['macd'] = ta.trend.MACD(df['close']).macd_diff()
bb = ta.volatility.BollingerBands(df['close'])
df['bb_upper'] = bb.bollinger_hband()
df['bb_lower'] = bb.bollinger_lband()
df['sma_20'] = ta.trend.SMAIndicator(df['close'], window=20).sma_indicator()
df['sma_50'] = ta.trend.SMAIndicator(df['close'], window=50).sma_indicator()

# Target: señal de compra si sube +2% en las próximas 3 velas
df['future_close'] = df['close'].shift(-3)
df['target'] = (df['future_close'] >= df['close'] * 1.02).astype(int)

# Limpiar
df.dropna(inplace=True)

# Split train/validation (80% / 20%)
split_idx = int(len(df) * 0.8)
df_train = df.iloc[:split_idx]
df_val = df.iloc[split_idx:]

# Guardar datasets
os.makedirs(DATA_PROCESSED, exist_ok=True)
df_train.to_csv(TRAIN_FILE)
df_val.to_csv(VAL_FILE)

print(f"✅ Train dataset: {TRAIN_FILE}")
print(f"✅ Validation dataset: {VAL_FILE}")
