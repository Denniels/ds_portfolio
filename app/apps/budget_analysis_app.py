"""
Análisis del Presupuesto Público de Chile
========================================

Esta aplicación analiza la distribución del Presupuesto del Sector Público de Chile,
mostrando patrones de asignación y concentración presupuestaria a través de
visualizaciones interactivas y análisis detallado.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.request
import json
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Configuración de la aplicación
@dataclass
class AppConfig:
    """Configuración global de la aplicación"""
    API_URL: str = 'https://datos.gob.cl/api/3/action/datastore_search'
    RESOURCE_ID: str = '372b0680-d5f0-4d53-bffa-7997cf6e6512'
    CACHE_TTL: int = 3600  # 1 hora
    NIVELES: List[str] = ('Partida', 'Capitulo', 'Programa', 'Subtitulo')

# Funciones para manejo de datos
@st.cache_data(ttl=AppConfig.CACHE_TTL)
def fetch_budget_data(url: str, resource_id: str) -> Optional[pd.DataFrame]:
    """
    Obtiene y cachea los datos del presupuesto desde la API
    
    Args:
        url: URL base de la API
        resource_id: ID del recurso a consultar
    
    Returns:
        DataFrame con los datos procesados o None si hay error
    """
    try:
        full_url = f"{url}?resource_id={resource_id}&limit=10000"
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
        
        with st.spinner('Consultando API de datos.gob.cl...'):
            request = urllib.request.Request(full_url, headers=headers)
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if not data.get('success'):
                    st.error('La API no retornó datos válidos')
                    return None
                
                records = data.get('result', {}).get('records', [])
                if not records:
                    st.error('No se encontraron registros en la respuesta')
                    return None
                
                # Crear DataFrame y procesar datos
                df = pd.DataFrame(records)
                df['Monto Pesos'] = pd.to_numeric(df['Monto Pesos'], errors='coerce')
                df['Monto Dolar'] = pd.to_numeric(df['Monto Dolar'], errors='coerce')
                return df.fillna(0)
                
    except Exception as e:
        st.error(f"Error al obtener datos: {str(e)}")
        return None

class BudgetAnalysisApp:
    """Aplicación de análisis del presupuesto público de Chile"""    
    def __init__(self):
        """Inicializa la aplicación y sus componentes"""
        self.config = AppConfig()
        self.load_custom_styles()
        self.data: Optional[pd.DataFrame] = None

    def load_custom_styles(self) -> None:
        """Carga los estilos CSS personalizados"""
        st.markdown("""
            <style>
                .metric-container {
                    background-color: #f8f9fa;
                    border-radius: 0.5rem;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    border-left: 4px solid #2a5298;
                }
                .metric-label {
                    font-size: 0.9rem;
                    color: #666;
                    margin-bottom: 0.5rem;
                }
                .metric-value {
                    font-size: 1.8rem;
                    font-weight: bold;
                    color: #1f2937;
                }
                .analysis-container {
                    background-color: white;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    margin: 1rem 0;
                }
                .info-box {
                    background-color: #e7f1ff;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin: 1rem 0;
                    border: 1px solid #b3d7ff;
                }
            </style>
        """, unsafe_allow_html=True)

    def load_data(self) -> Optional[pd.DataFrame]:
        """
        Carga los datos del presupuesto usando la función cacheada
        
        Returns:
            DataFrame procesado o None si hay error
        """
        with st.spinner('Cargando datos del presupuesto...'):
            self.data = fetch_budget_data(self.config.API_URL, self.config.RESOURCE_ID)
            return self.data

    def plot_distribution(self, df: pd.DataFrame, nivel: str, top_n: int = 10) -> go.Figure:
        """
        Crea visualización de distribución por nivel jerárquico
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico a analizar
            top_n: Cantidad de entidades a mostrar
            
        Returns:
            Figura de Plotly con el gráfico
        """
        grouped = df.groupby(nivel)['Monto Pesos'].sum().sort_values(ascending=True).tail(top_n)
        
        fig = px.bar(
            grouped.reset_index(),
            x='Monto Pesos',
            y=nivel,
            orientation='h',
            title=f'Top {top_n} {nivel}s por Monto Total',
            labels={'Monto Pesos': 'Monto Total (Pesos)', nivel: nivel.capitalize()},
            text='Monto Pesos',
            color='Monto Pesos',
            color_continuous_scale='viridis'
        )
        
        fig.update_traces(
            texttemplate='$%{text:,.0f}',
            textposition='outside'
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10),
            xaxis_title="Monto Total (Pesos)",
            yaxis_title=nivel.capitalize()
        )
        
        return fig

    def plot_concentration(self, df: pd.DataFrame, nivel: str) -> go.Figure:
        """
        Crea análisis de concentración con gráfico combinado
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico a analizar
            
        Returns:
            Figura de Plotly con el gráfico combinado
        """
        grouped = df.groupby(nivel)['Monto Pesos'].sum().sort_values(ascending=False)
        top_data = grouped.head(10)
        total = grouped.sum()
        
        data_df = pd.DataFrame({
            nivel: top_data.index,
            'Monto': top_data.values,
            'Porcentaje': (top_data / total * 100),
            'Porcentaje Acumulado': (top_data / total * 100).cumsum()
        })
        
        # Crear gráfico combinado
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barras del porcentaje individual
        fig.add_trace(
            go.Bar(
                x=data_df[nivel],
                y=data_df['Porcentaje'],
                name='% del Total',
                marker_color='royalblue'
            ),
            secondary_y=False
        )
        
        # Línea del porcentaje acumulado
        fig.add_trace(
            go.Scatter(
                x=data_df[nivel],
                y=data_df['Porcentaje Acumulado'],
                name='% Acumulado',
                line=dict(color='firebrick', width=2),
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title=f'Análisis de Concentración - {nivel}',
            height=500,
            xaxis_tickangle=-45,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=10, r=10, t=50, b=10)
        )
        
        fig.update_yaxes(
            title_text="Porcentaje del Total",
            secondary_y=False,
            gridcolor='lightgray'
        )
        fig.update_yaxes(
            title_text="Porcentaje Acumulado",
            secondary_y=True,
            gridcolor='lightgray'
        )
        
        return fig

    def show_metrics(self, df: pd.DataFrame) -> None:
        """
        Muestra métricas principales del presupuesto
        
        Args:
            df: DataFrame con los datos a analizar
        """
        total_presupuesto = df['Monto Pesos'].sum()
        total_partidas = df['Partida'].nunique()
        total_programas = df['Programa'].nunique()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            with st.container():
                st.markdown("""
                    <div class="metric-container">
                        <div class="metric-label">Total Presupuesto</div>
                        <div class="metric-value">${:,.0f}</div>
                    </div>
                """.format(total_presupuesto), unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown("""
                    <div class="metric-container">
                        <div class="metric-label">Número de Partidas</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(total_partidas), unsafe_allow_html=True)
        
        with col3:
            with st.container():
                st.markdown("""
                    <div class="metric-container">
                        <div class="metric-label">Total Programas</div>
                        <div class="metric-value">{}</div>
                    </div>
                """.format(total_programas), unsafe_allow_html=True)

    def show_detailed_data(self, df: pd.DataFrame, nivel: str) -> None:
        """
        Muestra tabla detallada de datos
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico seleccionado
        """
        with st.expander('Ver Datos Detallados', expanded=False):
            st.dataframe(
                df[[nivel, 'Denominacion', 'Monto Pesos']]
                .groupby(nivel)
                .agg({
                    'Denominacion': 'first',
                    'Monto Pesos': 'sum'
                })
                .sort_values('Monto Pesos', ascending=False)
                .style.format({
                    'Monto Pesos': '${:,.0f}'
                })
            )

    def run(self) -> None:
        """Ejecuta la aplicación principal"""
        st.title('📊 Análisis del Presupuesto Público de Chile')
        
        # Descripción de la aplicación
        with st.container():
            st.markdown("""
                Esta aplicación proporciona un análisis interactivo del Presupuesto del Sector 
                Público de Chile, permitiendo explorar su distribución a través de diferentes 
                niveles jerárquicos y visualizar patrones de concentración presupuestaria.
                
                Los datos son obtenidos en tiempo real desde [datos.gob.cl](https://datos.gob.cl/) 
                a través de su API pública.
            """)
        
        # Cargar y validar datos
        df = self.load_data()
        if df is None:
            st.error("No se pudieron cargar los datos. Por favor, intente más tarde.")
            return
        
        # Mostrar métricas principales
        self.show_metrics(df)
        
        # Selector de nivel jerárquico
        nivel = st.selectbox(
            'Seleccione nivel jerárquico para análisis:',
            self.config.NIVELES,
            help="Escoja el nivel jerárquico que desea analizar en detalle"
        )
        
        # Contenedor principal de visualizaciones
        with st.container():
            st.markdown('<div class="analysis-container">', unsafe_allow_html=True)
            
            # Distribución principal
            st.subheader(f"Distribución por {nivel}")
            st.plotly_chart(
                self.plot_distribution(df, nivel),
                use_container_width=True
            )
            
            # Análisis de concentración
            st.subheader(f"Análisis de Concentración - {nivel}")
            st.plotly_chart(
                self.plot_concentration(df, nivel),
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Datos detallados
        self.show_detailed_data(df, nivel)
        
        # Nota informativa
        st.markdown("""
            <div class="info-box">
                <b>📝 Nota:</b> Los montos se presentan en pesos chilenos. 
                Los gráficos son interactivos - puede hacer zoom, pan y hover para más detalles.
                Los datos se actualizan automáticamente cada hora desde la fuente oficial.
            </div>
        """, unsafe_allow_html=True)

if __name__ == '__main__':
    # Configurar página solo si se ejecuta directamente
    st.set_page_config(
        page_title="💰 Análisis Presupuestario Chile",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    app = BudgetAnalysisApp()
    app.run()

def main():
    """Función principal para ejecutar desde el portafolio"""
    app = BudgetAnalysisApp()
    app.run()
