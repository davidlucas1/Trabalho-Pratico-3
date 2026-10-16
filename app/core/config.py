from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_URL = f"sqlite:///{(BASE_DIR / 'biblioteca.db').as_posix()}"
