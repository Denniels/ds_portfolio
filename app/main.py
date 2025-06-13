"""
Portafolio de Data Science - Aplicación Principal
=================================================

Este es el punto de entrada principal para el portafolio de Data Science.
Permite navegar entre diferentes aplicaciones y proyectos.

Autor: Data Scientist
"""

import streamlit as st
import importlib.util
import sys
from pathlib import Path

# Configuración de la página principal
st.set_page_config(
    page_title="Portafolio Data Science",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar estado de la sesión de manera segura
if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    st.session_state['selected_app'] = "🏠 Inicio"
    st.session_state['current_app'] = None

# Funciones de navegación
def show_welcome():
    st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1 style='color: #1e3c72; margin-bottom: 1rem;'>👋 ¡Bienvenido a mi Portafolio de Data Science!</h1>
            <p style='font-size: 1.2rem; color: #4a4a4a; margin-bottom: 2rem;'>
                Explora una colección de análisis interactivos sobre datos ambientales y demográficos de Chile.
                Cada proyecto demuestra diferentes aspectos del análisis de datos, visualización y machine learning.
                La intencion de este portafolio es presentar mis habilidades y proyectos en el campo de la ciencia de datos.
                Esta es mi oportunidad de mostrar lo que he aprendido los ultimos 4 años de estudio practicas, bootcamps y muchos mas contenidos!
            </p>
            <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem;'>
                <h3 style='color: #2a5298; margin-bottom: 1rem;'>🚀 Novedades - Junio 2025</h3>
                <ul style='text-align: left; color: #4a4a4a;'>
                    <li>✨ Nuevo despliegue en Google Cloud Run (capa gratuita)</li>
                    <li>📊 Visualizaciones interactivas mejoradas</li>
                    <li>🔄 Actualizaciones automáticas vía GitHub Actions</li>
                    <li>📱 Interfaz adaptativa para móviles y tablets</li>
                    <li>📝 ¡Nuevo! Sistema de feedback y sugerencias</li>
                </ul>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Función eliminada ya que no es necesaria con el nuevo enfoque

# CSS personalizado para el portafolio
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .app-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
    }
    
    .app-card h3 {
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    
    .app-card p {
        color: #666;
        margin-bottom: 1rem;
    }
    
    .nav-button {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
    }
    
    .stat-box {
        text-align: center;
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #2a5298;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }
    
    /* Botón de Feedback */
    .feedback-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 10px 20px;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 20px;
        border: none;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 1000;
        font-weight: bold;
    }
    
    .feedback-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Estilos para el modal */
    .modal {
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1001;
        max-width: 500px;
        width: 90%;
    }
    
    .modal-overlay {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

def initialize_feedback_state():
    """Inicializa el estado para el sistema de feedback"""
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False

class DataSciencePortfolio:
    """Clase principal para el portafolio de Data Science"""
    
    def __init__(self):
        self.apps_dir = Path(__file__).parent / "apps"
        self.available_apps = self._get_available_apps()
        initialize_feedback_state()

    def _get_available_apps(self):
        """Obtiene la lista de aplicaciones disponibles"""
        apps = {
            "water_quality": {
                "name": "Análisis de Calidad del Agua",
                "description": "Análisis exhaustivo de parámetros de calidad del agua basado en datos oficiales del DGA Chile. Incluye análisis temporal, espacial y evaluación de estándares de calidad.",
                "file": "water_quality_app.py",
                "icon": "💧",
                "tags": ["Análisis Ambiental", "Visualización", "Datos Oficiales"],
                "status": "Disponible"
            },
            "co2_emissions": {
                "name": "Emisiones CO2 Chile",
                "description": "Análisis comprehensivo de emisiones de gases de efecto invernadero en Chile basado en datos del RETC 2023. Incluye análisis regional, sectorial y por tipos de fuente.",
                "file": "co2_emissions_app.py",
                "icon": "🏭",
                "tags": ["Cambio Climático", "RETC", "Análisis Ambiental", "GEI"],
                "status": "Disponible"
            },            "demographics": {
                "name": "Análisis Demográfico",
                "description": "Análisis de tendencias en nombres de EE.UU. (1910-2013) utilizando BigQuery. Explora patrones históricos, cambios generacionales y diferencias por género en la elección de nombres.",
                "file": "demographics_app_new.py",
                "icon": "👤",
                "tags": ["Demografía", "BigQuery", "Cloud", "Visualización"],
                "status": "Disponible"
            },
            "budget_analysis": {
                "name": "Análisis del Presupuesto Público",
                "description": "Análisis interactivo y detallado del Presupuesto del Sector Público de Chile v2.0. Incluye análisis de concentración, curvas de Lorenz, evolución temporal y métricas avanzadas de distribución presupuestaria.",
                "file": "budget_analysis_app_v2.py",
                "icon": "💰",
                "tags": ["Finanzas Públicas", "Datos Gubernamentales", "Visualización Interactiva", "Análisis Avanzado"],
                "status": "Disponible"
            },            # Sistema de Feedback
            "feedback": {
                "name": "Feedback y Sugerencias",
                "description": "¿Tienes comentarios o sugerencias? ¡Me encantaría escucharlos! Ayúdame a mejorar este portafolio compartiendo tus ideas.",
                "file": "firestore_feedback_system.py",  # Nueva versión con Firestore
                "icon": "📝",
                "tags": ["Feedback", "Sugerencias", "Mejoras"],
                "status": "Disponible"
            },            # Sistema de Feedback (versión anterior)
            "feedback_legacy": {
                "name": "Feedback (Versión Original)",
                "description": "Versión original del sistema de feedback (mantenida para compatibilidad).",
                "file": "feedback_system.py",
                "icon": "💬",
                "tags": ["Feedback", "Legacy"],
                "status": "Mantenimiento"
            },            # Servicios profesionales
            "servicios": {
                "name": "Servicios Profesionales",
                "description": "Catálogo de servicios profesionales de Data Science con tarifas referenciales en pesos chilenos.",
                "file": "services_display_fixed.py",
                "icon": "💼",
                "tags": ["Servicios", "Tarifas", "Profesional"],
                "status": "Nuevo"
            }
        }
        return apps
    
    def show_feedback_button(self):
        """Muestra el botón flotante de feedback"""
        # Añadir botón de feedback flotante
        st.markdown("""
            <button class="feedback-button" onclick="document.getElementById('feedbackModal').style.display='block';">
                💭 Dejar Feedback
            </button>
            
            <div id="feedbackModal" class="modal">
                <div class="modal-content">
                    <h2>📝 ¿Tienes algún comentario o sugerencia?</h2>
                    <form id="feedbackForm">
                        <input type="text" placeholder="Nombre (opcional)">
                        <textarea placeholder="Tu mensaje aquí..."></textarea>
                        <button type="submit">Enviar</button>
                    </form>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    def run_portfolio(self):
        """Ejecuta la aplicación principal del portafolio"""
        
        # Header principal  #style='font-size: 1.2rem; color: #4a4a4a; margin-bottom: 2rem;'
        st.markdown("""
        <div class="main-header">
            <h1>📊 Portafolio de Data Science</h1>
            <p>
                Aplicaciones interactivas y análisis de datos ambientales y demográficos.
                Explora una colección de análisis interactivos sobre datos ambientales y demográficos de Chile.
                Cada proyecto demuestra diferentes aspectos del análisis de datos, visualización y machine learning.
                La intencion de este portafolio es presentar mis habilidades y proyectos en el campo de la ciencia de datos.
                Esta es mi oportunidad de mostrar lo que he aprendido los ultimos 4 años de estudio practicas, bootcamps y muchos mas contenidos!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar para navegación
        with st.sidebar:
            st.markdown("### 🧭 Navegación")            # Selector de aplicación
            app_options = ["🏠 Inicio"] + [f"{app['icon']} {app['name']}" for app in self.available_apps.values() if app['status'] == 'Disponible']
            selected_app = st.selectbox(
                "Seleccionar aplicación:", 
                app_options,
                index=app_options.index(st.session_state['selected_app']) if st.session_state['selected_app'] in app_options else 0
            )
            
            # Actualizar estado de la sesión cuando cambia la selección
            if selected_app != st.session_state.get('selected_app'):
                st.session_state['selected_app'] = selected_app
                st.session_state['current_app'] = None
                st.rerun()
            
            st.markdown("---")
            
            # Información del portafolio
            st.markdown("### ℹ️ Información")
            st.info("Este portafolio contiene múltiples aplicaciones de Data Science desarrolladas con Streamlit.")
            
            # Enlaces útiles
            st.markdown("### 🔗 Enlaces")
            st.markdown("- [GitHub Repository](https://github.com/Denniels/ds_portfolio)")
            st.markdown("- [LinkedIn](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)")
            st.markdown("- [Documentación](https://github.com/Denniels/ds_portfolio/tree/main/docs)")
          # Contenido principal
        if st.session_state['selected_app'] == "🏠 Inicio":
            self._show_home_page()
        else:
            # Buscar la aplicación seleccionada
            for app_key, app_info in self.available_apps.items():
                if f"{app_info['icon']} {app_info['name']}" == st.session_state['selected_app']:
                    if app_info['status'] == 'Disponible':
                        self._run_app(app_info)
                    else:
                        st.warning(f"La aplicación '{app_info['name']}' estará disponible próximamente.")
                    break
    
    def _show_home_page(self):
        """Muestra la página de inicio del portafolio"""
        
        # Estadísticas del portafolio
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">4</div>
                <div class="stat-label">Apps Activas</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">459K+</div>
                <div class="stat-label">Registros</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">6+</div>
                <div class="stat-label">Tecnologías</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="stat-box">
                <div class="stat-number">100%</div>
                <div class="stat-label">Open Source</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("## 🚀 Aplicaciones Disponibles")
        
        # Mostrar aplicaciones en tarjetas
        for app_key, app_info in self.available_apps.items():
            with st.container():
                st.markdown(f"""
                <div class="app-card">
                    <h3>{app_info['icon']} {app_info['name']}</h3>
                    <p>{app_info['description']}</p>
                    <div style="margin-bottom: 1rem;">
                        {''.join([f'<span style="background: #e3f2fd; color: #1976d2; padding: 0.2rem 0.5rem; border-radius: 3px; margin-right: 0.5rem; font-size: 0.8rem;">{tag}</span>' for tag in app_info['tags']])}
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: {'#28a745' if app_info['status'] == 'Disponible' else '#ffc107'};">
                            {'✅' if app_info['status'] == 'Disponible' else '⏳'} {app_info['status']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
                if app_info['status'] == 'Disponible':
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        if st.button(f"🚀 Abrir {app_info['name']}", key=f"btn_{app_key}", use_container_width=True):
                            new_app = f"{app_info['icon']} {app_info['name']}"
                            if new_app != st.session_state.get('selected_app'):
                                st.session_state['selected_app'] = new_app
                                st.session_state['current_app'] = None
                                st.rerun()
        
        # Sección de tecnologías
        st.markdown("## 🛠️ Tecnologías Utilizadas")
        
        tech_cols = st.columns(6)
        technologies = [
            {"name": "Python", "icon": "🐍"},
            {"name": "Streamlit", "icon": "⚡"},
            {"name": "Pandas", "icon": "🐼"},
            {"name": "Plotly", "icon": "📊"},
            {"name": "Folium", "icon": "🗺️"},
            {"name": "NumPy", "icon": "🔢"}
        ]
        
        for i, tech in enumerate(technologies):
            with tech_cols[i]:
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem;">{tech['icon']}</div>
                    <div style="font-weight: bold; margin-top: 0.5rem;">{tech['name']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Sección de descripción del portafolio
        st.markdown("## 📋 Sobre este Portafolio")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 🎯 Enfoque en Datos reales
            
            Este portafolio se especializa en el **análisis de datos reales** con aplicaciones basadas 
            en fuentes oficiales:
            
            - 💧 Calidad del Agua**: Análisis de 174 estaciones de monitoreo del DGA
            - 🏭 Emisiones CO2**: Estudio comprehensivo del RETC 2023 con 285K+ registros
            - 👤 Análisis demográfico
            - 💰 Análisis del Presupuesto Público
            - 📊 Visualizaciones Interactivas**: Dashboards dinámicos con Plotly y Folium
            - 🔬 Metodología Científica**: Análisis estadístico robusto y conclusiones fundamentadas
            
            ### 💡 Características Técnicas
            
            - **Escalabilidad**: Manejo eficiente de grandes volúmenes de datos
            - **Interactividad**: Filtros dinámicos y visualizaciones responsive
            - **Modularidad**: Arquitectura limpia y reutilizable
            - **Documentación**: Metodologías y limitaciones claramente documentadas
            """)
        
        with col2:
            st.markdown("""
            ### 📈 Métricas del Portafolio
            
            **Datos Procesados:**
            - 🏭 285,403 registros RETC
            - 💧 174 estaciones DGA
            - 🗺️ 16 regiones Chile
            - 📊 50+ visualizaciones
            
            **Tecnologías:**
            - Python 3.11+
            - Streamlit Framework
            - Plotly Dashboard
            - Pandas Analytics
            - Folium Mapping
            - NumPy Computing
            
            **Impacto:**
            - Análisis política pública
            - Insights ambientales
            - Herramientas decisión
            - Código open source
            """)
    
    def _run_app(self, app_info):
        """Ejecuta una aplicación específica"""
        try:
            app_path = self.apps_dir / app_info['file']
            
            # Importar y ejecutar la aplicación
            spec = importlib.util.spec_from_file_location("app_module", app_path)
            app_module = importlib.util.module_from_spec(spec)
              # Agregar el directorio de apps al path para imports relativos
            if str(self.apps_dir) not in sys.path:
                sys.path.insert(0, str(self.apps_dir))
            
            # Ejecutar la aplicación basada en la clase disponible
            spec.loader.exec_module(app_module)
            
            if hasattr(app_module, 'BudgetAnalysisApp'):
                app_instance = app_module.BudgetAnalysisApp()
                app_instance.run()
            elif hasattr(app_module, 'WaterQualityApp'):
                app_instance = app_module.WaterQualityApp()
                app_instance.run()
            elif hasattr(app_module, 'CO2EmissionsApp'):
                app_instance = app_module.CO2EmissionsApp()
                app_instance.run()
            elif hasattr(app_module, 'DemographicsApp'):
                app_instance = app_module.DemographicsApp()
                app_instance.run()
            elif hasattr(app_module, 'FirestoreFeedbackApp'):
                # Nueva versión con Firestore
                app_instance = app_module.FirestoreFeedbackApp()
                app_instance.run()
            elif hasattr(app_module, 'FeedbackApp'):
                # Versión anterior
                app_instance = app_module.FeedbackApp()
                app_instance.run()
            elif hasattr(app_module, 'run'):
                app_module.run()
            elif hasattr(app_module, 'main'):
                app_module.main()
            elif hasattr(app_module, 'app'):
                # Asegurarse de que app es una función o un objeto llamable
                if callable(app_module.app):
                    app_module.app()
                else:
                    app_module.app.run()
            else:
                st.error("No se encontró una función main(), run(), app() o clase de aplicación en el módulo.")
                
        except Exception as e:
            st.error(f"Error al cargar la aplicación: {str(e)}")
            if st.session_state.get('debug_mode', False):
                st.exception(e)

def main():
    """Función principal"""
    # Asegurar que el estado está inicializado
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        st.session_state['selected_app'] = "🏠 Inicio"
        st.session_state['current_app'] = None
    
    portfolio = DataSciencePortfolio()
    portfolio.run_portfolio()

if __name__ == "__main__":
    main()
