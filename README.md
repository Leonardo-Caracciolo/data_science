## 📁 Estructura del Proyecto

```
Prueba-Tecnica-DS/
├── data/                # Archivos de entrada originales (.csv)
├── src/                 # Lógica modular de cada pregunta y visualizaciones
├── output/              # Archivos generados automáticamente (.csv, .txt, .png)
├── app.py               # Visualización interactiva (opcional, con Streamlit)
├── main.py              # Script principal que ejecuta todas las preguntas
├── requirements.txt     # Dependencias exactas y compatibles
└── README.md            # Documentación del proyecto
```

---

## ▶️ Cómo ejecutar el análisis

1. Crear y activar entorno virtual:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar el análisis completo:

```bash
python main.py
```

Esto generará todos los archivos en `output/`.

---

## 🖼️ Visualización interactiva (opcional)

Se puede lanzar una interfaz gráfica para explorar los resultados usando **Streamlit**:

```bash
streamlit run app.py
```

Incluye:
- Gráfico de Pareto (volumen vendido)
- Frecuencia de venta por producto
- Crecimiento del producto SALUS FRUTTE CERO ANANA
- Interpretaciones automáticas

---

## ✅ Justificación de decisiones

### Limpieza y consistencia
- Se convirtió `fecha_comercial` a tipo datetime.
- Se usó `.dropna()`, `.nunique()`, y chequeos condicionales para prevenir errores.
- No se asumió que los datos eran limpios: se filtraron fechas, ventas nulas y casos vacíos.

### Elección de métricas
- Se utilizó `cant_vta` (cantidad de ventas) como métrica principal por ser directa y confiable.
- Se calcularon porcentajes acumulados (`cumsum`) y frecuencias reales por punto de venta (`días abiertos / días con venta`).

### Desarrollo modular
- Cada pregunta se resolvió en una función separada, siguiendo una arquitectura clara (`src/preguntas.py`).
- El proyecto es reproducible, legible y escalable.

### Visualización profesional
- Se implementó visualización opcional con Streamlit y Seaborn.
- Se justifica como herramienta de entrega y entendimiento para usuarios no técnicos.

---

## 📂 Resultados generados

Los resultados se guardan automáticamente en la carpeta `output/`, por ejemplo:

- `pregunta_1_productos_80_por_ciento.csv`
- `pregunta_2_productos_pareto.csv`
- `pregunta_3_frecuencia_por_producto.csv`
- `pregunta_4_variacion_ventas.txt`
- `pregunta_5_ventas_producto_objetivo.csv`
- `pregunta_5_causa_crecimiento.txt`

---

## 📚 Librerías utilizadas

- Revisar el requirements.txt

---
