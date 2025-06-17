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
import streamlit.components.v1 as components
from datetime import datetime
import os
from utils.contact_components import add_page_footer, add_sidebar_contact

# Determinar el entorno
IS_STREAMLIT_CLOUD = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
IS_CLOUD_RUN = os.getenv('CLOUD_RUN_SERVICE', 'false').lower() == 'true'

# Configuración según plataforma
if IS_STREAMLIT_CLOUD:
    # Configuración específica para Streamlit Cloud
    from utils.streamlit_cloud_optimizer import StreamlitCloudOptimizer
    optimizer = StreamlitCloudOptimizer()
elif IS_CLOUD_RUN:
    # Configuración específica para Cloud Run
    from utils.cloud_cost_simulator import CloudCostSimulator
    optimizer = CloudCostSimulator()
else:
    # Configuración para desarrollo local
    from utils.local_optimizer import LocalOptimizer
    optimizer = LocalOptimizer()

# Definir directorio de caché según plataforma
if IS_STREAMLIT_CLOUD:
    cache_dir = Path('/tmp/streamlit_cache')
elif IS_CLOUD_RUN:
    cache_dir = Path('/var/cache/app_data')
else:
    cache_dir = Path(__file__).parent / 'data' / 'cache'

# Inicializar gestor de caché
cache_manager = CacheManager(cache_dir=cache_dir)

# Cargar estilos optimizados según plataforma
css_path = 'static/css/style.min.css' if IS_STREAMLIT_CLOUD else 'static/css/style.css'
try:
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback a estilos básicos si no se encuentra el archivo
    st.markdown("""
        <style>
        .main-container { padding: 2rem; }
        .hero-section { background: #f0f7ff; padding: 2rem; border-radius: 10px; }
        </style>
    """, unsafe_allow_html=True)

# Estructura principal de la página
def main():
    # Iniciar medición de recursos
    optimizer.start_measurement()
    
    # Crear sidebar y obtener la sección seleccionada
    selected = create_sidebar()

    # Renderizar sección seleccionada
    if selected == "principal":
        render_main_page()
    elif selected == "emisiones":
        render_emissions()
    elif selected == "agua":
        st.switch_page("pages/02_calidad_agua.py")
    elif selected == "demografia":
        st.switch_page("pages/03_demografia_bigquery.py")
    elif selected == "presupuesto":
        st.switch_page("pages/04_presupuesto_publico.py")
    
    # Agregar footer con enlaces en la parte inferior de la página principal
    add_footer()
    
    # Finalizar medición y obtener métricas
    metrics = optimizer.stop_measurement()
    
    # Panel de monitoreo de recursos en el sidebar
    with st.sidebar:
        st.markdown("### 📊 Monitor Local de Recursos")
        
        # Advertencia clara de simulación
        st.warning("⚠️ SIMULACIÓN LOCAL\nNo hay conexión con GCP")
        
        # Obtener métricas simuladas
        metrics = optimizer.stop_measurement()
        optimizer.start_measurement()  # Reiniciar medición
        
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
            try:
                st.write("CPU (simulado):", f"${metrics.get('cpu_cost', 0.0):.6f}")
                st.write("Memoria (simulado):", f"${metrics.get('memory_cost', 0.0):.6f}")
                st.write("Requests (simulado):", f"${metrics.get('request_cost', 0.0):.6f}")
                st.write("Total (simulado):", f"${(metrics.get('cpu_cost', 0.0) + metrics.get('memory_cost', 0.0) + metrics.get('request_cost', 0.0)):.6f}")
            except Exception as e:
                st.warning("Error mostrando costos simulados")
            
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
            """)
def render_objective():
    st.markdown("""
    ## 🎯 Objetivo del Portafolio
    
    Esta es mi forma de mostrar los resultados de 5 años de estudios, bootcamps y mucho más contenido sobre Python y DataScience.
    """)

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
    .metrics-section {
        margin-top: 2rem;
        padding: 1.5rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    .project-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Métricas destacadas
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

# Función para crear el sidebar con enlaces a redes sociales
def create_sidebar():
    with st.sidebar:
        st.title("🔍 Navegación")
        
        menu_options = {
            "principal": "📊 Principal",
            "emisiones": "🏭 Emisiones de CO2",
            "agua": "💧 Calidad del Agua",
            "demografia": "👥 Demografía",
            "presupuesto": "💰 Presupuesto Público"
        }
        
        selected = st.radio(
            "Selecciona una sección:",
            options=list(menu_options.keys()),
            format_func=lambda x: menu_options[x]
        )
        
        # Agregar separador
        st.markdown("---")
        
        # Agregar enlaces a redes sociales usando el componente reutilizable
        add_sidebar_contact()
        
    return selected

def add_footer():
    """
    Agrega un footer con enlaces de contacto y redes sociales
    al final de la página
    """
    add_page_footer()

def render_main_page():
    """Renderiza la página principal"""
    st.title("📊 Portafolio de Data Science")
    
    st.markdown("""
    Bienvenido a mi portafolio de análisis de datos, donde encontrarás:
    - 🏭 Análisis de emisiones de CO2
    - 💧 Estudios de calidad del agua
    - 👥 Análisis demográficos
    - 💰 Análisis de presupuesto público
    """)
    
    # Descripción del proyecto
    render_objective()

    # Secciones principales con botones de navegación
    st.subheader("Explora los análisis:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏭 Emisiones de CO2", use_container_width=True):
            st.switch_page("pages/01_emisiones_co2.py")
        
        if st.button("👥 Demografía", use_container_width=True):
            st.switch_page("pages/03_demografia_bigquery.py")
    
    with col2:
        if st.button("💧 Calidad del Agua", use_container_width=True):
            st.switch_page("pages/02_calidad_agua.py")
        
        if st.button("💰 Presupuesto Público", use_container_width=True):
            st.switch_page("pages/04_presupuesto_publico.py")
    
    # Sección de servicios
    st.markdown("---")
    st.subheader("💼 Servicios Profesionales")
    st.write("Ofrezco servicios de análisis de datos y desarrollo de dashboards personalizados.")
    
    if st.button("Ver Servicios Disponibles", use_container_width=True):
        st.switch_page("pages/06_servicios.py")
    
    # Sección de feedback
    st.markdown("---")
    st.subheader("💭 ¿Te gusta este portafolio?")
    st.write("Me encantaría recibir tus comentarios y sugerencias.")
    
    if st.button("Dejar Feedback", use_container_width=True):
        st.switch_page("pages/07_feedback.py")
        
    # Nota de actualización
    st.markdown(f"""
    <div style='margin-top: 2rem; font-size: 0.8em; color: #666;'>
        Última actualización: {datetime.now().strftime('%d/%m/%Y')}
    </div>
    """, unsafe_allow_html=True)

def render_emissions():
    """Renderiza la sección de emisiones de CO2"""
    st.title("🏭 Análisis de Emisiones de CO2 en Chile")
    
    # Descripción
    st.markdown("""
    Este estudio analiza las emisiones de CO2 en Chile entre 2010-2023, evaluando su evolución, 
    distribución por sectores y comparación con otros países latinoamericanos.
    """)
    
    # Botón para ir a la página completa
    if st.button("Ver análisis completo", use_container_width=True):
        st.switch_page("pages/01_emisiones_co2.py")

# Funciones de caché con optimización para GCP
@st.cache_data(ttl=3600)  # 1 hora de caché
def load_emissions_data():
    """Carga datos de emisiones con caché optimizado para GCP"""
    try:
        data = cache_manager.get_emissions_data()
        if data is None:
            # Datos de ejemplo si no hay caché
            return pd.DataFrame({
                'Año': list(range(2010, 2024)),
                'Emisiones_CO2_Mt': [80.2, 82.5, 85.3, 87.1, 86.5, 88.2, 89.7, 91.3, 92.6, 94.2, 91.5, 93.8, 95.1]
            })
        
        return pd.DataFrame({
            'Año': data['años'],
            'Emisiones_CO2_Mt': data['emisiones']
        })
    except Exception as e:
        st.warning(f"Error al cargar datos de emisiones: {e}")
        # Datos de respaldo por si falla la carga
        return pd.DataFrame({
            'Año': list(range(2010, 2024)),
            'Emisiones_CO2_Mt': [80.2, 82.5, 85.3, 87.1, 86.5, 88.2, 89.7, 91.3, 92.6, 94.2, 91.5, 93.8, 95.1]
        })

if __name__ == "__main__":
    main()