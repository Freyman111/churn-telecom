"""
PASO 1 · GENERACIÓN DE DATOS SINTÉTICOS

Genera un dataset sintético de clientes de telecomunicaciones.

El archivo resultante incluye errores intencionales (duplicados, textos
inconsistentes, valores vacíos) para practicar la limpieza de datos.

Uso (desde la raíz del proyecto):
    python src/generar_datos.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUTA_SALIDA = ROOT / "data" / "raw" / "clientes_telecom_raw.csv"
SEMILLA = 42
N_CLIENTES = 7000


def generar_clientes(n: int, rng: np.random.Generator) -> pd.DataFrame:
    """Crea clientes con una probabilidad de cancelación que depende de sus atributos."""
    servicio = rng.choice(["DSL", "Fibra óptica", "Ninguno"], size=n, p=[0.35, 0.42, 0.23])
    tipo_contrato = rng.choice(["Mensual", "Anual", "Bienal"], size=n, p=[0.55, 0.25, 0.20])
    metodo_pago = rng.choice(
        ["Transferencia bancaria", "Tarjeta de crédito", "Cheque electrónico", "Efectivo"],
        size=n,
        p=[0.25, 0.25, 0.35, 0.15],
    )
    adulto_mayor = rng.binomial(1, 0.16, size=n)
    antiguedad = rng.integers(0, 73, size=n)
    ruido = rng.normal(0, 1, size=n)

    cargo_mensual = np.where(
        servicio == "Fibra óptica",
        85 + 12 * ruido,
        np.where(servicio == "DSL", 55 + 8 * ruido, 25 + 5 * ruido),
    )
    cargo_mensual = np.round(np.clip(cargo_mensual, 18, None), 2)
    cargo_total = np.round(cargo_mensual * antiguedad * rng.uniform(0.95, 1.02, size=n), 2)

    # Probabilidad de cancelar (regresión logística simplificada)
    logit = (
        -1.2
        + 0.9 * (tipo_contrato == "Mensual")
        - 0.8 * (tipo_contrato == "Bienal")
        - 0.02 * antiguedad
        + 0.6 * (servicio == "Fibra óptica")
        + 0.5 * (metodo_pago == "Cheque electrónico")
        + 0.4 * adulto_mayor
        + 0.01 * (cargo_mensual - 60)
    )
    prob = 1 / (1 + np.exp(-logit))
    cancelo = np.where(rng.uniform(size=n) < prob, "Sí", "No")

    return pd.DataFrame(
        {
            "customer_id": [f"C{i:05d}" for i in range(1, n + 1)],
            "genero": rng.choice(["Hombre", "Mujer"], size=n),
            "adulto_mayor": adulto_mayor,
            "pareja": rng.choice(["Sí", "No"], size=n, p=[0.48, 0.52]),
            "dependientes": rng.choice(["Sí", "No"], size=n, p=[0.30, 0.70]),
            "antiguedad_meses": antiguedad,
            "tipo_contrato": tipo_contrato,
            "metodo_pago": metodo_pago,
            "facturacion_electronica": rng.choice(["Sí", "No"], size=n, p=[0.60, 0.40]),
            "servicio_internet": servicio,
            "cargo_mensual": cargo_mensual,
            "cargo_total": cargo_total,
            "cancelo": cancelo,
        }
    )


def ensuciar(df: pd.DataFrame, rng: np.random.Generator) -> pd.DataFrame:
    """Introduce errores típicos de datos reales."""
    n = len(df)
    df = df.copy()

    # 1. Textos inconsistentes en tipo_contrato (mayúsculas y espacios)
    idx = rng.choice(n, size=int(0.08 * n), replace=False)
    estilo = rng.choice(["mayusculas", "espacios"], size=len(idx))
    df.loc[idx, "tipo_contrato"] = [
        v.upper() if e == "mayusculas" else f" {v} "
        for v, e in zip(df.loc[idx, "tipo_contrato"], estilo)
    ]

    # 2. Respuestas Sí/No escritas de formas distintas
    for col in ["pareja", "dependientes"]:
        candidatos = df.index[df[col] == "Sí"]
        idx = rng.choice(candidatos, size=int(0.05 * n), replace=False)
        df.loc[idx, col] = rng.choice(["Si", "si", "SÍ"], size=len(idx))

    # 3. cargo_total vacío (un espacio en blanco)
    idx = rng.choice(n, size=int(0.015 * n), replace=False)
    df["cargo_total"] = df["cargo_total"].astype(object)
    df.loc[idx, "cargo_total"] = " "

    # 4. antiguedad_meses faltante
    idx = rng.choice(n, size=int(0.02 * n), replace=False)
    df["antiguedad_meses"] = df["antiguedad_meses"].astype(float)
    df.loc[idx, "antiguedad_meses"] = np.nan
    df["antiguedad_meses"] = df["antiguedad_meses"].astype("Int64")

    # 5. Filas duplicadas
    duplicados = df.sample(n=int(0.02 * n), random_state=SEMILLA)
    df = pd.concat([df, duplicados]).sample(frac=1, random_state=SEMILLA)
    return df.reset_index(drop=True)


def main() -> None:
    rng = np.random.default_rng(SEMILLA)
    df = generar_clientes(N_CLIENTES, rng)
    df = ensuciar(df, rng)

    RUTA_SALIDA.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(RUTA_SALIDA, index=False, encoding="utf-8")
    print(f"Dataset generado: {len(df)} filas -> {RUTA_SALIDA}")


if __name__ == "__main__":
    main()
