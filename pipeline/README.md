# Pipeline de línea de comandos (YouTube)
# Command-Line Pipeline (YouTube)

> 🇩🇴 [Español](#-español) · 🇬🇧 [English](#-english)

---

## 🇩🇴 Español

Versión de terminal del pipeline, para quien prefiera correr la recolección localmente en vez de en Colab. El paso de clasificación de sentimiento (pysentimiento) requiere PyTorch, que puede dar conflictos de versión en Python muy reciente (3.13+) — en ese caso, usa `notebooks/SonDatos_Pipeline_YouTube.ipynb` en Colab para ese paso puntual, que además corre con GPU gratuita.

### Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export YT_API_KEY='tu_api_key'   # Google Cloud Console → YouTube Data API v3 → Credenciales
```

### Ejecución (en orden)

| Paso | Comando | Salida |
|---|---|---|
| 1. Recolección | `python src/01_collect_youtube.py` | `data/raw/comments.parquet` |
| 2. Limpieza + relevancia + anti-bot | `python src/02_preprocess.py` | `data/processed/comments_clean.parquet` |
| 3. Sentimiento (robertuito) | `python src/03_sentiment.py` *(o el notebook de Colab)* | `comments_scored.parquet` + muestra de validación |
| 4. Análisis (series, IC, eventos) | `python src/04_analyze.py` | `weekly.csv`, `event_impact.csv`, `output/summary.md` |
| 5. Gráficos (web + IG 4:5) | `python src/05_charts.py` | `output/charts/*.png` |
| 6. Validación manual | etiquetar CSV → `python src/06_validate.py` | matriz de confusión + reporte |

`config.yaml` contiene la configuración usada en el estudio Alofoke 2028 (sujeto, keywords, eventos, marca). Para un estudio nuevo, edítalo — es el único archivo que cambia entre estudios.

Los datos crudos y procesados (`data/raw/`, `data/processed/*.parquet`) no se versionan (ver `.gitignore` en la raíz del repositorio): contienen texto y autor de comentarios individuales.

---

## 🇬🇧 English

Terminal version of the pipeline, for anyone who prefers to run the collection step locally instead of in Colab. The sentiment classification step (pysentimiento) requires PyTorch, which can hit version conflicts on very recent Python (3.13+) — if that happens, use `notebooks/SonDatos_Pipeline_YouTube.ipynb` in Colab for that specific step, which also runs on a free GPU.

### Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export YT_API_KEY='your_api_key'   # Google Cloud Console → YouTube Data API v3 → Credentials
```

### Running it (in order)

| Step | Command | Output |
|---|---|---|
| 1. Collection | `python src/01_collect_youtube.py` | `data/raw/comments.parquet` |
| 2. Cleaning + relevance + anti-bot | `python src/02_preprocess.py` | `data/processed/comments_clean.parquet` |
| 3. Sentiment (robertuito) | `python src/03_sentiment.py` *(or the Colab notebook)* | `comments_scored.parquet` + validation sample |
| 4. Analysis (series, CI, events) | `python src/04_analyze.py` | `weekly.csv`, `event_impact.csv`, `output/summary.md` |
| 5. Charts (web + IG 4:5) | `python src/05_charts.py` | `output/charts/*.png` |
| 6. Manual validation | label the CSV → `python src/06_validate.py` | confusion matrix + report |

`config.yaml` holds the configuration used for the Alofoke 2028 study (subject, keywords, events, branding). For a new study, edit it — it's the only file that changes between studies.

Raw and processed data (`data/raw/`, `data/processed/*.parquet`) are not version-controlled (see `.gitignore` at the repository root): they contain individual comment text and author handles.
