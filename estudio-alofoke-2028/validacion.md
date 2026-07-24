# Validación humana y corrección de sesgo del modelo

## Muestra

396 comentarios, muestreo estratificado proporcional por sentimiento del modelo y aspecto temático:

| Sentimiento (modelo) | n en muestra |
|---|---|
| NEG | 170 |
| NEU | 161 |
| POS | 65 |

Un analista humano etiquetó cada comentario de forma independiente por **tono** (POS/NEU/NEG) y, aparte, por **postura** declarada hacia el sujeto (a_favor/en_contra/no_clara). El etiquetado de tono no fue ciego respecto a la predicción del modelo, lo cual puede inflar levemente el acuerdo reportado a continuación.

*Nota: por las mismas razones de privacidad indicadas en el README principal, este repositorio no incluye el texto de los comentarios individuales de la muestra — solo los agregados estadísticos.*

## Matriz de confusión

Filas = etiqueta manual, columnas = predicción del modelo:

| | Modelo: POS | Modelo: NEU | Modelo: NEG |
|---|---|---|---|
| **Manual: POS** (122) | **59** | 45 | 18 |
| **Manual: NEU** (125) | 5 | **101** | 19 |
| **Manual: NEG** (149) | 1 | 15 | **133** |

- **Accuracy:** 74.0%
- **F1 macro:** 0.724
- **Recall NEG:** 89.3% (133/149)
- **Recall NEU:** 80.8% (101/125)
- **Recall POS:** 48.4% (59/122)

El error dominante es la confusión POS→NEU (45 casos) y POS→NEG (18 casos): el modelo subestima sistemáticamente el apoyo expresado en registro dominicano popular ("así se abla, toi contigo" tiende a leerse como neutro o negativo).

## Corrección por inversión de matriz de confusión

Usando la matriz de confusión como estimador del proceso de error, se invierte para estimar la distribución real de sentimiento a partir de la distribución observada por el modelo sobre el corpus completo (n=39,618):

| | Modelo (observado) | Corregido | IC 95% (bootstrap) |
|---|---|---|---|
| **Global** | −0.262 | **−0.063** | [−0.142, +0.040] |
| **Político + mixto** | −0.402 | **−0.298** | [−0.366, −0.224] |

**Lectura:** el intervalo de confianza del net sentiment global corregido cruza el cero — es decir, no se puede afirmar con confianza que la conversación general sea negativa neta; es más consistente con una conversación dividida. El net sentiment político corregido, en cambio, permanece robustamente negativo incluso tras la corrección.

**Supuesto declarado:** esta corrección asume que el patrón de error medido en los 396 casos validados es transferible al corpus completo de 39,618 comentarios. Es un supuesto razonable dado el muestreo estratificado proporcional, pero no ha sido verificado de forma independiente sobre una segunda muestra.

## Cruce tono × postura

Sobre los 396 casos validados, cruzando el **tono** asignado por el modelo con la **postura** etiquetada manualmente (solo casos con postura clara, n=186):

- De los comentarios que el modelo clasifica como **negativos**, ~20% corresponden a personas con postura **a favor** del sujeto (voto de rabia / antisistema).
- De los comentarios que el modelo clasifica como **positivos**, ~64% corresponden a personas con postura a favor — el apoyo casi no se expresa en negativo.

Este cruce es la base del hallazgo "paradoja de la rabia" descrito en [FINDINGS.md](FINDINGS.md).
