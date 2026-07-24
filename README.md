# SonDatos · Pipeline de análisis de sentimiento en redes sociales

**SonDatos** es un proyecto de datos abiertos de [SUBROSA](https://csubrosa.com), enfocado en el análisis riguroso de conversación pública en redes sociales sobre figuras y marcas dominicanas. Este repositorio contiene el pipeline completo (recolección → limpieza → clasificación de sentimiento → análisis estadístico → visualización) y los resultados agregados del primer estudio publicado.

📄 **Informe público:** [sondatos.do](https://sondatos.do)

## Qué hace el pipeline

1. **Recolección** (YouTube Data API v3, o CSV externo para Instagram)
2. **Limpieza y relevancia** — filtra comentarios relevantes al sujeto y descarta spam/duplicados/cuentas hiperactivas
3. **Clasificación de aspecto** — separa la conversación por dimensiones temáticas (ej. comunicador vs. candidato)
4. **Sentimiento** — [robertuito](https://github.com/pysentimiento/pysentimiento) (RoBERTa entrenado en español de redes sociales), corrido en Colab con GPU gratuita
5. **Análisis** — net sentiment semanal con intervalos de confianza (bootstrap), impacto de eventos clave (z-test de proporciones)
6. **Validación humana** — muestra estratificada etiquetada manualmente; matriz de confusión y corrección de sesgo del modelo por inversión de matriz
7. **Visualización** — gráficos con identidad de marca, en tema claro (documentos) u oscuro (redes)

## Estructura

```
notebooks/          → pipelines listos para Google Colab (no requieren instalación local)
  SonDatos_Pipeline_YouTube.ipynb      pipeline completo para cualquier sujeto/marca en YouTube
  SonDatos_Pipeline_Instagram.ipynb    idem, a partir de un CSV de comentarios de Instagram
  SonDatos_Paso3_Sentimiento_y_Graficos.ipynb   notebook específico usado en el estudio Alofoke 2028

pipeline/            → versión de línea de comandos del pipeline de YouTube (recolección local + Colab para el modelo)
  config.yaml         configuración del estudio Alofoke 2028 (editable para nuevos estudios)
  src/                 scripts numerados 01–06, ejecutables en orden

estudio-alofoke-2028/  → resultados agregados del primer estudio publicado
  resultados/           series temporales y tabla de impacto de eventos (CSV)
  graficos/             gráficos finales en PNG (300dpi)
  FINDINGS.md           hallazgos, con el mismo lenguaje y cautelas del informe público
  metodologia.md        ficha técnica completa
  validacion.md         matriz de confusión y corrección de sesgo del modelo
```

## Cómo usarlo para un estudio nuevo

La forma más simple: abre `notebooks/SonDatos_Pipeline_YouTube.ipynb` en Google Colab, edita la celda `⚙️ CONFIGURACIÓN` (sujeto, keywords, eventos, marca) y ejecuta todas las celdas. No requiere instalación — solo una API key gratuita de YouTube Data API v3.

Para Instagram, usa `SonDatos_Pipeline_Instagram.ipynb`: le das un CSV de comentarios (exportado vía Graph API para cuentas propias/autorizadas, o un servicio de extracción de terceros) y corre el mismo análisis.

## Nota sobre los datos

Este repositorio **no incluye comentarios individuales** (texto, autor) del corpus recolectado. Solo se publican estadísticas agregadas — series temporales, conteos por categoría, matrices de confusión — siguiendo la práctica estándar en estudios abiertos de datos de redes sociales: los comentarios eran públicos en su plataforma de origen, pero republicarlos en bloque, indexados y descargables, no es necesario para la reproducibilidad del análisis y plantea consideraciones de privacidad para quienes los escribieron.

Quien quiera reproducir la recolección puede hacerlo con su propia API key ejecutando el pipeline desde cero — los resultados agregados aquí publicados permiten verificar la metodología y las cifras sin necesitar acceso a los datos crudos.

## Licencia

El código de este repositorio se publica bajo licencia [MIT](LICENSE). Los hallazgos, textos y gráficos del estudio se comparten para fines de transparencia y verificación periodística; para uso comercial o redistribución de los informes, contactar a SonDatos.

## Autoría

**Omar Quezada**, M.Sc. en Ciencia de Datos (UCJC) · Director de SonDatos · SUBROSA — División de Análisis
