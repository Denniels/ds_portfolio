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

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #6366f1;
    }
    
    .stat-label {
        color: #4b5563;
        margin-top: 0.5rem;
    }
    
    .info-box {
        background: #f3f4f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class DemographicsApp:
    """Aplicación para análisis demográfico con BigQuery"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.data = None
        self.data_paths = {
            'names': DATA_DIR / 'nombres_demografia.csv',
            'html_viz': VISUALIZATIONS_DIR / 'tendencias_nombres.html',
            'png_viz': VISUALIZATIONS_DIR / 'tendencias_nombres.png',
        }
    
    def load_data(self):
        """Carga los datos para el análisis"""
        try:
            if self.data_paths['names'].exists():
                self.data = pd.read_csv(self.data_paths['names'])
                if 'decade' in self.data.columns:
                    self.data['decade'] = self.data['decade'].astype(int)
                return True
            else:
                st.warning("No se encontraron datos precalculados. Usando datos de demostración.")
                self.data = self._create_demo_data()
                return False
        except Exception as e:
            st.error(f"Error al cargar datos: {str(e)}")
            return False
    
    def _create_demo_data(self):
        """Crea datos de demostración"""
        decades = range(1910, 2020, 10)
        names_m = ['Juan', 'Carlos', 'Luis', 'Miguel', 'Pedro']
        names_f = ['María', 'Ana', 'Laura', 'Isabel', 'Carmen']
        
        data = []
        for decade in decades:
            for name in names_m:
                count = np.random.randint(1000, 10000)
                data.append({'name': name, 'gender': 'M', 'decade': decade, 'total_count': count})
            for name in names_f:
                count = np.random.randint(1000, 10000)
                data.append({'name': name, 'gender': 'F', 'decade': decade, 'total_count': count})
        
        return pd.DataFrame(data)
    
    def render_header(self):
        """Muestra el encabezado de la aplicación"""
        st.markdown("""
        <div class="main-header">
            <h1>👤 Análisis Demográfico Histórico</h1>
            <p>Exploración de tendencias en nombres (1910-2013) usando BigQuery</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_overview_metrics(self):
        """Muestra métricas generales del análisis"""
        if self.data is None:
            return
            
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_births = self.data['total_count'].sum()
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{total_births:,.0f}</div>
                <div class="stat-label">Nacimientos Registrados</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            unique_names = self.data['name'].nunique()
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{unique_names:,}</div>
                <div class="stat-label">Nombres Únicos</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            year_range = f"{self.data['decade'].min()}-{self.data['decade'].max()}"
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{year_range}</div>
                <div class="stat-label">Período de Análisis</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_trends_visualization(self):
        """Muestra las visualizaciones de tendencias"""
        st.subheader("📈 Tendencias de Nombres Populares")
        
        # Intentar mostrar visualización HTML existente
        if self.data_paths['html_viz'].exists():
            with open(self.data_paths['html_viz'], 'r', encoding='utf-8') as f:
                html_content = f.read()
                st.components.v1.html(
                    html_content,
                    height=900,
                    scrolling=True
                )
        else:
            # Crear visualización en tiempo real
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
    
    def render_temporal_analysis(self):
        """Muestra análisis temporal"""
        if self.data is None:
            return
            
        st.subheader("⏳ Evolución Temporal")
        
        # Diversidad de nombres por década
        df_diversity = self.data.groupby(['decade', 'gender'])['name'].nunique().reset_index()
        
        fig = px.line(
            df_diversity,
            x='decade',
            y='name',
            color='gender',
            color_discrete_map=GENDER_COLORS,
            labels={'name': 'Nombres Únicos', 'decade': 'Década', 'gender': 'Género'},
            title='Diversidad de Nombres por Década'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_methodology(self):
        """Muestra información sobre la metodología"""
        with st.expander("ℹ️ Metodología y Fuentes de Datos"):
            st.markdown("""
            ### 📊 Fuente de Datos
            
            Este análisis utiliza el conjunto de datos público de nombres de Estados Unidos disponible
            en Google BigQuery (`bigquery-public-data.usa_names.usa_1910_2013`).
            
            ### 🔍 Metodología de Análisis
            
            1. **Extracción de Datos**
               - Consultas SQL a BigQuery
               - Procesamiento con pandas
               - Agregación por décadas
            
            2. **Métricas Calculadas**
               - Total de nacimientos por nombre y género
               - Diversidad de nombres por década
               - Tendencias temporales
            
            3. **Visualizaciones**
               - Gráficos interactivos con Plotly
               - Exportación a HTML y PNG
               - Análisis comparativo por género
            
            ### ⚠️ Limitaciones
            
            - Los datos están limitados a EE.UU.
            - Período temporal: 1910-2013
            - Solo nombres con más de 5 ocurrencias por año
            - Posibles sesgos en el registro histórico
            """)
    
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
    
    def run(self):
        """Ejecuta la aplicación principal"""
        # Cargar datos
        self.load_data()
        
        # Renderizar interfaz
        self.render_header()
        
        # Métricas generales
        self.render_overview_metrics()
        
        # Separador
        st.markdown("---")
        
        # Crear tabs para diferentes análisis
        tab1, tab2, tab3 = st.tabs([
            "📈 Tendencias Históricas",
            "👥 Análisis por Género",
            "⏳ Análisis Temporal"
        ])
        
        with tab1:
            self.render_trends_visualization()
        
        with tab2:
            self.render_gender_analysis()
        
        with tab3:
            self.render_temporal_analysis()
        
        # Metodología
        st.markdown("---")
        self.render_methodology()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #64748b; padding: 1rem;'>
            👤 <strong>Análisis Demográfico Histórico</strong> | 
            Datos: BigQuery Public Datasets (usa_names) | 
            📊 <strong>Portafolio Data Science</strong>
        </div>
        """, unsafe_allow_html=True)

def run():
    """Punto de entrada para la aplicación cuando se carga desde el portafolio"""
    app = DemographicsApp()
    app.run()

if __name__ == "__main__":
    # Solo configurar la página si se ejecuta directamente (no desde el portafolio)
    st.set_page_config(
        page_title="👤 Análisis Demográfico - Tendencias Históricas",
        page_icon="👤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    run()
