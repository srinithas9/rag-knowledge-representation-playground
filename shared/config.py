from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
SOURCE_DATA_DIR = DATA_DIR / "source"
NORMALIZED_DATA_DIR = DATA_DIR / "normalized"
QUERY_DATA_DIR = DATA_DIR / "queries"

DEFAULT_TOP_K = 5