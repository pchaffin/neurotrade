import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# === Cargar el dataset ===
df = pd.read_csv('../data/ethusdt_1h_dataset.csv')

# === Features usadas en el entrenamiento ===
features = [
    'rsi', 'macd', 'macd_signal',
    'bb_middle', 'bb_upper', 'bb_lower',
    'ema_20', 'ema_50',
    'sma_20', 'sma_50'
]

# === Eliminar filas con valores faltantes ===
df = df.dropna(subset=features + ['target'])

# === Separar features y target ===
X = df[features]
y = df['target']

# === Dividir en entrenamiento y validación ===
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)

# === Entrenar modelo ===
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# === Evaluar el modelo ===
y_pred = modelo.predict(X_val)
print(classification_report(y_val, y_pred))

# === Guardar modelo ===
joblib.dump(modelo, '../models/modelo_v4_eth.joblib')
print("✅ Modelo entrenado y guardado como modelo_v4_eth.joblib")
