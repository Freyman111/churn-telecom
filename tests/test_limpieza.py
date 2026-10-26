"""
Pruebas automáticas para src/limpieza.py.

Uso (desde la raíz del proyecto):
    pip install pytest
    pytest tests/
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from limpieza import limpiar, normalizar_si_no  # noqa: E402


def datos_de_prueba() -> pd.DataFrame:
    """Dataset pequeño con los mismos tipos de error que el dataset real."""
    return pd.DataFrame(
        {
            "customer_id": ["C00001", "C00002", "C00002"],
            "genero": ["Hombre", "Mujer", "Mujer"],
            "adulto_mayor": [0, 1, 1],
            "pareja": ["Sí", "si", "si"],
            "dependientes": ["No", "SÍ", "SÍ"],
            "antiguedad_meses": [10, np.nan, np.nan],
            "tipo_contrato": ["MENSUAL", " anual ", " anual "],
            "metodo_pago": ["Efectivo", "Efectivo", "Efectivo"],
            "facturacion_electronica": ["Sí", "No", "No"],
            "servicio_internet": ["DSL", "Fibra óptica", "Fibra óptica"],
            "cargo_mensual": [50.0, 80.0, 80.0],
            "cargo_total": [500.0, " ", " "],
            "cancelo": ["Sí", "no", "no"],
        }
    )


def test_elimina_duplicados():
    df, reporte = limpiar(datos_de_prueba())
    assert len(df) == 2
    assert reporte["duplicados_eliminados"] == 1


def test_unifica_si_no():
    serie = pd.Series(["Sí", "si", "SÍ", "no", "NO"])
    assert normalizar_si_no(serie).tolist() == ["Sí", "Sí", "Sí", "No", "No"]


def test_normaliza_tipo_contrato():
    df, _ = limpiar(datos_de_prueba())
    assert df["tipo_contrato"].tolist() == ["Mensual", "Anual"]


def test_imputa_cargo_total_con_regla_de_negocio():
    # Cliente C00002: cargo_total vacío -> cargo_mensual (80) * antigüedad imputada (10)
    df, reporte = limpiar(datos_de_prueba())
    cargo = df.loc[df["customer_id"] == "C00002", "cargo_total"].iloc[0]
    assert cargo == 800.0
    assert reporte["cargo_total_imputado"] == 1


def test_crea_variable_objetivo_binaria():
    df, _ = limpiar(datos_de_prueba())
    assert df.loc[df["customer_id"] == "C00001", "cancelo_bin"].iloc[0] == 1
    assert df.loc[df["customer_id"] == "C00002", "cancelo_bin"].iloc[0] == 0


def test_rango_de_antiguedad():
    df, _ = limpiar(datos_de_prueba())
    assert df.loc[df["customer_id"] == "C00001", "rango_antiguedad"].iloc[0] == "0-12 meses"
