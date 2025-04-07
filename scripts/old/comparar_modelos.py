import os
import joblib
import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

# Rutas base
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'ethusdt_1h_dataset.csv')
MODELOS = {
    "v1": os.path.join(BASE_DIR, "models", "modelo_rf_v1.pkl"),
    "v2": os.path.join(BASE_DIR, "models", "modelo_rf_v2.pkl"),
    "v3": os.path.join(BASE_DIR, "models", "modelo_rf_v3.pkl"),
}

# Cargar dataset y preparar features
df = pd.read_csv(DATA_PATH)
df.set_index('timestamp', inplace=True)
features = ['rsi', 'macd', 'bb_upper', 'bb_lower', 'sma_20', 'sma_50']
X = df[features]
y = df['target']

# División fija (sin shuffle para consistencia)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Evaluación por modelo
print("\n📊 Comparativa de Modelos:\n")
for version, model_path in MODELOS.items():
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        y_pred = model.predict(X_test)
        print(f"\n🔎 Modelo {version.upper()}: {model_path}")
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print(classification_report(y_test, y_pred))
    else:
        print(f"⚠️ Modelo {version.upper()} no encontrado en: {model_path}")
