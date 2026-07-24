"""Paso 6 — Validación manual del modelo.

Después de etiquetar a mano output/validation/sample_to_label.csv
(columnas 'etiqueta_manual' con POS/NEU/NEG), este script calcula:
  - Matriz de confusión
  - Accuracy global y F1 macro
  - Precisión/recall por clase
  - Acuerdo en aspecto (si llenaste 'aspecto_manual')

Estos números van en la sección de metodología del informe web —
son tu sello de rigor frente a las "encuestas" sin método.
"""
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

from utils import OUTPUT


def main():
    path = OUTPUT / "validation" / "sample_to_label.csv"
    df = pd.read_csv(path)
    labeled = df[df["etiqueta_manual"].isin(["POS", "NEU", "NEG"])]
    if labeled.empty:
        raise SystemExit(
            "No hay etiquetas manuales todavía. Llena la columna "
            "'etiqueta_manual' (POS/NEU/NEG) en sample_to_label.csv"
        )
    print(f"Comentarios validados: {len(labeled)} / {len(df)}\n")

    y_true = labeled["etiqueta_manual"]
    y_pred = labeled["sentiment"]

    print("Matriz de confusión (filas=manual, columnas=modelo):")
    cm = pd.DataFrame(
        confusion_matrix(y_true, y_pred, labels=["POS", "NEU", "NEG"]),
        index=["POS", "NEU", "NEG"],
        columns=["POS", "NEU", "NEG"],
    )
    print(cm.to_string(), "\n")
    print(classification_report(y_true, y_pred, digits=3))

    if labeled["aspecto_manual"].notna().any() and (labeled["aspecto_manual"] != "").any():
        asp = labeled[labeled["aspecto_manual"] != ""]
        agree = (asp["aspecto_manual"] == asp["aspect"]).mean()
        print(f"Acuerdo en aspecto (reglas vs. manual): {agree:.1%} (n={len(asp)})")

    report_path = OUTPUT / "validation" / "validation_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Validación manual — n={len(labeled)}\n\n")
        f.write("Matriz de confusión (filas=manual, columnas=modelo):\n")
        f.write(cm.to_string() + "\n\n")
        f.write(classification_report(y_true, y_pred, digits=3))
    print(f"\nGuardado: {report_path}")


if __name__ == "__main__":
    main()
