"""
PASO 4 · GRÁFICOS ESTÁTICOS (PNG)

Genera gráficos PNG a partir de los resultados de las consultas SQL.

Entrada : data/processed/resultados/*.csv
Salidas : docs/img/*.png

Uso (desde la raíz del proyecto, después de ejecutar ejecutar_consultas.py):
    python src/graficos.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DIR_RESULTADOS = ROOT / "data" / "processed" / "resultados"
DIR_IMG = ROOT / "docs" / "img"
COLOR_BASE = "#9CA3AF"
COLOR_DESTACADO = "#DC2626"


def grafico_barras(csv: str, columna_categoria: str, titulo: str, nombre_salida: str,
                   columna_valor: str = "tasa_cancelacion_pct", sufijo: str = "%") -> None:
    """Barras horizontales ordenadas; la barra más alta se resalta en rojo."""
    df = pd.read_csv(DIR_RESULTADOS / csv).sort_values(columna_valor)
    colores = [COLOR_DESTACADO if v == df[columna_valor].max() else COLOR_BASE
               for v in df[columna_valor]]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.barh(df[columna_categoria], df[columna_valor], color=colores)
    ax.bar_label(barras, labels=[f"{v:,.1f}{sufijo}" for v in df[columna_valor]], padding=4)
    ax.set_title(titulo, loc="left", fontsize=13, fontweight="bold")
    ax.set_xlabel("")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.set_xlim(0, df[columna_valor].max() * 1.2)
    fig.tight_layout()
    fig.savefig(DIR_IMG / nombre_salida, dpi=150)
    plt.close(fig)
    print(f"Guardado: docs/img/{nombre_salida}")


def grafico_ingreso_perdido() -> None:
    """Ingreso mensual perdido por tipo de servicio, en dólares."""
    df = pd.read_csv(DIR_RESULTADOS / "ingreso_mensual_perdido.csv").sort_values(
        "ingreso_mensual_perdido"
    )
    colores = [COLOR_DESTACADO if v == df["ingreso_mensual_perdido"].max() else COLOR_BASE
               for v in df["ingreso_mensual_perdido"]]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.barh(df["servicio_internet"], df["ingreso_mensual_perdido"], color=colores)
    ax.bar_label(barras, labels=[f"${v:,.0f}" for v in df["ingreso_mensual_perdido"]], padding=4)
    ax.set_title("Ingreso mensual perdido por tipo de servicio (USD)", loc="left",
                 fontsize=13, fontweight="bold")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    ax.tick_params(axis="x", bottom=False, labelbottom=False)
    ax.set_xlim(0, df["ingreso_mensual_perdido"].max() * 1.2)
    fig.tight_layout()
    fig.savefig(DIR_IMG / "ingreso_perdido.png", dpi=150)
    plt.close(fig)
    print("Guardado: docs/img/ingreso_perdido.png")


def main() -> None:
    DIR_IMG.mkdir(parents=True, exist_ok=True)

    grafico_barras("tasa_por_contrato.csv", "tipo_contrato",
                   "Tasa de cancelación por tipo de contrato", "tasa_por_contrato.png")
    grafico_barras("tasa_por_servicio.csv", "servicio_internet",
                   "Tasa de cancelación por tipo de servicio", "tasa_por_servicio.png")
    grafico_barras("tasa_por_antiguedad.csv", "rango_antiguedad",
                   "Tasa de cancelación según antigüedad", "tasa_por_antiguedad.png")
    grafico_barras("tasa_por_metodo_pago.csv", "metodo_pago",
                   "Tasa de cancelación por método de pago", "tasa_por_metodo_pago.png")
    grafico_ingreso_perdido()


if __name__ == "__main__":
    main()
