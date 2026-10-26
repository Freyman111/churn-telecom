"""
PASO 5 · DASHBOARD INTERACTIVO (HTML)

Genera docs/dashboard.html: un dashboard interactivo en una sola página
(no necesita servidor) a partir de los resultados de las consultas SQL.

Se puede abrir en el navegador o publicar con GitHub Pages.

Uso (desde la raíz del proyecto, después de ejecutar ejecutar_consultas.py):
    python src/dashboard.py
"""
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DIR_RESULTADOS = ROOT / "data" / "processed" / "resultados"
RUTA_SALIDA = ROOT / "docs" / "dashboard.html"

PLANTILLA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dashboard de cancelación de clientes</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  body { font-family: system-ui, sans-serif; background: #f3f4f6; margin: 0; padding: 24px; color: #111827; }
  h1 { margin: 0 0 4px; font-size: 22px; }
  .sub { color: #6b7280; margin: 0 0 20px; }
  .kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 16px; }
  .kpi, .card { background: #fff; border-radius: 10px; padding: 16px; box-shadow: 0 1px 2px rgba(0,0,0,.06); }
  .kpi .valor { font-size: 26px; font-weight: 700; }
  .kpi .etiqueta { color: #6b7280; font-size: 13px; }
  .graficos { display: grid; grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); gap: 12px; }
  .card h2 { font-size: 15px; margin: 0 0 8px; }
  footer { color: #9ca3af; font-size: 12px; margin-top: 16px; }
</style>
</head>
<body>
<h1>¿Por qué cancelan los clientes?</h1>
<p class="sub">Análisis de churn · datos sintéticos de telecomunicaciones</p>

<div class="kpis">
  <div class="kpi"><div class="valor" id="kpi-total"></div><div class="etiqueta">Clientes totales</div></div>
  <div class="kpi"><div class="valor" id="kpi-cancelados"></div><div class="etiqueta">Clientes cancelados</div></div>
  <div class="kpi"><div class="valor" id="kpi-tasa"></div><div class="etiqueta">Tasa de cancelación</div></div>
  <div class="kpi"><div class="valor" id="kpi-ingreso"></div><div class="etiqueta">Ingreso mensual perdido</div></div>
</div>

<div class="graficos">
  <div class="card"><h2>Tasa de cancelación por contrato</h2><canvas id="g-contrato"></canvas></div>
  <div class="card"><h2>Tasa de cancelación por servicio</h2><canvas id="g-servicio"></canvas></div>
  <div class="card"><h2>Tasa de cancelación según antigüedad</h2><canvas id="g-antiguedad"></canvas></div>
  <div class="card"><h2>Tasa de cancelación por método de pago</h2><canvas id="g-metodo"></canvas></div>
  <div class="card"><h2>Ingreso mensual perdido por servicio (USD)</h2><canvas id="g-ingreso"></canvas></div>
</div>

<footer>Generado con src/dashboard.py a partir de data/processed/resultados/</footer>

<script>
const D = /*DATOS*/;

const pct = v => v.toFixed(1) + '%';
const usd = v => '$' + Math.round(v).toLocaleString('es-CO');

document.getElementById('kpi-total').textContent = D.kpis.total.toLocaleString('es-CO');
document.getElementById('kpi-cancelados').textContent = D.kpis.cancelados.toLocaleString('es-CO');
document.getElementById('kpi-tasa').textContent = pct(D.kpis.tasa);
document.getElementById('kpi-ingreso').textContent = usd(D.kpis.ingreso);

function barras(id, grafico, formato) {
  const maximo = Math.max(...grafico.values);
  new Chart(document.getElementById(id), {
    type: 'bar',
    data: {
      labels: grafico.labels,
      datasets: [{
        data: grafico.values,
        backgroundColor: grafico.values.map(v => v === maximo ? '#DC2626' : '#9CA3AF')
      }]
    },
    options: {
      indexAxis: 'y',
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: c => formato(c.raw) } }
      },
      scales: { x: { ticks: { callback: v => formato(v) } } }
    }
  });
}

barras('g-contrato', D.graficos.contrato, pct);
barras('g-servicio', D.graficos.servicio, pct);
barras('g-antiguedad', D.graficos.antiguedad, pct);
barras('g-metodo', D.graficos.metodo, pct);
barras('g-ingreso', D.graficos.ingreso, usd);
</script>
</body>
</html>
"""


def cargar(nombre: str) -> pd.DataFrame:
    return pd.read_csv(DIR_RESULTADOS / f"{nombre}.csv")


def a_grafico(df: pd.DataFrame, columna_valor: str) -> dict:
    return {
        "labels": df.iloc[:, 0].astype(str).tolist(),
        "values": [round(float(v), 2) for v in df[columna_valor]],
    }


def construir_datos() -> dict:
    resumen = cargar("resumen_general").iloc[0]
    ingreso = cargar("ingreso_mensual_perdido")

    return {
        "kpis": {
            "total": int(resumen["total_clientes"]),
            "cancelados": int(resumen["clientes_cancelados"]),
            "tasa": float(resumen["tasa_cancelacion_pct"]),
            "ingreso": float(ingreso["ingreso_mensual_perdido"].sum()),
        },
        "graficos": {
            "contrato": a_grafico(cargar("tasa_por_contrato"), "tasa_cancelacion_pct"),
            "servicio": a_grafico(cargar("tasa_por_servicio"), "tasa_cancelacion_pct"),
            "antiguedad": a_grafico(cargar("tasa_por_antiguedad"), "tasa_cancelacion_pct"),
            "metodo": a_grafico(cargar("tasa_por_metodo_pago"), "tasa_cancelacion_pct"),
            "ingreso": a_grafico(ingreso.sort_values("ingreso_mensual_perdido", ascending=False),
                                 "ingreso_mensual_perdido"),
        },
    }


def main() -> None:
    datos = construir_datos()
    html = PLANTILLA.replace("/*DATOS*/", json.dumps(datos, ensure_ascii=False))
    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    RUTA_SALIDA.write_text(html, encoding="utf-8")
    print(f"Dashboard generado: {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
