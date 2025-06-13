# 🌐 Despliegue del Portafolio de Data Science con GitHub Pages

> **Guía de Despliegue usando GitHub Pages (Junio 2025)**

Este documento proporciona instrucciones detalladas para desplegar el portafolio de Data Science utilizando GitHub Pages, y una comparativa con el despliegue en Google Cloud Run.

## 📋 Consideraciones Iniciales

GitHub Pages es ideal para contenido estático, mientras que nuestro portafolio Streamlit es una aplicación interactiva. Existen dos enfoques principales:

1. **Despliegue Estático**: Convertir partes del portafolio a HTML estático
2. **Despliegue Híbrido**: Sitio estático en GitHub Pages con enlaces a la aplicación Streamlit desplegada en otro servicio

## 🔍 Comparativa: GitHub Pages vs Google Cloud Run

| Característica | GitHub Pages | Google Cloud Run |
|----------------|-------------|-----------------|
| **Tipo** | Contenido estático | Aplicaciones containerizadas |
| **Capa Gratuita** | Ilimitada para repositorios públicos | 2M de solicitudes/mes, 360K GB-segundos |
| **Backend** | No (solo HTML, CSS, JS) | Sí (cualquier lenguaje) |
| **Interactividad** | Limitada (solo frontend) | Completa (frontend + backend) |
| **Personalización** | Limitada | Alta |
| **Dominio** | `username.github.io` o personalizado | Dominio de GCP o personalizado |
| **CI/CD** | Automático con GitHub Actions | Configurable con GitHub Actions |
| **Escalabilidad** | No aplicable | Automática |
| **Límite de tamaño** | 1GB por repositorio | Sin límite específico |
| **Adecuado para** | Documentación, portafolios estáticos | Aplicaciones interactivas, APIs |

## 📝 Enfoque 1: Sitio Estático Complementario

Este enfoque crea un sitio estático en GitHub Pages que sirve como punto de entrada y documentación, con enlaces a la aplicación Streamlit en Google Cloud Run.

### 1. Estructura del Proyecto

```
ds_portfolio/
├── app/                  # Aplicación Streamlit (para Cloud Run)
├── docs/                 # Documentación y archivos MD
└── github_pages/         # Contenido para GitHub Pages
    ├── index.html        # Página principal
    ├── css/              # Estilos
    ├── js/               # JavaScript
    └── assets/           # Imágenes y recursos
```

### 2. Configuración de GitHub Pages

1. **Habilitar GitHub Pages**:
   - Ve a la configuración del repositorio (`Settings`)
   - Desplázate hasta la sección `Pages`
   - En `Source`, selecciona la rama `main` y la carpeta `/github_pages`
   - Haz clic en `Save`

2. **Crear contenido básico**:

```html
<!-- github_pages/index.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portafolio de Data Science</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header>
        <h1>📊 Portafolio de Data Science</h1>
        <p>Análisis de Datos Gubernamentales, Ambientales y Demográficos</p>
    </header>
    
    <main>
        <section class="hero">
            <h2>Aplicaciones Interactivas</h2>
            <p>Explora aplicaciones de análisis de datos con visualizaciones avanzadas</p>
            <a href="https://tu-app-streamlit.run.app" class="cta-button">Acceder al Portafolio Interactivo</a>
        </section>
        
        <section class="features">
            <div class="feature">
                <h3>💰 Análisis del Presupuesto Público</h3>
                <p>Visualización y análisis del presupuesto de Chile con métricas avanzadas</p>
            </div>
            <div class="feature">
                <h3>💧 Calidad del Agua</h3>
                <p>Análisis geoespacial de la calidad del agua en Chile</p>
            </div>
            <div class="feature">
                <h3>🏭 Emisiones CO2</h3>
                <p>Análisis sectorial de emisiones por región</p>
            </div>
            <div class="feature">
                <h3>👤 Análisis Demográfico</h3>
                <p>Tendencias demográficas con BigQuery</p>
            </div>
        </section>
        
        <section class="documentation">
            <h2>Documentación</h2>
            <ul>
                <li><a href="docs/analisis_presupuesto.html">Análisis del Presupuesto</a></li>
                <li><a href="docs/calidad_agua.html">Calidad del Agua</a></li>
                <li><a href="docs/emisiones_co2.html">Emisiones CO2</a></li>
                <li><a href="docs/demografia.html">Análisis Demográfico</a></li>
            </ul>
        </section>
    </main>
    
    <footer>
        <p>Desarrollado con ❤️ - 2025</p>
    </footer>
    
    <script src="js/main.js"></script>
</body>
</html>
```

3. **Estilos básicos**:

```css
/* github_pages/css/styles.css */
:root {
    --primary: #2a5298;
    --secondary: #f8f9fa;
    --text: #333;
    --accent: #4CAF50;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text);
    margin: 0;
    padding: 0;
    background-color: #f8f9fa;
}

header, footer {
    background-color: var(--primary);
    color: white;
    text-align: center;
    padding: 2rem 1rem;
}

.hero {
    background-color: var(--secondary);
    padding: 3rem 1rem;
    text-align: center;
    border-bottom: 1px solid #e9ecef;
}

.cta-button {
    display: inline-block;
    background-color: var(--accent);
    color: white;
    text-decoration: none;
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    font-weight: bold;
    margin-top: 1rem;
    transition: background-color 0.3s;
}

.cta-button:hover {
    background-color: #3e8e41;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 3rem 1rem;
    max-width: 1200px;
    margin: 0 auto;
}

.feature {
    background-color: white;
    padding: 1.5rem;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.documentation {
    padding: 3rem 1rem;
    max-width: 800px;
    margin: 0 auto;
}

.documentation ul {
    list-style: none;
    padding: 0;
}

.documentation li {
    margin-bottom: 1rem;
}

.documentation a {
    color: var(--primary);
    text-decoration: none;
    font-weight: 500;
}

.documentation a:hover {
    text-decoration: underline;
}

footer {
    padding: 1rem;
}

@media (max-width: 768px) {
    .features {
        grid-template-columns: 1fr;
    }
}
```

### 3. Convertir Documentación Markdown a HTML

Para convertir tus archivos Markdown a HTML para GitHub Pages, puedes usar GitHub Actions:

1. **Crear un workflow de GitHub Actions**:

```yaml
# .github/workflows/build-pages.yml
name: Build GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'github_pages/**'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3
        
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
          
      - name: Install dependencies
        run: |
          npm install -g markdown-to-html-cli
          
      - name: Convert Markdown to HTML
        run: |
          mkdir -p github_pages/docs
          for file in docs/*.md; do
            filename=$(basename "$file" .md)
            markdown-to-html-cli "$file" -o "github_pages/docs/${filename}.html" --title "${filename}" --template-html "github_pages/template.html"
          done
          
      - name: Deploy to GitHub Pages
        uses: JamesIves/github-pages-deploy-action@4.1.4
        with:
          branch: gh-pages
          folder: github_pages
```

2. **Crear una plantilla HTML**:

```html
<!-- github_pages/template.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Portafolio de Data Science</title>
    <link rel="stylesheet" href="../css/styles.css">
    <link rel="stylesheet" href="../css/documentation.css">
</head>
<body>
    <header>
        <h1>📊 Portafolio de Data Science</h1>
        <p>Documentación Técnica</p>
    </header>
    
    <nav class="navigation">
        <a href="../index.html">Inicio</a>
        <a href="https://tu-app-streamlit.run.app">Aplicación Interactiva</a>
    </nav>
    
    <main class="documentation-content">
        {{content}}
    </main>
    
    <footer>
        <p>Desarrollado con ❤️ - 2025</p>
    </footer>
</body>
</html>
```

## 📝 Enfoque 2: Exportar Visualizaciones Estáticas

Este enfoque exporta visualizaciones y resultados clave de la aplicación Streamlit como HTML estático o imágenes para mostrarlos en GitHub Pages.

### 1. Exportar Visualizaciones de Plotly

Crea un script para exportar las visualizaciones de Plotly como HTML estático:

```python
# scripts/export_visualizations.py
import os
import sys
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Asegurarse de que se puede importar desde el directorio raíz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.apps.budget_analysis_app_v2 import BudgetAnalysisApp
from app.apps.co2_emissions_app import CO2EmissionsApp
from app.apps.water_quality_app import WaterQualityApp

# Directorio de salida
OUTPUT_DIR = "github_pages/visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Exportar visualizaciones del análisis de presupuesto
def export_budget_visualizations():
    app = BudgetAnalysisApp()
    df = app.fetch_budget_data()
    
    if df is not None:
        for nivel in app.config.NIVELES:
            # Exportar análisis de distribución
            fig_dist = app.plot_distribution_analysis(df, nivel)
            fig_dist.write_html(f"{OUTPUT_DIR}/budget_distribution_{nivel.lower()}.html")
            
            # Exportar evolución presupuestaria
            fig_evol = app.plot_budget_evolution(df, nivel)
            fig_evol.write_html(f"{OUTPUT_DIR}/budget_evolution_{nivel.lower()}.html")

# Exportar visualizaciones de emisiones CO2
def export_co2_visualizations():
    app = CO2EmissionsApp()
    # Código similar para exportar visualizaciones

# Exportar visualizaciones de calidad del agua
def export_water_visualizations():
    app = WaterQualityApp()
    # Código similar para exportar visualizaciones

if __name__ == "__main__":
    export_budget_visualizations()
    export_co2_visualizations()
    export_water_visualizations()
    print("Visualizaciones exportadas correctamente.")
```

### 2. Integrar Visualizaciones en GitHub Pages

Crea páginas para mostrar las visualizaciones exportadas:

```html
<!-- github_pages/visualizaciones.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualizaciones - Portafolio de Data Science</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <header>
        <h1>📊 Visualizaciones del Portafolio</h1>
        <p>Ejemplos estáticos de las visualizaciones interactivas</p>
    </header>
    
    <nav class="navigation">
        <a href="index.html">Inicio</a>
        <a href="https://tu-app-streamlit.run.app">Aplicación Interactiva</a>
    </nav>
    
    <main>
        <section class="visualizations">
            <h2>Análisis del Presupuesto Público</h2>
            
            <div class="visualization-container">
                <h3>Distribución Presupuestaria - Partidas</h3>
                <iframe src="visualizations/budget_distribution_partida.html" width="100%" height="500px" frameborder="0"></iframe>
            </div>
            
            <div class="visualization-container">
                <h3>Evolución Presupuestaria - Partidas</h3>
                <iframe src="visualizations/budget_evolution_partida.html" width="100%" height="500px" frameborder="0"></iframe>
            </div>
            
            <!-- Más visualizaciones -->
        </section>
    </main>
    
    <footer>
        <p>Desarrollado con ❤️ - 2025</p>
    </footer>
</body>
</html>
```

### 3. Configurar Workflow para Exportar Visualizaciones

Actualiza el workflow de GitHub Actions para exportar las visualizaciones:

```yaml
# .github/workflows/build-pages.yml (actualización)
# ...
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ...
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          
      - name: Export visualizations
        run: python scripts/export_visualizations.py
      
      # ...
```

## 📝 Enfoque 3: Sitio Completo de Documentación con MkDocs

Este enfoque utiliza MkDocs para crear un sitio de documentación completo basado en los archivos Markdown existentes.

### 1. Configurar MkDocs

1. **Instalar MkDocs y Material theme**:

```bash
pip install mkdocs mkdocs-material
```

2. **Inicializar MkDocs**:

```bash
mkdocs new .
```

3. **Configurar MkDocs** (`mkdocs.yml`):

```yaml
site_name: Portafolio de Data Science
site_url: https://tuusuario.github.io/ds_portfolio
repo_url: https://github.com/tuusuario/ds_portfolio
repo_name: tuusuario/ds_portfolio

theme:
  name: material
  palette:
    primary: indigo
    accent: green
  language: es
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.highlight
    - content.tabs.link
  icon:
    repo: fontawesome/brands/github

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed
  - pymdownx.emoji:
      emoji_index: !!python/name:materialx.emoji.twemoji
      emoji_generator: !!python/name:materialx.emoji.to_svg
  - admonition
  - footnotes

nav:
  - Inicio: index.md
  - Aplicaciones:
    - Análisis de Presupuesto: analisis_presupuesto_publico.md
    - Calidad del Agua: analisis_calidad_agua.md
    - Emisiones CO2: analisis_emisiones_co2.md
    - Análisis Demográfico: analisis_demografico_bigquery.md
  - Despliegue:
    - Google Cloud Run: roadmap_google_cloud_run.md
    - GitHub Pages: despliegue_github_pages.md
  - Actualizaciones:
    - Junio 2025: ACTUALIZACIONES_JUNIO_2025.md
  - Sobre el Proyecto: about.md
```

### 2. Copiar y Adaptar Documentación Existente

Configura un script para copiar y organizar los archivos Markdown existentes:

```python
# scripts/organize_docs.py
import os
import shutil

# Directorios
source_dir = "docs"
target_dir = "mkdocs_docs/docs"

# Crear directorio destino si no existe
os.makedirs(target_dir, exist_ok=True)

# Archivos a copiar y renombrar
files_to_copy = {
    "ACTUALIZACIONES_JUNIO_2025.md": "ACTUALIZACIONES_JUNIO_2025.md",
    "analisis_demografico_bigquery.md": "analisis_demografico_bigquery.md",
    "analisis_presupuesto_publico.md": "analisis_presupuesto_publico.md",
    "roadmap_google_cloud_run.md": "roadmap_google_cloud_run.md",
    "despliegue_github_pages.md": "despliegue_github_pages.md",
    # Añadir más archivos según sea necesario
}

# README como index.md
shutil.copy("README.md", os.path.join(target_dir, "index.md"))

# Copiar y renombrar archivos
for source, target in files_to_copy.items():
    source_path = os.path.join(source_dir, source)
    target_path = os.path.join(target_dir, target)
    
    if os.path.exists(source_path):
        shutil.copy(source_path, target_path)
        print(f"Copiado: {source} -> {target}")
    else:
        print(f"Advertencia: {source} no existe")

print("Organización de documentación completada.")
```

### 3. Configurar GitHub Actions para MkDocs

```yaml
# .github/workflows/deploy-mkdocs.yml
name: Deploy MkDocs

on:
  push:
    branches:
      - main
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
      - 'mkdocs_docs/**'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mkdocs mkdocs-material
      
      - name: Organize documentation
        run: python scripts/organize_docs.py
      
      - name: Deploy MkDocs
        run: mkdocs gh-deploy --force
```

## 🔀 Estrategia Híbrida: GitHub Pages + Google Cloud Run

La estrategia más efectiva combina ambas plataformas:

1. **GitHub Pages**: Documentación estática, tutoriales, descripciones de proyectos
2. **Google Cloud Run**: Aplicación Streamlit interactiva completa

### Ventajas de esta Estrategia Híbrida

1. **Optimización de Costos**:
   - Contenido estático en GitHub Pages (gratis, ilimitado)
   - Componentes interactivos en Google Cloud Run (capa gratuita para uso moderado)

2. **Mejor Experiencia de Usuario**:
   - Documentación rápida y accesible en GitHub Pages
   - Interactividad completa en Google Cloud Run

3. **SEO Mejorado**:
   - GitHub Pages facilita la indexación por motores de búsqueda
   - Mejor descubrimiento de tu trabajo

### Implementación de la Estrategia Híbrida

1. **Configurar redirecciones entre ambas plataformas**:
   - Botones "Ver aplicación interactiva" en GitHub Pages que redirijan a Google Cloud Run
   - Enlaces "Ver documentación" en la aplicación Streamlit que redirijan a GitHub Pages

2. **Mantener coherencia visual**:
   - Usar los mismos colores, fuentes y estilos en ambas plataformas
   - Crear una experiencia unificada

3. **Sistema de despliegue automatizado**:
   - GitHub Actions para desplegar ambas plataformas desde el mismo repositorio

## 📊 Comparativa de Costos: GitHub Pages vs Google Cloud Run

| Escenario | GitHub Pages | Google Cloud Run |
|-----------|-------------|-----------------|
| **Tráfico bajo** (<1000 visitas/mes) | $0 | $0 (dentro de capa gratuita) |
| **Tráfico medio** (<5000 visitas/mes) | $0 | $0-$5 (dependiendo de duración de sesiones) |
| **Tráfico alto** (>10000 visitas/mes) | $0 | $10-$50 (fuera de capa gratuita) |
| **Almacenamiento** | Hasta 1GB gratis | Costos adicionales para almacenamiento >5GB |
| **Ancho de banda** | Límite de 100GB/mes | Sin límites explícitos (pago por uso) |

## 🛠️ Recursos Adicionales

### Herramientas Útiles

1. **Herramientas para GitHub Pages**:
   - [Jekyll](https://jekyllrb.com/) - Generador de sitios estáticos
   - [MkDocs](https://www.mkdocs.org/) - Generador de documentación
   - [GitHub Pages Themes](https://pages.github.com/themes/) - Temas oficiales

2. **Optimización para la Estrategia Híbrida**:
   - [Streamlit-Static](https://github.com/sfc-gh-brianhess/streamlit-static) - Genera capturas estáticas de apps Streamlit
   - [HTML-to-Image](https://github.com/frinyvonnick/node-html-to-image) - Convierte HTML a imágenes

### Plantillas y Ejemplos

1. **Plantillas de MkDocs**:
   - [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
   - [MkDocs Bootswatch Themes](https://mkdocs.github.io/mkdocs-bootswatch/)

2. **Ejemplos de Portafolios de Data Science**:
   - [Example Portfolio with GitHub Pages](https://github.com/topics/data-science-portfolio)

## 📝 Conclusión

Tanto GitHub Pages como Google Cloud Run ofrecen excelentes opciones gratuitas para desplegar diferentes aspectos de tu portafolio de Data Science. La estrategia más efectiva es utilizar:

- **GitHub Pages** para documentación, descripciones de proyectos y visualizaciones estáticas
- **Google Cloud Run** para la aplicación Streamlit interactiva completa

Esta combinación optimiza costos mientras ofrece una experiencia completa para los visitantes de tu portafolio.

---

Con esta guía detallada, podrás implementar una estrategia eficaz para desplegar tu portafolio utilizando GitHub Pages, ya sea como complemento a Google Cloud Run o como una alternativa independiente.
