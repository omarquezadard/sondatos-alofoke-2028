# Hallazgos — Estudio Alofoke 2028

**SD-2026-001** · SonDatos · división de análisis de SUBROSA
Corpus: comentarios públicos de YouTube, 1 ene 2025 – 11 jul 2026

> Este documento resume los hallazgos con el mismo lenguaje y las mismas cautelas metodológicas del informe público. El diseño es observacional; no establece causalidad. Ver [metodologia.md](metodologia.md) y [validacion.md](validacion.md) para el detalle técnico completo.

## Resumen del corpus

| Etapa | n | Nota |
|---|---|---|
| Comentarios crudos | 207,337 | 481 videos (6 búsquedas temáticas + 4 canales) |
| Excluidos por irrelevancia | 163,113 | No mencionan al sujeto ni provienen de videos monotemáticos |
| Relevantes | 44,224 | |
| Excluidos por spam/duplicación/hiperactividad | 4,606 | Sobre el corpus crudo completo, 35,848 comentarios (17%) presentaron estas señales |
| **Utilizables** | **39,618** | Base del análisis |

## Hallazgo 1 — La brecha comunicador / candidato

Separando la conversación por aspecto temático:

- **Como comunicador/empresario:** net sentiment +0.13 (n=2,156)
- **Como candidato político:** net sentiment −0.40 (n=10,824; agrupa 10,463 comentarios clasificados como "político" + 361 "mixto")

Esta distancia es el hallazgo más robusto del estudio: la comparación es relativamente robusta al sesgo del modelo, bajo el supuesto de que ese sesgo opera de forma similar en ambos aspectos (ver validación).

## Hallazgo 2 — Tendencia temporal

La negatividad base pasó de aproximadamente 32% (marzo 2025) a 54% (julio 2026), en paralelo con un crecimiento explosivo del volumen de conversación. La pendiente de este deterioro es un hallazgo firme porque el sesgo del clasificador es constante en el tiempo.

## Hallazgo 3 — Cambios observados alrededor de eventos clave

Ventanas de ±14 días, z-test de dos colas sobre proporción de comentarios negativos. **Diseño observacional: documenta coincidencias temporales, no causalidad**, y los eventos de junio–julio 2026 se solapan entre sí.

| Evento | Fecha | %Neg pre → post | Δ | p-value |
|---|---|---|---|---|
| Anuncia candidatura independiente | 2025-03-05 | 32.4% → 32.1% | −0.3pp | 0.96 |
| Declara rol de influencia (sin candidatura) | 2025-11-29 | 42.7% → 34.1% | **−8.6pp** | 0.099 (tendencia, no significativa al 5%) |
| Tuit dominical + reacción nacional | 2026-06-21 | 47.4% → 49.5% | +2.0pp | 0.017 * |
| PRSC abre puertas a su candidatura | 2026-06-24 | 49.6% → 48.8% | −0.8pp | 0.25 |
| Fans presionan inicio de campaña | 2026-07-06 | 49.3% → 54.2% | +4.9pp | <0.0001 * |

La única señal favorable medida (tendencia, no significativa al 5%) coincidió con el distanciamiento de la candidatura en noviembre 2025.

## Hallazgo 4 — La paradoja de la rabia (postura vs. tono)

Sobre una muestra estratificada de 396 comentarios, un analista humano etiquetó la **postura** declarada hacia Matías, independientemente del tono del texto:

- Postura clara en 186 de 396 comentarios (47%)
- De esos 186: **72% a favor / 28% en contra** (±6.4pp) — *cifra calculada sobre estos 186 casos, no sobre el corpus completo de 39,618 comentarios*
- 1 de cada 5 comentarios clasificados como negativos por el modelo proviene de personas que declaran apoyo explícito ("hay que sacar esas ratas del poder... yo voto por Santiago")

## Hallazgo 5 — Los modelos subestiman el apoyo en registro dominicano

La validación humana (ver [validacion.md](validacion.md)) muestra que el clasificador detecta el 89% de lo negativo pero solo el 48% de lo positivo. Corrigiendo por esta matriz de confusión:

- Net sentiment global: −0.26 (medido) → **−0.06** (corregido, IC 95% bootstrap: [−0.14, +0.04] — estadísticamente indistinguible de una conversación dividida)
- Net sentiment político: −0.40 (medido) → **−0.30** (corregido, IC 95%: [−0.37, −0.22] — robustamente negativo)

La corrección asume que el error medido en los 396 casos validados es transferible al corpus completo — supuesto razonable dado el muestreo estratificado proporcional, pero un supuesto declarado, no un hecho verificado independientemente.

## Limitaciones

- Sentimiento y postura en YouTube no equivalen a intención de voto ni a representatividad electoral.
- Quienes comentan se autoseleccionan; el perfil demográfico no es el del padrón electoral.
- El sarcasmo y la jerga dominicana degradan la clasificación automática; la validación humana cuantifica ese error y las correcciones lo mitigan, no lo eliminan.
- Los eventos de junio–julio 2026 se solapan; sus efectos individuales no son separables.
