# Guía para construir el dashboard en Tableau

Esta guía asume que ya ejecutaste el proyecto y tienes los archivos en `data/processed/`.

## 1. Fuentes de datos

Puedes conectarte a cualquiera de estas dos opciones:

- **Tabla completa:** `data/processed/clientes_limpios.csv`. Sirve para explorar todos los clientes.
- **Resultados agregados:** los CSV de `data/processed/resultados/`. Son más livianos y ya están resumidos.

En Tableau: *Conectar → Texto (CSV)* y selecciona el archivo.

## 2. Hojas recomendadas

Crea una hoja por cada pregunta de negocio:

| Hoja | Tipo de gráfico | Fuente sugerida |
|---|---|---|
| Tasa por contrato | Barras horizontales, ordenadas de mayor a menor | `tasa_por_contrato.csv` |
| Tasa por servicio | Barras | `tasa_por_servicio.csv` |
| Tasa por antigüedad | Barras o línea por `rango_antiguedad` | `tasa_por_antiguedad.csv` |
| Tasa por método de pago | Barras | `tasa_por_metodo_pago.csv` |
| Ingreso perdido | Barras o texto (KPI) | `ingreso_mensual_perdido.csv` |
| Segmentos de riesgo | Tabla con mapa de calor | `segmentos_riesgo.csv` |

## 3. KPIs superiores

Crea tarjetas con:

- Total de clientes (`total_clientes`)
- Tasa de cancelación (`tasa_cancelacion_pct`)
- Ingreso mensual perdido (suma de `ingreso_mensual_perdido`)

## 4. Dashboard

1. Arrastra las hojas a un *Dashboard* nuevo.
2. Agrega los KPIs arriba y los gráficos debajo.
3. Usa un título claro, por ejemplo: *"¿Por qué cancelan los clientes?"*.
4. Agrega filtros de `tipo_contrato` y `servicio_internet` si usas la tabla completa.

## 5. Publicar

- Guarda el libro como `.twbx` dentro de `docs/` (opcional).
- Publica en **Tableau Public** y copia el enlace en el README.
- Guarda una captura en `docs/img/dashboard.png` y muéstrala en el README.

## Buenas prácticas

- Un mensaje por gráfico: el título debe decir qué concluir, no solo qué se mide.
- Ordena las barras por valor, no alfabéticamente.
- Usa un solo color para resaltar lo importante (por ejemplo, la tasa más alta).
