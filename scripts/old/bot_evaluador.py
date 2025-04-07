import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Ruta al dataset procesado
dataset_path = os.path.join("..", "data", "processed", "ethusdt_1h_dataset.csv")
modelo_path = os.path.join("..", "models", "modelo_rf_v1.pkl")

# Cargar dataset
df = pd.read_csv(dataset_path)

# Separar variables
X = df.drop(columns=["target"])
y = df["target"]

# División entrenamiento / prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Entrenar modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluar modelo
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Precisión del modelo:", round(acc * 100, 2), "%")
print("\nReporte de clasificación:\n", classification_report(y_test, y_pred))

# Guardar modelo entrenado
joblib.dump(clf, modelo_path)
print(f"\n✅ Modelo guardado en: {modelo_path}")
