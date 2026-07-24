"""Paso 2 — Limpieza, filtro de relevancia, aspecto y heurísticas anti-bot.

Entrada:  data/raw/comments.parquet
Salida:   data/processed/comments_clean.parquet

Reglas:
  - Relevancia: el comentario menciona al sujeto, O el título del video es
    monotemático (sujeto + keyword política) y el comentario supera min_chars.
  - Aspecto: 'politico' / 'entretenimiento' / 'mixto' / 'general' por keywords.
  - Bots/spam: texto duplicado masivo, comentarios sin contenido léxico,
    autores hiperactivos en un mismo video. Se MARCAN (flag), no se borran,
    para poder reportar cuánto tráfico se filtró.
"""
import pandas as pd

from utils import DATA_PROC, DATA_RAW, clean_for_model, load_config, normalize_text

CFG = load_config()


def tag_aspect(text_norm: str, kw_pol: list[str], kw_ent: list[str]) -> str:
    has_pol = any(k in text_norm for k in kw_pol)
    has_ent = any(k in text_norm for k in kw_ent)
    if has_pol and has_ent:
        return "mixto"
    if has_pol:
        return "politico"
    if has_ent:
        return "entretenimiento"
    return "general"


def main():
    df = pd.read_parquet(DATA_RAW / "comments.parquet")
    n0 = len(df)
    print(f"Comentarios crudos: {n0:,}")

    # --- normalización ---
    df["published_at"] = pd.to_datetime(df["published_at"], utc=True, errors="coerce")
    df = df.dropna(subset=["published_at", "text"])
    df["text_norm"] = df["text"].map(normalize_text)
    df["text_model"] = df["text"].map(clean_for_model)

    # --- filtro de ventana temporal ---
    start = pd.Timestamp(CFG["study"]["date_start"], tz="UTC")
    end = pd.Timestamp(CFG["study"]["date_end"], tz="UTC")
    df = df[(df["published_at"] >= start) & (df["published_at"] <= end)]

    # --- relevancia ---
    rel = CFG["relevance"]
    subj = [normalize_text(k) for k in rel["subject_keywords"]]
    pol = [normalize_text(k) for k in rel["political_keywords"]]

    df["video_title_norm"] = df["video_title"].map(normalize_text)
    video_is_topical = df["video_title_norm"].map(
        lambda t: any(k in t for k in subj) and any(k in t for k in pol)
    )
    comment_mentions = df["text_norm"].map(lambda t: any(k in t for k in subj))
    long_enough = df["text_model"].str.len() >= rel["min_chars"]

    df["relevant"] = (comment_mentions | video_is_topical) & long_enough
    print(f"Relevantes: {df['relevant'].sum():,} / {len(df):,}")

    # --- aspecto ---
    kw_pol = [normalize_text(k) for k in CFG["aspects"]["politico"]]
    kw_ent = [normalize_text(k) for k in CFG["aspects"]["entretenimiento"]]
    df["aspect"] = df["text_norm"].map(lambda t: tag_aspect(t, kw_pol, kw_ent))

    # --- heurísticas anti-bot ---
    bf = CFG["bot_filter"]
    dup_counts = df.groupby("text_norm")["comment_id"].transform("count")
    flag_dup = dup_counts > bf["max_duplicate_text"]

    flag_low_content = df["text_norm"].map(
        lambda t: len(set(c for c in t if c.isalpha())) < bf["min_unique_chars"]
    )

    per_author = df.groupby(["video_id", "author"])["comment_id"].transform("count")
    flag_hyper = per_author > bf["max_comments_per_author_per_video"]

    df["bot_flag"] = flag_dup | flag_low_content | flag_hyper
    print(
        f"Marcados como spam/bot: {df['bot_flag'].sum():,} "
        f"(dup: {flag_dup.sum():,}, sin contenido: {flag_low_content.sum():,}, "
        f"hiperactivos: {flag_hyper.sum():,})"
    )

    out = df.drop(columns=["video_title_norm"])
    DATA_PROC.mkdir(parents=True, exist_ok=True)
    out.to_parquet(DATA_PROC / "comments_clean.parquet", index=False)

    usable = out[out["relevant"] & ~out["bot_flag"]]
    print(f"\nDataset final utilizable: {len(usable):,} comentarios")
    print(usable["aspect"].value_counts().to_string())
    print(f"\nGuardado: {DATA_PROC / 'comments_clean.parquet'}")


if __name__ == "__main__":
    main()
