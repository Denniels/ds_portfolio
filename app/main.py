"""
Aplicación principal del portafolio - Versión simplificada y optimizada
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
import sys
import os
from datetime import datetime
import streamlit.components.v1 as components

# Asegurarse de que app/ esté en el path de Python
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# Configuración de la página
st.set_page_config(
    page_title="Aprendizajes en Ciencia de Datos: Proyectos y Análisis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importaciones
from utils.cache_manager import CacheManager
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
if IS_STREAMLIT_CLOUD:
    css_path = 'static/css/streamlit_cloud.css'
else:
    css_path = 'static/css/style.css'

try:
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback a estilos básicos si no se encuentra el archivo
    st.markdown("""
        <style>
        .main-container { padding: 2rem; }
        .hero-section { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 3rem 2rem; 
            border-radius: 15px; 
            color: white; 
            text-align: center; 
            margin: 2rem 0; 
        }        .social-buttons { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
        .social-button { 
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 12px 20px; 
            border-radius: 4px; 
            color: white; 
            text-decoration: none; 
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            min-width: 120px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .social-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }
        .linkedin { background-color: #0077B5; border: 2px solid #0077B5; }
        .linkedin:hover { background-color: #005885; border-color: #005885; }
        .github { background-color: #333; border: 2px solid #333; }
        .github:hover { background-color: #1a1a1a; border-color: #1a1a1a; }
        </style>
    """, unsafe_allow_html=True)

# Estructura principal de la página
def main():
    # Iniciar medición de recursos
    optimizer.start_measurement()
    
    # Crear sidebar simplificado solo con enlaces de contacto
    create_simple_sidebar()

    # Renderizar página principal
    render_main_page()
    
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
def create_simple_sidebar():
    """
    Crea una barra lateral simplificada solo con enlaces de contacto y monitoreo
    """
    with st.sidebar:
        # Agregar enlaces a redes sociales usando el componente reutilizable
        add_sidebar_contact()

def add_footer():
    """
    Agrega un footer con enlaces de contacto y redes sociales
    al final de la página
    """
    add_page_footer()

def render_main_page():
    """Renderiza la página principal con estilos CSS optimizados"""
    
    # Título principal con clase CSS
    st.markdown('<h1 class="page-title">📊 Portafolio de Data Science</h1>', unsafe_allow_html=True)
    
    # Sección hero
    st.markdown("""
    <div class="hero-section">
        <p style="font-size: 1.2rem; line-height: 1.6; margin-bottom: 0;">
            La transición de la electricidad y la automatización industrial al mundo de los datos ha sido un desafío apasionante. 
            Este portafolio es una presentación de mis habilidades en análisis de datos y programación en Python.
            <br><br>
            Aquí encontrarás estudios realizados con metodologías rigurosas, mostrando la capacidad de transformar datos en conocimiento estructurado.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Proyectos destacados con cards
    st.markdown('<h2 class="section-title">Proyectos Destacados</h2>', unsafe_allow_html=True)
    
    # Grid de proyectos usando HTML/CSS
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin: 2rem 0;">
        <div class="project-card">
            <div class="project-icon">🏭</div>
            <div class="project-title">Análisis de emisiones de CO2</div>
            <div class="project-description">Estudio comprehensivo de emisiones industriales en Chile</div>
        </div>
        <div class="project-card">
            <div class="project-icon">💧</div>
            <div class="project-title">Estudios de calidad del agua</div>
            <div class="project-description">Análisis de parámetros de calidad en fuentes hídricas</div>
        </div>
        <div class="project-card">
            <div class="project-icon">👥</div>
            <div class="project-title">Análisis demográficos</div>
            <div class="project-description">Exploración de datos poblacionales de chile</div>
        </div>
        <div class="project-card">
            <div class="project-icon">💰</div>
            <div class="project-title">Análisis de presupuesto público de chile</div>
            <div class="project-description">Visualización de gastos gubernamentales y tendencias</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Descripción del objetivo
    render_objective()

    # Secciones principales con botones de navegación estilizados
    st.markdown('<h3 class="section-title">Explora los análisis:</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏭 Emisiones de CO2", use_container_width=True, type="primary"):
            st.switch_page("pages/01_emisiones_co2.py")
        
        if st.button("👥 Demografía", use_container_width=True, type="primary"):
            st.switch_page("pages/03_demografia_bigquery.py")
    
    with col2:
        if st.button("💧 Calidad del Agua", use_container_width=True, type="primary"):
            st.switch_page("pages/02_calidad_agua.py")
        
        if st.button("💰 Presupuesto Público", use_container_width=True, type="primary"):
            st.switch_page("pages/04_presupuesto_publico.py")
      
    # Sección de servicios
    st.markdown("---")
    st.subheader("💼 Servicios Profesionales")
    st.write("Ofrezco servicios de análisis de datos y desarrollo de dashboards personalizados.")
    
    if st.button("Ver Servicios Disponibles", use_container_width=True, type="secondary"):
        st.switch_page("pages/06_servicios.py")
    
    # Sección de currículum
    st.markdown("---")
    st.subheader("📄 Sobre Mí")
    st.write("Conoce más sobre mi formación, experiencia y habilidades profesionales.")
    
    if st.button("Ver Currículum Vitae", use_container_width=True, type="secondary"):
        st.switch_page("pages/05_curriculum.py")
    
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