"""
Script para exportar visualizaciones del notebook de análisis demográfico
"""
import os
import json
import nbformat
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from google.cloud import bigquery

def ejecutar_consulta_nombres():
    """Ejecuta la consulta de análisis de nombres y retorna el DataFrame"""
    client = bigquery.Client()
    
    query = """
    WITH DecadeData AS (
        SELECT
            CAST(FLOOR(year/10) * 10 AS INT64) as decade,
            name,
            gender,
            CAST(SUM(number) AS INT64) as total_count
        FROM `bigquery-public-data.usa_names.usa_1910_2013`
        GROUP BY 
            CAST(FLOOR(year/10) * 10 AS INT64),
            name, 
            gender
        HAVING CAST(SUM(number) AS INT64) > 10000
    ),
    RankedNames AS (
        SELECT
            decade,
            name,
            gender,
            total_count,
            RANK() OVER(
                PARTITION BY decade, gender 
                ORDER BY total_count DESC
            ) as rank
        FROM DecadeData
    )
    SELECT *
    FROM RankedNames
    WHERE rank <= 5
    ORDER BY decade, gender, rank
    """
    
    return client.query(query).to_dataframe()

def crear_visualizacion_nombres(df_nombres):
    """Crea la visualización de tendencias de nombres"""
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Nombres más populares - Masculinos',
                       'Nombres más populares - Femeninos'),
        vertical_spacing=0.12
    )
    
    # Gráfico para nombres masculinos
    df_m = df_nombres[df_nombres['gender'] == 'M']
    for name in df_m['name'].unique():
        data_name = df_m[df_m['name'] == name]
        fig.add_trace(
            go.Scatter(x=data_name['decade'], 
                      y=data_name['total_count'],
                      name=name, 
                      mode='lines+markers'),
            row=1, col=1
        )
    
    # Gráfico para nombres femeninos
    df_f = df_nombres[df_nombres['gender'] == 'F']
    for name in df_f['name'].unique():
        data_name = df_f[df_f['name'] == name]
        fig.add_trace(
            go.Scatter(x=data_name['decade'], 
                      y=data_name['total_count'],
                      name=name, 
                      mode='lines+markers'),
            row=2, col=1
        )
    
    fig.update_layout(
        height=800, width=1000,
        title_text="Tendencias de Nombres Populares por Década (1910-2013)",
        showlegend=True
    )
    fig.update_xaxes(title_text="Década", row=2, col=1)
    fig.update_yaxes(title_text="Número total", row=1, col=1)
    fig.update_yaxes(title_text="Número total", row=2, col=1)
    
    return fig

def guardar_visualizaciones(fig, nombre_base, carpeta='notebooks/visualizaciones'):
    """Guarda una figura en formatos PNG y HTML"""
    # Crear carpeta si no existe
    os.makedirs(carpeta, exist_ok=True)
    
    # Rutas completas
    ruta_png = os.path.join(carpeta, f"{nombre_base}.png")
    ruta_html = os.path.join(carpeta, f"{nombre_base}.html")
    
    try:
        # Guardar como PNG
        fig.write_image(ruta_png)
        print(f"✅ PNG guardado en: {ruta_png}")
        
        # Guardar como HTML
        fig.write_html(ruta_html)
        print(f"✅ HTML guardado en: {ruta_html}")
        
    except Exception as e:
        print(f"❌ Error al guardar visualización: {str(e)}")
        raise

def main():
    try:
        print("📊 Iniciando exportación de visualizaciones...")
        
        # 1. Obtener datos
        print("\n1️⃣ Ejecutando consulta de nombres...")
        df_nombres = ejecutar_consulta_nombres()
        print(f"✅ Datos obtenidos: {len(df_nombres)} registros")
        
        # 2. Crear visualización
        print("\n2️⃣ Creando visualización...")
        fig = crear_visualizacion_nombres(df_nombres)
        print("✅ Visualización creada")
        
        # 3. Guardar visualizaciones
        print("\n3️⃣ Guardando visualizaciones...")
        guardar_visualizaciones(fig, 'tendencias_nombres')
        
        print("\n✨ Proceso completado exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error en el proceso: {str(e)}")
        raise

if __name__ == "__main__":
    main()
