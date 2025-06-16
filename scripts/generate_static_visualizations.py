"""
Script para generar visualizaciones estáticas previas al despliegue
Reduce significativamente la carga en tiempo de ejecución y mejora la experiencia del usuario
"""

import os
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

print("Iniciando generación de visualizaciones estáticas...")

# Directorios importantes
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = BASE_DIR / "app" / "data" / "cache"
STATIC_DIR = BASE_DIR / "app" / "static" / "visualizations"

# Crear directorios si no existen
STATIC_DIR.mkdir(exist_ok=True, parents=True)

print(f"Directorios configurados: {STATIC_DIR}")

# Función para guardar figuras de Plotly como HTML
def save_plotly_as_html(fig, filename):
    path = STATIC_DIR / filename
    fig.write_html(path, include_plotlyjs='cdn', full_html=False)
    print(f"Guardada visualización: {path}")
    return path

# Función para cargar datos desde caché
def load_cache(filename):
    with open(CACHE_DIR / filename) as f:
        return json.load(f)

# 1. Generar gráfico de emisiones CO2
try:
    print("\nGenerando visualización de emisiones CO2...")
    emisiones = load_cache("emisiones_anuales.json")
    
    fig = go.Figure()
    
    # Añadir línea de tendencia
    fig.add_trace(go.Scatter(
        x=list(emisiones.keys()),
        y=list(emisiones.values()),
        mode='lines+markers',
        name='Emisiones',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))
    
    # Añadir área sombreada
    fig.add_trace(go.Scatter(
        x=list(emisiones.keys()),
        y=[min(emisiones.values()) * 0.9] * len(emisiones),
        fill=None,
        mode='lines',
        line=dict(width=0),
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=list(emisiones.keys()),
        y=list(emisiones.values()),
        fill='tonexty',
        mode='lines',
        line=dict(width=0),
        fillcolor='rgba(31, 119, 180, 0.2)',
        showlegend=False
    ))
    
    # Personalizar el gráfico
    fig.update_layout(
        title='Emisiones de CO₂ en Chile (2010-2025)',
        xaxis_title='Año',
        yaxis_title='Emisiones (Mt CO₂)',
        template='plotly_white',
        height=500,
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Resaltar años específicos
    for year in ['2015', '2020', '2025']:
        if year in emisiones:
            fig.add_annotation(
                x=year,
                y=emisiones[year],
                text=f"{emisiones[year]} Mt",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-30
            )
    
    save_plotly_as_html(fig, "emisiones_co2.html")
    print("✅ Visualización de emisiones CO2 completada")
except Exception as e:
    print(f"Error generando visualización de emisiones CO2: {e}")

# 2. Generar mapa de calidad del agua
try:
    print("\nGenerando mapa de calidad del agua...")
    import folium
    from folium.plugins import MarkerCluster
    
    # Cargar datos de estaciones
    estaciones = load_cache("coordenadas_estaciones.json")
    
    # Simular índices de calidad
    indices = {
        'Est. Santiago': 85,
        'Est. Valparaíso': 78,
        'Est. Concepción': 82,
        'Est. Antofagasta': 68,
        'Est. Puerto Montt': 90,
        'Est. Temuco': 76,
        'Est. La Serena': 72,
        'Est. Copiapó': 65
    }
    
    # Crear mapa base
    m = folium.Map(location=[-33.45, -70.67], zoom_start=5)
    marker_cluster = MarkerCluster().add_to(m)
    
    # Función para determinar color según índice
    def get_color(indice):
        if indice >= 85:
            return 'green'
        elif indice >= 70:
            return 'blue'
        elif indice >= 55:
            return 'orange'
        else:
            return 'red'
    
    # Añadir marcadores para cada estación
    for nombre, coords in estaciones.items():
        indice = indices.get(nombre, 50)
        color = get_color(indice)
        
        folium.Marker(
            location=[coords['lat'], coords['lon']],
            popup=f"<b>{nombre}</b><br>Índice de calidad: {indice}/100",
            tooltip=nombre,
            icon=folium.Icon(color=color, icon='tint', prefix='fa')
        ).add_to(marker_cluster)
    
    # Guardar mapa
    mapa_path = STATIC_DIR / "mapa_calidad_agua.html"
    m.save(str(mapa_path))
    print(f"✅ Mapa de calidad del agua guardado en: {mapa_path}")
except Exception as e:
    print(f"Error generando mapa de calidad del agua: {e}")

# 3. Generar gráficos de datos demográficos
try:
    print("\nGenerando visualización de datos demográficos...")
    datos_demo = load_cache("demograficos_procesados.json")
    
    # Pirámide poblacional
    piramide = datos_demo['piramide']
    grupos_edad = piramide['grupos_edad']
    
    # Convertir a valores positivos para mujeres (para la pirámide)
    hombres_2010 = piramide['hombres_2010']
    mujeres_2010 = [abs(x) for x in piramide['mujeres_2010']]
    hombres_2025 = piramide['hombres_2025']
    mujeres_2025 = [abs(x) for x in piramide['mujeres_2025']]
    
    # Pirámide para 2025
    fig = go.Figure()
    
    # Hombres 2010 (línea transparente)
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=hombres_2010,
        name='Hombres 2010',
        orientation='h',
        marker=dict(color='rgba(58, 71, 80, 0.3)')
    ))
    
    # Hombres 2025
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=hombres_2025,
        name='Hombres 2025',
        orientation='h',
        marker=dict(color='rgba(58, 71, 80, 0.8)')
    ))
    
    # Mujeres 2010 (línea transparente)
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=mujeres_2010,
        name='Mujeres 2010',
        orientation='h',
        marker=dict(color='rgba(191, 67, 66, 0.3)')
    ))
    
    # Mujeres 2025
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=mujeres_2025,
        name='Mujeres 2025',
        orientation='h',
        marker=dict(color='rgba(191, 67, 66, 0.8)')
    ))
    
    # Personalizar diseño
    fig.update_layout(
        title='Pirámide Poblacional: Chile 2010 vs 2025',
        barmode='overlay',
        bargap=0.1,
        bargroupgap=0,
        xaxis=dict(
            title='Población (miles)',
            tickvals=[-800, -600, -400, -200, 0, 200, 400, 600, 800],
            ticktext=['800', '600', '400', '200', '0', '200', '400', '600', '800'],
            zeroline=True,
            zerolinewidth=2,
            zerolinecolor='black'
        ),
        yaxis=dict(title='Grupos de edad'),
        legend=dict(x=0.5, y=1.1, orientation='h', xanchor='center'),
        template='plotly_white',
        height=600
    )
    
    save_plotly_as_html(fig, "piramide_poblacional.html")
    
    print("✅ Visualizaciones demográficas completadas")
except Exception as e:
    print(f"Error generando visualizaciones demográficas: {e}")

# 4. Generar gráficos de presupuesto
try:
    print("\nGenerando visualización de presupuesto público...")
    presupuesto = load_cache("presupuesto_procesado.json")
    
    # Gráfico de evolución por sectores
    fig = go.Figure()
    
    sectores = [s for s in presupuesto.keys() if s != 'años']
    años = presupuesto['años']
    
    for sector in sectores:
        fig.add_trace(go.Scatter(
            x=años,
            y=presupuesto[sector],
            mode='lines+markers',
            name=sector,
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title='Evolución del Presupuesto por Sector (2010-2025)',
        xaxis_title='Año',
        yaxis_title='Porcentaje del Presupuesto Total',
        template='plotly_white',
        height=500,
        legend_title='Sector',
        yaxis=dict(
            ticksuffix='%',
            range=[0, max([max(presupuesto[s]) for s in sectores]) * 1.1]
        )
    )
    
    save_plotly_as_html(fig, "evolucion_presupuesto.html")
    
    # Gráfico circular del último año
    año_actual = años[-1]
    idx_actual = años.index(año_actual)
    
    labels = sectores
    values = [presupuesto[sector][idx_actual] for sector in sectores]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values,
        hole=.4,
        textinfo='label+percent',
        insidetextorientation='radial',
        pull=[0.1 if sector == 'Educación' else 0 for sector in sectores]
    )])
    
    fig.update_layout(
        title=f'Distribución del Presupuesto Público {año_actual}',
        annotations=[dict(text=f'{año_actual}', x=0.5, y=0.5, font_size=20, showarrow=False)],
        template='plotly_white',
        height=500
    )
    
    save_plotly_as_html(fig, "distribucion_presupuesto.html")
    
    # Proyecciones futuras
    fig = go.Figure()
    
    # Proyectar 3 escenarios para 5 años adicionales
    años_proyección = list(range(años[-1] + 1, años[-1] + 6))
    todos_años = años + años_proyección
    
    # Proyección para Educación
    base = presupuesto['Educación'][-1]
    escenario_optimista = [base] + [base * (1 + 0.03 * i) for i in range(1, 6)]
    escenario_pesimista = [base] + [base * (1 - 0.015 * i) for i in range(1, 6)]
    escenario_neutro = [base] + [base * (1 + 0.01 * i) for i in range(1, 6)]
    
    # Valores históricos
    fig.add_trace(go.Scatter(
        x=años,
        y=presupuesto['Educación'],
        mode='lines+markers',
        name='Datos históricos',
        line=dict(color='blue', width=3)
    ))
    
    # Proyecciones
    fig.add_trace(go.Scatter(
        x=años_proyección,
        y=escenario_optimista,
        mode='lines',
        name='Escenario optimista',
        line=dict(color='green', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=años_proyección,
        y=escenario_neutro,
        mode='lines',
        name='Escenario neutro',
        line=dict(color='orange', dash='dash')
    ))
    
    fig.add_trace(go.Scatter(
        x=años_proyección,
        y=escenario_pesimista,
        mode='lines',
        name='Escenario pesimista',
        line=dict(color='red', dash='dash')
    ))
    
    # Sombreado entre escenarios
    fig.add_trace(go.Scatter(
        x=años_proyección + años_proyección[::-1],
        y=escenario_optimista + escenario_pesimista[::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Rango de proyección',
        showlegend=False
    ))
    
    fig.update_layout(
        title='Proyección del Presupuesto en Educación (2025-2030)',
        xaxis_title='Año',
        yaxis_title='Porcentaje del Presupuesto Total',
        template='plotly_white',
        height=500,
        legend_title='Escenario',
        yaxis=dict(
            ticksuffix='%',
            range=[min(escenario_pesimista) * 0.9, max(escenario_optimista) * 1.1]
        )
    )
    
    # Añadir anotación de fecha de proyección
    fig.add_annotation(
        x=años[-1],
        y=presupuesto['Educación'][-1],
        text="Inicio de proyección",
        showarrow=True,
        arrowhead=1,
        ax=0,
        ay=-40
    )
    
    save_plotly_as_html(fig, "proyeccion_presupuesto.html")
    
    print("✅ Visualizaciones de presupuesto completadas")
except Exception as e:
    print(f"Error generando visualizaciones de presupuesto: {e}")

# Crear archivo de metadatos de visualizaciones
metadata = {
    "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "visualizaciones": [
        {"nombre": "emisiones_co2.html", "tipo": "líneas", "tamaño_kb": os.path.getsize(STATIC_DIR / "emisiones_co2.html") / 1024},
        {"nombre": "mapa_calidad_agua.html", "tipo": "mapa", "tamaño_kb": os.path.getsize(STATIC_DIR / "mapa_calidad_agua.html") / 1024},
        {"nombre": "piramide_poblacional.html", "tipo": "barras", "tamaño_kb": os.path.getsize(STATIC_DIR / "piramide_poblacional.html") / 1024},
        {"nombre": "evolucion_presupuesto.html", "tipo": "líneas", "tamaño_kb": os.path.getsize(STATIC_DIR / "evolucion_presupuesto.html") / 1024},
        {"nombre": "distribucion_presupuesto.html", "tipo": "pie", "tamaño_kb": os.path.getsize(STATIC_DIR / "distribucion_presupuesto.html") / 1024},
        {"nombre": "proyeccion_presupuesto.html", "tipo": "líneas", "tamaño_kb": os.path.getsize(STATIC_DIR / "proyeccion_presupuesto.html") / 1024}
    ],
    "total_kb": sum([os.path.getsize(STATIC_DIR / f) / 1024 for f in os.listdir(STATIC_DIR) if f.endswith('.html')])
}

with open(STATIC_DIR / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("\n=== Resumen de visualizaciones generadas ===")
print(f"Total de visualizaciones: {len(metadata['visualizaciones'])}")
print(f"Tamaño total: {metadata['total_kb']:.1f} KB")
print("Visualizaciones listas para ser utilizadas en la aplicación")
print("Esto reducirá significativamente el consumo de recursos en Cloud Run")
