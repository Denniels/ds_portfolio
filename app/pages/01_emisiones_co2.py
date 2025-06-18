"""
Página para el análisis de emisiones de CO2 en Chile - VERSIÓN CON DATOS REALES
"""

import streamlit as st

# Configuración de la página - DEBE SER EL PRIMER COMANDO DE STREAMLIT
st.set_page_config(
    page_title="Emisiones de CO2 Chile - DS Portfolio",
    page_icon="🏭",
    layout="wide"
)

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from folium import plugins
import branca.colormap as cm
from datetime import datetime
import json

# Agregar el directorio raíz al path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Importar gestor de datos optimizado para Streamlit Cloud
from utils.streamlit_cloud_data import StreamlitCloudDataManager

# Rutas para datos reales
DATA_CACHE_DIR = parent_dir / "data" / "cache"
DATA_DIR = parent_dir / "data"

# Funciones para cargar datos reales con fallback robusto
@st.cache_data
def load_real_co2_data():
    """Cargar datos reales de emisiones CO2 con fallback para Streamlit Cloud"""
    manager = StreamlitCloudDataManager()
    data = manager.load_co2_data()
    return data['emisiones_anuales'], data['emisiones_regionales'], data['metadata']

@st.cache_data
def process_regional_data_for_visualization(emisiones_regionales):
    """Procesar datos regionales para visualización"""
    if not emisiones_regionales:
        return pd.DataFrame()
    
    # Convertir a DataFrame para facilitar el manejo
    data_list = []
    for region, data in emisiones_regionales.items():
        data_list.append({
            'Region': region,
            'lat': data['lat'],
            'lon': data['lon'],
            'emisiones': data['emisiones'],
            'emisiones_mt': round(data['emisiones'] / 1000000, 2)  # Convertir a mega toneladas
        })
    
    return pd.DataFrame(data_list)

# Importar componente de contacto
try:
    from utils.contact_components import add_page_footer, add_sidebar_contact
except ImportError:
    # Fallback por si no encuentra el módulo
    def add_page_footer():
        st.markdown("---")
        st.markdown("© 2025 DS Portfolio")
    def add_sidebar_contact():
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📱 Contacto")
        st.sidebar.markdown("""
        <div style="display:flex;gap:10px">            <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" style="text-decoration:none">
                🔗 LinkedIn
            </a>
            <a href="https://github.com/Denniels" target="_blank" style="text-decoration:none">
                💻 GitHub
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"Actualizado: {datetime.now().strftime('%d/%m/%Y')}")

# ===== INICIO DE LA APLICACIÓN =====

# Cargar datos reales con fallback robusto
emisiones_anuales, emisiones_regionales, metadata = load_real_co2_data()

# Crear gestor de datos para estadísticas
manager = StreamlitCloudDataManager()
data_dict = {
    'emisiones_anuales': emisiones_anuales,
    'emisiones_regionales': emisiones_regionales, 
    'metadata': metadata
}

# Procesar datos para visualización
df_regiones = process_regional_data_for_visualization(emisiones_regionales)

# Calcular estadísticas usando el gestor
stats = manager.get_stats(data_dict)
total_emisiones_mt = round(stats.get('total_emisiones_ton', 0) / 1000000, 1)
region_mayor = stats.get('region_mayor_emision', {})
region_menor = stats.get('region_menor_emision', {})
fecha_analisis = metadata.get('ultima_actualizacion', 'No disponible')

# Detectar si estamos usando datos de demo
is_demo = metadata.get('tipo') == 'datos_demostración'
data_source_label = "DEMOSTRACIÓN" if is_demo else "RETC 2023"
data_warning = "⚠️ Datos de demostración - " if is_demo else ""

# Configurar página con datos reales
st.markdown(f"""
<div class="co2-header">
    <h1 class="co2-title">🏭 Análisis de Emisiones de CO₂ en Chile</h1>
    <p class="co2-subtitle"><strong>Fuente:</strong> {data_warning}Registro de Emisiones y Transferencias de Contaminantes ({data_source_label})</p>
    <p class="co2-source"><strong>Última actualización:</strong> {fecha_analisis}</p>
</div>
""", unsafe_allow_html=True)

# Información del estudio real
st.markdown(f"""
## 🔬 Análisis del RETC Chile 2023

Este análisis presenta los resultados reales del Registro de Emisiones y Transferencias de Contaminantes 
de Chile para el año 2023, procesados desde los datasets oficiales del Ministerio del Medio Ambiente.

### Datos Procesados:
- **Datasets analizados:** {len(metadata.get('fuentes_datos', []))} fuentes oficiales
- **Regiones cubiertas:** {stats.get('total_regiones', 0)} regiones
- **Instalaciones analizadas:** {stats.get('total_instalaciones', 0)} principales emisores
- **Período:** {metadata.get('periodo_analisis', '2023')}

### Objetivos del Análisis:
1. Caracterizar las fuentes principales de emisiones CO₂ por tipo
2. Analizar distribución geográfica y sectorial real
3. Identificar patrones en los datos del RETC 2023
4. Generar visualizaciones basadas en datos oficiales
""")

# Pestañas para organizar el contenido
tab1, tab2, tab3, tab4 = st.tabs(["Resultados Principales", "Visualizaciones", "Conclusiones", "Próximos Avances"])

with tab1:
    st.header("📊 Hallazgos Clave del RETC 2023")
    
    # Contenedor de métricas con clase CSS
    st.markdown('<div class="co2-metrics-grid">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Emisiones totales RETC 2023",
            value=f"{total_emisiones_mt} Mt CO₂",
            help="Datos reales procesados del RETC Chile 2023"
        )
        
        st.markdown(f"""
        ### 🏆 Región con Mayores Emisiones
        **{region_mayor.get('nombre', 'N/A')}**  
        📊 {round(region_mayor.get('emisiones', 0) / 1000000, 1)} Mt CO₂
        
        ### 📋 Cobertura del Análisis
        - **{stats.get('total_regiones', 0)}** regiones analizadas
        - **{stats.get('total_instalaciones', 0)}** instalaciones principales
        - **3** tipos de emisiones (EFD, EFP, TR)
        """)
    
    with col2:
        st.metric(
            label="Concentración máxima",
            value=f"{round((region_mayor.get('emisiones', 0) / stats.get('total_emisiones_ton', 1)) * 100, 1)}%",
            delta="Una sola región",
            help=f"Porcentaje de emisiones de {region_mayor.get('nombre', 'N/A')}"
        )
        
        st.markdown(f"""
        ### 📉 Región con Menores Emisiones  
        **{region_menor.get('nombre', 'N/A')}**  
        📊 {round(region_menor.get('emisiones', 0) / 1000000, 2)} Mt CO₂
        
        ### 📈 Dispersión de Datos
        - **Rango:** {round((region_mayor.get('emisiones', 0) - region_menor.get('emisiones', 0)) / 1000000, 1)} Mt CO₂        - **Ratio:** {round(region_mayor.get('emisiones', 1) / max(region_menor.get('emisiones', 1), 1), 1)}:1
        """)
    
    # Cerrar contenedor de métricas
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Agregar análisis estadístico mejorado
    st.markdown("### 📊 Análisis Estadístico Avanzado")
    
    if not df_regiones.empty and total_emisiones_mt > 0:
        # Crear contenedor para estadísticas
        stats_col1, stats_col2, stats_col3 = st.columns(3)
        
        # Calcular estadísticas descriptivas
        media_emisiones = df_regiones['emisiones_mt'].mean()
        mediana_emisiones = df_regiones['emisiones_mt'].median()
        std_emisiones = df_regiones['emisiones_mt'].std()
        
        with stats_col1:
            st.metric(
                label="Media Nacional",
                value=f"{media_emisiones:.2f} Mt CO₂",
                help="Promedio de emisiones por región"
            )
        
        with stats_col2:
            st.metric(
                label="Mediana Nacional", 
                value=f"{mediana_emisiones:.2f} Mt CO₂",
                help="Valor central de la distribución"
            )
            
        with stats_col3:
            st.metric(
                label="Desviación Estándar",
                value=f"{std_emisiones:.2f} Mt CO₂",
                help="Variabilidad entre regiones"
            )

with tab2:
    st.header("📈 Visualizaciones de Datos Reales")
    
    st.markdown("### 🗺️ Distribución Regional de Emisiones CO₂")
    
    # Crear gráfico de barras con datos reales
    if not df_regiones.empty:
        # Ordenar por emisiones
        df_sorted = df_regiones.sort_values('emisiones_mt', ascending=True)
        
        fig_regiones = px.bar(
            df_sorted, 
            x='emisiones_mt', 
            y='Region',
            title='Emisiones de CO₂ por Región (RETC 2023)',
            labels={'emisiones_mt': 'Emisiones (Mt CO₂)', 'Region': 'Región'},
            orientation='h',
            color='emisiones_mt',
            color_continuous_scale='Reds'
        )
        fig_regiones.update_layout(
            height=600,
            showlegend=False,
            plot_bgcolor='rgba(240,240,240,0.3)'
        )
        
        st.plotly_chart(fig_regiones, use_container_width=True)
        
        # Mostrar tabla de datos
        st.markdown("### 📋 Tabla de Datos por Región")
        display_df = df_regiones[['Region', 'emisiones_mt']].copy()
        display_df['emisiones_mt'] = display_df['emisiones_mt'].round(2)
        display_df = display_df.sort_values('emisiones_mt', ascending=False)
        display_df.columns = ['Región', 'Emisiones (Mt CO₂)']
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("No hay datos regionales disponibles para mostrar")

    # División en columnas para métricas adicionales
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Top 5 Regiones - Mayores Emisiones")
        if not df_regiones.empty:
            top5 = df_regiones.nlargest(5, 'emisiones_mt')[['Region', 'emisiones_mt']]
            for idx, row in top5.iterrows():
                st.write(f"**{row['Region']}:** {row['emisiones_mt']} Mt CO₂")
        
    with col2:
        st.markdown("### 🎯 Top 5 Regiones - Menores Emisiones")
        if not df_regiones.empty:
            bottom5 = df_regiones.nsmallest(5, 'emisiones_mt')[['Region', 'emisiones_mt']]
            for idx, row in bottom5.iterrows():
                st.write(f"**{row['Region']}:** {row['emisiones_mt']} Mt CO₂")
    
    # Mapa interactivo
    st.markdown("### 🗺️ Mapa Interactivo de Emisiones")
    if not df_regiones.empty:
        # Crear mapa centrado en Chile
        mapa = folium.Map(
            location=[-35.6751, -71.5430],
            zoom_start=5,
            tiles='cartodbpositron'
        )
        
        # Agregar marcadores para cada región
        for _, row in df_regiones.iterrows():
            # Determinar color según emisiones
            if row['emisiones_mt'] > 1.0:
                color = 'red'
                radius = 15
            elif row['emisiones_mt'] > 0.5:
                color = 'orange'
                radius = 10
            else:
                color = 'green'
                radius = 7
            
            folium.CircleMarker(
                location=[row['lat'], row['lon']],
                radius=radius,
                popup=f"""
                <b>{row['Region']}</b><br>
                Emisiones: {row['emisiones_mt']} Mt CO₂<br>
                Coordenadas: ({row['lat']:.2f}, {row['lon']:.2f})
                """,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=2
            ).add_to(mapa)
        
        # Mostrar mapa
        st.components.v1.html(mapa._repr_html_(), height=500)
    else:
        st.warning("No hay datos de coordenadas disponibles para el mapa")
    
    # Nuevas visualizaciones avanzadas
    st.markdown("---")
    st.markdown("### 📈 Análisis Avanzado de Distribución")
    
    if not df_regiones.empty:
        # Gráfico de distribución (histograma)
        col_hist1, col_hist2 = st.columns(2)
        
        with col_hist1:
            fig_hist = px.histogram(
                df_regiones, 
                x='emisiones_mt',
                nbins=8,
                title='Distribución de Emisiones por Región',
                labels={'emisiones_mt': 'Emisiones (Mt CO₂)', 'count': 'Número de Regiones'},
                color_discrete_sequence=['#FF6B6B']
            )
            fig_hist.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(240,240,240,0.3)'
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col_hist2:
            # Gráfico de caja (boxplot)
            fig_box = px.box(
                df_regiones,
                y='emisiones_mt',
                title='Análisis de Distribución (Boxplot)',
                labels={'emisiones_mt': 'Emisiones (Mt CO₂)'},
                color_discrete_sequence=['#4ECDC4']
            )
            fig_box.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(240,240,240,0.3)'
            )
            st.plotly_chart(fig_box, use_container_width=True)
    
    # Gráfico de barras apiladas por cuartiles
    st.markdown("### 📊 Clasificación por Niveles de Emisión")
    
    if not df_regiones.empty:
        # Clasificar regiones por cuartiles
        df_classified = df_regiones.copy()
        q1 = df_regiones['emisiones_mt'].quantile(0.25)
        q2 = df_regiones['emisiones_mt'].quantile(0.50)
        q3 = df_regiones['emisiones_mt'].quantile(0.75)
        
        def classify_emissions(value):
            if value <= q1:
                return 'Bajo (Q1)'
            elif value <= q2:
                return 'Medio-Bajo (Q2)'
            elif value <= q3:
                return 'Medio-Alto (Q3)'
            else:
                return 'Alto (Q4)'
        
        df_classified['Nivel'] = df_classified['emisiones_mt'].apply(classify_emissions)
        
        # Contar regiones por nivel
        nivel_counts = df_classified['Nivel'].value_counts()
        
        # Crear gráfico de dona
        fig_dona = px.pie(
            values=nivel_counts.values,
            names=nivel_counts.index,
            title='Distribución de Regiones por Nivel de Emisiones',
            hole=0.4,
            color_discrete_sequence=['#FF9999', '#FFB366', '#FFCC66', '#FF6B6B']
        )
        fig_dona.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_dona, use_container_width=True)
        
        # Mostrar clasificación detallada
        col_class1, col_class2 = st.columns(2)
        
        with col_class1:
            st.markdown("#### 📋 Clasificación por Cuartiles")
            st.write(f"**Q1 (Bajo):** ≤ {q1:.2f} Mt CO₂")
            st.write(f"**Q2 (Medio-Bajo):** {q1:.2f} - {q2:.2f} Mt CO₂")
            st.write(f"**Q3 (Medio-Alto):** {q2:.2f} - {q3:.2f} Mt CO₂")
            st.write(f"**Q4 (Alto):** > {q3:.2f} Mt CO₂")
        
        with col_class2:
            st.markdown("#### 🎯 Regiones por Nivel")
            for nivel in ['Alto (Q4)', 'Medio-Alto (Q3)', 'Medio-Bajo (Q2)', 'Bajo (Q1)']:
                regiones_nivel = df_classified[df_classified['Nivel'] == nivel]['Region'].tolist()
                if regiones_nivel:
                    st.write(f"**{nivel}:** {', '.join(regiones_nivel)}")
    
    # Análisis comparativo con benchmarks internacionales
    st.markdown("---")
    st.markdown("### 🌍 Contexto Internacional (Estimación)")
    
    benchmark_col1, benchmark_col2 = st.columns(2)
    
    with benchmark_col1:
        # Datos estimados para comparación (ejemplo)
        paises_referencia = {
            'Chile (RETC 2023)': total_emisiones_mt,
            'Uruguay (est.)': 2.1,
            'Costa Rica (est.)': 3.8,
            'Dinamarca (est.)': 31.2,
            'Nueva Zelanda (est.)': 37.8
        }
        
        fig_benchmark = px.bar(
            x=list(paises_referencia.keys()),
            y=list(paises_referencia.values()),
            title='Comparación Internacional - Emisiones CO₂ Totales',
            labels={'x': 'País', 'y': 'Emisiones (Mt CO₂)'},
            color=list(paises_referencia.values()),
            color_continuous_scale='Viridis'
        )
        fig_benchmark.update_layout(showlegend=False)
        st.plotly_chart(fig_benchmark, use_container_width=True)
    
    with benchmark_col2:
        st.markdown("""
        #### 📊 Análisis Contextual
        
        **Nota:** Los datos de comparación internacional son estimaciones 
        referenciales basadas en informes públicos y pueden no corresponder 
        exactamente al mismo año o metodología.
        
        **Observaciones:**
        - Chile muestra un perfil típico de país en desarrollo con sector minero
        - Las emisiones están concentradas en pocas regiones (patrón común)
        - Se requiere análisis per cápita para comparación más precisa
        
        **Fuentes sugeridas para análisis futuro:**
        - Global Carbon Atlas
        - UNFCCC National Inventory Reports
        - IEA CO₂ Emissions Statistics
        """)

with tab3:
    st.header("📋 Conclusiones del Análisis RETC 2023")
    
    st.markdown(f"""
    ### 🎯 **Hallazgos Principales**
    
    El análisis de los datos del Registro de Emisiones y Transferencias de Contaminantes (RETC) 
    de Chile para 2023 revela patrones significativos en la distribución de emisiones de CO₂:
    
    #### 🏭 **Concentración Regional**
    - **Región Metropolitana** lidera con **{round(region_mayor.get('emisiones', 0) / 1000000, 1)} Mt CO₂** 
      ({round((region_mayor.get('emisiones', 0) / stats.get('total_emisiones_ton', 1)) * 100, 1)}% del total nacional)
    - Esta concentración refleja la alta densidad industrial y poblacional del área metropolitana
    - **Dispersión significativa**: La región con mayores emisiones supera en 
      **{round(region_mayor.get('emisiones', 1) / max(region_menor.get('emisiones', 1), 1), 1)}x** 
      a la región con menores emisiones
    
    #### 📊 **Distribución Nacional**  
    - **{stats.get('total_regiones', 0)} regiones** reportaron emisiones en el RETC 2023
    - **Total nacional**: {total_emisiones_mt} Mt CO₂ registradas oficialmente
    - **{stats.get('total_instalaciones', 0)} instalaciones principales** identificadas como mayores emisores
    
    #### 🔍 **Calidad de Datos**
    - Datos procesados desde **{len(metadata.get('fuentes_datos', []))} fuentes oficiales** del MMA
    - Análisis basado en **3 tipos de emisiones**: Fugitivas Difusas (EFD), Fugitivas Puntuales (EFP) y Transferencias (TR)
    - Cobertura geográfica completa de Chile continental
    """)
    
    st.info(f"""
    **📅 Metadata del Análisis:**
    - **Versión de datos:** {metadata.get('version', 'N/A')}
    - **Generado:** {metadata.get('generado_en', 'N/A').split('T')[0] if metadata.get('generado_en') else 'N/A'}
    - **Optimizado para:** Streamlit Community Cloud
    - **Fuente oficial:** Ministerio del Medio Ambiente de Chile
    """)
    
    # Sección de recomendaciones basadas en datos reales
    st.markdown("""
    ### 💡 **Recomendaciones Basadas en Datos**
    
    #### Para Política Pública:
    1. **Focalizar esfuerzos** en la Región Metropolitana debido a su alta concentración de emisiones
    2. **Desarrollar estrategias diferenciadas** según el perfil de emisiones de cada región
    3. **Fortalecer el sistema RETC** para capturar más instalaciones medianas y pequeñas
    
    #### Para Investigación:
    1. **Análisis temporal** comparando con años anteriores del RETC
    2. **Correlación con variables socioeconómicas** por región
    3. **Estudios sectoriales específicos** en las principales fuentes identificadas
    
    #### Para el Sector Privado:
    1. **Benchmarking sectorial** usando datos RETC como referencia
    2. **Oportunidades de mejora** en regiones con alta intensidad de emisiones
    3. **Desarrollo de tecnologías limpias** focalizadas en los sectores más emisores
    """)
    
    # Nota metodológica
    st.markdown("""
    ---
    ### 📚 **Nota Metodológica**
    
    Este análisis utiliza exclusivamente datos oficiales del **Registro de Emisiones y Transferencias 
    de Contaminantes (RETC)** del Ministerio del Medio Ambiente de Chile para el año 2023. 
    
    Los datos fueron procesados mediante análisis estadístico exploratorio, incluyendo:
    - Limpieza y validación de datos
    - Detección de outliers
    - Agregación por región y tipo de emisión
    - Optimización para visualización web
    
    **Limitaciones:** Los datos RETC representan emisiones reportadas por instalaciones reguladas 
    y pueden no incluir todas las fuentes de CO₂ del país.
    """)

with tab4:
    st.header("🚀 Próximos Avances del Estudio de Emisiones CO₂")
    
    st.markdown("""
    Esta sección presenta las **líneas de investigación futuras** y **mejoras planificadas** 
    para profundizar el análisis de emisiones de CO₂ en Chile.
    """)
    
    # Roadmap visual
    st.markdown("### 🗺️ Roadmap de Desarrollo")
    
    roadmap_col1, roadmap_col2 = st.columns(2)
    
    with roadmap_col1:
        st.markdown("""
        #### 📅 **Corto Plazo (3-6 meses)**
        
        **🔄 Análisis Temporal**
        - Comparación con años anteriores (2020-2022)
        - Identificación de tendencias post-COVID
        - Análisis de estacionalidad de emisiones
        
        **📊 Mejoras en Visualización**
        - Dashboard interactivo en tiempo real
        - Mapas de calor dinámicos
        - Filtros avanzados por sector y período
        
        **🔍 Validación de Datos**
        - Cross-validation con otras fuentes oficiales
        - Análisis de consistencia inter-anual
        - Detección automatizada de anomalías
        """)
    
    with roadmap_col2:
        st.markdown("""
        #### 📅 **Mediano Plazo (6-12 meses)**
        
        **🌍 Análisis Comparativo Internacional**
        - Benchmarking con países similares
        - Análisis per cápita y por PIB
        - Estudio de mejores prácticas globales
        
        **🏭 Análisis Sectorial Profundo**
        - Desagregación por industrias específicas
        - Análisis de eficiencia energética
        - Identificación de oportunidades de reducción
        
        **🤖 Machine Learning**
        - Modelos predictivos de emisiones
        - Clustering de patrones regionales
        - Forecasting con variables climáticas
        """)
    
    # Metodologías avanzadas
    st.markdown("---")
    st.markdown("### 🔬 Metodologías Avanzadas a Implementar")
    
    metodologias_col1, metodologias_col2, metodologias_col3 = st.columns(3)
    
    with metodologias_col1:
        st.markdown("""
        #### 📈 **Análisis Estadístico**
        - **Análisis de series temporales**
          - ARIMA para forecasting
          - Detección de puntos de cambio
          - Análisis de estacionalidad
        
        - **Análisis multivariado**
          - PCA para reducción dimensional
          - Clustering k-means por perfiles
          - Análisis de correlación espacial
        """)
    
    with metodologias_col2:
        st.markdown("""
        #### 🌐 **Análisis Geoespacial**
        - **Análisis de hotspots**
          - Identificación de clusters de emisión
          - Análisis de proximidad geográfica
          - Correlación con uso de suelo
        
        - **Modelado espacial**
          - Interpolación kriging
          - Análisis de autocorrelación espacial
          - Modelos de difusión geográfica
        """)
    
    with metodologias_col3:
        st.markdown("""
        #### 🤖 **Machine Learning**
        - **Modelos predictivos**
          - Random Forest para clasificación
          - Redes neuronales para forecasting
          - Ensemble methods
        
        - **Análisis de patrones**
          - Algoritmos de asociación
          - Detección de anomalías
          - Segmentación automática
        """)
    
    # Integración de datos
    st.markdown("---")
    st.markdown("### 🔄 Integración de Nuevas Fuentes de Datos")
    
    integracion_col1, integracion_col2 = st.columns(2)
    
    with integracion_col1:
        st.markdown("""
        #### 📊 **Fuentes de Datos Planificadas**
        
        **Datos Oficiales:**
        - **INE Chile**: Datos económicos y demográficos
        - **CNE**: Consumo energético por región
        - **SINIA**: Indicadores ambientales complementarios
        - **SII**: Datos de actividad económica por sector
        
        **Datos Satelitales:**
        - **Sentinel-5P**: Concentraciones atmosféricas CO₂
        - **MODIS**: Uso de suelo y vegetación
        - **Landsat**: Cambios en cobertura terrestre
        
        **APIs Internacionales:**
        - **Global Carbon Atlas**: Comparación internacional
        - **World Bank Open Data**: Indicadores socioeconómicos
        - **UNFCCC**: Inventarios nacionales de GEI
        """)
    
    with integracion_col2:
        st.markdown("""
        #### 🛠️ **Herramientas y Tecnologías**
        
        **Pipeline de Datos:**
        - **Apache Airflow**: Automatización ETL
        - **Google Earth Engine**: Procesamiento satelital
        - **PostGIS**: Base de datos geoespacial
        
        **Análisis y Modelado:**
        - **scikit-learn**: Machine learning
        - **geopandas**: Análisis geoespacial
        - **statsmodels**: Modelado estadístico
        
        **Visualización Avanzada:**
        - **Plotly Dash**: Dashboards interactivos
        - **Folium**: Mapas web avanzados
        - **Streamlit**: Prototipos rápidos
        """)
    
    # Impacto esperado
    st.markdown("---")
    st.markdown("### 🎯 Impacto Esperado de los Avances")
    
    st.success("""
    #### 🌟 **Valor Agregado del Estudio Expandido**
    
    **Para Tomadores de Decisión:**
    - Predicciones más precisas para políticas públicas
    - Identificación temprana de tendencias preocupantes
    - Optimización de recursos para reducción de emisiones
    
    **Para la Comunidad Científica:**
    - Metodología replicable para otros países latinoamericanos
    - Datasets procesados y validados disponibles públicamente
    - Publicaciones en revistas especializadas
    
    **Para el Sector Privado:**
    - Benchmarking sectorial detallado
    - Herramientas de autodiagnóstico empresarial
    - Identificación de oportunidades de negocio verde
    """)
    
    # Cronograma de implementación
    st.markdown("### 📅 Cronograma de Implementación")
    
    # Crear datos para gráfico de Gantt simplificado
    import plotly.express as px
    import pandas as pd
    from datetime import datetime, timedelta
    
    # Datos del cronograma
    tareas = [
        {"Tarea": "Análisis Temporal", "Inicio": "2025-07-01", "Fin": "2025-09-30", "Tipo": "Corto Plazo"},
        {"Tarea": "Mejoras Visualización", "Inicio": "2025-07-15", "Fin": "2025-10-15", "Tipo": "Corto Plazo"},
        {"Tarea": "Validación Datos", "Inicio": "2025-08-01", "Fin": "2025-10-30", "Tipo": "Corto Plazo"},
        {"Tarea": "Análisis Internacional", "Inicio": "2025-10-01", "Fin": "2026-03-31", "Tipo": "Mediano Plazo"},
        {"Tarea": "Análisis Sectorial", "Inicio": "2025-11-01", "Fin": "2026-04-30", "Tipo": "Mediano Plazo"},
        {"Tarea": "Machine Learning", "Inicio": "2026-01-01", "Fin": "2026-06-30", "Tipo": "Mediano Plazo"},
    ]
    
    df_cronograma = pd.DataFrame(tareas)
    df_cronograma['Inicio'] = pd.to_datetime(df_cronograma['Inicio'])
    df_cronograma['Fin'] = pd.to_datetime(df_cronograma['Fin'])
    
    fig_gantt = px.timeline(
        df_cronograma, 
        x_start="Inicio", 
        x_end="Fin", 
        y="Tarea",
        color="Tipo",
        title="Cronograma de Implementación de Avances",
        color_discrete_map={"Corto Plazo": "#FF6B6B", "Mediano Plazo": "#4ECDC4"}
    )
    fig_gantt.update_yaxes(autorange="reversed")
    fig_gantt.update_layout(height=400)
    st.plotly_chart(fig_gantt, use_container_width=True)
    
    # Call to action
    st.markdown("---")
    st.info("""
    ### 🤝 **¿Interesado en Colaborar?**
    
    Este roadmap está abierto a colaboraciones con:
    - **Instituciones académicas** interesadas en investigación ambiental
    - **Organizaciones públicas** que requieran análisis especializados
    - **Empresas privadas** buscando soluciones de monitoreo ambiental
    - **Investigadores independientes** con expertise complementario
    
    📧 **Contacto para colaboraciones:** [LinkedIn Profile](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
    """)

# Footer con información adicional
st.markdown("---")
st.markdown("### 📊 Información Técnica")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    **Datos utilizados:**
    - Emisiones totales: {total_emisiones_mt} Mt CO₂
    - Regiones analizadas: {stats.get('total_regiones', 0)}
    - Fuentes de datos: {len(metadata.get('fuentes_datos', []))}
    """)

with col2:
    st.markdown(f"""
    **Última actualización:**
    - Datos: {fecha_analisis}
    - Versión: {metadata.get('version', 'N/A')}
    - Tipo: Datos reales RETC 2023
    """)

# Importar componentes de contacto
try:
    from utils.contact_components import add_page_footer, add_sidebar_contact
    add_sidebar_contact()
    add_page_footer()
except ImportError:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Contacto")
    st.sidebar.markdown("🔗 LinkedIn | 💻 GitHub")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"Actualizado: {datetime.now().strftime('%d/%m/%Y')}")
