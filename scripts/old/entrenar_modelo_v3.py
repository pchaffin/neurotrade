#entrenar_modelo_v4.py
import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from imblearn.over_sampling import RandomOverSampler

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'ethusdt_1h_dataset.csv')
MODEL_OUTPUT = os.path.join(BASE_DIR, 'models', 'modelo_rf_v3.pkl')

# Carga el dataset
df = pd.read_csv(DATA_PROCESSED)
df.set_index('timestamp', inplace=True)

# Features e información objetivo
features = ['rsi', 'macd', 'bb_upper', 'bb_lower', 'sma_20', 'sma_50']
X = df[features]
y = df['target']

# División Train/Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Oversampling (Rebalanceo de clases)
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

# Grid Search para optimizar hiperparámetros
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_resampled, y_train_resampled)

best_model = grid_search.best_estimator_

# Evaluación básica
y_pred = best_model.predict(X_test)
print("\n🔍 Resultados en test:")
print(classification_report(y_test, y_pred))

# Evaluación final y guardado
os.makedirs(os.path.dirname(MODEL_OUTPUT), exist_ok=True)
joblib.dump(best_model, MODEL_OUTPUT)
print(f"\n✅ Modelo guardado en: {MODEL_OUTPUT}")
print(f"🏆 Mejor combinación de hiperparámetros: {grid_search.best_params_}")
