import os
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

load_dotenv()

URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

COLUMNAS = [
    "unique_key",
    "created_date",
    "closed_date",
    "descriptor",
    "incident_zip",
    "borough",
    "police_precinct",
    "latitude",
    "longitude",
    "open_data_channel_type",
    "status",
]

LIMIT = 50_000


def rango_mes(anio: int, mes: int) -> tuple[str, str]:
    """Devuelve un rango de fechas para un mes específico en formato ISO 8601.

    Args:
        anio (int): Año en formato de cuatro dígitos (por ejemplo, 2023).
        mes (int): Mes en formato numérico (1-12).

    Returns:
        tuple[str, str]: (inicio, fin). inicio es el primer día del mes y fin el
        primer día del mes siguiente (exclusivo, para usar con `<`).
        Por ejemplo, rango_mes(2025, 12) devuelve
        ("2025-12-01T00:00:00", "2026-01-01T00:00:00").

    Raises:
        ValueError: Si el mes no está entre 1 y 12 (lo lanza pd.Timestamp).
    """

    fecha = pd.Timestamp(anio, mes, 1)
    fecha_inicio = fecha.strftime("%Y-%m-%dT%H:%M:%S")
    fecha_fin = (fecha + pd.DateOffset(months=1)).strftime("%Y-%m-%dT%H:%M:%S")

    return fecha_inicio, fecha_fin


def descargar_mes(
    anio: int, mes: int, complaint_type: str = "Noise - Residential"
) -> pd.DataFrame:
    """Descarga los datos de NYC 311 para un mes en específico y los guarda en un archivo Parquet.

    Args:
        anio (int): Año en formato de cuatro dígitos (por ejemplo, 2026).
        mes (int): Mes en formato numérico (1-12).
        complaint_type (str): Tipo de queja a filtrar. Por defecto es "Noise - Residential".

    Returns:
        pd.DataFrame: DataFrame con las 11 columnas de COLUMNAS; fechas como datetime64 y latitudes y longitudes como números.

    Raises:
        ValueError: Si no se encuentra el token de la aplicación.
        ValueError: Si el mes no está entre 1 y 12 (lo lanza pd.Timestamp).
        requests.HTTPError: Si la solicitud HTTP falla (por ejemplo, por un error de red o un código de estado 4xx/5xx).
    """

    token = os.getenv("NYC_APP_TOKEN")

    if token is None:
        raise ValueError("Falta NYC_APP_TOKEN en el archivo .env")

    headers = {"X-App-Token": token}

    inicio, fin = rango_mes(anio, mes)

    where = (
        f"complaint_type = '{complaint_type}' "
        f"AND created_date >= '{inicio}' "
        f"AND created_date < '{fin}'"
    )

    offset = 0
    paginas = []

    while True:
        params = {
            "$where": where,
            "$select": ",".join(COLUMNAS),
            "$order": "unique_key",
            "$limit": LIMIT,
            "$offset": offset,
        }

        r = requests.get(URL, params=params, headers=headers, timeout=60)
        r.raise_for_status()

        pagina = pd.DataFrame(r.json())
        paginas.append(pagina)
        print(f"offset={offset}, {len(pagina)} filas recibidas")

        if len(pagina) < LIMIT:
            break

        offset += LIMIT

    df = pd.concat(paginas, ignore_index=True)
    df = df.reindex(columns=COLUMNAS)

    df["created_date"] = pd.to_datetime(df["created_date"], errors="coerce")
    df["closed_date"] = pd.to_datetime(df["closed_date"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    ruta = RAW_DIR / f"{anio}-{mes:02d}.parquet"
    df.to_parquet(ruta, index=False)
    print(f"Guardado {ruta.name}: {len(df)} filas")

    return df
