from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def get_data_path(filename: str = "bank_churn.csv") -> Path:
    """Return the path to a dataset file in the data directory."""
    return DATA_DIR / filename


def list_available_data_files() -> list[str]:
    if not DATA_DIR.exists():
        return []
    return sorted([p.name for p in DATA_DIR.iterdir() if p.is_file()])
