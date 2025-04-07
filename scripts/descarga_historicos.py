import os
from pathlib import Path
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta, timezone
from tqdm import tqdm
from dotenv import load_dotenv
import time

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")
client = Client(API_KEY, API_SECRET)

# Parámetros
symbol = "ETHUSDT"
interval = Client.KLINE_INTERVAL_1HOUR
limit = 1000  # máximo por consulta
days = 30  # Descargamos 30 días

# Ruta para guardar los datos
ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
output_file = DATA_DIR / f"{symbol.lower()}_1h.csv"

# Rango de tiempo
end_time = datetime.now(timezone.utc) - timedelta(days=60)  # 60 días atrás desde hoy
start_time = end_time - timedelta(days=days)
current_time = start_time  # Ya es timezone-aware

print(f"📥 Descargando datos de {symbol} (1h) desde {start_time.date()} hasta {end_time.date()}...\n")

# Descargar datos en bloques
all_klines = []
with tqdm(total=days * 24, desc="Progreso") as pbar:
    while current_time < end_time:
        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=current_time.strftime("%Y-%m-%d %H:%M:%S"),
            limit=limit
        )
        if not klines:
            break
        all_klines += klines
        last_time = klines[-1][0]
        current_time = datetime.fromtimestamp(last_time / 1000, tz=timezone.utc) + timedelta(hours=1)
        pbar.update(len(klines))

        time.sleep(0.2)  # Evitar rate limit

# DataFrame
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume',
           'close_time', 'quote_asset_volume', 'number_of_trades',
           'taker_buy_base', 'taker_buy_quote', 'ignore']

df = pd.DataFrame(all_klines, columns=columns)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

# Guardar CSV
df.to_csv(output_file)
print(f"\n✅ Datos guardados en: {output_file}")
