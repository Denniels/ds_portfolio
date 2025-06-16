"""
Aplicación principal del portafolio - Versión simplificada y optimizada
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

# Configuración de la página
st.set_page_config(
    page_title="Portfolio Data Science | Chile",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importaciones
from utils.cache_manager import CacheManager
from utils.cloud_cost_simulator import CloudCostSimulator
import streamlit.components.v1 as components
from datetime import datetime

# Cargar estilos personalizados
with open('static/css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inicializar gestor de caché
cache_manager = CacheManager()

# Inicializar simulador de costos
cost_simulator = CloudCostSimulator()

# Estructura principal de la página
def main():
    # Iniciar medición de recursos
    cost_simulator.start_measurement()

    # Banner principal
    st.markdown("""
    <div class="hero-section">
        <h1>🔍 Portafolio para DataScience </h1>
        <p style='font-size: 1.2em;'>
            El objetivo de este portafolio es mostrar mis habilidades en el mundo de los datos.
            Encontraras estudios realziados con datos reales de fuentes oficiales de Chile,
            como el Ministerio del Medio Ambiente, o la API de https://datos.gob.cl/.
        </p>
    </div>
    """, unsafe_allow_html=True)    # Panel de monitoreo de recursos
    with st.sidebar:
        st.markdown("### 📊 Monitor Local de Recursos")
        
        # Advertencia clara de simulación
        st.warning("⚠️ SIMULACIÓN LOCAL\nNo hay conexión con GCP")
        
        # Obtener métricas simuladas
        metrics = cost_simulator.stop_measurement()
        cost_simulator.start_measurement()  # Reiniciar medición
        
        st.markdown("#### Uso de Recursos Locales")
        # Mostrar métricas locales
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="CPU Local",
                value=f"{metrics['cpu_percent']:.1f}%"
            )
        with col2:
            st.metric(
                label="Memoria Local",
                value=f"{metrics['memory_gb']:.2f}GB"
            )
        
        st.markdown("#### Simulación de Costos")
        st.info("💡 Estos valores son simulados\nNo representan costos reales de GCP")
        
        # Desglose de simulación
        with st.expander("Ver simulación de costos"):
            st.markdown("""
            ##### Valores Simulados (No Reales)
            Estos números son una aproximación local y NO reflejan:
            - Costos reales de GCP
            - Uso real de recursos en la nube
            - Facturación real
            """)
            st.write("CPU (simulado):", f"${metrics['cpu_cost']:.6f}")
            st.write("Memoria (simulado):", f"${metrics['memory_cost']:.6f}")
            st.write("Requests (simulado):", f"${metrics['request_cost']:.6f}")
            
        st.markdown("---")
        st.markdown("### ✅ Estado del Sistema")
        st.success("Modo Local Activo")
        st.info("No hay conexión con GCP")
        
        # Información de seguridad
        with st.expander("ℹ️ Información de Seguridad"):
            st.markdown("""
            - ✅ No hay servicios de GCP activos
            - ✅ No hay APIs de GCP habilitadas
            - ✅ No hay costos reales generados
            - ✅ Todos los datos son locales
            """)    # Descripción del proyecto
    st.markdown("""
    ## 🎯 Objetivo del Portafolio
    
    Esta es mi forma de mostrar los resultados de 5 años de estudios, bootcamps y mucho más contenido sobre Python y DataScience.
    """)

    # Secciones principales con botones de navegación que coinciden con el menú lateral
    # Estilos para los botones y tarjetas
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #3B82F6;
        color: white;
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .grid-container-2 {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .button-container {
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)    # Primera fila - Análisis principales
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🏭 Emisiones de CO2")
        st.markdown("""
        Análisis detallado de las emisiones de carbono en Chile:
        - Tendencias históricas
        - Distribución geográfica
        - Comparativas regionales
        """)
        if st.button("Ver Análisis de Emisiones", key="emisiones_btn"):
            st.switch_page("pages/01_emisiones_co2.py")

    with col2:
        st.markdown("### 💧 Calidad del Agua")
        st.markdown("""
        Monitoreo de la calidad del agua en Chile:
        - Índices de calidad
        - Puntos de muestreo
        - Tendencias temporales
        """)
        if st.button("Ver Monitoreo de Agua", key="agua_btn"):
            st.switch_page("pages/02_calidad_agua.py")

    with col3:
        st.markdown("### 📊 Demografía y Presupuesto")
        st.markdown("""
        Análisis socioeconómico integral:
        - Datos demográficos
        - Presupuesto público
        - Impacto ambiental
        """)
        if st.button("Ver Análisis Demográfico", key="demografia_btn"):
            st.switch_page("pages/03_demografia_bigquery.py")    # Segunda fila - Servicios y recursos adicionales
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👨‍💼 Servicios Profesionales")
        st.markdown("""
        Ofrecemos servicios especializados en:
        - Consultoría ambiental
        - Análisis de datos
        - Desarrollo de dashboards
        """)
        if st.button("Ver Servicios", key="servicios_btn"):
            st.switch_page("pages/06_servicios.py")

    with col2:
        st.markdown("### 📚 Plan de Estudios")
        st.markdown("""
        Recursos educativos y materiales:
        - Guías metodológicas
        - Documentación técnica
        - Casos de estudio
        """)
        if st.button("Ver Plan de Estudios", key="estudios_btn"):
            st.switch_page("pages/05_curriculum.py")

    # Sección de comentarios y feedback
    st.markdown("---")
    st.markdown("### 💬 Comentarios y Feedback")
    st.markdown("Tu opinión es importante para mejorar nuestros análisis y servicios.")
    if st.button("Dejar Comentario", key="comentario_btn"):
        st.switch_page("pages/07_feedback.py")

    # Sección de métricas
    st.markdown("""
    <div class='metrics-section'>
        <h3>📈 Métricas Destacadas</h3>
        <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;'>
            <div class='project-card'>
                <div class='metric-icon'>🗺️</div>
                <h4>Cobertura Nacional</h4>
                <p>16 regiones analizadas</p>
            </div>
            <div class='project-card'>
                <div class='metric-icon'>📅</div>
                <h4>Datos Históricos</h4>
                <p>+10 años de registros</p>
            </div>
            <div class='project-card'>
                <div class='metric-icon'>📊</div>
                <h4>Visualizaciones</h4>
                <p>+20 gráficos interactivos</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nota de actualización
    st.markdown(f"""
    <div style='margin-top: 2rem; font-size: 0.8em; color: #666;'>
        Última actualización: {datetime.now().strftime('%d/%m/%Y')}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

#                                             # 
#=============================================#
#                                             #

## Funciones de caché con optimización para GCP
#@st.cache_data(ttl=3600)  # 1 hora de caché
#def load_emissions_data():
#    """Carga datos de emisiones con caché optimizado para GCP"""
#    data = cache_manager.get_emissions_data()
#    if data is None:
#        return None
#    
#    return pd.DataFrame({
#        'Año': data['años'],
#        'Emisiones_CO2_Mt': data['emisiones']
#    })##
#
#@st.cache_data(ttl=86400)  # 24 horas de caché
#def load_regional_data():
#    """Carga datos regionales con caché optimizado para GCP"""
#    data = cache_manager.get_regional_data()
#    if data is None:
#        return None
#    
#    return pd.DataFrame([
#        {
#            'Region': region,
#            'lat': info['coords']['lat'],
#            'lon': info['coords']['lon'],
#            'emisiones': info.get('emisiones', 0)
#       }
#        for region, info in data['regiones'].items()
#    ])
#
#def render_main_page():
#    """Renderiza la página principal"""
#    st.title("📊 Portafolio de Data Science")
#    st.markdown("""
#    Bienvenido a mi portafolio de análisis de datos, donde encontrarás:
#   - 🏭 Análisis de emisiones de CO2
#    - 💧 Estudios de calidad del agua
#    - 👥 Análisis demográficos
#    - 💰 Análisis de presupuesto público
#    """)
#
#def render_emissions():
#    """Renderiza la sección de emisiones de CO2"""
#    st.title("🏭 Análisis de Emisiones de CO2 en Chile")
#    
#    # Descripción
#    st.markdown("""
#    Este estudio analiza las emisiones de CO2 en Chile entre 2010-2023, evaluando su evolución, 
#    distribución por sectores y comparación con otros países latinoamericanos.
#   """)
#    
#    # Pestañas
#    tab1, tab2, tab3 = st.tabs(["📈 Resultados", "🗺️ Mapa", "📊 Visualizaciones"])
#    
#    with tab1:
#        df = load_emissions_data()
#        latest = df.iloc[-1]
#        change = ((latest['Emisiones_CO2_Mt'] - df.iloc[-2]['Emisiones_CO2_Mt']) / 
#                 df.iloc[-2]['Emisiones_CO2_Mt'] * 100)
#        
#        col1, col2 = st.columns(2)
#       with col1:
#            st.metric(
#                "Emisiones totales 2023",
#                f"{latest['Emisiones_CO2_Mt']:.1f} Mt CO2",
#                f"{change:+.1f}%"
#            )
#        with col2:
#            st.metric(
#                "Región más contaminante",
#                "Metropolitana",
#                "42.3% del total"
#            )
#    
#    with tab2:
#        st.markdown("### 🗺️ Distribución Regional de Emisiones")
#        map_path = STATIC_DIR / "maps" / "emisiones_co2_latest.html"
#        
#        if map_path.exists():
#            with open(map_path, 'r', encoding='utf-8') as f:
#                st.components.v1.html(f.read(), height=600)
#        else:
#            st.warning("Mapa en proceso de actualización...")
#    
#    with tab3:
#        st.markdown("### 📈 Tendencia Histórica")
#        df = load_emissions_data()
#        
#        fig = px.line(
#            df,
#            x='Año',
#            y='Emisiones_CO2_Mt',
#            title='Evolución de Emisiones de CO2 en Chile (2010-2023)',
#            markers=True
#        )
#        
#        fig.update_layout(
#            xaxis_title="Año",
#            yaxis_title="Emisiones (Mt CO2)",
#        )
#        
#        st.plotly_chart(fig, use_container_width=True)
#
#def main():
#    # Menú lateral
#    with st.sidebar:
#        st.title("🔍 Navegación")
#        
#        menu_options = {
#            "principal": "📊 Principal",
#            "emisiones": "🏭 Emisiones de CO2",
#            "agua": "💧 Calidad del Agua",
#            "demografia": "👥 Demografía",
#            "presupuesto": "💰 Presupuesto Público"
#        }
#        
#        selected = st.radio(
#            "Selecciona una sección:",
#            options=list(menu_options.keys()),
#            format_func=lambda x: menu_options[x]
#        )
#    
#    # Renderizar sección seleccionada
#    if selected == "principal":
#        render_main_page()
#    elif selected == "emisiones":
#        render_emissions()
#    else:
#        st.info("Esta sección está en desarrollo...")
#
#if __name__ == "__main__":
#    main()
