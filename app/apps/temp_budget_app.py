import streamlit as st

"""
Análisis del Presupuesto Público de Chile v2.0
============================================

Esta aplicación proporciona un análisis interactivo y detallado del Presupuesto del 
Sector Público de Chile, con visualizaciones avanzadas y análisis contextual.
"""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.request
import json
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass

# Configuración de la aplicación
@dataclass
class AppConfig:
    """Configuración global de la aplicación"""
    API_URL: str = 'https://datos.gob.cl/api/3/action/datastore_search'
    RESOURCE_ID: str = '372b0680-d5f0-4d53-bffa-7997cf6e6512'
    CACHE_TTL: int = 3600  # 1 hora
    NIVELES: List[str] = ('Partida', 'Capitulo', 'Programa', 'Subtitulo')

# Función global cacheada
@st.cache_data(ttl=3600)  # 1 hora de caché
def fetch_budget_data_cached(api_url: str, resource_id: str) -> Optional[pd.DataFrame]:
    """
    Función cacheada para obtener datos del presupuesto
    
    Args:
        api_url: URL base de la API
        resource_id: ID del recurso a consultar
        
    Returns:
        DataFrame procesado o None si hay error
    """
    try:
        url = f"{api_url}?resource_id={resource_id}&limit=10000"
        headers = {'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}
        
        with st.spinner('Consultando datos oficiales...'):
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if not data.get('success'):
                    st.error('La API no retornó datos válidos')
                    return None
                
                records = data.get('result', {}).get('records', [])
                if not records:
                    st.error('No se encontraron registros')
                    return None
                
                df = pd.DataFrame(records)
                df['Monto Pesos'] = pd.to_numeric(df['Monto Pesos'], errors='coerce')
                df['Monto Dolar'] = pd.to_numeric(df['Monto Dolar'], errors='coerce')
                return df.fillna(0)
                
    except Exception as e:
        st.error(f"Error al obtener datos: {str(e)}")
        return None

class BudgetAnalysisApp:
    """Aplicación de análisis del presupuesto público de Chile (Versión 2.0)"""
    
    def __init__(self):
        """Inicializa la aplicación y sus componentes"""
        self.config = AppConfig()
        self.load_custom_styles()
        self.data: Optional[pd.DataFrame] = None
        self.nivel_actual: Optional[str] = None
        self.insights: Dict[str, str] = self.get_insights_dict()

    def load_custom_styles(self) -> None:
        """Define los estilos personalizados de la aplicación"""
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
                .insight-box {
                    background-color: #e7f1ff;
                    border-radius: 0.5rem;
                    padding: 1rem;
                    margin: 1rem 0;
                    border: 1px solid #b3d7ff;
                }
                .analysis-section {
                    background-color: white;
                    padding: 1.5rem;
                    border-radius: 0.5rem;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    margin: 1rem 0;
                }
                .help-text {
                    font-size: 0.9rem;
                    color: #666;
                    font-style: italic;
                }
                .trend-indicator-up {
                    color: #28a745;
                }
                .trend-indicator-down {
                    color: #dc3545;
                }
                .sidebar-info {
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-top: 2rem;
                }
            </style>
        """, unsafe_allow_html=True)

    def fetch_budget_data(self) -> Optional[pd.DataFrame]:
        """
        Obtiene datos del presupuesto usando la función cacheada
        
        Returns:
            DataFrame procesado o None si hay error
        """
        return fetch_budget_data_cached(self.config.API_URL, self.config.RESOURCE_ID)

    def get_insights_dict(self) -> Dict[str, str]:
        """
        Define los insights y explicaciones para cada nivel jerárquico
        
        Returns:
            Diccionario con explicaciones por nivel
        """
        return {
            'Partida': """
                Las Partidas representan el nivel más alto de la estructura presupuestaria, 
                correspondiendo generalmente a ministerios o grandes servicios del Estado.
                Un alto nivel de concentración en pocas partidas puede indicar prioridades
                gubernamentales específicas o áreas de foco en el gasto público.
            """,
            'Capitulo': """
                Los Capítulos son subdivisiones de las Partidas y representan servicios
                públicos específicos o unidades administrativas. La distribución a este
                nivel muestra cómo se asignan los recursos dentro de cada ministerio
                o servicio principal.
            """,
            'Programa': """
                Los Programas son unidades operativas que representan iniciativas
                específicas. La concentración a nivel de programas puede indicar
                las prioridades específicas de política pública y cómo se están
                asignando recursos a diferentes iniciativas.
            """,
            'Subtitulo': """
                Los Subtítulos representan la clasificación económica del gasto,
                indicando el tipo de transacción (ej: gastos en personal, bienes
                y servicios, inversión). Este nivel ayuda a entender cómo se está
                gastando el presupuesto en términos económicos.
            """
        }

    def calculate_concentration_metrics(self, df: pd.DataFrame, nivel: str) -> Tuple[float, float, float]:
        """
        Calcula métricas de concentración presupuestaria
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico a analizar
            
        Returns:
            Tuple con índice de concentración, % top 3 y % top 10
        """
        grouped = df.groupby(nivel)['Monto Pesos'].sum().sort_values(ascending=False)
        total = grouped.sum()
        
        # Calcular métricas
        top_3_pct = (grouped.head(3).sum() / total) * 100
        top_10_pct = (grouped.head(10).sum() / total) * 100
        
        # Índice de concentración (HHI simplificado)
        shares = (grouped / total) * 100
        hhi = (shares ** 2).sum() / 10000  # Normalizado entre 0 y 1
        
        return hhi, top_3_pct, top_10_pct

    def plot_budget_evolution(self, df: pd.DataFrame, nivel: str) -> go.Figure:
        """
        Crea visualización de tendencias y patrones
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico a analizar
            
        Returns:
            Figura de Plotly
        """
        # Simulamos evolución temporal (ya que los datos son de un punto en el tiempo)
        grouped = df.groupby(nivel)['Monto Pesos'].sum().sort_values(ascending=False).head(5)
        
        # Crear matriz de datos simulados
        periods = ['2021', '2022', '2023', '2024', '2025']
        data = {}
        for entity in grouped.index:
            base = grouped[entity]
            # Simular variación con tendencia y ruido
            variations = np.random.normal(1.05, 0.02, len(periods))
            values = base * np.cumprod(variations)
            data[entity] = values
        
        # Crear figura
        fig = go.Figure()
        
        for entity in data.keys():
            fig.add_trace(
                go.Scatter(
                    x=periods,
                    y=data[entity],
                    name=entity,
                    mode='lines+markers',
                    hovertemplate=f"{entity}<br>Monto: $%{{y:,.0f}}<extra></extra>"
                )
            )
        
        fig.update_layout(
            title=f'Simulación de Evolución Presupuestaria - Top 5 {nivel}s',
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            xaxis_title="Año",
            yaxis_title="Monto (Pesos)",
            hovermode='x unified'
        )
        
        return fig

    def plot_distribution_analysis(self, df: pd.DataFrame, nivel: str) -> go.Figure:
        """
        Crea visualización de distribución y desigualdad
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico a analizar
            
        Returns:
            Figura de Plotly
        """
        grouped = df.groupby(nivel)['Monto Pesos'].sum().sort_values(ascending=False)
        total_entities = len(grouped)
        cumsum = grouped.cumsum() / grouped.sum() * 100
        
        # Línea de perfecta igualdad
        perfect_equality = np.linspace(0, 100, total_entities)
        
        # Crear figura
        fig = go.Figure()
        
        # Agregar línea de perfecta igualdad
        fig.add_trace(
            go.Scatter(
                x=np.linspace(0, 100, total_entities),
                y=perfect_equality,
                name='Igualdad Perfecta',
                line=dict(color='gray', dash='dash'),
                hovertemplate="Igualdad Perfecta<br>%{y:.1f}%<extra></extra>"
            )
        )
        
        # Agregar curva de Lorenz
        fig.add_trace(
            go.Scatter(
                x=np.linspace(0, 100, total_entities),
                y=cumsum.values,
                name='Distribución Real',
                line=dict(color='firebrick'),
                fill='tonexty',
                hovertemplate="Distribución Real<br>%{y:.1f}%<extra></extra>"
            )
        )
        
        fig.update_layout(
            title=f'Análisis de Desigualdad en la Distribución - {nivel}',
            height=500,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            xaxis_title="Porcentaje Acumulado de Entidades",
            yaxis_title="Porcentaje Acumulado del Presupuesto",
            hovermode='x unified'
        )
        
        return fig

    def show_concentration_metrics(self, df: pd.DataFrame, nivel: str) -> None:
        """
        Muestra métricas de concentración
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico actual
        """
        hhi, top_3_pct, top_10_pct = self.calculate_concentration_metrics(df, nivel)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Índice de Concentración</div>
                    <div class="metric-value">{hhi:.2f}</div>
                    <div class="help-text">Un valor cercano a 1 indica alta concentración</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Concentración Top 3</div>
                    <div class="metric-value">{top_3_pct:.1f}%</div>
                    <div class="help-text">Porcentaje del presupuesto en top 3</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Concentración Top 10</div>
                    <div class="metric-value">{top_10_pct:.1f}%</div>
                    <div class="help-text">Porcentaje del presupuesto en top 10</div>
                </div>
            """, unsafe_allow_html=True)

    def show_insights(self, nivel: str) -> None:
        """
        Muestra insights y explicaciones para el nivel actual
        
        Args:
            nivel: Nivel jerárquico seleccionado
        """
        with st.expander("ℹ️ Información sobre este nivel jerárquico", expanded=True):
            st.markdown(f"""
                <div class="insight-box">
                    <h4>📊 {nivel}</h4>
                    {self.insights.get(nivel, 'Información no disponible')}
                </div>
            """, unsafe_allow_html=True)

    def show_detailed_data(self, df: pd.DataFrame, nivel: str) -> None:
        """
        Muestra tabla detallada de datos
        
        Args:
            df: DataFrame con los datos
            nivel: Nivel jerárquico seleccionado
        """
        with st.expander('📑 Ver Datos Detallados', expanded=False):
            # Preparar datos
            detailed_df = (df.groupby(nivel)
                         .agg({
                             'Denominacion': 'first',
                             'Monto Pesos': ['sum', 'count', 'mean']
                         })
                         .round(2))
            
            detailed_df.columns = ['Denominación', 'Monto Total', 'N° Items', 'Monto Promedio']
            detailed_df = detailed_df.sort_values('Monto Total', ascending=False)
            
            # Mostrar tabla
            st.dataframe(
                detailed_df.style.format({
                    'Monto Total': '${:,.0f}',
                    'Monto Promedio': '${:,.0f}'
                }),
                use_container_width=True
            )
            
            # Agregar botón de descarga
            csv = detailed_df.to_csv(index=True)
            st.download_button(
                "⬇️ Descargar datos como CSV",
                csv,
                f"datos_presupuesto_{nivel.lower()}.csv",
                "text/csv",
                key=f'download_{nivel}'
            )

    def run(self) -> None:
        """Ejecuta la aplicación principal"""
        st.title('📊 Análisis del Presupuesto Público de Chile v2.0')
        
        # Descripción principal
        st.markdown("""
            Esta aplicación proporciona un análisis interactivo y detallado del Presupuesto del 
            Sector Público de Chile. Explore diferentes niveles jerárquicos, descubra patrones
            de concentración y analice la distribución de recursos públicos.
        """)
        
        # Sidebar con información adicional
        with st.sidebar:
            st.markdown("""
                ### 📌 Acerca del Análisis
                
                Este análisis permite explorar:
                - 📊 Distribución presupuestaria
                - 📈 Patrones de concentración
                - 🎯 Asignación de recursos
                - 📉 Desigualdad en la distribución
                
                Los datos son obtenidos directamente 
                desde [datos.gob.cl](https://datos.gob.cl/)
                y se actualizan automáticamente.
            """)
            
            st.markdown("""
                <div class="sidebar-info">
                <h4>🔄 Actualización de Datos</h4>
                Los datos se actualizan cada hora para
                garantizar información actualizada.
                </div>
            """, unsafe_allow_html=True)
        
        # Cargar datos
        df = self.fetch_budget_data()
        
        if df is not None:
            # Selector de nivel jerárquico
            nivel = st.selectbox(
                'Seleccione nivel jerárquico para análisis:',
                self.config.NIVELES,
                help="Escoja el nivel jerárquico que desea analizar en detalle"
            )
            
            # Mostrar insights del nivel seleccionado
            self.show_insights(nivel)
            
            # Métricas de concentración
            st.subheader('📊 Métricas de Concentración')
            self.show_concentration_metrics(df, nivel)
            
            # Análisis de distribución
            st.subheader('📈 Análisis de Distribución')
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    self.plot_distribution_analysis(df, nivel),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    self.plot_budget_evolution(df, nivel),
                    use_container_width=True
                )
            
            # Datos detallados
            st.subheader('📑 Datos Detallados')
            self.show_detailed_data(df, nivel)
            
            # Nota informativa
            st.markdown("""
                <div class="insight-box">
                <h4>📝 Notas Metodológicas</h4>
                
                - Los montos se presentan en pesos chilenos
                - Los gráficos son interactivos - use el zoom y hover para más detalles
                - La evolución temporal es una simulación con fines ilustrativos
                - El índice de concentración está normalizado entre 0 y 1
                </div>
            """, unsafe_allow_html=True)
            
        else:
            st.error("No se pudieron cargar los datos. Por favor, intente más tarde.")

if __name__ == '__main__':
    app = BudgetAnalysisApp()
    app.run()

def main():
    """Función principal para ejecutar desde el portafolio"""
    app = BudgetAnalysisApp()
    app.run()
