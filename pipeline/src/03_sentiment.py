"""Paso 3 — Inferencia de sentimiento (pysentimiento / robertuito).

Entrada:  data/processed/comments_clean.parquet
Salida:   data/processed/comments_scored.parquet
          output/validation/sample_to_label.csv  (muestra para etiquetado manual)

El mismo stack del TFM: robertuito-sentiment-analysis (POS/NEU/NEG con
probabilidades). Corre en batches; en CPU procesa ~2,000-4,000 comentarios/min,
con GPU (MPS en Mac o CUDA) mucho más.

Nota: la primera ejecución descarga el modelo (~500 MB) de Hugging Face.
"""
import numpy as np
import pandas as pd

from utils import DATA_PROC, OUTPUT, load_config

CFG = load_config()
BATCH = 128


def main():
    from pysentimiento import create_analyzer

    df = pd.read_parquet(DATA_PROC / "comments_clean.parquet")
    work = df[df["relevant"] & ~df["bot_flag"]].copy()
    print(f"Comentarios a clasificar: {len(work):,}")

    analyzer = create_analyzer(task="sentiment", lang="es")

    labels, p_pos, p_neu, p_neg = [], [], [], []
    texts = work["text_model"].tolist()
    for i in range(0, len(texts), BATCH):
        batch = texts[i : i + BATCH]
        results = analyzer.predict(batch)
        for r in results:
            labels.append(r.output)
            p_pos.append(r.probas.get("POS", 0.0))
            p_neu.append(r.probas.get("NEU", 0.0))
            p_neg.append(r.probas.get("NEG", 0.0))
        if (i // BATCH) % 20 == 0:
            print(f"  {i + len(batch):,}/{len(texts):,}")

    work["sentiment"] = labels
    work["p_pos"] = p_pos
    work["p_neu"] = p_neu
    work["p_neg"] = p_neg
    # score continuo [-1, 1] útil para promedios ponderados
    work["score"] = work["p_pos"] - work["p_neg"]
    # confianza del modelo (máxima probabilidad)
    work["confidence"] = work[["p_pos", "p_neu", "p_neg"]].max(axis=1)

    work.to_parquet(DATA_PROC / "comments_scored.parquet", index=False)
    print(f"\nGuardado: {DATA_PROC / 'comments_scored.parquet'}")
    print(work["sentiment"].value_counts(normalize=True).round(3).to_string())

    # --- muestra estratificada para validación manual ---
    n = CFG["validation"]["sample_size"]
    strat = CFG["validation"]["stratify_by"]
    sample = (
        work.groupby(strat, group_keys=False)
        .apply(lambda g: g.sample(min(len(g), max(1, int(n * len(g) / len(work)))), random_state=33))
        .head(n)
    )
    val_dir = OUTPUT / "validation"
    val_dir.mkdir(parents=True, exist_ok=True)
    cols = ["comment_id", "text", "sentiment", "aspect", "confidence"]
    out = sample[cols].copy()
    out["etiqueta_manual"] = ""  # POS / NEU / NEG — llenar a mano
    out["aspecto_manual"] = ""   # politico / entretenimiento / mixto / general
    out.to_csv(val_dir / "sample_to_label.csv", index=False, encoding="utf-8-sig")
    print(f"\nMuestra de validación ({len(out)}): {val_dir / 'sample_to_label.csv'}")
    print("Etiquétala a mano y luego corre: python src/06_validate.py")


if __name__ == "__main__":
    main()
