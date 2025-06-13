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
        </div>
    """, unsafe_allow_html=True)

# Estilos CSS aplicados a toda la aplicación
st.markdown("""
<style>
    /* Optimización Visual y Experiencia de Usuario */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Tarjetas de Aplicación */
    .app-card {
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        margin-bottom: 1rem;
        background: white;
        transition: all 0.3s;
        display: flex;
        flex-direction: column;
    }
    .app-card:hover {
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
        transform: translateY(-2px);
    }
    .app-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .app-badge.Análisis {
        background: #e0f7fa;
        color: #006064;
    }
    .app-badge.Visualización {
        background: #e8f5e9;
        color: #1b5e20;
    }
    .app-badge.Ambiental {
        background: #f1f8e9;
        color: #33691e;
    }
    .app-badge.Datos {
        background: #e8eaf6;
        color: #1a237e;
    }
    .app-badge.Oficial {
        background: #e3f2fd;
        color: #0d47a1;
    }
    .app-badge.Feedback {
        background: #fff3e0;
        color: #e65100;
    }
    .app-badge.Servicios {
        background: #ede7f6;
        color: #4527a0;
    }
    .app-badge.Tarifas {
        background: #fce4ec;
        color: #880e4f;
    }
    .app-badge.Profesional {
        background: #f3e5f5;
        color: #4a148c;
    }
    .app-badge.Legacy {
        background: #eeeeee;
        color: #424242;
    }
    .app-badge.Nuevo {
        background: #e8f5e9;
        color: #1b5e20;
        animation: pulse 2s infinite;
    }
    .app-status {
        margin-top: auto;
        padding-top: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .app-status-badge {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
    }
    .app-status-badge.Disponible {
        background: #c8e6c9;
        color: #2e7d32;
    }
    .app-status-badge.Próximamente {
        background: #ffecb3;
        color: #ff8f00;
    }
    .app-status-badge.Mantenimiento {
        background: #ffcdd2;
        color: #c62828;
    }
    .app-status-badge.Nuevo {
        background: #bbdefb;
        color: #1976d2;
    }
    
    /* Estadísticas del portafolio */
    .stat-box {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #64748b;
    }
    
    /* Responsividad para móviles */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        .stat-number {
            font-size: 1.4rem;
        }
    }
    
    /* Animación para elementos "Nuevo" */
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(46, 125, 50, 0.4);
        }
        70% {
            box-shadow: 0 0 0 6px rgba(46, 125, 50, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(46, 125, 50, 0);
        }
    }
    
    /* Sistema de Feedback */
    .feedback-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(45deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 10px 20px;
        font-size: 16px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        cursor: pointer;
        z-index: 1000;
        transition: all 0.3s;
    }
    .feedback-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.15);
    }
    .modal {
        display: none;
        position: fixed;
        z-index: 1001;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
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
                "name": "Emisiones CO2 por Industria",
                "description": "Exploración de emisiones de CO2 por sector industrial y ubicación geográfica. Análisis detallado basado en datos del RETC de Chile con visualizaciones interactivas.",
                "file": "co2_emissions_app.py",
                "icon": "🏭",
                "tags": ["Análisis Ambiental", "Visualización", "Datos Oficiales"],
                "status": "Disponible"
            },
            "demographics": {
                "name": "Análisis Demográfico",
                "description": "Análisis de tendencias demográficas históricas utilizando BigQuery y datos de patrones de nombres. Incluye visualizaciones interactivas de tendencias temporales.",
                "file": "demographics_app.py",
                "icon": "👥",
                "tags": ["Análisis", "Visualización", "BigQuery"],
                "status": "Disponible"
            },
            "budget_analysis": {
                "name": "Análisis Presupuesto Público",
                "description": "Análisis detallado del presupuesto del sector público de Chile por ministerio, partida y programa. Incluye comparativas interanuales y métricas de ejecución.",
                "file": "budget_analysis_app_v2.py",
                "icon": "📊",
                "tags": ["Análisis", "Visualización", "Datos Oficiales"],
                "status": "Disponible"
            },            # Sistema de Feedback (versión anterior)
            "feedback_legacy": {
                "name": "Feedback (Versión Original)",
                "description": "Versión original del sistema de feedback (mantenida para compatibilidad).",
                "file": "feedback_system.py",
                "icon": "💬",
                "tags": ["Feedback", "Legacy"],
                "status": "Mantenimiento"
            },            # Servicios profesionales            "servicios": {
                "name": "Servicios Profesionales",
                "description": "Catálogo de servicios profesionales de Data Science con tarifas referenciales en pesos chilenos.",
                "file": "services_display_fixed.py",
                "icon": "💼",
                "tags": ["Servicios", "Tarifas", "Profesional"],
                "status": "Disponible"
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
                    <span onclick="document.getElementById('feedbackModal').style.display='none';" class="close">&times;</span>
                    <h2>Tu opinión es importante</h2>
                    <p>Por favor comparte tus comentarios sobre el portafolio</p>
                    <div id="feedbackForm">
                        <!-- Aquí iría el formulario que se carga con JavaScript -->
                    </div>
                </div>
            </div>
            
            <script>
                // Función para cerrar el modal
                window.onclick = function(event) {
                    if (event.target == document.getElementById('feedbackModal')) {
                        document.getElementById('feedbackModal').style.display = "none";
                    }
                }
            </script>
        """, unsafe_allow_html=True)

    def run(self):
        """Ejecuta la aplicación principal del portafolio"""
        # Sidebar para navegación
        with st.sidebar:
            st.image("https://raw.githubusercontent.com/tu-usuario/ds-portfolio/main/static/logo.png", width=150)
            st.markdown("### 📊 Portafolio Data Science")
            st.markdown("---")
            
            # Crear opciones de menú
            menu_options = ["🏠 Inicio"]
            for app_info in self.available_apps.values():
                menu_options.append(f"{app_info['icon']} {app_info['name']}")
            
            # Selector de aplicación
            st.session_state['selected_app'] = st.selectbox(
                "Selecciona una aplicación:",
                menu_options
            )
            
            st.markdown("---")
            st.markdown("### 🔍 Sobre este proyecto")
            st.markdown("""
                Este portafolio demuestra habilidades en:
                - Análisis y visualización de datos
                - Machine Learning e IA
                - Desarrollo de aplicaciones web
                - Procesamiento de datos geoespaciales
            """)
            
            # Información de contacto
            st.markdown("### 📱 Contacto")
            st.markdown("""
                - 📧 [datascientist@portfolio.com](mailto:datascientist@portfolio.com)
                - 🔗 [LinkedIn](https://linkedin.com/in/datascientist)
                - 💻 [GitHub](https://github.com/datascientist)
            """)
            
            # Información de versión
            st.markdown("---")
            st.markdown("##### v1.3.0 | Última actualización: Junio 2025")
        
        # Contenido principal
        if st.session_state['selected_app'] == "🏠 Inicio":
            self._show_home_page()
        else:
            for app_key, app_info in self.available_apps.items():
                if f"{app_info['icon']} {app_info['name']}" == st.session_state['selected_app']:
                    if app_info['status'] == 'Disponible' or app_info['status'] == 'Nuevo':
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
                cols = st.columns([2, 8])
                with cols[0]:
                    st.markdown(f"""
                        <div style='font-size: 4rem; text-align: center; height: 100%; display: flex; align-items: center; justify-content: center;'>
                            {app_info['icon']}
                        </div>
                    """, unsafe_allow_html=True)
                
                with cols[1]:
                    st.markdown(f"""
                    <div class="app-card">
                        <h3>{app_info['name']}</h3>
                        <p>{app_info['description']}</p>
                        <div>
                    """, unsafe_allow_html=True)
                    
                    # Tags de la aplicación
                    for tag in app_info['tags']:
                        st.markdown(f"""
                            <span class="app-badge {tag}">{tag}</span>
                        """, unsafe_allow_html=True)
                    
                    # Estado y botón
                    st.markdown(f"""
                        <div class="app-status">
                            <span class="app-status-badge {app_info['status']}">{app_info['status']}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Botón para ejecutar la aplicación
                    if app_info['status'] == 'Disponible' or app_info['status'] == 'Nuevo':
                        if st.button(f"Abrir {app_info['name']}", key=f"btn_{app_key}"):
                            st.session_state['selected_app'] = f"{app_info['icon']} {app_info['name']}"
                            st.rerun()
                    
                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)
        
        # Mostrar el botón de feedback
        self.show_feedback_button()
                
        # Información del proyecto
        st.markdown("## 📝 Acerca de este portafolio")
        st.markdown("""
        Este portafolio demuestra la aplicación de ciencia de datos en diferentes contextos, con enfoque en datos ambientales y públicos de Chile. Cada aplicación está diseñada para ofrecer análisis significativos e interactivos.
        
        ### Tecnologías utilizadas:
        - **Frontend**: Streamlit para interfaces interactivas
        - **Data Analysis**: Pandas, NumPy, SciPy
        - **Visualización**: Plotly, Folium, Matplotlib
        - **Cloud**: Google Cloud Platform (BigQuery, Cloud Run)
        - **Geoespacial**: GeoPandas, Shapely
        - **Machine Learning**: Scikit-learn, TensorFlow
        
        El código fuente está disponible en GitHub bajo licencia MIT.
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
            elif hasattr(app_module, 'ServicesDisplay'):
                # Servicios Profesionales
                app_instance = app_module.ServicesDisplay()
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
                    st.error(f"Error: el atributo 'app' en {app_info['file']} no es una función llamable")
            else:
                st.error(f"Error: No se encontró punto de entrada en {app_info['file']}")
        except Exception as e:
            st.error(f"Error al ejecutar la aplicación: {str(e)}")
            st.exception(e)

# Ejecutar la aplicación principal
if __name__ == "__main__":
    portfolio = DataSciencePortfolio()
    portfolio.run()
