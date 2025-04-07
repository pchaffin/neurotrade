# 🧠 NeuroTrade

**NeuroTrade** es una plataforma experimental de trading automatizado basada en Machine Learning, orientada a detectar oportunidades de compra en criptomonedas a partir de datos históricos, indicadores técnicos y modelos de predicción entrenados con alta precisión.

> 🚧 Proyecto en desarrollo - fase experimental

---

## 📌 Objetivos

- Desarrollar un sistema de señales de compra para trading algorítmico.
- Entrenar y mejorar modelos de ML que superen el 60% de aciertos en tendencias alcistas.
- Evaluar estrategias con indicadores técnicos como RSI, MACD, Bollinger Bands y medias móviles.
- Automatizar el pipeline de descarga, entrenamiento y ejecución de señales.

---

## 🧱 Estructura del Proyecto

---

## 🚀 ¿Cómo empezar?

### 1. Clonar el repositorio
git clone https://github.com/pchaffin/neurotrade.git
cd neurotrade
### 2. Crear un entorno virtual
bash
Copiar
Editar
python3 -m venv venv
source venv/bin/activate
### 3. Instalar dependencias
bash
Copiar
Editar
pip install -r requirements.txt
### 4. Configurar variables
Crea un archivo .env con tus claves de API de Binance.

⚙️ Scripts principales
Entrenamiento del modelo
python3 scripts/entrenar_modelo_v4.py

Generar señales
python3 scripts/bot_signals_eth.py

Automatización completa (scheduler)
python3 scripts/task_scheduler.py
Este script ejecuta en orden:
- Descarga histórica
- Generación de indicadores
- Generación del dataset v4
- Detección de señales

🧠 Modelos
El proyecto actualmente incluye un modelo v4 entrenado con etiquetas que identifican subas de precio superiores al 4% dentro de las 3 horas posteriores.
Próximas versiones incluirán detección de señales de venta y mejoras con modelos más robustos.

📈 Señales
Las señales generadas se almacenan en signals/ethusdt_signals.csv, con el siguiente formato:

Fecha	Hora	Par	Señal	Monto USDT
2025-04-06	13:00	ETHUSDT	BUY	10
📋 TODO
 Pipeline automatizado diario
 Entrenamiento con etiquetas personalizadas
 Señales de venta y gestión de posiciones
 Interfaz web para monitoreo
 Mejora del dataset con datos históricos desde 2023
 Backtesting integrado

📄 Licencia
MIT License

👨‍💻 Autor
Desarrollado por @pchaffin
Contribuciones bienvenidas.

