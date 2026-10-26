# Diccionario de datos

Dataset sintético de clientes de una empresa de telecomunicaciones.

## Archivo raw (`data/raw/clientes_telecom_raw.csv`)

Contiene errores intencionales para practicar la limpieza.

| Columna | Tipo | Descripción | Problemas conocidos |
|---|---|---|---|
| `customer_id` | texto | Identificador único del cliente (`C00001`...) | Filas duplicadas (~2%) |
| `genero` | texto | `Hombre` o `Mujer` | Sin problemas |
| `adulto_mayor` | entero (0/1) | 1 si el cliente es adulto mayor | Sin problemas |
| `pareja` | texto | ¿Tiene pareja? (`Sí`/`No`) | Variantes: `Si`, `si`, `SÍ` |
| `dependientes` | texto | ¿Tiene dependientes? (`Sí`/`No`) | Variantes: `Si`, `si`, `SÍ` |
| `antiguedad_meses` | entero | Meses que lleva como cliente | Valores faltantes (~2%) |
| `tipo_contrato` | texto | `Mensual`, `Anual` o `Bienal` | Mayúsculas y espacios extra (~8%) |
| `metodo_pago` | texto | Forma de pago | Sin problemas |
| `facturacion_electronica` | texto | ¿Usa facturación electrónica? (`Sí`/`No`) | Sin problemas |
| `servicio_internet` | texto | `DSL`, `Fibra óptica` o `Ninguno` | Sin problemas |
| `cargo_mensual` | decimal | Cobro mensual en USD | Sin problemas |
| `cargo_total` | decimal | Cobro acumulado en USD | Espacios en blanco en lugar de vacío (~1.5%) |
| `cancelo` | texto | Variable objetivo: ¿canceló? (`Sí`/`No`) | Variantes de `Sí`/`No` |

## Archivo limpio (`data/processed/clientes_limpios.csv`)

Todas las columnas anteriores, con estas diferencias:

| Columna | Cambio |
|---|---|
| `customer_id` | Sin duplicados |
| `tipo_contrato` | Normalizado a `Mensual`, `Anual`, `Bienal` |
| `pareja`, `dependientes`, `facturacion_electronica`, `cancelo` | Solo `Sí` o `No` |
| `antiguedad_meses` | Entero, faltantes imputados con la mediana |
| `cargo_total` | Numérico, faltantes calculados como `cargo_mensual × antiguedad_meses` |

### Columnas nuevas

| Columna | Descripción |
|---|---|
| `cancelo_bin` | 1 si canceló, 0 si no. Útil para calcular tasas con `AVG` |
| `rango_antiguedad` | Agrupa `antiguedad_meses` en `0-12`, `13-24`, `25-48` y `49+` meses |

## Decisiones de limpieza

1. **Duplicados:** se conserva la primera aparición de cada `customer_id`.
2. **Sí/No:** se unifican todas las variantes a `Sí` y `No`.
3. **Antigüedad faltante:** se usa la mediana. Es una decisión simple; una alternativa es estimarla con otros atributos.
4. **Cargo total faltante:** se calcula con la regla de negocio `cargo_mensual × antiguedad_meses`.
