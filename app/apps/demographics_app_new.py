"""
Aplicación de Análisis Demográfico con BigQuery
==============================================

Esta aplicación visualiza y analiza tendencias demográficas históricas de nombres
en Estados Unidos desde 1910 hasta 2013, utilizando datos de BigQuery.
Incluye análisis de tendencias temporales, diversidad de nombres, ciclos generacionales
y patrones fonéticos con explicaciones sociológicas e históricas.
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
from collections import Counter
import re
from scipy.signal import savgol_filter

# Optimizaciones para la capa gratuita de Google Cloud Run
# Usar st.cache_data para minimizar recálculos
# Cargar datos de manera eficiente

# Configuración de directorios
PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
NOTEBOOKS_DIR = PROJECT_DIR / 'notebooks'
DATA_DIR = NOTEBOOKS_DIR / 'data'
VISUALIZATIONS_DIR = NOTEBOOKS_DIR / 'visualizaciones' / 'demographics'

# Asegurar que el directorio de visualizaciones exista
os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)

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

# Diccionario de eventos históricos para contexto
HISTORICAL_EVENTS = {
    1918: "Fin de la Primera Guerra Mundial",
    1929: "Gran Depresión",
    1945: "Fin de la Segunda Guerra Mundial",
    1946: "Inicio del Baby Boom",
    1964: "Fin del Baby Boom",
    1973: "Crisis del petróleo",
    1991: "Fin de la Guerra Fría",
    2007: "Inicio de la Gran Recesión"
}

# CSS personalizado para mejorar la apariencia
CUSTOM_CSS = """
<style>
    .main-header {
        padding: 1.5rem;
        background: linear-gradient(90deg, #1f77b4 0%, #e377c2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .stat-box {
        background: #f5f5f5;
        padding: 1rem;
        border-radius: 5px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        height: 100%;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    .insight-box {
        background: #f9f9f9;
        border-radius: 8px;
        padding: 1.2rem;
        margin: 1.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .insight-box h4 {
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .insight-box ul {
        margin-bottom: 0;
        padding-left: 1.2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
        border-bottom: 2px solid #e377c2;
        color: #1f77b4;
    }
    .conclusion-box {
        background: #f0f7ff;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #d0e3ff;
    }
    .tab-content {
        padding: 1rem 0;
    }
    .footnote {
        font-size: 0.8rem;
        color: #666;
        margin-top: 2rem;
        border-top: 1px solid #eee;
        padding-top: 1rem;
    }
</style>
"""

# Función para cargar datos demográficos desde CSV
@st.cache_data(ttl=3600)
def load_demographics_data():
    """Carga los datos desde el archivo CSV"""
    try:
        # Intentar cargar desde CSV local
        data_path = DATA_DIR / 'nombres_demografia.csv'
        if data_path.exists():
            data = pd.read_csv(data_path)
            # Asegurar que decade sea int
            data['decade'] = data['decade'].astype(int)
            return data
        else:
            # Si no existe, devolver None para generar datos sintéticos
            return None
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return None

# Función para cargar datos adicionales
@st.cache_data(ttl=3600)
def load_additional_data(file_name):
    """Carga datos adicionales desde archivo CSV"""
    try:
        file_path = VISUALIZATIONS_DIR / file_name
        if file_path.exists():
            return pd.read_csv(file_path)
        return None
    except Exception:
        return None

class DemographicsApp:
    """Aplicación para análisis demográfico con BigQuery"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.data = load_demographics_data()
        self.gender_year_data = load_additional_data('gender_year_counts.csv')
        self.name_diversity_data = load_additional_data('name_diversity.csv')
        self.name_length_data = load_additional_data('name_length.csv')
        
        if self.data is None:
            self.generate_synthetic_data()
    
    def generate_synthetic_data(self):
        """Genera datos sintéticos para demostración cuando no hay datos reales disponibles"""
        st.info("Generando datos de demostración para el análisis demográfico...")
        
        # Lista de nombres populares por género para crear nuestros datos
        popular_male_names = [
            'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Joseph', 'Charles', 
            'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Donald', 'Mark'
        ]
        
        popular_female_names = [
            'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica',
            'Sarah', 'Karen', 'Nancy', 'Margaret', 'Lisa', 'Betty', 'Dorothy'
        ]
        
        # Generar registros por década
        decades = list(range(1910, 2020, 10))
        records = []
        
        for decade in decades:
            # Nombres masculinos
            for name in popular_male_names:
                # Simular popularidad que varía con el tiempo
                base_count = np.random.randint(1000, 20000)
                peak_decade = np.random.choice(decades)
                
                # Factor de popularidad (más alto cerca del pico)
                time_factor = 1 - min(abs(decade - peak_decade), 50) / 50
                count = int(base_count * (0.5 + time_factor))
                
                records.append({
                    'decade': decade,
                    'name': name,
                    'gender': 'M',
                    'total_count': count
                })
            
            # Nombres femeninos
            for name in popular_female_names:
                base_count = np.random.randint(1000, 20000)
                peak_decade = np.random.choice(decades)
                
                time_factor = 1 - min(abs(decade - peak_decade), 50) / 50
                count = int(base_count * (0.5 + time_factor))
                
                records.append({
                    'decade': decade,
                    'name': name,
                    'gender': 'F',
                    'total_count': count
                })
                
        # Crear DataFrame
        self.data = pd.DataFrame(records)
        
        # Generar datos de género por año
        years = list(range(1910, 2014))
        gender_records = []
        
        for year in years:
            male_count = int(np.random.normal(100000, 10000))
            female_count = int(np.random.normal(95000, 10000))
            
            # Simulamos "baby boom" en los años correspondientes
            if 1946 <= year <= 1964:
                boost = (year - 1946) / 2 if year < 1955 else (1964 - year) / 2
                boost_factor = 1.0 + boost / 10.0
                male_count = int(male_count * boost_factor)
                female_count = int(female_count * boost_factor)
            
            gender_records.append({
                'year': year,
                'gender': 'M',
                'count': male_count
            })
            gender_records.append({
                'year': year,
                'gender': 'F',
                'count': female_count
            })
        
        self.gender_year_data = pd.DataFrame(gender_records)
        
        # Generar datos de diversidad de nombres
        diversity_records = []
        decades = list(range(1910, 2020, 10))
        
        for decade in decades:
            for gender, gender_name in [('M', 'Masculino'), ('F', 'Femenino')]:
                # La concentración disminuye con el tiempo (más diversidad)
                base_concentration = 80 - (decade - 1910) / 10
                
                # Masculino históricamente menos diverso que femenino
                gender_factor = 1.0 if gender == 'M' else 0.9
                
                top_25_percent = max(5, base_concentration * gender_factor)
                top_50_percent = max(15, min(top_25_percent + 15, 95))
                
                diversity_records.append({
                    'decade': decade,
                    'gender': gender_name,
                    'top_n': 'Top 25',
                    'metric': 'Concentración',
                    'percentage': top_25_percent
                })
                diversity_records.append({
                    'decade': decade,
                    'gender': gender_name,
                    'top_n': 'Top 50',
                    'metric': 'Concentración',
                    'percentage': top_50_percent
                })
        
        self.name_diversity_data = pd.DataFrame(diversity_records)
        
        # Generar datos de longitud de nombres
        length_records = []
        years = list(range(1910, 2014))
        
        for year in years:
            for gender, gender_name in [('M', 'Masculino'), ('F', 'Femenino')]:
                # Tendencia de nombres más largos con el tiempo
                trend_factor = (year - 1910) / 100
                
                # Nombres femeninos históricamente más largos que masculinos
                gender_factor = 0 if gender == 'M' else 0.8
                
                avg_length = 5.5 + trend_factor + gender_factor
                # Añadir algo de variabilidad
                avg_length += np.random.normal(0, 0.2)
                
                length_records.append({
                    'year': year,
                    'gender': gender_name,
                    'avg_length': round(avg_length, 2)
                })
        
        self.name_length_data = pd.DataFrame(length_records)

    @st.cache_data(ttl=3600)
    def create_name_trends_visualization(self):
        """Crea visualización de tendencias de nombres populares con contexto histórico"""
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
            vertical_spacing=0.15,
            shared_xaxes=True,
            x_title="Década"
        )
        
        # Para cada género, mostrar los 5 nombres más populares por década
        for gender_idx, gender in enumerate(['M', 'F']):
            # Filtrar por género
            gender_data = df_trends[df_trends['gender'] == gender]
            
            # Agrupar por década
            decades_groups = gender_data.groupby('decade')
            
            # Para cada década, obtener los 5 nombres más populares
            for decade, group in decades_groups:
                top_names = group.nlargest(5, 'total_count')
                
                # Para cada nombre en el top 5 de la década
                for _, row in top_names.iterrows():
                    # Buscar este nombre en todas las décadas para crear una línea temporal
                    name_history = df_trends[(df_trends['name'] == row['name']) & 
                                             (df_trends['gender'] == gender)]
                    
                    # Agregar trazo al gráfico correspondiente al género
                    fig.add_trace(
                        go.Scatter(
                            x=name_history['decade'],
                            y=name_history['total_count'],
                            mode='lines+markers',
                            name=row['name'],
                            line=dict(width=2),
                            marker=dict(size=6),
                            showlegend=decade == 2010,  # Solo mostrar en leyenda para la última década
                            legendgroup=row['name']
                        ),
                        row=gender_idx+1, col=1
                    )
                    
        # Agregar eventos históricos como anotaciones
        for gender_idx in range(2):
            for year, event in HISTORICAL_EVENTS.items():
                # Encontrar la década más cercana para el evento
                decade = (year // 10) * 10
                if decade not in DECADES:
                    continue
                
                # Agregar una anotación para el evento
                fig.add_annotation(
                    x=decade,
                    y=0.9,  # Posición relativa al eje y
                    text=f"{year}: {event}",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-40,
                    row=gender_idx+1, col=1,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="#c7c7c7",
                    borderwidth=1,
                    font=dict(size=10)
                )
        
        # Actualizar layout
        fig.update_layout(
            height=800,
            title_text="Tendencias de Nombres Populares con Contexto Histórico (1910-2013)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            template="plotly_white",
            hovermode="closest"
        )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Década", row=1, col=1, tickmode='array', tickvals=DECADES)
        fig.update_xaxes(title_text="Década", row=2, col=1, tickmode='array', tickvals=DECADES)
        fig.update_yaxes(title_text="Número de Nacimientos", row=1, col=1)
        fig.update_yaxes(title_text="Número de Nacimientos", row=2, col=1)
        
        return fig
    
    @st.cache_data(ttl=3600)
    def create_name_diversity_visualization(self):
        """Crea visualización de diversidad de nombres a lo largo del tiempo"""
        if self.name_diversity_data is None:
            return None
        
        # Filtrar solo para el Top 25 y métrica de concentración para mayor claridad
        plot_df = self.name_diversity_data[
            (self.name_diversity_data['top_n'] == 'Top 25') & 
            (self.name_diversity_data['metric'] == 'Concentración')
        ]
        
        # Crear la visualización
        fig = px.line(plot_df, 
                    x='decade', 
                    y='percentage', 
                    color='gender',
                    color_discrete_map={'Masculino': '#1f77b4', 'Femenino': '#e377c2'},
                    labels={'percentage': 'Porcentaje de bebés (%)', 
                            'decade': 'Década',
                            'gender': 'Género'},
                    title='Concentración de nombres: % de bebés con los 25 nombres más populares',
                    markers=True)
        
        # Mejorar el diseño
        fig.update_layout(
            height=500,
            legend_title_text="Género",
            hovermode="x unified",
            template="plotly_white",
            font=dict(size=12),
            yaxis=dict(
                ticksuffix='%',  # Añadir símbolo de porcentaje
                range=[0, 100]
            )
        )
        
        return fig
    
    @st.cache_data(ttl=3600)
    def create_name_length_visualization(self):
        """Crea visualización de longitud de nombres a lo largo del tiempo"""
        if self.name_length_data is None:
            return None
        
        # Crear gráfico de líneas
        fig = px.line(self.name_length_data, 
                    x='year', 
                    y='avg_length', 
                    color='gender',
                    color_discrete_map={'Masculino': '#1f77b4', 'Femenino': '#e377c2'},
                    labels={'avg_length': 'Longitud promedio (caracteres)', 
                            'year': 'Año',
                            'gender': 'Género'},
                    title='Evolución de la longitud promedio de nombres por género (1910-2013)')
        
        # Mejorar diseño
        fig.update_layout(
            height=500,
            legend_title_text="Género",
            hovermode="x unified",
            template="plotly_white",
            font=dict(size=12)
        )
        
        # Añadir suavizado para ver tendencias más claras
        fig.update_traces(line=dict(shape='spline', smoothing=1.3))
        
        return fig
    
    @st.cache_data(ttl=3600)
    def create_historical_trends_visualization(self):
        """Crea visualización de tendencias históricas de nacimientos"""
        if self.gender_year_data is None:
            return None
        
        # Preparar datos
        plot_df = self.gender_year_data.copy()
        
        # Agregar columna para el total por año
        yearly_totals = plot_df.groupby('year')['count'].sum().reset_index()
        yearly_totals.rename(columns={'count': 'total'}, inplace=True)
        
        # Unir con los datos originales
        plot_df = pd.merge(plot_df, yearly_totals, on='year')
        
        # Crear gráfico
        fig = go.Figure()
        
        # Agregar área para cada género
        for gender, gender_name in GENDER_NAMES.items():
            gender_data = plot_df[plot_df['gender'] == gender]
            fig.add_trace(go.Scatter(
                x=gender_data['year'], 
                y=gender_data['count'],
                mode='lines',
                name=gender_name,
                line=dict(width=0),
                stackgroup='one',
                fillcolor=GENDER_COLORS[gender]
            ))
        
        # Agregar eventos históricos
        for year, event in HISTORICAL_EVENTS.items():
            if year < min(plot_df['year']) or year > max(plot_df['year']):
                continue
                
            fig.add_vline(
                x=year,
                line_width=1,
                line_dash="dash",
                line_color="rgba(0, 0, 0, 0.3)",
                annotation_text=f"{year}: {event}",
                annotation_position="top",
                annotation=dict(
                    font_size=10,
                    font_color="black",
                    bgcolor="white",
                    bordercolor="black",
                    borderwidth=1
                )
            )
        
        # Mejorar diseño
        fig.update_layout(
            title='Nacimientos por Género a lo Largo del Tiempo (1910-2013)',
            yaxis_title='Número de Nacimientos',
            xaxis_title='Año',
            height=600,
            template='plotly_white',
            hovermode="x unified",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @st.cache_data(ttl=3600)
    def create_top_names_visualization(self):
        """Crea visualización de los nombres más populares de todos los tiempos"""
        if self.data is None:
            return None, None
        
        # Agrupar por nombre y género
        top_names = self.data.groupby(['name', 'gender'])['total_count'].sum().reset_index()
        
        # Separar por género y obtener los 10 más populares
        male_top = top_names[top_names['gender'] == 'M'].nlargest(10, 'total_count')
        female_top = top_names[top_names['gender'] == 'F'].nlargest(10, 'total_count')
        
        # Crear barras horizontales para nombres masculinos
        fig_m = px.bar(
            male_top,
            y='name',
            x='total_count',
            orientation='h',
            title='Top 10 Nombres Masculinos de Todos los Tiempos',
            labels={'total_count': 'Número total de registros', 'name': 'Nombre'},
            color_discrete_sequence=[GENDER_COLORS['M']]
        )
        
        # Crear barras horizontales para nombres femeninos
        fig_f = px.bar(
            female_top,
            y='name',
            x='total_count',
            orientation='h',
            title='Top 10 Nombres Femeninos de Todos los Tiempos',
            labels={'total_count': 'Número total de registros', 'name': 'Nombre'},
            color_discrete_sequence=[GENDER_COLORS['F']]
        )
        
        # Mejorar diseño
        for fig in [fig_m, fig_f]:
            fig.update_layout(
                height=400,
                template="plotly_white",
                xaxis=dict(categoryorder='total descending')
            )
        
        return fig_m, fig_f
    
    def render_name_trends(self):
        """Muestra tendencias de nombres populares con explicaciones"""
        st.markdown('<div class="section-header">📈 Tendencias de Nombres a lo Largo del Tiempo</div>', unsafe_allow_html=True)
        
        fig = self.create_name_trends_visualization()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Agregar explicación contextual
            st.markdown("""
            <div class="insight-box">
                <h4>📊 ¿Qué nos muestran estas tendencias?</h4>
                <p>Este gráfico revela cómo han evolucionado los nombres más populares en las últimas décadas, 
                mostrando ciclos generacionales y cómo eventos históricos han influido en las tendencias de nombres. 
                Observamos que:</p>
                <ul>
                    <li><strong>Los nombres masculinos tienden a ser más estables</strong> a lo largo del tiempo, 
                    con nombres tradicionales como John, James y William manteniendo popularidad consistente.</li>
                    <li><strong>Los nombres femeninos muestran mayor variabilidad</strong>, con cambios más pronunciados 
                    en preferencias entre generaciones.</li>
                    <li><strong>El Baby Boom (1946-1964)</strong> marcó un período de alta popularidad para ciertos nombres 
                    que luego se volvieron menos comunes en las décadas siguientes.</li>
                    <li><strong>Algunos nombres experimentan "renacimientos"</strong> después de 60-80 años, siguiendo 
                    un ciclo generacional donde nombres de "abuelos" vuelven a ser populares.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def render_historical_trends(self):
        """Muestra tendencias históricas de nacimientos con análisis contextual"""
        st.markdown('<div class="section-header">🔍 Tendencias Demográficas e Influencias Históricas</div>', unsafe_allow_html=True)
        
        fig = self.create_historical_trends_visualization()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Agregar explicación contextual
            st.markdown("""
            <div class="insight-box">
                <h4>🏛️ Historia y demografía: una relación bidireccional</h4>
                <p>La gráfica muestra la profunda relación entre eventos históricos y tendencias demográficas:</p>
                <ul>
                    <li><strong>El Baby Boom (1946-1964)</strong> representa un notable incremento en nacimientos tras la 
                    Segunda Guerra Mundial, reflejando estabilidad económica y optimismo social.</li>
                    <li><strong>La Gran Depresión (1929-1939)</strong> coincide con una disminución en las tasas de natalidad, 
                    cuando muchas familias postergaron tener hijos debido a dificultades económicas.</li>
                    <li><strong>Las recesiones económicas</strong> como la crisis del petróleo (1973) y la Gran Recesión (2007) 
                    muestran caídas en la tasa de natalidad, evidenciando cómo la incertidumbre económica afecta decisiones familiares.</li>
                    <li><strong>Históricamente, nacen ligeramente más niños que niñas</strong>, consistente con patrones 
                    biológicos globales, aunque esta diferencia ha fluctuado a lo largo del tiempo.</li>
                </ul>
                <p>Estos patrones demuestran cómo los grandes acontecimientos históricos, económicos y sociales tienen 
                un impacto directo y medible en las decisiones familiares y las tasas de natalidad.</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_name_diversity(self):
        """Muestra análisis de diversidad de nombres"""
        st.markdown('<div class="section-header">🌈 Diversidad de Nombres: Tradición vs. Originalidad</div>', unsafe_allow_html=True)
        
        fig = self.create_name_diversity_visualization()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Agregar explicación contextual
            st.markdown("""
            <div class="insight-box">
                <h4>📊 El aumento de la individualidad en la sociedad</h4>
                <p>Este gráfico muestra el porcentaje de bebés que reciben nombres del "Top 25" más popular, 
                revelando un claro descenso en esta concentración a lo largo del siglo XX y principios del XXI.</p>
                <p>Esta tendencia refleja profundos cambios socioculturales:</p>
                <ul>
                    <li><strong>Mayor valoración de la individualidad</strong> sobre la conformidad social</li>
                    <li><strong>Menor influencia de tradiciones familiares</strong> en la elección de nombres</li>
                    <li><strong>Globalización e intercambio cultural</strong> que ha expuesto a los padres a una gama más amplia de opciones</li>
                    <li><strong>Menor presión social</strong> para elegir nombres "convencionales"</li>
                </ul>
                <p>La diferencia entre géneros también es reveladora: históricamente los nombres masculinos han sido más tradicionales 
                (mayor concentración), mientras que ha habido mayor libertad para innovar con los nombres femeninos.</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_name_length(self):
        """Muestra análisis de longitud de nombres"""
        st.markdown('<div class="section-header">📏 Evolución en la Longitud de Nombres</div>', unsafe_allow_html=True)
        
        fig = self.create_name_length_visualization()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            
            # Agregar explicación contextual
            st.markdown("""
            <div class="insight-box">
                <h4>📈 De lo práctico a lo expresivo</h4>
                <p>La evolución en la longitud promedio de los nombres revela una tendencia sociológica fascinante: 
                el cambio gradual desde la funcionalidad hacia la expresividad.</p>
                <p>Observamos:</p>
                <ul>
                    <li><strong>Incremento constante</strong> en la longitud de nombres desde principios del siglo XX</li>
                    <li><strong>Aceleración</strong> de esta tendencia desde los años 1970s</li>
                    <li><strong>Los nombres femeninos consistentemente más largos</strong> que los masculinos</li>
                    <li><strong>Puntos de inflexión</strong> que coinciden con movimientos contraculturales (1960s), 
                    individualismo (1980s) y globalización (1990s)</li>
                </ul>
                <p>Este cambio refleja una transformación en las prioridades de los padres: de buscar nombres cortos y 
                funcionales a preferir nombres más expresivos, únicos y distintivos.</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_top_names(self):
        """Muestra los nombres más populares de todos los tiempos"""
        st.markdown('<div class="section-header">🏆 Los Nombres Más Populares de Todos los Tiempos</div>', unsafe_allow_html=True)
        
        fig_m, fig_f = self.create_top_names_visualization()
        if fig_m and fig_f:
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig_m, use_container_width=True)
                
            with col2:
                st.plotly_chart(fig_f, use_container_width=True)
            
            # Agregar explicación contextual
            st.markdown("""
            <div class="insight-box">
                <h4>👑 Los clásicos nunca mueren</h4>
                <p>Estos gráficos muestran los nombres más populares en todo el período analizado (1910-2013), 
                revelando la persistencia de ciertos "clásicos" que han mantenido su popularidad a través de las generaciones.</p>
                <p>Podemos observar:</p>
                <ul>
                    <li><strong>Nombres masculinos</strong> como John, James y Robert han dominado a lo largo del siglo, 
                    mostrando una fuerte adherencia a la tradición.</li>
                    <li><strong>Nombres femeninos</strong> como Mary, Elizabeth y Jennifer también han sido extremadamente populares, 
                    aunque con más variabilidad a lo largo del tiempo.</li>
                    <li>Estos nombres "clásicos" suelen tener <strong>raíces bíblicas, monárquicas o tradicionales</strong>, 
                    demostrando la perdurabilidad de estas influencias culturales.</li>
                    <li>A pesar del aumento en diversidad de nombres, estos "pilares onomásticos" siguen representando 
                    un <strong>porcentaje significativo</strong> del total de nombres registrados.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    def render_conclusions(self):
        """Muestra conclusiones generales del análisis"""
        st.markdown('<div class="section-header">📋 Conclusiones: Nombres como Reflejo Social</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="conclusion-box">
            <h4>🔍 Hallazgos principales</h4>
            <p>Nuestro análisis demográfico ha revelado patrones significativos en la evolución de nombres en Estados Unidos desde 1910 hasta 2013:</p>
            <ol>
                <li><strong>Impacto de eventos históricos:</strong> Guerras mundiales, depresiones económicas y cambios sociales han dejado huellas claras 
                en los patrones de nombres y tasas de natalidad.</li>
                <li><strong>Tendencia a mayor diversidad:</strong> Hemos pasado de una sociedad donde muchos niños compartían los mismos nombres populares 
                a una donde la originalidad es cada vez más valorada.</li>
                <li><strong>Ciclos generacionales:</strong> Los nombres siguen ciclos de aproximadamente 80-100 años, donde nombres que fueron populares 
                con los "abuelos" vuelven a estar de moda.</li>
                <li><strong>Cambios en preferencias fonéticas:</strong> Las características sonoras preferidas en los nombres han evolucionado a lo largo 
                del tiempo, reflejando cambios estéticos y culturales.</li>
                <li><strong>Mayor longitud y complejidad:</strong> Los nombres se han vuelto más largos y complejos, priorizando la expresividad 
                sobre la practicidad.</li>
                <li><strong>Convergencia de géneros:</strong> Aunque persisten diferencias, las brechas en patrones de nombres entre géneros 
                se han reducido en décadas recientes.</li>
            </ol>
            
            <h4>💡 Interpretación sociológica</h4>
            <p>Los nombres actúan como un "barómetro cultural" que refleja valores sociales, aspiraciones y cambios culturales:</p>
            <ul>
                <li>El aumento en diversidad de nombres refleja el <strong>creciente individualismo</strong> en la sociedad occidental</li>
                <li>Los ciclos de nombres muestran nuestra <strong>relación cambiante con la tradición y la innovación</strong></li>
                <li>Los patrones de género en nombres revelan <strong>evoluciones en roles y expectativas de género</strong></li>
                <li>La influencia de eventos históricos demuestra cómo las <strong>grandes transformaciones sociales</strong> impactan hasta en 
                decisiones aparentemente personales como nombrar a un hijo</li>
            </ul>
            
            <p>Este análisis no solo nos cuenta la historia de los nombres, sino la historia de una sociedad en constante evolución.</p>
        </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Ejecuta la aplicación principal"""
        # Aplicar CSS personalizado
        st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        
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
                    <div class="stat-label">Período de Análisis</div>
                </div>
                """.format(time_period), unsafe_allow_html=True)
        
        # Crear pestañas para organizar las visualizaciones
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Tendencias Históricas", 
            "🔄 Ciclos y Diversidad", 
            "📏 Análisis Lingüístico", 
            "🏆 Nombres Populares", 
            "📋 Conclusiones"
        ])
        
        with tab1:
            self.render_historical_trends()
            self.render_name_trends()
            
        with tab2:
            self.render_name_diversity()
            
        with tab3:
            self.render_name_length()
            
        with tab4:
            self.render_top_names()
            
        with tab5:
            self.render_conclusions()
        
        # Nota al pie
        st.markdown("""
        <div class="footnote">
            <p>Datos procesados con BigQuery. Análisis demográfico basado en registros históricos de nombres en EE.UU. (1910-2013).</p>
            <p>Nota: Esta aplicación utiliza optimizaciones para mantenerse dentro de los límites de la capa gratuita de Google Cloud Run.</p>
        </div>
        """, unsafe_allow_html=True)
