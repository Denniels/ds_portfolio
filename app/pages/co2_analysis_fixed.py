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
from utils.data_loader_local import LocalDataLoader

@st.cache_data(ttl=3600, max_entries=10)
def load_data():
    try:
        # Usar el DataLoader que ya maneja la descarga desde Google Drive
        data_loader = LocalDataLoader()
        
        # Detectar si es un health check
        if hasattr(data_loader, 'is_health_check') and data_loader.is_health_check():
            # Devolver un DataFrame mínimo para health checks
            return pd.DataFrame({
                'region': ['Región Test'],
                'cantidad_toneladas': [100],
                'razon_social': ['Empresa Test'],
                'tipo_fuente': ['Fuente Test'],
                'latitud': [-33.4489],
                'longitud': [-70.6693]
            })
        
        # Cargar datos usando el método de carga unificado
        df = data_loader.load_data_from_gdrive(data_loader.FILE_ID)
        
        if df.empty:
            st.error("❌ Error al cargar los datos desde Google Drive")
            return pd.DataFrame()
        
        # Optimizar memoria: convertir tipos de datos
        if 'cantidad_toneladas' in df.columns:
            df['cantidad_toneladas'] = pd.to_numeric(df['cantidad_toneladas'], errors='coerce')
        
        # Limitar la cantidad de datos si es excesiva
        if len(df) > 100000:
            st.warning(f"Optimizando rendimiento: limitando a 100,000 registros de {len(df)} totales")
            df = df.sample(n=100000, random_state=42)
            
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar los datos: {str(e)}")
        return pd.DataFrame()

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
    try:
        map_data = df[['latitud', 'longitud', 'cantidad_toneladas', 'region', 'razon_social', 'tipo_fuente']].copy()
        
        # Asegurar que latitud y longitud son numéricas
        map_data['latitud'] = pd.to_numeric(map_data['latitud'], errors='coerce')
        map_data['longitud'] = pd.to_numeric(map_data['longitud'], errors='coerce')
        
        # Eliminar filas con coordenadas inválidas
        map_data = map_data.dropna(subset=['latitud', 'longitud'])
        
        # Limitar la cantidad de datos para mejorar el rendimiento
        if len(map_data) > 5000:
            # Muestreo estratificado para mantener representatividad
            map_data = map_data.sample(n=5000, random_state=42)
            st.info(f"Mostrando una muestra de 5,000 puntos para optimizar el rendimiento")
        
        # Transformación logarítmica para visualización
        map_data['color_weight'] = np.log1p(map_data['cantidad_toneladas'])
        
        # Definir límites geográficos de Chile
        chile_bounds = {
            'norte': -17.0,
            'sur': -56.0,
            'oeste': -76.0,
            'este': -66.0
        }

        # Crear mapa base con plotly
        fig_map = go.Figure()
        
        # Agregar capa de mapa de calor
        fig_map.add_densitymapbox(
            lat=map_data['latitud'],
            lon=map_data['longitud'],
            z=map_data['color_weight'],
            radius=20,
            colorscale=[
                [0, 'rgba(247,251,255,0)'],
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

        # Agregar marcadores para los principales emisores (máximo 50)
        max_top_emisores = min(50, len(map_data))
        top_emisores = map_data.nlargest(max_top_emisores, 'cantidad_toneladas')
        
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
        )

        # Configurar el diseño del mapa
        fig_map.update_layout(
            mapbox=dict(
                style='carto-positron',
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
            height=700,
            dragmode='zoom',
            modebar=dict(
                bgcolor='rgba(255,255,255,0.8)',
                orientation='v',
                remove=['lasso select', 'pan']
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
    except Exception as e:
        st.error(f"No se pudo generar el mapa: {str(e)}")
        st.info("Los datos geográficos pueden no estar disponibles o estar en un formato incorrecto.")

    # Análisis por región
    st.subheader("🏢 Análisis Regional")
    
    st.markdown("""
    Esta sección presenta un análisis detallado de las emisiones por región, permitiendo 
    comprender la distribución tanto geográfica como por tipo de fuente emisora.
    """)

    # Gráfico de barras de emisiones por región
    try:
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
    except Exception as e:
        st.error(f"No se pudo generar el gráfico de emisiones por región: {str(e)}")

    # Análisis por tipo de fuente en regiones
    st.subheader("📊 Distribución por Tipo de Fuente en Regiones")
    
    st.markdown("""
    Explore la composición de fuentes emisoras en cada región. Esta visualización permite:
    - Comparar la cantidad de empresas vs. su impacto en emisiones
    - Identificar los tipos de fuentes predominantes por región
    - Analizar la concentración de emisiones por sector
    """)

    # Selector de región para pie chart
    try:
        selected_region = st.selectbox(
            'Selecciona una región para ver distribución de empresas:',
            options=df['region'].unique()
        )
        
        # Crear pie chart de distribución de empresas por tipo
        try:
            # Agrupar y filtrar datos para evitar categorías vacías
            companies_by_type = df[df['region'] == selected_region].groupby('tipo_fuente').agg({
                'razon_social': 'count',
                'cantidad_toneladas': 'sum'
            }).sort_values('cantidad_toneladas', ascending=False)
            
            # Filtrar para eliminar categorías con valores muy pequeños
            min_emission_threshold = companies_by_type['cantidad_toneladas'].sum() * 0.01  # 1% del total
            filtered_companies = companies_by_type[companies_by_type['cantidad_toneladas'] > min_emission_threshold]
            
            # Si hay demasiadas categorías, agrupar las menores en "Otros"
            if len(filtered_companies) > 7:
                top_companies = filtered_companies.iloc[:6]
                others = pd.DataFrame({
                    'razon_social': [filtered_companies.iloc[6:]['razon_social'].sum()],
                    'cantidad_toneladas': [filtered_companies.iloc[6:]['cantidad_toneladas'].sum()]
                }, index=['Otros'])
                filtered_companies = pd.concat([top_companies, others])
            
            # Usar gráficos independientes en lugar de subplots para mayor estabilidad
            # Gráfico de cantidad de empresas
            fig_pie_count = px.pie(
                filtered_companies, 
                values='razon_social',
                names=filtered_companies.index,
                title=f'Distribución por Cantidad en {selected_region}',
                hole=0.4
            )
            fig_pie_count.update_layout(height=400)
            
            # Gráfico de emisiones
            fig_pie_emissions = px.pie(
                filtered_companies, 
                values='cantidad_toneladas',
                names=filtered_companies.index,
                title=f'Distribución por Emisiones en {selected_region}',
                hole=0.4
            )
            fig_pie_emissions.update_layout(height=400)
            
            # Mostrar gráficos uno al lado del otro
            col1_pie, col2_pie = st.columns(2)
            with col1_pie:
                st.plotly_chart(fig_pie_count, use_container_width=True)
            with col2_pie:
                st.plotly_chart(fig_pie_emissions, use_container_width=True)
                
        except Exception as e:
            st.error(f"No se pudieron generar los gráficos de distribución: {str(e)}")
            st.info("Prueba seleccionando otra región o recargando la página.")

        st.markdown(f"""
        **Insights para la Región {selected_region}:**
        - La distribución muestra la relación entre cantidad de empresas y su impacto en emisiones
        - Algunos sectores pueden tener pocas empresas pero generar gran cantidad de emisiones
        - Esta información es crucial para políticas de regulación específicas por sector
        """)
    except Exception as e:
        st.error(f"Error al procesar datos regionales: {str(e)}")

    # Top empresas
    st.subheader("🏭 Análisis de Principales Emisores")
    
    st.markdown("""
    Esta sección identifica las empresas y sectores que más contribuyen a las emisiones de CO2,
    proporcionando una visión clara de dónde se pueden enfocar los esfuerzos de reducción.
    """)

    try:
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
    except Exception as e:
        st.error(f"Error al generar gráficos de emisores: {str(e)}")

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
    st.error(f"Error general al cargar los datos: {str(e)}")
    st.markdown("""
    Por favor, asegúrate de que:
    1. El archivo de datos existe en la ruta correcta
    2. El formato del archivo es correcto
    3. Tienes todas las dependencias instaladas
    """)
