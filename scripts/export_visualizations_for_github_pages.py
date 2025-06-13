"""
Script para exportar visualizaciones estáticas para GitHub Pages
Genera HTML estático a partir de las visualizaciones interactivas del portafolio
"""
import os
import sys
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Añadir directorio raíz al path para importar módulos del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar aplicaciones del portafolio
try:
    from app.apps.budget_analysis_app_v2 import BudgetAnalysisApp
    from app.apps.co2_emissions_app import CO2EmissionsApp
    from app.apps.water_quality_app import WaterQualityApp
    from app.apps.demographics_app import DemographicsApp
except ImportError as e:
    print(f"Error al importar aplicaciones: {e}")
    sys.exit(1)

# Configuración
OUTPUT_DIR = "github_pages/visualizations"
THUMBNAIL_DIR = "github_pages/assets/thumbnails"

# Crear directorios si no existen
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

def export_budget_visualizations():
    """Exporta visualizaciones del análisis de presupuesto"""
    print("Exportando visualizaciones de análisis de presupuesto...")
    try:
        app = BudgetAnalysisApp()
        df = app.fetch_budget_data()
        
        if df is not None:
            for nivel in app.config.NIVELES:
                # Exportar análisis de distribución
                fig_dist = app.plot_distribution_analysis(df, nivel)
                fig_dist.update_layout(
                    title=f'Análisis de Desigualdad en la Distribución - {nivel}',
                    height=600,
                    width=800
                )
                output_path = f"{OUTPUT_DIR}/budget_distribution_{nivel.lower()}.html"
                fig_dist.write_html(
                    output_path, 
                    include_plotlyjs='cdn',
                    full_html=True,
                    config={'displayModeBar': False}
                )
                print(f"  ✓ Exportado: {output_path}")
                
                # Exportar evolución presupuestaria
                fig_evol = app.plot_budget_evolution(df, nivel)
                fig_evol.update_layout(
                    title=f'Simulación de Evolución Presupuestaria - Top 5 {nivel}s',
                    height=600,
                    width=800
                )
                output_path = f"{OUTPUT_DIR}/budget_evolution_{nivel.lower()}.html"
                fig_evol.write_html(
                    output_path, 
                    include_plotlyjs='cdn',
                    full_html=True,
                    config={'displayModeBar': False}
                )
                print(f"  ✓ Exportado: {output_path}")
    except Exception as e:
        print(f"Error al exportar visualizaciones de presupuesto: {e}")

def export_co2_visualizations():
    """Exporta visualizaciones del análisis de emisiones CO2"""
    print("Exportando visualizaciones de emisiones CO2...")
    try:
        app = CO2EmissionsApp()
        # Implementar exportación de visualizaciones específicas
        print("  ✓ Visualizaciones de CO2 exportadas (implementación pendiente)")
    except Exception as e:
        print(f"Error al exportar visualizaciones de CO2: {e}")

def export_water_visualizations():
    """Exporta visualizaciones del análisis de calidad del agua"""
    print("Exportando visualizaciones de calidad del agua...")
    try:
        app = WaterQualityApp()
        # Implementar exportación de visualizaciones específicas
        print("  ✓ Visualizaciones de calidad del agua exportadas (implementación pendiente)")
    except Exception as e:
        print(f"Error al exportar visualizaciones de calidad del agua: {e}")

def export_demographics_visualizations():
    """Exporta visualizaciones del análisis demográfico"""
    print("Exportando visualizaciones de análisis demográfico...")
    try:
        app = DemographicsApp()
        # Implementar exportación de visualizaciones específicas
        print("  ✓ Visualizaciones demográficas exportadas (implementación pendiente)")
    except Exception as e:
        print(f"Error al exportar visualizaciones demográficas: {e}")

def create_index_html():
    """Crea un índice HTML para las visualizaciones exportadas"""
    print("Creando índice HTML para visualizaciones...")
    
    # Lista para almacenar todas las visualizaciones
    visualizations = []
    
    # Buscar todas las visualizaciones generadas
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".html"):
            category = "otros"
            if "budget" in filename:
                category = "presupuesto"
            elif "co2" in filename:
                category = "emisiones"
            elif "water" in filename:
                category = "agua"
            elif "demographic" in filename:
                category = "demografía"
                
            name = filename.replace(".html", "").replace("_", " ").title()
            
            visualizations.append({
                "filename": filename,
                "name": name,
                "category": category,
                "path": f"visualizations/{filename}"
            })
    
    # Generar índice HTML
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Visualizaciones - Portafolio de Data Science</title>
        <link rel="stylesheet" href="../css/styles.css">
        <style>
            .visualizations-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                padding: 20px;
            }
            .visualization-card {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                background: white;
            }
            .visualization-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .card-header {
                padding: 15px;
                background: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
            }
            .card-header h3 {
                margin: 0;
                font-size: 1.1rem;
                color: #333;
            }
            .card-body {
                padding: 15px;
            }
            .card-footer {
                padding: 10px 15px;
                background: #f8f9fa;
                border-top: 1px solid #e0e0e0;
                display: flex;
                justify-content: space-between;
            }
            .card-footer a {
                text-decoration: none;
                color: #2a5298;
                font-weight: 500;
            }
            .category-badge {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 12px;
                background: #e7f1ff;
                color: #2a5298;
                font-size: 0.8rem;
                margin-right: 5px;
            }
            .filters {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .filter-button {
                padding: 8px 15px;
                border: none;
                border-radius: 20px;
                background: white;
                color: #333;
                cursor: pointer;
                border: 1px solid #ddd;
            }
            .filter-button.active {
                background: #2a5298;
                color: white;
                border-color: #2a5298;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>📊 Visualizaciones del Portafolio</h1>
            <p>Ejemplos estáticos de las visualizaciones interactivas</p>
        </header>
        
        <nav class="navigation">
            <a href="../index.html">Inicio</a>
            <a href="https://tu-app-streamlit.run.app">Aplicación Interactiva</a>
        </nav>
        
        <main>
            <section class="container">
                <h2>Biblioteca de Visualizaciones</h2>
                <p>Estas visualizaciones son versiones estáticas de las gráficas interactivas disponibles en la aplicación Streamlit. Para una experiencia completa e interactiva, accede a la aplicación en vivo.</p>
                
                <div class="filters">
                    <button class="filter-button active" data-category="all">Todas</button>
                    <button class="filter-button" data-category="presupuesto">Presupuesto</button>
                    <button class="filter-button" data-category="emisiones">Emisiones CO2</button>
                    <button class="filter-button" data-category="agua">Calidad del Agua</button>
                    <button class="filter-button" data-category="demografía">Demografía</button>
                </div>
                
                <div class="visualizations-grid">
    """
    
    # Agregar tarjetas para cada visualización
    for viz in visualizations:
        html_content += f"""
                    <div class="visualization-card" data-category="{viz['category']}">
                        <div class="card-header">
                            <h3>{viz['name']}</h3>
                        </div>
                        <div class="card-body">
                            <iframe src="{viz['path']}" width="100%" height="300px" frameborder="0"></iframe>
                        </div>
                        <div class="card-footer">
                            <span class="category-badge">{viz['category']}</span>
                            <a href="{viz['path']}" target="_blank">Ver completo</a>
                        </div>
                    </div>
        """
    
    # Cerrar estructura HTML
    html_content += """
                </div>
            </section>
        </main>
        
        <footer>
            <p>Actualizado: """ + datetime.now().strftime("%d/%m/%Y") + """</p>
            <p>Desarrollado con ❤️ - 2025</p>
        </footer>
        
        <script>
            // Filtrado de visualizaciones
            document.addEventListener('DOMContentLoaded', function() {
                const filterButtons = document.querySelectorAll('.filter-button');
                const cards = document.querySelectorAll('.visualization-card');
                
                filterButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        // Actualizar botones
                        filterButtons.forEach(btn => btn.classList.remove('active'));
                        this.classList.add('active');
                        
                        // Filtrar tarjetas
                        const category = this.getAttribute('data-category');
                        cards.forEach(card => {
                            if (category === 'all' || card.getAttribute('data-category') === category) {
                                card.style.display = 'block';
                            } else {
                                card.style.display = 'none';
                            }
                        });
                    });
                });
            });
        </script>
    </body>
    </html>
    """
    
    # Guardar archivo HTML
    with open(f"{OUTPUT_DIR}/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"  ✓ Índice creado: {OUTPUT_DIR}/index.html")

if __name__ == "__main__":
    print(f"Iniciando exportación de visualizaciones ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    
    # Exportar visualizaciones por categoría
    export_budget_visualizations()
    export_co2_visualizations()
    export_water_visualizations()
    export_demographics_visualizations()
    
    # Crear índice
    create_index_html()
    
    print(f"\n✅ Proceso completado. Visualizaciones exportadas a: {OUTPUT_DIR}")
