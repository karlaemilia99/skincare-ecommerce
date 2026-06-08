# ✨ Skincare E-Commerce Analytics

Análisis completo de una marca D2C de skincare sobre 6 tablas relacionadas. El proyecto cubre dos análisis independientes pero complementarios: rentabilidad de productos y customer analytics (CLV, canales, retención, cohortes y devoluciones).

| Reporte | Link |
|---|---|
| 📊 Rentabilidad de Productos | [Ver reporte](reports/profitability_dashboard.html) |
| 👥 Customer Analytics | [Ver reporte](reports/full_dashboard.html) |

---

## 🗂️ Dataset — 6 tablas relacionadas

| Tabla | Filas | Descripción |
|---|---|---|
| `customers.csv` | 500 | Datos demográficos y canal de adquisición |
| `products.csv` | 28 | Productos con MRP, costo y categoría |
| `orders.csv` | 1,250 | Órdenes con estado, canal y montos |
| `order_items.csv` | 2,042 | Items por orden con descuento aplicado |
| `returns.csv` | 79 | Devoluciones con motivo y estado |
| `reviews.csv` | 494 | Reseñas con rating por producto |

---

## 📦 Parte A — Rentabilidad de Productos

### El problema
El margen bruto miente. Un producto puede tener 50% de margen pero si tiene 9% de devoluciones y 10% de descuento promedio, su rentabilidad real es significativamente menor.

### Profitability Score
Métrica compuesta que refleja la rentabilidad operativa real:

```
Score = (avg_margin_pct × 0.5) + ((100 - avg_discount) × 0.3) + ((100 - return_rate) × 0.2)
```

### Resultados

| Producto | Margen | Descuento | Devoluciones | Score |
|---|---|---|---|---|
| **Lip Balm SPF 30** | 59.1% | 9.3% | 1.9% | **76.35** |
| Rose Water Toner | 56.3% | 8.6% | 0.0% | 75.56 |
| Salicylic Acid Cleanser | 57.1% | 8.8% | 2.9% | 75.30 |
| **2% Salicylic Acid Serum** | 50.4% | 9.1% | 8.7% | **70.73** |
| Alpha Arbutin 2% Serum | 50.4% | 9.3% | 8.7% | 70.67 |

### Hallazgos clave
- **Revenue ≠ Rentabilidad:** Serum genera ₹430K (mayor revenue) pero tiene el peor score promedio
- **Serums activos:** devoluciones del 7-9% por irritación generan costos operativos ocultos
- **Cleansers:** mejor relación riesgo/retorno — margen ~56% con menos del 3% de devoluciones

---

## 👥 Parte B — Customer Analytics

### CLV por canal de adquisición

| Canal | Clientes | CLV Promedio | Retención |
|---|---|---|---|
| **Referral** | 56 | **₹2,543** | **78.6%** |
| Website Direct | 63 | ₹2,260 | 66.7% |
| Instagram | 123 | ₹2,218 | 68.3% |
| YouTube | 65 | ₹2,197 | 66.2% |
| Google Search | 131 | ₹2,149 | 65.7% |

### Retención y cohortes
- Retención Q+1 estable entre **19-32%** — 1 de cada 4 clientes vuelve al trimestre siguiente
- Cohorte 2024Q1 mantiene **20-24%** de retención hasta Q+7 — núcleo leal consolidado
- 2025Q2 tiene el mejor Q+1 (32%) pero colapsa en Q+2 (9%) — posible efecto de campaña puntual

### Devoluciones
- **35.4%** por skin irritation — problema estructural de producto, no logístico
- **37%** operacional (late delivery + damaged packaging) — resoluble sin cambiar el producto
- **Serum** acapara 43% de todas las devoluciones

### Hallazgos clave
- **Referral** gana en CLV, retención y ticket promedio — invertir en programa de referidos tiene mayor ROI que escalar Google Search
- **Segmento 45+** tiene el mayor CLV (₹2,339) — probablemente subrrepresentado en estrategia de contenido
- El **primer trimestre post-compra** es la ventana crítica para convertir compradores únicos en recurrentes

---

## 🗂️ Estructura del proyecto

```
skincare-ecommerce/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   ├── order_items.csv
│   ├── returns.csv
│   ├── reviews.csv
│   ├── product_profitability.csv
│   ├── delivered_items.csv
│   ├── clv.csv
│   ├── channel_stats.csv
│   ├── retention.csv
│   ├── cohort_retention.csv
│   └── returns_full.csv
├── src/
│   ├── eda.py
│   ├── preprocessing.py
│   ├── profitability.py
│   ├── clv.py
│   ├── retention.py
│   └── full_analysis.py
├── reports/
│   ├── profitability.png
│   ├── full_analysis.png
│   ├── profitability_dashboard.html
│   └── full_dashboard.html
└── README.md
```

---

## ⚙️ Cómo ejecutar

```bash
git clone https://github.com/karlaemilia99/skincare-ecommerce.git
cd skincare-ecommerce
pip install -r requirements.txt

# Parte A — Rentabilidad
python src/eda.py
python src/preprocessing.py
python src/profitability.py

# Parte B — Customer Analytics
python src/clv.py
python src/retention.py
python src/full_analysis.py
```

---

## 🛠️ Stack

- **Python 3.11**
- **pandas / numpy** — joins entre 6 tablas relacionadas
- **scikit-learn** — métricas y transformaciones
- **matplotlib / seaborn** — visualizaciones estáticas
- **HTML / CSS / Chart.js** — reportes interactivos

---

## 📁 Dataset

[D2C Skincare E-Commerce Analytics — Kaggle](https://www.kaggle.com)

Dataset sintético que simula una marca D2C de skincare con 6 tablas relacionadas: clientes, productos, órdenes, items, devoluciones y reseñas.

---

## 👩‍💻 Autora

**Karla Altamirano** — Software Engineer & Digital Transformation Specialist
[LinkedIn](https://www.linkedin.com/in/karlaemilia99/) · [GitHub](https://github.com/karlaemilia99)
