"""Paso 5 — Gráficos con identidad SonDatos (IG 4:5 y versión web).

Entrada:  data/processed/weekly.csv, by_aspect.csv, event_impact.csv
Salida:   output/charts/*.png  (versión web 16:9 y versión IG 1080x1350)

Principios: título = hallazgo (no descripción), IC 95% como banda,
eventos anotados, fondo oscuro de marca, fuente de datos al pie.
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

from utils import DATA_PROC, OUTPUT, load_config

CFG = load_config()
B = CFG["brand"]["colors"]
CHARTS = OUTPUT / "charts"
FOOTER = f"Fuente: comentarios públicos de YouTube · Modelo: robertuito · {CFG['brand']['name']} — {CFG['brand']['url']}"


def _style(ax, fig):
    fig.patch.set_facecolor(B["background"])
    ax.set_facecolor(B["background"])
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(B["neutral"])
    ax.tick_params(colors=B["text"], labelsize=11)
    ax.yaxis.label.set_color(B["text"])
    ax.xaxis.label.set_color(B["text"])
    ax.grid(True, alpha=0.25, color="#D8CDD4")


def _footer(fig):
    fig.text(0.5, 0.015, FOOTER, ha="center", fontsize=7.5, color=B["neutral"])


def _events(ax, ymax):
    for ev in CFG["events"]:
        d = pd.Timestamp(ev["date"])
        ax.axvline(d, color=B["accent"], alpha=0.5, linewidth=1, linestyle="--")
        ax.annotate(
            ev["short"], xy=(d, ymax), fontsize=10, color=B["accent"],
            rotation=90, va="top", ha="right", alpha=0.9,
        )


def _save(fig, name):
    CHARTS.mkdir(parents=True, exist_ok=True)
    # versión web
    fig.savefig(CHARTS / f"{name}_web.png", dpi=300, bbox_inches="tight",
                facecolor=B["background"])
    # versión IG 4:5
    w, h = CFG["brand"]["ig_format"]
    fig.set_size_inches(w / 150, h / 150)
    fig.savefig(CHARTS / f"{name}_ig.png", dpi=150, bbox_inches="tight",
                facecolor=B["background"])
    plt.close(fig)
    print(f"  {name} ✓")


def chart_timeline(weekly: pd.DataFrame, title: str):
    weekly["week"] = pd.to_datetime(weekly["week"])
    fig, ax = plt.subplots(figsize=(12, 6))
    _style(ax, fig)

    ax.fill_between(weekly["week"], weekly["ci_low"], weekly["ci_high"],
                    color=B["positive"], alpha=0.12, label="IC 95%")
    ax.plot(weekly["week"], weekly["net_sentiment"], color=B["positive"],
            linewidth=2.8, label="Net sentiment (%POS − %NEG)")
    ax.axhline(0, color=B["neutral"], linewidth=0.8)
    _events(ax, ax.get_ylim()[1])

    ax.set_title(title, color=B["text"], fontsize=17, fontweight="bold", pad=18)
    ax.set_ylabel("Net sentiment")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    leg = ax.legend(loc="lower left", frameon=False, fontsize=11)
    for t in leg.get_texts():
        t.set_color(B["text"])
    _footer(fig)
    _save(fig, "01_timeline")


def chart_aspects(by_aspect: pd.DataFrame):
    by_aspect["week"] = pd.to_datetime(by_aspect["week"])
    fig, ax = plt.subplots(figsize=(12, 6))
    _style(ax, fig)
    colors = {"politico": B["negative"], "entretenimiento": B["positive"],
              "mixto": B["accent"], "general": B["neutral"]}
    names = {"politico": "Como candidato", "entretenimiento": "Como comunicador",
             "mixto": "Mixto", "general": "General"}
    for aspect in ["politico", "entretenimiento"]:
        g = by_aspect[by_aspect["aspect"] == aspect]
        if g.empty:
            continue
        ax.plot(g["week"], g["net_sentiment"].rolling(2, min_periods=1).mean(),
                color=colors[aspect], linewidth=2.8, label=names[aspect])
    ax.axhline(0, color=B["neutral"], linewidth=0.8)
    ax.set_title("¿Lo quieren como comunicador… y como candidato?",
                 color=B["text"], fontsize=17, fontweight="bold", pad=18)
    ax.set_ylabel("Net sentiment")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    leg = ax.legend(loc="lower left", frameon=False, fontsize=11)
    for t in leg.get_texts():
        t.set_color(B["text"])
    _footer(fig)
    _save(fig, "02_aspectos")


def chart_events(impact: pd.DataFrame):
    if "note" in impact:
        imp = impact[impact["note"].fillna("") == ""].copy()
    else:
        imp = impact.copy()
    if imp.empty:
        print("  [!] Sin eventos con muestra suficiente")
        return
    fig, ax = plt.subplots(figsize=(11, 6))
    _style(ax, fig)
    colors = [B["negative"] if d < 0 else B["positive"] for d in imp["delta_net"]]
    bars = ax.barh(imp["event"], imp["delta_net"], color=colors)
    for bar, (_, row) in zip(bars, imp.iterrows()):
        sig = " *" if row.get("p_value", 1) < 0.05 else ""
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f' {row["delta_net"]:+.2f}{sig}', va="center", fontsize=9,
                color=B["text"])
    ax.axvline(0, color=B["neutral"], linewidth=0.8)
    ax.set_title("Cambio en el sentimiento tras cada evento clave",
                 color=B["text"], fontsize=17, fontweight="bold", pad=18)
    ax.set_xlabel("Δ Net sentiment (post − pre, ventana ±14 días)  ·  * p<0.05")
    _footer(fig)
    _save(fig, "03_eventos")


def chart_volume(weekly: pd.DataFrame):
    weekly["week"] = pd.to_datetime(weekly["week"])
    fig, ax = plt.subplots(figsize=(12, 5))
    _style(ax, fig)
    ax.bar(weekly["week"], weekly["n"], width=6, color=B["accent"], alpha=0.85)
    _events(ax, ax.get_ylim()[1])
    ax.set_title("Volumen de conversación por semana", color=B["text"],
                 fontsize=17, fontweight="bold", pad=18)
    ax.set_ylabel("Comentarios")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %y"))
    _footer(fig)
    _save(fig, "04_volumen")


def main():
    weekly = pd.read_csv(DATA_PROC / "weekly.csv")
    by_aspect = pd.read_csv(DATA_PROC / "by_aspect.csv")
    impact = pd.read_csv(DATA_PROC / "event_impact.csv")

    print("Generando gráficos:")
    chart_timeline(weekly, "Sentimiento hacia Alofoke en la conversación política")
    chart_aspects(by_aspect)
    chart_events(impact)
    chart_volume(weekly)
    print(f"\nListo: {CHARTS}")


if __name__ == "__main__":
    main()
