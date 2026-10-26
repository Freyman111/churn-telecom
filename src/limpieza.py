"""
PASO 2 · LIMPIEZA DE DATOS Y CARGA EN SQLITE

Limpia el dataset de clientes y lo carga en una base SQLite.

Entrada : data/raw/clientes_telecom_raw.csv
Salidas : data/processed/clientes_limpios.csv
          data/processed/churn.db  (tabla 'clientes')

Uso (desde la raíz del proyecto):
    python src/limpieza.py
"""
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUTA_RAW = ROOT / "data" / "raw" / "clientes_telecom_raw.csv"
DIR_PROC = ROOT / "data" / "processed"
RUTA_CSV = DIR_PROC / "clientes_limpios.csv"
RUTA_DB = DIR_PROC / "churn.db"

COLUMNAS_SI_NO = ["pareja", "dependientes", "facturacion_electronica", "cancelo"]
MAPA_SI_NO = {"sí": "Sí", "si": "Sí", "no": "No"}


def normalizar_si_no(serie: pd.Series) -> pd.Series:
    """Unifica 'Sí', 'Si', 'si', 'SÍ' -> 'Sí' y 'no' -> 'No'."""
    return serie.astype(str).str.strip().str.lower().map(MAPA_SI_NO)


def limpiar(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Aplica las reglas de limpieza y devuelve el dataframe limpio y un reporte."""
    reporte = {"filas_originales": len(df)}
    df = df.copy()

    # 1. Nombres de columnas en minúsculas y sin espacios
    df.columns = df.columns.str.strip().str.lower()

    # 2. Duplicados (mismo customer_id)
    df = df.drop_duplicates(subset="customer_id", keep="first")
    reporte["duplicados_eliminados"] = reporte["filas_originales"] - len(df)

    # 3. Categorías de texto
    df["tipo_contrato"] = df["tipo_contrato"].astype(str).str.strip().str.capitalize()
    for col in ["genero", "metodo_pago", "servicio_internet"]:
        df[col] = df[col].astype(str).str.strip()

    # 4. Respuestas Sí/No
    for col in COLUMNAS_SI_NO:
        df[col] = normalizar_si_no(df[col])
        reporte[f"sin_mapear_{col}"] = int(df[col].isna().sum())

    # 5. Numéricos: texto vacío o inválido -> NaN
    df["cargo_total"] = pd.to_numeric(
        df["cargo_total"].astype(str).str.strip().replace("", np.nan), errors="coerce"
    )
    df["antiguedad_meses"] = pd.to_numeric(df["antiguedad_meses"], errors="coerce")

    # 6. Imputación de faltantes
    #    - antiguedad_meses: mediana (decisión simple; se puede mejorar)
    #    - cargo_total: cargo_mensual * antiguedad_meses (regla de negocio)
    reporte["antiguedad_imputada"] = int(df["antiguedad_meses"].isna().sum())
    df["antiguedad_meses"] = df["antiguedad_meses"].fillna(df["antiguedad_meses"].median())
    df["antiguedad_meses"] = df["antiguedad_meses"].round().astype(int)

    faltan_cargo = df["cargo_total"].isna()
    reporte["cargo_total_imputado"] = int(faltan_cargo.sum())
    df.loc[faltan_cargo, "cargo_total"] = (
        df.loc[faltan_cargo, "cargo_mensual"] * df.loc[faltan_cargo, "antiguedad_meses"]
    ).round(2)

    # 7. Variables derivadas
    df["cancelo_bin"] = (df["cancelo"] == "Sí").astype(int)
    df["rango_antiguedad"] = pd.cut(
        df["antiguedad_meses"],
        bins=[-1, 12, 24, 48, np.inf],
        labels=["0-12 meses", "13-24 meses", "25-48 meses", "49+ meses"],
    ).astype(str)

    reporte["filas_finales"] = len(df)
    return df.reset_index(drop=True), reporte


def main() -> None:
    DIR_PROC.mkdir(parents=True, exist_ok=True)

    df_raw = pd.read_csv(RUTA_RAW)
    df, reporte = limpiar(df_raw)

    df.to_csv(RUTA_CSV, index=False, encoding="utf-8")

    con = sqlite3.connect(RUTA_DB)
    try:
        df.to_sql("clientes", con, if_exists="replace", index=False)
    finally:
        con.close()

    print("Reporte de limpieza:")
    for clave, valor in reporte.items():
        print(f"  {clave}: {valor}")
    print(f"\nCSV limpio : {RUTA_CSV}")
    print(f"SQLite     : {RUTA_DB} (tabla 'clientes')")


if __name__ == "__main__":
    main()
