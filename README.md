# Análisis de cancelación de clientes (Churn) — Telecomunicaciones

Proyecto de análisis de datos de principio a fin: generación y limpieza de datos con **Python**, consultas con **SQL**, gráficos y dashboard.

> **Nota:** el dataset es sintético, generado por código, con errores intencionales para que la limpieza tenga sentido. Los hallazgos describen ese dataset, no a clientes reales. Puede reemplazarse por un dataset real con la misma estructura, como el [Telco Customer Churn de Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn).

## Pregunta de negocio

> ¿Qué características de los clientes explican que cancelen el servicio, y cuánto ingreso mensual se pierde por esas cancelaciones?

## Estructura del proyecto

```
churn-telecom/
├── data/
│   ├── raw/                  # Datos originales (con errores)
│   └── processed/            # Datos limpios, base SQLite y resultados
├── docs/
│   ├── img/                  # Gráficos PNG para el README
│   ├── dashboard.html        # Dashboard interactivo (abrir en el navegador)
│   ├── diccionario_datos.md  # Descripción de cada columna y decisiones de limpieza
│   └── guia_tableau.md       # Cómo construir el dashboard en Tableau (opcional)
├── sql/
│   └── consultas.sql         # Consultas de análisis (cada una con "-- @nombre")
├── src/
│   ├── generar_datos.py      # Paso 1: crea el dataset sintético
│   ├── limpieza.py           # Paso 2: limpieza con pandas y carga en SQLite
│   ├── ejecutar_consultas.py # Paso 3: ejecuta el SQL y exporta resultados a CSV
│   ├── graficos.py           # Paso 4: genera los gráficos PNG
│   └── dashboard.py          # Paso 5: genera el dashboard HTML
├── tests/
│   └── test_limpieza.py      # Pruebas automáticas de la limpieza
├── LICENSE
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python (pandas, numpy, matplotlib) | Generación, limpieza, transformación y gráficos |
| SQL (SQLite) | Consultas de análisis sobre la tabla limpia |
| Chart.js | Dashboard interactivo en HTML |
| pytest | Pruebas automáticas de la limpieza |

## Cómo reproducir el proyecto

Requisitos: Python 3.9 o superior.

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/churn-telecom.git
cd churn-telecom

# 2. Crear y activar un entorno virtual
python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el pipeline, en orden
python src/generar_datos.py        # Paso 1: crea data/raw/clientes_telecom_raw.csv
python src/limpieza.py             # Paso 2: crea data/processed/clientes_limpios.csv y churn.db
python src/ejecutar_consultas.py   # Paso 3: ejecuta sql/consultas.sql y guarda resultados/
python src/graficos.py             # Paso 4: genera los gráficos en docs/img/
python src/dashboard.py            # Paso 5: genera docs/dashboard.html

# 5. (Opcional) Ejecutar las pruebas
pip install -r requirements-dev.txt
pytest tests/
```

Para ver el dashboard, abre `docs/dashboard.html` en el navegador. Necesitas conexión a internet, porque la librería de gráficos se carga desde la red.

## Proceso de limpieza

Problemas encontrados en los datos crudos y cómo se resolvieron:

| Problema | Solución |
|---|---|
| Clientes duplicados | Se conserva la primera aparición de cada `customer_id` |
| `Sí`, `Si`, `si`, `SÍ` en la misma columna | Se unifican a `Sí` / `No` |
| `tipo_contrato` con mayúsculas y espacios | Se normaliza a `Mensual`, `Anual`, `Bienal` |
| `cargo_total` con espacios en blanco | Se convierte a numérico y se calcula como `cargo_mensual × antiguedad_meses` |
| `antiguedad_meses` faltante | Se imputa con la mediana |

Más detalle en [docs/diccionario_datos.md](docs/diccionario_datos.md).

## Hallazgos principales

Cifras obtenidas de las consultas sobre 7 000 clientes (después de limpiar):

- **Tasa general de cancelación:** 28.4 % (1 991 clientes cancelaron).
- **Por tipo de contrato:** los contratos mensuales cancelan el 37.9 %, frente al 20.7 % de los anuales y el 11.9 % de los bienales. El compromiso de más tiempo reduce la cancelación.
- **Por tipo de servicio:** la fibra óptica tiene la tasa más alta (38.2 %), seguida de DSL (22.5 %) y de clientes sin internet (19.8 %).
- **Por antigüedad:** los clientes de 0 a 12 meses cancelan el 42.1 %, y los de 49 meses o más, solo el 20.5 %. Los primeros meses son el momento más delicado de la relación con el cliente.
- **Por método de pago:** pagar con cheque electrónico tiene la tasa más alta (34.5 %). Los otros métodos están entre 24 % y 26 %.
- **Ingreso perdido:** cada mes se pierden unos **$135 000 USD** en ingreso por cancelaciones. La fibra óptica explica cerca del 71 % de esa pérdida ($95 681 USD).
- **Segmento más riesgoso:** clientes con contrato mensual, fibra óptica y pago por cheque electrónico cancelan el 57.8 % (597 clientes). Es el grupo prioritario para una estrategia de retención.

**Conclusión:** la cancelación se concentra en clientes nuevos, con contrato mensual y con fibra óptica. Un programa de retención enfocado en los primeros 12 meses y en el cambio a contratos anuales podría reducir de forma directa la pérdida de ingreso.

## Dashboard

- **Versión interactiva (HTML):** [docs/dashboard.html](docs/dashboard.html). Muestra los KPIs y los gráficos principales en una sola página.
- **Versión Tableau (opcional):** la guía está en [docs/guia_tableau.md](docs/guia_tableau.md).



## Autor

**freyman rodriguez.(www.linkedin.com/in/freyma-rodriguez-alvarez/) · [GitHub](https://github.com/Freyman111)

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver [LICENSE](LICENSE).
