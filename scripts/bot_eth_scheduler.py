# scripts/bot_eth_scheduler.py

import subprocess
import time
import datetime

def log(msg):
    print(f"[{datetime.datetime.now()}] {msg}")

scripts = [
    "descarga_historicos.py",
    "generar_indicadores.py",
    "generar_dataset_v4.py",
    "bot_signals_eth.py"
]

if __name__ == "__main__":
    for script in scripts:
        log(f"Ejecutando {script}...")
        result = subprocess.run(["python3", script], capture_output=True, text=True, cwd=".")
        log(result.stdout)
        if result.stderr:
            log(f"⚠️ Error en {script}:\n{result.stderr}")
        time.sleep(1)  # un respiro entre scripts
