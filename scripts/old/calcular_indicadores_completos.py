# calcular_indicadores_completo.py
import pandas as pd
import ta

# Cargar el dataset unificado
df = pd.read_csv('../data/ethusdt_1h_dataset.csv')

# Calcular indicadores técnicos
df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()
macd = ta.trend.MACD(close=df['close'])
df['macd'] = macd.macd()
df['macd_signal'] = macd.macd_signal()
df['bb_bbm'] = ta.volatility.BollingerBands(close=df['close'], window=20).bollinger_mavg()
df['bb_bbh'] = ta.volatility.BollingerBands(close=df['close'], window=20).bollinger_hband()
df['bb_bbl'] = ta.volatility.BollingerBands(close=df['close'], window=20).bollinger_lband()
df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()

# Eliminar nulos que se generan por las ventanas
df = df.dropna()

# Guardar dataset con indicadores
df.to_csv('../data/ethusdt_1h_dataset.csv', index=False)
print(f"✅ Indicadores añadidos y guardados en data/ethusdt_1h_dataset.csv")
print(f"🔢 Total de filas: {len(df)}")
print(f"📅 Desde: {df['timestamp'].iloc[0]} - Hasta: {df['timestamp'].iloc[-1]}")
