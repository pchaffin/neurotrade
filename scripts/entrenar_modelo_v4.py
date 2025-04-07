import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Cargar el dataset
df = pd.read_csv('../data/ethusdt_1h_dataset.csv')

# Verificar que la columna target exista
if 'target' not in df.columns:
    raise ValueError("❌ El dataset no contiene la columna 'target'. Asegurate de generarla en generar_dataset_v4.py")

# Definir las features exactas que tiene el CSV
features = [
    'rsi', 'macd', 'macd_signal',
    'bb_middle', 'bb_upper', 'bb_lower',
    'ema_20', 'ema_50',
    'sma_20', 'sma_50'
]

# Eliminar filas con valores faltantes
df = df.dropna(subset=features + ['target'])

# Separar en X e y
X = df[features]
y = df['target']

# Dividir en train y validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)

# Crear y entrenar el modelo
modelo_entrenado = RandomForestClassifier(n_estimators=100, random_state=42)
modelo_entrenado.fit(X_train, y_train)

# Evaluar
y_pred = modelo_entrenado.predict(X_val)
print("📊 Reporte de clasificación:")
print(classification_report(y_val, y_pred))
print("✅ Accuracy:", accuracy_score(y_val, y_pred))

# Guardar el modelo
os.makedirs('../models', exist_ok=True)
joblib.dump(modelo_entrenado, '../models/modelo_v4_eth.joblib')  # <== ahora sí coincide
print("✅ Modelo entrenado y guardado como modelo_v4_eth.joblib")

#joblib.dump(modelo_entrenado, '../models/modelo_v4.pkl')
#print("✅ Modelo entrenado y guardado como modelo_v4.pkl")
