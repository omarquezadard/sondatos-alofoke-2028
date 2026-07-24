"""Paso 4 — Análisis: series temporales, IC bootstrap y comparación por evento.

Entrada:  data/processed/comments_scored.parquet
Salida:   data/processed/weekly.csv          serie semanal con IC 95%
          data/processed/by_aspect.csv       serie semanal por aspecto
          data/processed/event_impact.csv    pre/post por evento (z-test proporciones)
          output/summary.md                  resumen de hallazgos en texto

Métrica principal: NET SENTIMENT = %POS - %NEG (por bucket semanal),
con IC 95% por bootstrap. Igual que en el TFM: reportamos incertidumbre,
no solo el punto.
"""
import numpy as np
import pandas as pd
from scipy import stats

from utils import DATA_PROC, OUTPUT, load_config

CFG = load_config()
RNG = np.random.default_rng(33)


def net_sentiment_ci(labels: pd.Series, n_boot: int) -> tuple[float, float, float]:
    """Net sentiment con IC 95% por bootstrap."""
    arr = labels.map({"POS": 1, "NEU": 0, "NEG": -1}).to_numpy()
    point = arr.mean()
    if len(arr) < 5:
        return point, np.nan, np.nan
    boots = RNG.choice(arr, size=(n_boot, len(arr)), replace=True).mean(axis=1)
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return point, lo, hi


def weekly_series(df: pd.DataFrame) -> pd.DataFrame:
    n_boot = CFG["analysis"]["bootstrap_iterations"]
    freq = CFG["analysis"]["aggregation"]
    min_n = CFG["analysis"]["min_comments_per_bucket"]

    rows = []
    for week, g in df.groupby(pd.Grouper(key="published_at", freq=freq)):
        if g.empty:
            continue
        point, lo, hi = net_sentiment_ci(g["sentiment"], n_boot)
        rows.append(
            {
                "week": week,
                "n": len(g),
                "pct_pos": (g["sentiment"] == "POS").mean(),
                "pct_neu": (g["sentiment"] == "NEU").mean(),
                "pct_neg": (g["sentiment"] == "NEG").mean(),
                "net_sentiment": point,
                "ci_low": lo,
                "ci_high": hi,
                "low_confidence": len(g) < min_n,
            }
        )
    return pd.DataFrame(rows)


def event_impact(df: pd.DataFrame) -> pd.DataFrame:
    """Comparación pre/post por evento: z-test de proporciones sobre %NEG
    y diferencia de net sentiment."""
    win = pd.Timedelta(days=CFG["analysis"]["event_window_days"])
    rows = []
    for ev in CFG["events"]:
        d = pd.Timestamp(ev["date"], tz="UTC")
        pre = df[(df["published_at"] >= d - win) & (df["published_at"] < d)]
        post = df[(df["published_at"] >= d) & (df["published_at"] < d + win)]
        if len(pre) < 20 or len(post) < 20:
            rows.append({"event": ev["short"], "date": ev["date"],
                         "n_pre": len(pre), "n_post": len(post),
                         "note": "muestra insuficiente"})
            continue

        neg_pre = (pre["sentiment"] == "NEG").sum()
        neg_post = (post["sentiment"] == "NEG").sum()
        p_pool = (neg_pre + neg_post) / (len(pre) + len(post))
        se = np.sqrt(p_pool * (1 - p_pool) * (1 / len(pre) + 1 / len(post)))
        z = ((neg_post / len(post)) - (neg_pre / len(pre))) / se if se > 0 else np.nan
        p_val = 2 * (1 - stats.norm.cdf(abs(z))) if not np.isnan(z) else np.nan

        ns_pre, *_ = net_sentiment_ci(pre["sentiment"], 500)
        ns_post, *_ = net_sentiment_ci(post["sentiment"], 500)

        rows.append(
            {
                "event": ev["short"],
                "date": ev["date"],
                "n_pre": len(pre),
                "n_post": len(post),
                "pct_neg_pre": neg_pre / len(pre),
                "pct_neg_post": neg_post / len(post),
                "delta_neg_pp": (neg_post / len(post) - neg_pre / len(pre)) * 100,
                "z": z,
                "p_value": p_val,
                "net_pre": ns_pre,
                "net_post": ns_post,
                "delta_net": ns_post - ns_pre,
                "note": "",
            }
        )
    return pd.DataFrame(rows)


def main():
    df = pd.read_parquet(DATA_PROC / "comments_scored.parquet")
    print(f"Comentarios clasificados: {len(df):,}")

    weekly = weekly_series(df)
    weekly.to_csv(DATA_PROC / "weekly.csv", index=False)

    by_aspect = []
    for aspect, g in df.groupby("aspect"):
        w = weekly_series(g)
        w["aspect"] = aspect
        by_aspect.append(w)
    pd.concat(by_aspect).to_csv(DATA_PROC / "by_aspect.csv", index=False)

    impact = event_impact(df)
    impact.to_csv(DATA_PROC / "event_impact.csv", index=False)

    # --- resumen en texto ---
    total = len(df)
    dist = df["sentiment"].value_counts(normalize=True)
    ns_global, lo, hi = net_sentiment_ci(df["sentiment"], 2000)
    pol = df[df["aspect"].isin(["politico", "mixto"])]
    ns_pol, plo, phi = net_sentiment_ci(pol["sentiment"], 2000)
    ent = df[df["aspect"] == "entretenimiento"]
    ns_ent, elo, ehi = net_sentiment_ci(ent["sentiment"], 2000) if len(ent) else (np.nan,) * 3

    lines = [
        "# Resumen — Sentimiento hacia Alofoke (contexto electoral 2028)",
        f"\n- **Comentarios analizados:** {total:,}",
        f"- **Distribución global:** POS {dist.get('POS', 0):.1%} | NEU {dist.get('NEU', 0):.1%} | NEG {dist.get('NEG', 0):.1%}",
        f"- **Net sentiment global:** {ns_global:+.3f} (IC 95%: [{lo:+.3f}, {hi:+.3f}])",
        f"- **Net sentiment aspecto POLÍTICO:** {ns_pol:+.3f} (IC 95%: [{plo:+.3f}, {phi:+.3f}]) — n={len(pol):,}",
        f"- **Net sentiment aspecto ENTRETENIMIENTO:** {ns_ent:+.3f} — n={len(ent):,}",
        "\n## Impacto por evento (ventanas de "
        f"{CFG['analysis']['event_window_days']} días pre/post)\n",
        impact.to_markdown(index=False),
        "\n*Los p-values corresponden a z-test de dos colas sobre la proporción de",
        "comentarios negativos pre vs. post evento.*",
    ]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\nResumen: {OUTPUT / 'summary.md'}")
    print("\n".join(lines[:6]))


if __name__ == "__main__":
    main()
