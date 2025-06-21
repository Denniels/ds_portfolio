"""
Aplicación principal del portafolio - Versión simplificada y optimizada
"""
# Importar environment.py primero para configurar el ambiente
import importlib.util
import sys
from pathlib import Path

# Cargar environment.py
env_path = Path(__file__).parent.parent / '.streamlit' / 'environment.py'
if env_path.exists():
    spec = importlib.util.spec_from_file_location("environment", env_path)
    environment = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(environment)

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import datetime
import streamlit.components.v1 as components
import logging
from functools import lru_cache

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Path(__file__).parent / 'app.log')
    ]
)
logger = logging.getLogger(__name__)

# Configuración de la página - debe estar al inicio
try:
    st.set_page_config(
        page_title="Portfolio de Ciencia de Datos",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception as e:
    logger.error(f"Error al configurar la página: {str(e)}")

# Caché para componentes pesados
@lru_cache(maxsize=32)
def get_cached_component(name: str):
    try:
        cache_file = Path(__file__).parent / 'data' / 'cache' / f'{name}.html'
        if cache_file.exists():
            return cache_file.read_text(encoding='utf-8')
    except Exception as e:
        logger.error(f"Error al cargar componente cacheado {name}: {str(e)}")
    return None

# Asegurarse de que app/ esté en el path de Python
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.append(str(current_dir))

# Determinar el entorno
IS_STREAMLIT_CLOUD = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
IS_CLOUD_RUN = os.getenv('CLOUD_RUN_SERVICE', 'false').lower() == 'true'

# Configuración específica para Streamlit Cloud
if IS_STREAMLIT_CLOUD:
    try:
        # Verificar dependencias críticas de forma silenciosa
        import numpy as np
        np.set_printoptions(precision=3, suppress=True)
        os.environ['OPENBLAS_NUM_THREADS'] = '1'
        os.environ['MKL_NUM_THREADS'] = '1'
        
        import pandas as pd
        pd.options.mode.chained_assignment = None
        
        import scipy
        import sklearn
        logger.info("Dependencias críticas cargadas correctamente")
        
    except ImportError as e:
        logger.error(f"Error al cargar dependencias críticas: {str(e)}")
        st.error("""
        ⚠️ Error al cargar dependencias críticas
        
        Por favor, verifica:
        1. La instalación de numpy y otras dependencias científicas
        2. La compatibilidad de versiones entre paquetes
        3. La disponibilidad de recursos del sistema
        """)
        st.stop()
        
    # Configurar opciones de rendimiento
    try:
        import streamlit.config as st_config
        st_config.set_option('server.maxUploadSize', 200)
        st_config.set_option('server.maxMessageSize', 200)
        st_config.set_option('server.enableXsrfProtection', True)
        st_config.set_option('server.enableCORS', False)
        logger.info("Configuración de Streamlit Cloud optimizada")
    except Exception as e:
        logger.warning(f"No se pudo optimizar configuración: {str(e)}")

# Importar módulo de monitoreo de salud
try:
    from app.streamlit.healthcheck import check_app_health, init_session, cleanup_session
    logger.info("Módulo de healthcheck cargado correctamente")
except ImportError as e:
    logger.warning(f"No se pudo cargar el módulo de healthcheck: {str(e)}")
    def check_app_health(): return True
    def init_session(): pass
    def cleanup_session(): pass

# Inicializar sesión y verificar salud
init_session()
if not check_app_health():
    st.error("La aplicación está experimentando problemas técnicos. Por favor, intenta recargar la página.")
    st.stop()

# Importaciones
from utils.cache_manager import CacheManager
from utils.contact_components import add_page_footer, add_sidebar_contact
# from utils.sidebar_components import create_simple_sidebar

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
    """Función principal de la aplicación"""
    try:
        # Asegurarse de que el estado de la sesión está inicializado
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
            st.session_state.metrics = {}
            st.session_state.sidebar_state = 'expanded'

        # Iniciar medición de recursos
        try:
            optimizer.start_measurement()
        except Exception as e:
            logger.error(f"Error al iniciar medición: {str(e)}")
        
        # Estructura principal con manejo de errores
        try:
            # Sidebar con enlaces de contacto
            with st.sidebar:
                create_simple_sidebar()
                
                # Monitor de recursos (solo si no estamos en Streamlit Cloud)
                if not IS_STREAMLIT_CLOUD:
                    try:
                        st.markdown("### 📊 Monitor Local de Recursos")
                        st.warning("⚠️ SIMULACIÓN LOCAL\nNo hay conexión con GCP")
                        
                        # Obtener y mostrar métricas
                        metrics = optimizer.stop_measurement()
                        optimizer.start_measurement()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("CPU Local", f"{metrics.get('cpu_percent', 0):.1f}%")
                        with col2:
                            st.metric("Memoria Local", f"{metrics.get('memory_gb', 0):.2f}GB")
                    except Exception as e:
                        logger.error(f"Error al mostrar métricas: {str(e)}")
                        
            # Contenido principal
            render_main_page()
            
            # Footer
            add_footer()
            
        except Exception as e:
            logger.error(f"Error en la estructura principal: {str(e)}")
            st.error("Ha ocurrido un error al cargar la página. Por favor, recarga la página.")
            
    except Exception as e:
        logger.error(f"Error crítico en main(): {str(e)}")
        st.error("Error crítico en la aplicación. Por favor, contacta al administrador.")
        
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

@st.cache_data(ttl=3600)
def get_cached_html_content():
    """Retorna el contenido HTML cacheado para mejorar el rendimiento"""
    return {
        'title': '<h1 class="page-title">📊 Portafolio de Data Science</h1>',
        'hero': """
        <div class="hero-section">
            <p style="font-size: 1.2rem; line-height: 1.6; margin-bottom: 0;">
                La transición de la electricidad y la automatización industrial al mundo de los datos ha sido un desafío apasionante. 
                Este portafolio es una presentación de mis habilidades en análisis de datos y programación en Python.
                <br><br>
                Aquí encontrarás estudios realizados con metodologías rigurosas, mostrando la capacidad de transformar datos en conocimiento estructurado.
            </p>
        </div>
        """,
        'projects_title': '<h2 class="section-title">Proyectos Destacados</h2>'
    }

def render_main_page():
    """Renderiza la página principal con estilos CSS optimizados y manejo de errores"""
    try:
        # Obtener contenido HTML cacheado
        content = get_cached_html_content()
        
        # Título principal
        st.markdown(content['title'], unsafe_allow_html=True)
        
        # Sección hero
        st.markdown(content['hero'], unsafe_allow_html=True)
        
        # Proyectos destacados
        st.markdown(content['projects_title'], unsafe_allow_html=True)
        
    except Exception as e:
        logger.error(f"Error al renderizar la página principal: {str(e)}")
        st.error("Error al cargar el contenido. Por favor, recarga la página.")
    
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