"""
Aplicación de Análisis Demográfico con BigQuery
==============================================

Esta aplicación visualiza y analiza tendencias demográficas históricas de nombres
en Estados Unidos desde 1910 hasta 2013, utilizando datos de BigQuery.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import sys
from pathlib import Path
from datetime import datetime

# Configuración de directorios
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
NOTEBOOKS_DIR = PROJECT_DIR / 'notebooks'
DATA_DIR = NOTEBOOKS_DIR / 'data'
VISUALIZATIONS_DIR = NOTEBOOKS_DIR / 'visualizaciones'

# Configuración de estilos y colores
GENDER_COLORS = {
    'M': '#1f77b4',  # Azul
    'F': '#e377c2'   # Rosa
}

GENDER_NAMES = {
    'M': 'Masculino',
    'F': 'Femenino'
}

DECADES = list(range(1910, 2020, 10))

class DemographicsApp:
    """Aplicación para análisis demográfico con BigQuery"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.data = None
        self.load_data()
        
    def load_data(self):
        """Carga los datos desde el archivo CSV"""
        try:
            # Intentar cargar desde CSV local
            data_path = DATA_DIR / 'nombres_demografia.csv'
            if data_path.exists():
                self.data = pd.read_csv(data_path)
                # Asegurar que decade sea int
                self.data['decade'] = self.data['decade'].astype(int)
            else:
                st.error("No se encontró el archivo de datos")
        except Exception as e:
            st.error(f"Error al cargar los datos: {str(e)}")

    def create_name_trends_visualization(self):
        """Crea visualización de tendencias de nombres populares"""
        if self.data is None:
            return None
            
        # Preparar datos
        df_trends = self.data.groupby(['decade', 'name', 'gender'])['total_count'].sum().reset_index()
        df_trends = df_trends.sort_values(['decade', 'total_count'], ascending=[True, False])
        
        # Crear figura con subplots
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Nombres Masculinos más Populares por Década', 
                          'Nombres Femeninos más Populares por Década'),
            vertical_spacing=0.12,
            row_heights=[0.5, 0.5]
        )
        
        # Procesar datos por género
        for idx, (gender, title) in enumerate([('M', 'Masculinos'), ('F', 'Femeninos')]):
            df_gender = df_trends[df_trends['gender'] == gender]
            top_names = []
            
            # Obtener top 5 nombres por década
            for decade in DECADES:
                decade_names = df_gender[df_gender['decade'] == decade] \
                    .nlargest(5, 'total_count')['name'].tolist()
                top_names.extend(decade_names)
            
            top_names = list(set(top_names))  # Eliminar duplicados
            
            # Crear líneas para cada nombre
            for name in top_names:
                name_data = df_gender[df_gender['name'] == name]
                
                fig.add_trace(
                    go.Scatter(
                        x=name_data['decade'],
                        y=name_data['total_count'],
                        name=name,
                        mode='lines+markers',
                        line=dict(width=2),
                        marker=dict(size=6),
                        showlegend=True
                    ),
                    row=idx+1, col=1
                )
        
        # Actualizar layout
        fig.update_layout(
            height=800,
            title_text="Tendencias de Nombres Populares (1910-2013)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Década", row=1, col=1)
        fig.update_xaxes(title_text="Década", row=2, col=1)
        fig.update_yaxes(title_text="Número de Nacimientos", row=1, col=1)
        fig.update_yaxes(title_text="Número de Nacimientos", row=2, col=1)
        
        return fig
    
    def render_name_trends(self):
        """Muestra tendencias de nombres populares"""
        st.subheader("📈 Tendencias de Nombres Populares")
        fig = self.create_name_trends_visualization()
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    def render_gender_analysis(self):
        """Muestra análisis por género"""
        if self.data is None:
            return
            
        st.subheader("👥 Análisis por Género")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top nombres masculinos
            df_m = self.data[self.data['gender'] == 'M']
            top_m = df_m.groupby('name')['total_count'].sum().sort_values(ascending=False).head(5)
            
            fig_m = go.Figure(data=[
                go.Bar(
                    x=top_m.index,
                    y=top_m.values,
                    marker_color=GENDER_COLORS['M']
                )
            ])
            fig_m.update_layout(
                title="Top 5 Nombres Masculinos",
                height=400
            )
            st.plotly_chart(fig_m, use_container_width=True)
            
        with col2:
            # Top nombres femeninos
            df_f = self.data[self.data['gender'] == 'F']
            top_f = df_f.groupby('name')['total_count'].sum().sort_values(ascending=False).head(5)
            
            fig_f = go.Figure(data=[
                go.Bar(
                    x=top_f.index,
                    y=top_f.values,
                    marker_color=GENDER_COLORS['F']
                )
            ])
            fig_f.update_layout(
                title="Top 5 Nombres Femeninos",
                height=400
            )
            st.plotly_chart(fig_f, use_container_width=True)
    
    def run(self):
        """Ejecuta la aplicación principal"""
        # Título y descripción
        st.markdown("""
        <div class="main-header">
            <h1>👤 Análisis Demográfico Histórico</h1>
            <p>Exploración de tendencias en nombres (1910-2013) usando BigQuery</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar estadísticas generales
        if self.data is not None:
            total_births = self.data['total_count'].sum()
            unique_names = self.data['name'].nunique()
            time_period = f"{self.data['decade'].min()}-{self.data['decade'].max()}"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                <div class="stat-box">
                    <div class="stat-number">{:,}</div>
                    <div class="stat-label">Nacimientos Registrados</div>
                </div>
                """.format(int(total_births)), unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div class="stat-box">
                    <div class="stat-number">{:,}</div>
                    <div class="stat-label">Nombres Únicos</div>
                </div>
                """.format(unique_names), unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                <div class="stat-box">
                    <div class="stat-number">{}</div>
                    <div class="stat-label">Periodo de análisis</div>
                </div>
                """.format(time_period), unsafe_allow_html=True)
        
        # Mostrar diferentes análisis
        self.render_name_trends()
        self.render_gender_analysis()
