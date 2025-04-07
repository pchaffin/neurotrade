🚀 Fase 1: Recolección y preparación de datos
Objetivo: obtener históricos limpios para entrenar modelos.

✅ Paso 1.1: Descargar datos históricos desde Binance
Par: por ejemplo ETH/USDT

Intervalo: 1h o 15m

Rango: últimos 30 días para empezar

Formato: CSV

👉 Archivo: scripts/descarga_historicos.py
Este script se conecta con Binance y guarda datos en data/.

✅ Paso 1.2: Procesar los datos
Limpieza: nulos, columnas innecesarias

Agregado de indicadores técnicos (ta, como RSI, MACD, EMA, etc.)

Guardar el resultado en data/processed/

👉 Lo vamos a usar luego para entrenar modelos.

🧠 Fase 2: Machine Learning inicial
Objetivo: generar señales de compra/venta básicas a partir de features.

✅ Paso 2.1: Crear etiquetas ("targets")
Por ejemplo: "1" si el precio sube un X% en las próximas 3 velas, "0" si no.

Esta es la variable que el modelo aprende a predecir.

✅ Paso 2.2: Entrenar un modelo simple
Modelo inicial: Random Forest

Entrenar con los features (RSI, EMA, etc.) y la etiqueta

👉 Archivo: scripts/bot_evaluador.py
Guarda el modelo en models/modelo_rf_v1.pkl

📈 Fase 3: Evaluación y backtesting
Objetivo: saber si el modelo tiene sentido.

✅ Paso 3.1: Simular señales en datos históricos
¿Qué precisión tiene?

¿Genera ganancias?

👉 Archivo: logs/evaluacion.log

🤖 Fase 4: Generación de señales en tiempo real
Objetivo: usar el modelo entrenado para detectar señales en vivo.

👉 Archivo: scripts/bot_detector.py
Se conecta a Binance, descarga nuevas velas, genera predicción y muestra la señal.

💰 Fase 5: Ejecución de órdenes en Binance (opcional al principio)
Objetivo: automatizar compras/ventas (solo cuando estés seguro).

👉 Archivo: scripts/bot_executor.py
Lee las señales y ejecuta órdenes si hay señal válida.

🧪 BONUS: Visualización y prueba en notebooks
Podemos usar notebooks/01-exploracion.ipynb para explorar datos, visualizar señales, debuggear el modelo, etc.

--

🪜 Proyecto ML Trading – Recapitulación Paso a Paso
✅ 1. Descarga de históricos
Script: descargar_historico.py

Objetivo: Obtener velas 1h de ETH/USDT desde Binance y guardarlas como CSV (ethusdt_1h.csv).

Ubicación: /data

✅ 2. Procesamiento del dataset
Script: generar_dataset.py

Objetivo:

Calcular indicadores técnicos (RSI, MACD, Bollinger Bands, SMA).

Generar la columna target indicando si el precio subirá un X% en las próximas N horas.

Output: ethusdt_1h_dataset.csv en /data

✅ 3. Entrenamiento de modelos
Scripts: entrenar_modelo_rf_v1.py, v2, v3…

Objetivo:

Entrenar modelos Random Forest con diferentes técnicas:

V1: Sin oversampling

V2: Con oversampling (mejor balance)

V3: Con shuffle + oversampling (más robusto)

Output: Modelos guardados en /models/ como .pkl

✅ 4. Comparación de modelos
Script: comparar_modelos.py

Objetivo: Cargar V1, V2 y V3, ejecutar predicciones en el mismo test set y comparar métricas de clasificación (accuracy, f1-score, etc).

✅ 5. Generación de señales de compra
Script: generar_senales.py

Objetivo:

Usar modelo V3 para escanear el dataset completo.

Dejar señales de compra (buy) en un CSV (buy_signals.csv).

Ubicación: /signals/

Formato: datetime, pair, signal, price_usdt

✅ 6. Validación de señales
Script: validar_senales.py

Objetivo:

Leer el archivo de señales.

Validar si el precio subió al menos un 2% dentro de las 5 horas siguientes.

Añadir columna success (True/False).

Output: validated_signals.csv en /signals/

Resultado: 15.68% de aciertos sobre 1001 señales.

🧠 Estado actual del sistema
✅ Podemos generar y validar señales.

🔄 Podemos seguir iterando con nuevos modelos, nuevos parámetros de validación o múltiples pares.

🧪 Estamos en condiciones de afinar precisión y frecuencia de señales.
