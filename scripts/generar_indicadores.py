import pandas as pd
import ta

# Rutas
#INPUT_PATH = '../data/ethusdt_1h_dataset.csv'
#OUTPUT_PATH = '../data/ethusdt_1h.csv'
# Rutas corregidas
INPUT_PATH = '../data/ethusdt_1h.csv'
OUTPUT_PATH = '../data/ethusdt_1h_dataset.csv'


# Leer archivo unificado
df = pd.read_csv(INPUT_PATH)

# Asegurar que esté ordenado por tiempo
#df = df.sort_values('timestamp')
df = df.sort_index()

# Calcular indicadores técnicos
df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
df['macd'] = ta.trend.MACD(close=df['close']).macd()
df['macd_signal'] = ta.trend.MACD(close=df['close']).macd_signal()

df['sma_20'] = df['close'].rolling(window=20).mean()
df['sma_50'] = df['close'].rolling(window=50).mean()

bb = ta.volatility.BollingerBands(close=df['close'], window=20)
df['bb_middle'] = bb.bollinger_mavg()
df['bb_upper'] = bb.bollinger_hband()
df['bb_lower'] = bb.bollinger_lband()

df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()

# Eliminar filas con NaN generados por los indicadores
df = df.dropna()

# Guardar resultados
df.to_csv(OUTPUT_PATH, index=False)
print(f"✅ Indicadores guardados en {OUTPUT_PATH}")
print(f"🔢 Total de filas: {len(df)}")
print(f"📅 Desde: {df['timestamp'].iloc[0]} - Hasta: {df['timestamp'].iloc[-1]}")
