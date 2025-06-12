"""
Utilidades para creación de gráficos y visualizaciones
=====================================================
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st

def create_temporal_chart(df, parameter, title=None):
    """Crea gráfico temporal para un parámetro"""
    
    if parameter not in df.columns:
        return None
    
    # Verificar que existan las columnas necesarias para el análisis temporal
    if 'año' not in df.columns or 'mes' not in df.columns:
        st.warning("⚠️ No se encontraron columnas de fecha válidas para análisis temporal")
        return None
    
    try:
        # Agrupar por año y mes
        monthly_data = df.groupby(['año', 'mes'])[parameter].agg(['mean', 'count']).reset_index()
        
        # Crear columna de fecha usando datetime iterativo (corrección aplicada)
        dates = []
        for _, row in monthly_data.iterrows():
            try:
                date = datetime(int(row['año']), int(row['mes']), 1)
                dates.append(date)
            except (ValueError, TypeError):
                dates.append(None)
        
        monthly_data['fecha'] = dates
        monthly_data = monthly_data.dropna(subset=['fecha'])
        
        if len(monthly_data) == 0:
            st.warning("⚠️ No hay datos temporales válidos para crear el gráfico")
            return None
        
        # Crear gráfico
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=monthly_data['fecha'],
            y=monthly_data['mean'],
            mode='lines+markers',
            name=f'Promedio mensual',
            line=dict(width=3, color='#0891b2'),
            marker=dict(size=6),
            hovertemplate="<b>%{x|%Y-%m}</b><br>" +
                        f"{parameter}: %{{y:.2f}}<br>" +
                        "N° mediciones: %{customdata}<br>" +
                        "<extra></extra>",
            customdata=monthly_data['count']
        ))
        
        # Configurar layout
        fig.update_layout(
            title=title or f"Evolución Temporal - {parameter}",
            xaxis_title="Fecha",
            yaxis_title=parameter,
            template='plotly_white',
            hovermode='x unified',
            height=400
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error creando gráfico temporal: {str(e)}")
        return None

def create_station_comparison_chart(df, parameter, stations, chart_type='box'):
    """Crea gráfico de comparación entre estaciones"""
    
    if parameter not in df.columns or 'GLS_ESTACION' not in df.columns:
        return None
    
    # Filtrar datos por estaciones seleccionadas
    station_data = df[df['GLS_ESTACION'].isin(stations)]
    
    if station_data.empty:
        return None
    
    try:
        if chart_type == 'box':
            fig = px.box(
                station_data,
                x='GLS_ESTACION',
                y=parameter,
                title=f'Distribución de {parameter} por Estación',
                color='GLS_ESTACION'
            )
            
        elif chart_type == 'violin':
            fig = px.violin(
                station_data,
                x='GLS_ESTACION',
                y=parameter,
                title=f'Distribución de {parameter} por Estación',
                color='GLS_ESTACION'
            )
            
        else:  # bar chart con promedios
            station_summary = station_data.groupby('GLS_ESTACION')[parameter].agg(['mean', 'std', 'count']).reset_index()
            
            fig = px.bar(
                station_summary,
                x='GLS_ESTACION',
                y='mean',
                error_y='std',
                title=f'Promedio de {parameter} por Estación',
                color='mean',
                color_continuous_scale='Viridis'
            )
        
        # Configurar layout
        fig.update_layout(
            xaxis_tickangle=-45,
            template='plotly_white',
            height=400
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error creando gráfico de comparación: {str(e)}")
        return None

def create_correlation_heatmap(df, parameters):
    """Crea un mapa de calor de correlaciones entre parámetros"""
    
    # Filtrar solo columnas numéricas que existen
    numeric_params = [p for p in parameters if p in df.columns and pd.api.types.is_numeric_dtype(df[p])]
    
    if len(numeric_params) < 2:
        return None
    
    try:
        # Calcular matriz de correlación
        corr_matrix = df[numeric_params].corr()
        
        # Crear heatmap
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Matriz de Correlación entre Parámetros",
            color_continuous_scale='RdBu'
        )
        
        fig.update_layout(
            template='plotly_white',
            height=500
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error creando mapa de correlación: {str(e)}")
        return None

def create_seasonal_analysis_chart(df, parameter):
    """Crea gráfico de análisis estacional"""
    
    if parameter not in df.columns or 'mes' not in df.columns:
        return None
    
    try:
        # Datos estacionales
        seasonal_data = df.groupby('mes')[parameter].agg(['mean', 'std', 'count']).reset_index()
        
        # Nombres de meses
        month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                      'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        seasonal_data['mes_nombre'] = seasonal_data['mes'].map(lambda x: month_names[x-1] if 1 <= x <= 12 else 'N/A')
        
        # Crear gráfico
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=seasonal_data['mes_nombre'],
            y=seasonal_data['mean'],
            mode='lines+markers',
            name='Promedio mensual',
            line=dict(width=3, color='#0891b2'),
            marker=dict(size=8),
            error_y=dict(type='data', array=seasonal_data['std'], visible=True),
            hovertemplate="<b>%{x}</b><br>" +
                        "Promedio: %{y:.2f}<br>" +
                        "Desv. Est.: %{error_y.array:.2f}<br>" +
                        "N° mediciones: %{customdata}<br>" +
                        "<extra></extra>",
            customdata=seasonal_data['count']
        ))
        
        fig.update_layout(
            title=f"Variación Estacional - {parameter}",
            xaxis_title="Mes",
            yaxis_title=parameter,
            template='plotly_white',
            height=400
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error creando análisis estacional: {str(e)}")
        return None

def create_distribution_chart(df, parameter):
    """Crea gráfico de distribución de un parámetro"""
    
    if parameter not in df.columns:
        return None
    
    try:
        # Crear subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Histograma', 'Box Plot'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Histograma
        fig.add_trace(
            go.Histogram(
                x=df[parameter].dropna(),
                nbinsx=30,
                name='Distribución',
                marker_color='#0891b2',
                opacity=0.7
            ),
            row=1, col=1
        )
        
        # Box plot
        fig.add_trace(
            go.Box(
                y=df[parameter].dropna(),
                name='Estadísticas',
                marker_color='#06b6d4'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f"Distribución de {parameter}",
            template='plotly_white',
            height=400,
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Error creando gráfico de distribución: {str(e)}")
        return None
