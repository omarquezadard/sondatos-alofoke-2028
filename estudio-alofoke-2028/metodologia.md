# Metodología — Ficha técnica SD-2026-001

| | |
|---|---|
| **Fuente** | Comentarios públicos de YouTube: 6 búsquedas temáticas + 4 canales monitoreados (Alofoke Radio Show, El Nuevo Diario TV, Noticias SIN, CDN 37). 481 videos. |
| **Período** | 1 enero 2025 — 11 julio 2026 |
| **Corpus** | 207,337 comentarios crudos → 163,113 excluidos por irrelevancia → 44,224 relevantes → 4,606 excluidos por spam/duplicación/hiperactividad → 39,618 utilizables. Sobre el corpus crudo completo, 35,848 comentarios (17%) presentaron señales de spam o duplicación. |
| **Relevancia** | Un comentario se conserva si menciona directamente al sujeto, o si proviene de un video cuyo título es monotemático (sujeto + contexto político). |
| **Anti-bot** | Se marcan y excluyen: texto duplicado masivo (>3 repeticiones exactas), comentarios sin contenido léxico (menos de 4 caracteres alfabéticos únicos), y autores con más de 10 comentarios en un mismo video. |
| **Modelo** | [robertuito-sentiment](https://huggingface.co/pysentimiento/robertuito-sentiment-analysis) (pysentimiento), RoBERTa entrenado en español de redes sociales. Clasificación POS/NEU/NEG con probabilidades. |
| **Aspecto** | Clasificación por diccionario de keywords: político (10,463), entretenimiento (2,156), mixto (361), general (26,638). En el análisis, el aspecto "político" agrupa político + mixto: n=10,824. |
| **Métrica principal** | Net sentiment = %POS − %NEG, agregación semanal, intervalo de confianza 95% por bootstrap (2,000 iteraciones). |
| **Impacto de eventos** | Ventanas de ±14 días alrededor de cada evento ancla. Z-test de dos colas sobre la proporción de comentarios negativos pre vs. post. Diseño observacional: no establece causalidad. |
| **Postura** | Etiquetado manual independiente sobre una submuestra: a_favor / en_contra / no_clara, según lo que el comentario declara hacia el sujeto (distinto del tono del texto). |
| **Validación** | Muestra estratificada proporcional de 396 comentarios (por sentimiento del modelo y aspecto), etiquetada por un analista humano. Ver [validacion.md](validacion.md) para la matriz de confusión y la corrección de sesgo. |

## Eventos ancla del estudio

| Evento | Fecha |
|---|---|
| Anuncia candidatura independiente | 2025-03-05 |
| Declara rol de influencia (sin candidatura) | 2025-11-29 |
| Tuit dominical + reacción nacional | 2026-06-21 |
| PRSC abre puertas a su candidatura | 2026-06-24 |
| Fans presionan inicio de campaña | 2026-07-06 |

## Reproducibilidad

El pipeline completo (recolección, limpieza, clasificación, análisis, gráficos) está publicado en este repositorio: ver `notebooks/` para la versión Colab (sin instalación) o `pipeline/` para la versión de línea de comandos. Cualquiera puede replicar este estudio, o adaptarlo a un sujeto distinto, con su propia API key de YouTube Data API v3.
