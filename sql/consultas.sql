-- ============================================================
-- Consultas de analisis de cancelacion (churn)
-- Tabla: clientes (generada por src/limpieza.py)
-- Cada bloque empieza con "-- @nombre" y se exporta a CSV.
-- ============================================================

-- @resumen_general
SELECT
    COUNT(*)                              AS total_clientes,
    SUM(cancelo_bin)                      AS clientes_cancelados,
    ROUND(100.0 * AVG(cancelo_bin), 2)    AS tasa_cancelacion_pct,
    ROUND(AVG(cargo_mensual), 2)          AS cargo_mensual_promedio
FROM clientes;

-- @tasa_por_contrato
SELECT
    tipo_contrato,
    COUNT(*)                              AS clientes,
    ROUND(100.0 * AVG(cancelo_bin), 2)    AS tasa_cancelacion_pct
FROM clientes
GROUP BY tipo_contrato
ORDER BY tasa_cancelacion_pct DESC;

-- @tasa_por_servicio
SELECT
    servicio_internet,
    COUNT(*)                              AS clientes,
    ROUND(100.0 * AVG(cancelo_bin), 2)    AS tasa_cancelacion_pct
FROM clientes
GROUP BY servicio_internet
ORDER BY tasa_cancelacion_pct DESC;

-- @tasa_por_antiguedad
SELECT
    rango_antiguedad,
    COUNT(*)                              AS clientes,
    ROUND(100.0 * AVG(cancelo_bin), 2)    AS tasa_cancelacion_pct
FROM clientes
GROUP BY rango_antiguedad
ORDER BY MIN(antiguedad_meses);

-- @tasa_por_metodo_pago
SELECT
    metodo_pago,
    COUNT(*)                              AS clientes,
    ROUND(100.0 * AVG(cancelo_bin), 2)    AS tasa_cancelacion_pct
FROM clientes
GROUP BY metodo_pago
ORDER BY tasa_cancelacion_pct DESC;

-- @ingreso_mensual_perdido
SELECT
    servicio_internet,
    COUNT(*)                              AS clientes_cancelados,
    ROUND(SUM(cargo_mensual), 2)          AS ingreso_mensual_perdido
FROM clientes
WHERE cancelo_bin = 1
GROUP BY servicio_internet
ORDER BY ingreso_mensual_perdido DESC;

-- @segmentos_riesgo
SELECT
    tipo_contrato,
    servicio_internet,
    metodo_pago,
    COUNT(*)                              AS clientes,
    ROUND(100.0 * AVG(cancelo_bin), 2)    AS tasa_cancelacion_pct
FROM clientes
GROUP BY tipo_contrato, servicio_internet, metodo_pago
HAVING COUNT(*) >= 30
ORDER BY tasa_cancelacion_pct DESC
LIMIT 10;
