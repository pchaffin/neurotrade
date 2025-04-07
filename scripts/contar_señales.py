import pandas as pd
import os

# Ruta al dataset unificado
file_path = "../data/ethusdt_1h_dataset.csv"

# Cargar dataset
df = pd.read_csv(file_path)

# Contar valores de la columna target
conteo = df['target'].value_counts()

# Mostrar resultados
print("📊 Distribución de etiquetas 'target':")
for valor, cantidad in conteo.items():
    etiqueta = "📈 BUY (1)" if valor == 1 else "📉 NO BUY (0)"
    print(f"  {etiqueta}: {cantidad} casos")

print(f"\n🔢 Total de ejemplos: {len(df)}")
