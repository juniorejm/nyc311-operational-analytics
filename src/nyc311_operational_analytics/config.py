from pathlib import Path

from dotenv import load_dotenv

# Raíz del repositorio: config.py -> nyc311_operational_analytics -> src -> raíz
PROJ_ROOT = Path(__file__).resolve().parents[2]

# Carpetas de datos
DATA_DIR = PROJ_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"

# Salidas
FIGURES_DIR = PROJ_ROOT / "reports" / "figures"

# Variables de entorno (Token de NYC Open Data)
load_dotenv(PROJ_ROOT / ".env")
