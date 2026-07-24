# SonDatos · Pipeline de análisis de sentimiento en redes sociales
# SonDatos · Social Media Sentiment Analysis Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Model](https://img.shields.io/badge/NLP-pysentimiento%20RoBERTa--es-teal)](https://github.com/pysentimiento/pysentimiento)
[![Data](https://img.shields.io/badge/Data-YouTube%20Data%20API%20v3-orange)](https://developers.google.com/youtube/v3)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)
[![SonDatos](https://img.shields.io/badge/SonDatos-SUBROSA%20Data%20Division-421034)](https://sondatos.do)

---

> 🇩🇴 [Español](#-español) · 🇬🇧 [English](#-english)

---

## 🇩🇴 Español

### Descripción

**SonDatos** es un proyecto de datos abiertos de [SUBROSA](https://csubrosa.com), enfocado en el análisis riguroso de conversación pública en redes sociales sobre figuras y marcas dominicanas. Este repositorio contiene el pipeline completo (recolección → limpieza → clasificación de sentimiento → análisis estadístico → visualización) y los resultados agregados del primer estudio publicado.

📄 **Informe público:** [sondatos.do](https://sondatos.do)

### Qué hace el pipeline

1. **Recolección** (YouTube Data API v3, o CSV externo para Instagram)
2. **Limpieza y relevancia** — filtra comentarios relevantes al sujeto y descarta spam/duplicados/cuentas hiperactivas
3. **Clasificación de aspecto** — separa la conversación por dimensiones temáticas (ej. comunicador vs. candidato)
4. **Sentimiento** — [robertuito](https://github.com/pysentimiento/pysentimiento) (RoBERTa entrenado en español de redes sociales), corrido en Colab con GPU gratuita
5. **Análisis** — net sentiment semanal con intervalos de confianza (bootstrap), impacto de eventos clave (z-test de proporciones)
6. **Validación humana** — muestra estratificada etiquetada manualmente; matriz de confusión y corrección de sesgo del modelo por inversión de matriz
7. **Visualización** — gráficos con identidad de marca, en tema claro (documentos) u oscuro (redes)

### Estructura del repositorio

```
notebooks/          → pipelines listos para Google Colab (no requieren instalación local)
  SonDatos_Pipeline_YouTube.ipynb      pipeline completo para cualquier sujeto/marca en YouTube
  SonDatos_Pipeline_Instagram.ipynb    idem, a partir de un CSV de comentarios de Instagram
  SonDatos_Paso3_Sentimiento_y_Graficos.ipynb   notebook específico usado en el estudio Alofoke 2028

pipeline/            → versión de línea de comandos del pipeline de YouTube
  config.yaml         configuración del estudio Alofoke 2028 (editable para nuevos estudios)
  src/                 scripts numerados 01–06, ejecutables en orden

estudio-alofoke-2028/  → resultados agregados del primer estudio publicado
  resultados/           series temporales y tabla de impacto de eventos (CSV)
  graficos/             gráficos finales en PNG (300dpi)
  FINDINGS.md           hallazgos, con el mismo lenguaje y cautelas del informe público
  metodologia.md        ficha técnica completa
  validacion.md         matriz de confusión y corrección de sesgo del modelo
```

### Cómo usarlo para un estudio nuevo

La forma más simple: abre `notebooks/SonDatos_Pipeline_YouTube.ipynb` en Google Colab, edita la celda `⚙️ CONFIGURACIÓN` (sujeto, keywords, eventos, marca) y ejecuta todas las celdas. No requiere instalación — solo una API key gratuita de YouTube Data API v3.

Para Instagram, usa `SonDatos_Pipeline_Instagram.ipynb`: le das un CSV de comentarios (exportado vía Graph API para cuentas propias/autorizadas, o un servicio de extracción de terceros) y corre el mismo análisis.

### Nota sobre los datos

Este repositorio **no incluye comentarios individuales** (texto, autor) del corpus recolectado. Solo se publican estadísticas agregadas — series temporales, conteos por categoría, matrices de confusión — siguiendo la práctica estándar en estudios abiertos de datos de redes sociales: los comentarios eran públicos en su plataforma de origen, pero republicarlos en bloque, indexados y descargables, no es necesario para la reproducibilidad del análisis y plantea consideraciones de privacidad para quienes los escribieron.

Quien quiera reproducir la recolección puede hacerlo con su propia API key ejecutando el pipeline desde cero.

### Instalación

```bash
git clone https://github.com/TU_USUARIO/sondatos-alofoke-2028.git
cd sondatos-alofoke-2028/pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export YT_API_KEY='tu_api_key'
```

Ver `pipeline/README.md` para el flujo paso a paso, o abrir directamente los notebooks de `notebooks/` en Colab.

### Licencia

El código de este repositorio se publica bajo licencia [MIT](LICENSE). Los hallazgos, textos y gráficos del estudio se comparten para fines de transparencia y verificación periodística; para uso comercial o redistribución de los informes, contactar a SonDatos.

### Autor

**Omar Quezada**, M.Sc. en Ciencia de Datos (UCJC)
Director, SonDatos · Fundador, SUBROSA
🇩🇴 República Dominicana
[GitHub](https://github.com/TU_USUARIO)

---

## 🇬🇧 English

### Overview

**SonDatos** is an open-data project by [SUBROSA](https://csubrosa.com), focused on rigorous analysis of public conversation on social media about Dominican public figures and brands. This repository contains the full pipeline (collection → cleaning → sentiment classification → statistical analysis → visualization) and the aggregated results from the first published study.

📄 **Public report:** [sondatos.do](https://sondatos.do)

### What the pipeline does

1. **Collection** (YouTube Data API v3, or an external CSV for Instagram)
2. **Cleaning and relevance filtering** — keeps comments relevant to the subject and discards spam/duplicates/hyperactive accounts
3. **Aspect classification** — splits the conversation by thematic dimension (e.g. communicator vs. candidate)
4. **Sentiment** — [robertuito](https://github.com/pysentimiento/pysentimiento) (a RoBERTa model pretrained on Spanish-language social media), run on free GPU via Google Colab
5. **Analysis** — weekly net sentiment with bootstrap confidence intervals, impact of key events (two-proportion z-test)
6. **Human validation** — a stratified sample manually labeled; confusion matrix and bias correction via matrix inversion
7. **Visualization** — branded charts, in a light theme (documents) or dark theme (social media)

### Repository structure

```
notebooks/          → ready-to-run Google Colab pipelines (no local install required)
  SonDatos_Pipeline_YouTube.ipynb      full pipeline for any subject/brand on YouTube
  SonDatos_Pipeline_Instagram.ipynb    same, starting from an Instagram comments CSV
  SonDatos_Paso3_Sentimiento_y_Graficos.ipynb   notebook used specifically for the Alofoke 2028 study

pipeline/            → command-line version of the YouTube pipeline
  config.yaml         configuration used for the Alofoke 2028 study (editable for new studies)
  src/                 numbered scripts 01–06, run in order

estudio-alofoke-2028/  → aggregated results from the first published study
  resultados/           time series and event-impact table (CSV)
  graficos/             final PNG charts (300dpi)
  FINDINGS.md            findings, with the same wording and caveats as the public report
  metodologia.md         full methodology fact sheet (Spanish)
  validacion.md          confusion matrix and model bias correction (Spanish)
```

### Running a new study

The simplest path: open `notebooks/SonDatos_Pipeline_YouTube.ipynb` in Google Colab, edit the `⚙️ CONFIGURACIÓN` cell (subject, keywords, events, branding) and run all cells. No installation required — just a free YouTube Data API v3 key.

For Instagram, use `SonDatos_Pipeline_Instagram.ipynb`: feed it a CSV of comments (exported via the Graph API for owned/authorized accounts, or a third-party extraction service) and it runs the same analysis.

### A note on the data

This repository **does not include individual comments** (text, author) from the collected corpus. Only aggregated statistics are published — time series, category counts, confusion matrices — following standard practice in open social-media data studies: the comments were public on their original platform, but republishing them in bulk, indexed and downloadable, isn't necessary for reproducing the analysis and raises privacy considerations for the people who wrote them.

Anyone who wants to reproduce the collection can do so with their own API key by running the pipeline from scratch.

### Setup

```bash
git clone https://github.com/YOUR_USERNAME/sondatos-alofoke-2028.git
cd sondatos-alofoke-2028/pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export YT_API_KEY='your_api_key'
```

See `pipeline/README.md` for the full step-by-step, or open the notebooks in `notebooks/` directly in Colab.

### License

The code in this repository is released under the [MIT License](LICENSE). The study's findings, text, and charts are shared for transparency and journalistic verification purposes; for commercial use or redistribution of the reports, contact SonDatos.

### Author

**Omar Quezada**, M.Sc. in Data Science (UCJC)
Director, SonDatos · Founder, SUBROSA
🇩🇴 Dominican Republic
[GitHub](https://github.com/YOUR_USERNAME)
