import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pydeck as pdk
import numpy as np
from pathlib import Path
from components.theme import set_theme, apply_theme

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Emisiones CO2 en Chile",
    page_icon="🌍",
    layout="wide"
)

# Aplicar tema
set_theme()
apply_theme()

# Función para cargar datos
@st.cache_data
def load_data():
    DATA_DIR = Path(__file__).parents[2] / 'data'
    RAW_DATA_PATH = DATA_DIR / 'raw' / 'retc_emisiones_aire_2023.csv'
    
    def detect_delimiter(file_path):
        delimiters = [',', ';', '\t']
        with open(file_path, 'r', encoding='utf-8') as f:
            header = f.readline().strip()
            for delimiter in delimiters:
                if header.count(delimiter) > 0:
                    return delimiter
        return ','
    
    delimiter = detect_delimiter(RAW_DATA_PATH)
    df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8', delimiter=delimiter)
    
    # Convertir columnas numéricas
    def convert_numeric(x):
        if isinstance(x, str):
            return float(x.replace(',', '.'))
        return x

    df['cantidad_toneladas'] = df['cantidad_toneladas'].apply(convert_numeric)
    df['latitud'] = df['latitud'].apply(convert_numeric)
    df['longitud'] = df['longitud'].apply(convert_numeric)
    
    return df

# Cargar datos
try:
    df = load_data()
    
    # Título principal y descripción
    st.title("🌍 Análisis de Emisiones de CO2 en Chile")
    st.markdown("""
    Este dashboard presenta un análisis comprehensivo de las emisiones de CO2 en Chile, 
    basado en datos del Registro de Emisiones y Transferencias de Contaminantes (RETC).
    """)

    # Métricas principales
    col1, col2, col3 = st.columns(3)
    with col1:
        total_emissions = df['cantidad_toneladas'].sum()
        st.metric("Emisiones Totales", f"{total_emissions:,.2f} ton")
    with col2:
        total_sources = len(df)
        st.metric("Fuentes Emisoras", f"{total_sources:,}")
    with col3:
        avg_emissions = df['cantidad_toneladas'].mean()
        st.metric("Promedio por Fuente", f"{avg_emissions:,.2f} ton")

    # Mapa de emisiones
    st.subheader("📍 Distribución Geográfica de Emisiones")
    
    st.markdown("""
    Este mapa interactivo muestra la distribución espacial de las emisiones de CO2 en Chile. 
    La intensidad del color representa la concentración de emisiones, mientras que los puntos rojos 
    indican los 50 principales emisores.
    
    **Cómo interpretar el mapa:**
    - Las áreas más oscuras indican mayor concentración de emisiones
    - Los puntos rojos representan las principales fuentes emisoras
    - Puede hacer zoom y desplazarse por el mapa
    - Al pasar el cursor sobre los puntos verá información detallada
    """)

    # Preparar datos para el mapa
    map_data = df[['latitud', 'longitud', 'cantidad_toneladas', 'region', 'razon_social', 'tipo_fuente']].copy()
    map_data['color_weight'] = np.log1p(map_data['cantidad_toneladas'])  # Log scale for better visualization
    
    # Definir límites geográficos de Chile
    chile_bounds = {
        'norte': -17.0,
        'sur': -56.0,
        'oeste': -76.0,
        'este': -66.0
    }

    # Crear mapa base con plotly
    fig_map = go.Figure()    # Agregar capa de mapa de calor con escala logarítmica y colores optimizados
    fig_map.add_densitymapbox(
        lat=map_data['latitud'],
        lon=map_data['longitud'],
        z=map_data['color_weight'],
        radius=20,  # Reducido para mejor detalle
        colorscale=[
            [0, 'rgba(247,251,255,0)'],   # Transparente para valores bajos
            [0.2, 'rgba(222,235,247,0.5)'],
            [0.4, 'rgba(198,219,239,0.6)'],
            [0.6, 'rgba(158,202,225,0.7)'],
            [0.8, 'rgba(107,174,214,0.8)'],
            [1, 'rgba(8,81,156,0.9)']
        ],
        showscale=True,
        name='Emisiones',
        hoverinfo='text',
        hovertemplate='<b>Emisiones:</b> %{customdata[0]:.2f} ton/año<br>' +
                      '<b>Región:</b> %{customdata[1]}<br>' +
                      '<b>Tipo:</b> %{customdata[2]}<extra></extra>',
        colorbar=dict(
            title=dict(
                text='Emisiones (log)',
                side='right'
            ),
            thickness=15,
            len=0.7,
            bgcolor='rgba(255,255,255,0.8)',
        ),
        customdata=np.column_stack((
            map_data['cantidad_toneladas'],
            map_data['region'],
            map_data['tipo_fuente']
        ))
    )

    # Agregar marcadores para los principales emisores
    top_emisores = map_data.nlargest(50, 'cantidad_toneladas')
    fig_map.add_scattermapbox(
        lat=top_emisores['latitud'],
        lon=top_emisores['longitud'],
        mode='markers',
        marker=dict(
            size=10,
            color='red',
            symbol='circle'
        ),
        text=top_emisores['razon_social'],
        hovertemplate='<b>Empresa:</b> %{text}<br>' +
                     '<b>Emisiones:</b> %{customdata[0]:.2f} ton/año<br>' +
                     '<b>Región:</b> %{customdata[1]}<br>' +
                     '<b>Tipo:</b> %{customdata[2]}<extra></extra>',
        customdata=np.column_stack((
            top_emisores['cantidad_toneladas'],
            top_emisores['region'],
            top_emisores['tipo_fuente']
        )),
        name='Principales Emisores'
    )    # Configurar el diseño del mapa
    fig_map.update_layout(
        mapbox=dict(
            style='carto-positron',  # Mapa base más claro
            center=dict(lat=-35.6751, lon=-71.5430),
            zoom=4,
            bounds=dict(
                south=chile_bounds['sur'],
                north=chile_bounds['norte'],
                east=chile_bounds['este'],
                west=chile_bounds['oeste']
            )
        ),
        showlegend=True,
        margin=dict(l=0, r=0, t=30, b=0),
        height=700,  # Mayor altura para mejor visualización
        dragmode='zoom',  # Permite zoom con el ratón
        modebar=dict(
            bgcolor='rgba(255,255,255,0.8)',
            orientation='v',
            remove=['lasso select', 'pan']  # Simplificar controles
        ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[
                dict(
                    label='Restablecer Vista',
                    method='relayout',
                    args=[{'mapbox.zoom': 4, 
                          'mapbox.center': dict(lat=-35.6751, lon=-71.5430)}]
                )
            ],
            x=0.05,
            y=1.05,
        )]
    )

    map_col1, map_col2 = st.columns([2, 1])
    with map_col1:
        st.plotly_chart(fig_map, use_container_width=True)
    with map_col2:
        st.markdown("""
        ### 📊 Principales Hallazgos del Mapa

        **Concentración Geográfica:**
        - Las emisiones se concentran principalmente en zonas industriales y urbanas
        - Existe una clara correlación entre actividad industrial y niveles de emisión
        - Se observan clusters significativos en las regiones centrales
        
        **Patrones Identificados:**
        - Mayor concentración en zonas costeras industriales
        - Focos importantes cerca de centros urbanos mayores
        - Zonas mineras del norte muestran patrones distintivos
        
        **Implicaciones:**
        - La distribución sugiere una fuerte relación con la actividad económica
        - Las zonas de alta concentración requieren especial atención en políticas ambientales
        - Se identifican oportunidades para descentralizar fuentes emisoras
        """)

    # Análisis por región
    st.subheader("🏢 Análisis Regional")
    
    st.markdown("""
    Esta sección presenta un análisis detallado de las emisiones por región, permitiendo 
    comprender la distribución tanto geográfica como por tipo de fuente emisora.
    """)

    # Gráfico de barras de emisiones por región
    emissions_by_region = df.groupby('region')['cantidad_toneladas'].sum().sort_values(ascending=True)
    fig_bar = px.bar(
        emissions_by_region,
        orientation='h',
        title='Emisiones Totales por Región',
        labels={'value': 'Emisiones (toneladas)', 'region': 'Región'},
        color=emissions_by_region.values,
        color_continuous_scale='Viridis'
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
    **Análisis de Emisiones por Región:**
    - Las regiones con mayor actividad industrial muestran los niveles más altos de emisiones
    - Se observa una distribución desigual, con algunas regiones concentrando gran parte de las emisiones
    - La variación entre regiones refleja diferentes niveles de desarrollo industrial y económico
    """)

    # Análisis por tipo de fuente en regiones
    st.subheader("📊 Distribución por Tipo de Fuente en Regiones")
    
    st.markdown("""
    Explore la composición de fuentes emisoras en cada región. Esta visualización permite:
    - Comparar la cantidad de empresas vs. su impacto en emisiones
    - Identificar los tipos de fuentes predominantes por región
    - Analizar la concentración de emisiones por sector
    """)

    # Selector de región para pie chart
    selected_region = st.selectbox(
        'Selecciona una región para ver distribución de empresas:',
        options=df['region'].unique()
    )
    
    # Crear pie chart de distribución de empresas por tipo
    companies_by_type = df[df['region'] == selected_region].groupby('tipo_fuente').agg({
        'razon_social': 'count',
        'cantidad_toneladas': 'sum'
    }).sort_values('cantidad_toneladas', ascending=False)
    
    fig_pie = make_subplots(
        rows=1, cols=2,
        specs=[[{'type':'pie'}, {'type':'pie'}]],
        subplot_titles=('Distribución por Cantidad', 'Distribución por Emisiones')
    )
    
    # Pie chart por cantidad de empresas
    fig_pie.add_trace(
        go.Pie(
            labels=companies_by_type.index,
            values=companies_by_type['razon_social'],
            name="Cantidad",
            title="Por cantidad",
            hole=.4
        ),
        row=1, col=1
    )
    
    # Pie chart por emisiones
    fig_pie.add_trace(
        go.Pie(
            labels=companies_by_type.index,
            values=companies_by_type['cantidad_toneladas'],
            name="Emisiones",
            title="Por emisiones",
            hole=.4
        ),
        row=1, col=2
    )
    
    fig_pie.update_layout(
        title=f'Distribución de Empresas en {selected_region}',
        height=500,
        showlegend=True
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown(f"""
    **Insights para la Región {selected_region}:**
    - La distribución muestra la relación entre cantidad de empresas y su impacto en emisiones
    - Algunos sectores pueden tener pocas empresas pero generar gran cantidad de emisiones
    - Esta información es crucial para políticas de regulación específicas por sector
    """)

    # Top empresas
    st.subheader("🏭 Análisis de Principales Emisores")
    
    st.markdown("""
    Esta sección identifica las empresas y sectores que más contribuyen a las emisiones de CO2,
    proporcionando una visión clara de dónde se pueden enfocar los esfuerzos de reducción.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        # Top 10 empresas por emisiones totales
        top_companies = df.groupby('razon_social')['cantidad_toneladas'].sum().nlargest(10)
        fig = px.bar(
            top_companies,
            title='Top 10 Empresas por Emisiones',
            labels={'value': 'Emisiones (toneladas)', 'razon_social': 'Empresa'},
            color=top_companies.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        **Análisis de Top Empresas:**
        - Estas empresas representan una proporción significativa del total de emisiones
        - La concentración en pocas empresas sugiere oportunidades para políticas focalizadas
        - Los sectores representados son principalmente energía y minería
        """)
    
    with col2:
        # Análisis sectorial
        sector_emissions = df.groupby('tipo_fuente')['cantidad_toneladas'].sum().sort_values(ascending=True)
        fig = px.bar(
            sector_emissions,
            orientation='h',
            title='Emisiones por Tipo de Fuente',
            labels={'value': 'Emisiones (toneladas)', 'tipo_fuente': 'Tipo de Fuente'},
            color=sector_emissions.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Análisis Sectorial:**
        - Algunos sectores tienen mayor impacto debido a la naturaleza de sus operaciones
        - La distribución por tipo de fuente ayuda a identificar prioridades en políticas ambientales
        - Se observan oportunidades de mejora en sectores específicos
        """)

    # Footer con información adicional
    st.markdown("""
    ---
    ### 📝 Notas Metodológicas
    
    - Datos obtenidos del Registro de Emisiones y Transferencias de Contaminantes (RETC)
    - Período de análisis: 2023
    - Las visualizaciones son interactivas - prueba haciendo hover o zoom
    - Las gráficas regionales muestran tanto distribución por cantidad como por emisiones
    
    Para más información, visita [RETC Chile](https://retc.mma.gob.cl/)
    """)

except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    st.markdown("""
    Por favor, asegúrate de que:
    1. El archivo de datos existe en la ruta correcta
    2. El formato del archivo es correcto
    3. Tienes todas las dependencias instaladas
    """)
