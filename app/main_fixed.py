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
</style>
""", unsafe_allow_html=True)

class DataSciencePortfolio:
    """Clase principal para el portafolio de Data Science"""
    
    def __init__(self):
        self.apps_dir = Path(__file__).parent / "apps"
        self.available_apps = self._get_available_apps()
        
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
            },
            # Aquí se pueden agregar más aplicaciones en el futuro
            "coming_soon_1": {
                "name": "Análisis de Mercado Financiero",
                "description": "Análisis de tendencias del mercado financiero con machine learning predictivo.",
                "file": None,
                "icon": "📈",
                "tags": ["Finanzas", "Machine Learning", "Predicción"],
                "status": "Próximamente"
            },
            "coming_soon_2": {
                "name": "Dashboard de Ventas",
                "description": "Dashboard interactivo para análisis de ventas y métricas de negocio.",
                "file": None,
                "icon": "🛒",
                "tags": ["Business Intelligence", "KPIs", "Dashboard"],
                "status": "Próximamente"
            }
        }
        return apps
    
    def run_portfolio(self):
        """Ejecuta la aplicación principal del portafolio"""
        
        # Header principal
        st.markdown("""
        <div class="main-header">
            <h1>📊 Portafolio de Data Science</h1>
            <p>< style='font-size: 1.2rem; color: #4a4a4a; margin-bottom: 2rem;'>
                Explora una colección de análisis interactivos sobre datos ambientales y demográficos de Chile.
                Cada proyecto demuestra diferentes aspectos del análisis de datos, visualización y machine learning.
                La intencion de este portafolio es presentar mis habilidades y proyectos en el campo de la ciencia de datos.
                Esta es mi oportunidad de mostrar lo que he aprendido los ultimos 4 años de estudio practicas, bootcamps y muchos mas contenidos!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar para navegación
        with st.sidebar:
            st.markdown("### 🧭 Navegación")
            
            # Selector de aplicación
            app_options = ["🏠 Inicio"] + [f"{app['icon']} {app['name']}" for app in self.available_apps.values() if app['status'] == 'Disponible']
            selected_app = st.selectbox("Seleccionar aplicación:", app_options)
            
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
        if selected_app == "🏠 Inicio":
            self._show_home_page()
        else:
            # Buscar la aplicación seleccionada
            for app_key, app_info in self.available_apps.items():
                if f"{app_info['icon']} {app_info['name']}" == selected_app:
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
                <div class="stat-number">2</div>
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
                    if st.button(f"Abrir {app_info['name']}", key=f"btn_{app_key}"):
                        st.session_state['selected_app'] = f"{app_info['icon']} {app_info['name']}"
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
            ### 🎯 Enfoque en Datos Ambientales
            
            Este portafolio se especializa en el **análisis de datos ambientales** con aplicaciones reales 
            basadas en fuentes oficiales del gobierno de Chile:
            
            - **💧 Calidad del Agua**: Análisis de 174 estaciones de monitoreo del DGA
            - **🏭 Emisiones CO2**: Estudio comprehensivo del RETC 2023 con 285K+ registros
            - **📊 Visualizaciones Interactivas**: Dashboards dinámicos con Plotly y Folium
            - **🔬 Metodología Científica**: Análisis estadístico robusto y conclusiones fundamentadas
            
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
            
            spec.loader.exec_module(app_module)
            
            # Ejecutar la aplicación
            if hasattr(app_module, 'WaterQualityApp'):
                app_instance = app_module.WaterQualityApp()
                app_instance.run()
            elif hasattr(app_module, 'CO2EmissionsApp'):
                app_instance = app_module.CO2EmissionsApp()
                app_instance.run()
            elif hasattr(app_module, 'main'):
                app_module.main()
            else:
                st.error("No se encontró una función main() o clase de aplicación en el módulo.")
                
        except Exception as e:
            st.error(f"Error al cargar la aplicación: {str(e)}")
            st.exception(e)

def main():
    """Función principal"""
    # Verificar si se seleccionó una aplicación desde la página de inicio
    if 'selected_app' in st.session_state:
        selected = st.session_state['selected_app']
        del st.session_state['selected_app']  # Limpiar después de usar
        
        # Simular la selección en el sidebar
        st.sidebar.selectbox("Seleccionar aplicación:", [selected], index=0)
    
    portfolio = DataSciencePortfolio()
    portfolio.run_portfolio()

if __name__ == "__main__":
    main()
