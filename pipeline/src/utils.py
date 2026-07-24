"""Utilidades compartidas del pipeline SonDatos."""
import os
import re
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_PROC = ROOT / "data" / "processed"
OUTPUT = ROOT / "output"


def load_config() -> dict:
    with open(ROOT / "config.yaml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_youtube_client():
    """Cliente de YouTube Data API v3. Requiere env var YT_API_KEY."""
    from googleapiclient.discovery import build

    api_key = os.environ.get("YT_API_KEY")
    if not api_key:
        raise SystemExit(
            "Falta la API key. Ejecuta: export YT_API_KEY='tu_key'\n"
            "(Google Cloud Console -> APIs -> YouTube Data API v3 -> Credentials)"
        )
    return build("youtube", "v3", developerKey=api_key)


def resolve_channel(handle_or_name: str) -> None:
    """Busca el channel ID de un canal por nombre o @handle.

    Uso: python src/utils.py "Alofoke Radio Show"
    """
    yt = get_youtube_client()
    resp = yt.search().list(
        q=handle_or_name, type="channel", part="snippet", maxResults=5
    ).execute()
    for item in resp.get("items", []):
        print(f"{item['snippet']['title']:40s}  {item['snippet']['channelId']}")


def normalize_text(text: str) -> str:
    """Minúsculas + sin acentos, para matching de keywords."""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))


def clean_for_model(text: str) -> str:
    """Limpieza ligera pre-inferencia (robertuito maneja emojis y jerga)."""
    text = re.sub(r"https?://\S+", "", text)          # URLs
    text = re.sub(r"@[A-Za-z0-9_.-]+", "@usuario", text)  # menciones
    text = re.sub(r"\s+", " ", text).strip()
    return text


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        resolve_channel(" ".join(sys.argv[1:]))
    else:
        print("Uso: python src/utils.py 'Nombre del canal'")
