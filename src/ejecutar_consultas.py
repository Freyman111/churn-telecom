"""
PASO 3 · EJECUCIÓN DE CONSULTAS SQL

Ejecuta las consultas de sql/consultas.sql sobre la base SQLite y guarda
cada resultado como CSV en data/processed/resultados/ (listo para Tableau).

Cada consulta empieza con una línea del tipo:  -- @nombre_consulta

Uso (desde la raíz del proyecto):
    python src/ejecutar_consultas.py
"""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUTA_DB = ROOT / "data" / "processed" / "churn.db"
RUTA_SQL = ROOT / "sql" / "consultas.sql"
DIR_RESULTADOS = ROOT / "data" / "processed" / "resultados"


def leer_consultas(ruta: Path) -> dict[str, str]:
    """Separa el archivo .sql en un diccionario {nombre: consulta}."""
    consultas: dict[str, str] = {}
    nombre, lineas = None, []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if linea.startswith("-- @"):
            if nombre and "".join(lineas).strip():
                consultas[nombre] = "\n".join(lineas)
            nombre, lineas = linea[4:].strip(), []
        elif nombre is not None:
            lineas.append(linea)
    if nombre and "".join(lineas).strip():
        consultas[nombre] = "\n".join(lineas)
    return consultas


def main() -> None:
    DIR_RESULTADOS.mkdir(parents=True, exist_ok=True)
    consultas = leer_consultas(RUTA_SQL)

    con = sqlite3.connect(RUTA_DB)
    try:
        for nombre, sql in consultas.items():
            resultado = pd.read_sql_query(sql, con)
            ruta_salida = DIR_RESULTADOS / f"{nombre}.csv"
            resultado.to_csv(ruta_salida, index=False, encoding="utf-8")

            print(f"\n== {nombre} ==")
            print(resultado.to_string(index=False))
    finally:
        con.close()

    print(f"\nResultados guardados en: {DIR_RESULTADOS}")


if __name__ == "__main__":
    main()
