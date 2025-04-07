import time
import subprocess
from datetime import datetime

LOG_FILE = "../logs/task_scheduler.log"

def log(msg):
    timestamp = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S] ")
    full_msg = f"{timestamp}{msg}"
    print(full_msg)
    with open(LOG_FILE, "a") as f:
        f.write(full_msg + "\n")

scripts = [
    "descarga_historicos.py",
    "generar_indicadores.py",
    "generar_dataset_v4.py",
    "bot_signals_eth.py"
]

log("🚀 Iniciando ciclo automático de ejecución de scripts...")

while True:
    for script in scripts:
        log(f"▶️ Ejecutando {script}...")
        try:
            result = subprocess.run(
                ["python3", script],
                check=True,
                text=True,
                capture_output=True
            )
            log(result.stdout)
            if result.stderr:
                log(f"⚠️ STDERR: {result.stderr}")
        except subprocess.CalledProcessError as e:
            log(f"❌ Error al ejecutar {script}:\n{e.stderr}")

    log("⏱ Esperando 1 hora para el próximo ciclo...\n")
    time.sleep(3600)  # Esperar 1 hora (3600 segundos)
