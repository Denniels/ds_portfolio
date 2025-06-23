"""
Función personalizada para crear gráficos avanzados de distribución con Plotly
para el análisis de emisiones de CO2
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any

def create_region_scatter_plot(df_regiones, color_scale='Reds'):
    """
    Crea un scatter plot personalizado para mostrar la distribución regional de emisiones
    
    Args:
        df_regiones: DataFrame con datos regionales
        color_scale: Escala de colores para los puntos
        
    Returns:
        go.Figure: Gráfico de scatter personalizado
    """
    if df_regiones.empty or len(df_regiones) == 0:
        # Crear figura vacía con mensaje
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="red")
        )
        return fig
    
    # Ordenar por emisiones para mejor visualización
    df_sorted = df_regiones.sort_values('emisiones_mt', ascending=False)
    
    # Calcular tamaño para los puntos (normalizado entre 10 y 40)
    min_size = 10
    max_size = 40
    
    if len(df_sorted) > 1:
        min_val = df_sorted['emisiones_mt'].min()
        max_val = df_sorted['emisiones_mt'].max()
        size_range = max_val - min_val
        
        if size_range > 0:
            # Calcular tamaño normalizado
            df_sorted['point_size'] = df_sorted['emisiones_mt'].apply(
                lambda x: min_size + ((x - min_val) / size_range) * (max_size - min_size)
            )
        else:
            df_sorted['point_size'] = min_size
    else:
        df_sorted['point_size'] = min_size
    
    # Crear figura base
    fig = go.Figure()
    
    # Agregar scatter plot
    fig.add_trace(go.Scatter(
        x=df_sorted['emisiones_mt'],
        y=df_sorted['Region'],
        mode='markers',
        marker=dict(
            size=df_sorted['point_size'],
            color=df_sorted['emisiones_mt'],
            colorscale=color_scale,
            colorbar=dict(title='Mt CO₂'),
            line=dict(width=1, color='DarkSlateGray')
        ),
        text=[f"{row.Region}: {row.emisiones_mt} Mt CO₂" for _, row in df_sorted.iterrows()],
        hoverinfo='text'
    ))
    
    # Configuración avanzada
    fig.update_layout(
        title={
            'text': 'Distribución de Emisiones por Región',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#2F4F4F'}
        },
        height=600,
        template='plotly_white',
        margin=dict(l=80, r=40, t=100, b=60),
        xaxis=dict(
            title='Emisiones (Mt CO₂)',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='lightgray',
            zeroline=True,
            zerolinecolor='gray',
            zerolinewidth=1
        ),
        yaxis=dict(
            title='Región',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='lightgray'
        )
    )
    
    return fig

def create_boxplot_distribution(df_regiones, height=450):
    """
    Crea un boxplot mejorado para el análisis de distribución
    
    Args:
        df_regiones: DataFrame con datos regionales
        height: Altura del gráfico
        
    Returns:
        go.Figure: Boxplot mejorado
    """
    if df_regiones.empty or len(df_regiones) == 0:
        # Crear figura vacía con mensaje
        fig = go.Figure()
        fig.add_annotation(
            text="No hay datos disponibles para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="red")
        )
        return fig
    
    # Crear boxplot directamente con go.Box para mayor control
    fig = go.Figure()
    
    fig.add_trace(go.Box(
        y=df_regiones['emisiones_mt'],
        name='Emisiones',
        boxpoints='all',  # Mostrar todos los puntos
        jitter=0.5,  # Dispersar puntos
        pointpos=0,  # Centrar puntos en la caja
        marker=dict(
            color='#4ECDC4',
            size=8,
            line=dict(width=1, color='DarkSlateGray')
        ),
        line=dict(color='DarkSlateGray'),
        fillcolor='rgba(78, 205, 196, 0.5)'
    ))
    
    # Configuración avanzada
    fig.update_layout(
        title={
            'text': 'Análisis de Distribución (Boxplot)',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#2F4F4F'}
        },
        height=height,
        template='plotly_white',
        margin=dict(l=60, r=40, t=100, b=60),
        yaxis=dict(
            title='Emisiones (Mt CO₂)',
            showgrid=True,
            gridwidth=0.5,
            gridcolor='lightgray',
            zeroline=True,
            zerolinecolor='gray',
            zerolinewidth=1
        ),
        showlegend=False
    )
    
    return fig
