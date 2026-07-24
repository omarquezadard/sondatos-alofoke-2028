# Hallazgos — Estudio Alofoke 2028
# Findings — Alofoke 2028 Study

**SD-2026-001** · SonDatos · división de análisis de SUBROSA / SUBROSA Analysis Division
Corpus: comentarios públicos de YouTube / public YouTube comments, 1 ene 2025 – 11 jul 2026

> 🇩🇴 [Español](#-español) · 🇬🇧 [English](#-english)

---

## 🇩🇴 Español

> Este documento resume los hallazgos con el mismo lenguaje y las mismas cautelas metodológicas del informe público. El diseño es observacional; no establece causalidad. Ver [metodologia.md](metodologia.md) y [validacion.md](validacion.md) para el detalle técnico completo.

### Resumen del corpus

| Etapa | n | Nota |
|---|---|---|
| Comentarios crudos | 207,337 | 481 videos (6 búsquedas temáticas + 4 canales) |
| Excluidos por irrelevancia | 163,113 | No mencionan al sujeto ni provienen de videos monotemáticos |
| Relevantes | 44,224 | |
| Excluidos por spam/duplicación/hiperactividad | 4,606 | Sobre el corpus crudo completo, 35,848 comentarios (17%) presentaron estas señales |
| **Utilizables** | **39,618** | Base del análisis |

### Hallazgo 1 — La brecha comunicador / candidato

Separando la conversación por aspecto temático:

- **Como comunicador/empresario:** net sentiment +0.13 (n=2,156)
- **Como candidato político:** net sentiment −0.40 (n=10,824; agrupa 10,463 comentarios clasificados como "político" + 361 "mixto")

Esta distancia es el hallazgo más robusto del estudio: la comparación es relativamente robusta al sesgo del modelo, bajo el supuesto de que ese sesgo opera de forma similar en ambos aspectos (ver validación).

### Hallazgo 2 — Tendencia temporal

La negatividad base pasó de aproximadamente 32% (marzo 2025) a 54% (julio 2026), en paralelo con un crecimiento explosivo del volumen de conversación. La pendiente de este deterioro es un hallazgo firme porque el sesgo del clasificador es constante en el tiempo.

### Hallazgo 3 — Cambios observados alrededor de eventos clave

Ventanas de ±14 días, z-test de dos colas sobre proporción de comentarios negativos. **Diseño observacional: documenta coincidencias temporales, no causalidad**, y los eventos de junio–julio 2026 se solapan entre sí.

| Evento | Fecha | %Neg pre → post | Δ | p-value |
|---|---|---|---|---|
| Anuncia candidatura independiente | 2025-03-05 | 32.4% → 32.1% | −0.3pp | 0.96 |
| Declara rol de influencia (sin candidatura) | 2025-11-29 | 42.7% → 34.1% | **−8.6pp** | 0.099 (tendencia, no significativa al 5%) |
| Tuit dominical + reacción nacional | 2026-06-21 | 47.4% → 49.5% | +2.0pp | 0.017 * |
| PRSC abre puertas a su candidatura | 2026-06-24 | 49.6% → 48.8% | −0.8pp | 0.25 |
| Fans presionan inicio de campaña | 2026-07-06 | 49.3% → 54.2% | +4.9pp | <0.0001 * |

La única señal favorable medida (tendencia, no significativa al 5%) coincidió con el distanciamiento de la candidatura en noviembre 2025.

### Hallazgo 4 — La paradoja de la rabia (postura vs. tono)

Sobre una muestra estratificada de 396 comentarios, un analista humano etiquetó la **postura** declarada hacia Matías, independientemente del tono del texto:

- Postura clara en 186 de 396 comentarios (47%)
- De esos 186: **72% a favor / 28% en contra** (±6.4pp) — *cifra calculada sobre estos 186 casos, no sobre el corpus completo de 39,618 comentarios*
- 1 de cada 5 comentarios clasificados como negativos por el modelo proviene de personas que declaran apoyo explícito ("hay que sacar esas ratas del poder... yo voto por Santiago")

### Hallazgo 5 — Los modelos subestiman el apoyo en registro dominicano

La validación humana (ver [validacion.md](validacion.md)) muestra que el clasificador detecta el 89% de lo negativo pero solo el 48% de lo positivo. Corrigiendo por esta matriz de confusión:

- Net sentiment global: −0.26 (medido) → **−0.06** (corregido, IC 95% bootstrap: [−0.14, +0.04] — estadísticamente indistinguible de una conversación dividida)
- Net sentiment político: −0.40 (medido) → **−0.30** (corregido, IC 95%: [−0.37, −0.22] — robustamente negativo)

La corrección asume que el error medido en los 396 casos validados es transferible al corpus completo — supuesto razonable dado el muestreo estratificado proporcional, pero un supuesto declarado, no un hecho verificado independientemente.

### Limitaciones

- Sentimiento y postura en YouTube no equivalen a intención de voto ni a representatividad electoral.
- Quienes comentan se autoseleccionan; el perfil demográfico no es el del padrón electoral.
- El sarcasmo y la jerga dominicana degradan la clasificación automática; la validación humana cuantifica ese error y las correcciones lo mitigan, no lo eliminan.
- Los eventos de junio–julio 2026 se solapan; sus efectos individuales no son separables.

---

## 🇬🇧 English

> This document summarizes the findings using the same wording and methodological caveats as the public report. The design is observational; it does not establish causality. See [metodologia.md](metodologia.md) and [validacion.md](validacion.md) (Spanish) for full technical detail.

### Corpus summary

| Stage | n | Note |
|---|---|---|
| Raw comments | 207,337 | 481 videos (6 thematic searches + 4 channels) |
| Excluded for irrelevance | 163,113 | Don't mention the subject or come from single-topic videos |
| Relevant | 44,224 | |
| Excluded for spam/duplication/hyperactivity | 4,606 | Across the full raw corpus, 35,848 comments (17%) showed these signals |
| **Usable** | **39,618** | Analysis base |

### Finding 1 — The communicator / candidate gap

Splitting the conversation by thematic aspect:

- **As communicator/entrepreneur:** net sentiment +0.13 (n=2,156)
- **As political candidate:** net sentiment −0.40 (n=10,824; groups 10,463 comments classified as "political" + 361 "mixed")

This gap is the study's most robust finding: the comparison is relatively robust to model bias, under the assumption that the bias operates similarly across both aspects (see validation).

### Finding 2 — Temporal trend

Baseline negativity rose from roughly 32% (March 2025) to 54% (July 2026), alongside an explosive growth in conversation volume. The slope of this deterioration is a solid finding because the classifier's bias is constant over time.

### Finding 3 — Changes observed around key events

±14-day windows, two-tailed z-test on the proportion of negative comments. **Observational design: documents temporal coincidence, not causation**, and the June–July 2026 events overlap with one another.

| Event | Date | %Neg pre → post | Δ | p-value |
|---|---|---|---|---|
| Announces independent candidacy | 2025-03-05 | 32.4% → 32.1% | −0.3pp | 0.96 |
| Declares an influence role (not running) | 2025-11-29 | 42.7% → 34.1% | **−8.6pp** | 0.099 (trend, not significant at 5%) |
| Sunday tweet + national reaction | 2026-06-21 | 47.4% → 49.5% | +2.0pp | 0.017 * |
| PRSC opens the door to his candidacy | 2026-06-24 | 49.6% → 48.8% | −0.8pp | 0.25 |
| Fans push for a campaign launch | 2026-07-06 | 49.3% → 54.2% | +4.9pp | <0.0001 * |

The only favorable signal measured (a trend, not significant at 5%) coincided with distancing from the candidacy in November 2025.

### Finding 4 — The rage paradox (stance vs. tone)

Over a stratified sample of 396 comments, a human analyst labeled the **stance** declared toward Matías, independent of the text's tone:

- Clear stance in 186 of 396 comments (47%)
- Of those 186: **72% supportive / 28% opposed** (±6.4pp) — *figure calculated over these 186 cases, not over the full 39,618-comment corpus*
- 1 in 5 comments the model classifies as negative comes from people declaring explicit support ("those rats need to go... I'm voting for Santiago")

### Finding 5 — Models underestimate support in Dominican vernacular

Human validation (see [validacion.md](validacion.md)) shows the classifier catches 89% of negative comments but only 48% of positive ones. Correcting for this confusion matrix:

- Global net sentiment: −0.26 (measured) → **−0.06** (corrected, 95% bootstrap CI: [−0.14, +0.04] — statistically indistinguishable from a divided conversation)
- Political net sentiment: −0.40 (measured) → **−0.30** (corrected, 95% CI: [−0.37, −0.22] — robustly negative)

The correction assumes the error measured on the 396 validated cases transfers to the full corpus — a reasonable assumption given proportional stratified sampling, but a stated assumption, not an independently verified fact.

### Limitations

- Sentiment and stance on YouTube do not equal voting intention or electoral representativeness.
- Commenters self-select; the demographic profile is not that of the electoral roll.
- Sarcasm and Dominican vernacular degrade automatic classification; human validation quantifies that error, and the corrections mitigate it without eliminating it.
- The June–July 2026 events overlap; their individual effects are not separable.
