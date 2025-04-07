# scripts/descargar_anteriores_30dias.py
import os
import pandas as pd
from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

client = Client(api_key, api_secret)

SYMBOL = "ETHUSDT"
INTERVAL = Client.KLINE_INTERVAL_1HOUR
START = "2024-12-09 16:00:00"
END = "2025-01-08 16:00:00"
OUTPUT_PATH = os.path.join('data', 'ethusdt_1h_anteriores.csv')

klines = client.get_historical_klines(SYMBOL, INTERVAL, START, END)

df = pd.DataFrame(klines, columns=[
    'timestamp', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'num_trades',
    'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
])

df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
df = df.astype({
    'open': float, 'high': float, 'low': float,
    'close': float, 'volume': float
})

# Guardar CSV
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Datos históricos anteriores guardados en {OUTPUT_PATH}")
print(f"📅 Desde: {df['timestamp'].min()} - Hasta: {df['timestamp'].max()}")
print(f"🔢 Total de filas: {len(df)}")
