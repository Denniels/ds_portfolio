"""
Página de Servicios Profesionales del Portafolio
"""
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# Importar configuración de página
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Configurar directorios de datos
DATA_CACHE_DIR = parent_dir / "data" / "cache"
DATA_DIR = parent_dir / "data"

from utils.page_setup import setup_page, add_page_title, create_card

# Configurar página
st = setup_page(
    title="Servicios Profesionales",
    icon="🛠️"
)

# Título y descripción de la página
add_page_title(
    "Servicios Profesionales",
    "Soluciones personalizadas en Data Science, Machine Learning y desarrollo de software para empresas y particulares.",
    "🛠️"
)

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

def load_services_data():
    """Carga y procesa los datos de servicios desde el archivo markdown"""
    services = {
        "Análisis y Dashboards": {
            "Dashboard Interactivo Básico": {
                "precio": 1500000,
                "descripcion": "Dashboard con 3-5 visualizaciones interactivas, filtros básicos y análisis descriptivo.",
                "duracion": "2-3 semanas",
                "incluye": ["Hosting por 3 meses", "Configuración inicial", "1 sesión de capacitación"],
                "categoria": "dashboard"
            },
            "Dashboard Interactivo Avanzado": {
                "precio": 2800000,
                "descripcion": "Dashboard con 5+ visualizaciones avanzadas, filtros complejos, análisis predictivo básico.",
                "duracion": "4-6 semanas",
                "incluye": ["Hosting por 6 meses", "Configuración avanzada", "2 sesiones de capacitación"],
                "categoria": "dashboard"
            },
            "Integración de Fuentes de Datos": {
                "precio": 450000,
                "descripcion": "Integración de fuentes de datos adicionales en dashboards existentes.",
                "duracion": "1 semana",
                "incluye": ["Configuración ETL", "Validación de datos", "Documentación"],
                "categoria": "integracion"
            }
        },
        "Análisis Geoespacial": {
            "Mapa Interactivo Básico": {
                "precio": 1200000,
                "descripcion": "Visualización geoespacial con hasta 3 capas de datos y filtros básicos.",
                "duracion": "2-3 semanas",
                "incluye": ["Hosting por 3 meses", "Configuración de capas", "1 sesión de capacitación"],
                "categoria": "mapa"
            },
            "Mapa Interactivo Avanzado": {
                "precio": 2500000,
                "descripcion": "Visualización geoespacial con 5+ capas, análisis de clusters, heatmaps.",
                "duracion": "4-6 semanas",
                "incluye": ["Hosting por 6 meses", "Análisis avanzado", "2 sesiones de capacitación"],
                "categoria": "mapa"
            }
        },
        "Análisis Sectorial": {
            "Análisis de Emisiones": {
                "precio": 2800000,
                "descripcion": "Estudio detallado de emisiones contaminantes y tendencias.",
                "duracion": "6-8 semanas",
                "incluye": ["Reporte detallado", "Dashboard interactivo", "Presentación ejecutiva"],
                "categoria": "sectorial"
            },
            "Análisis de Calidad del Agua": {
                "precio": 2400000,
                "descripcion": "Evaluación de parámetros de calidad del agua y distribución geográfica.",
                "duracion": "4-6 semanas",
                "incluye": ["Reporte técnico", "Visualización geoespacial", "Recomendaciones"],
                "categoria": "sectorial"
            }
        }
    }
    return services

def format_currency(value):
    """Formatea valores monetarios a CLP"""
    return f"${value:,.0f} CLP"

def create_service_card(service_name, details):
    """Crea una tarjeta visual para un servicio"""
    with st.container():
        st.subheader(service_name)
        col1, col2 = st.columns([2,1])
        
        with col1:
            st.write(details["descripcion"])
            st.write("**Incluye:**")
            for item in details["incluye"]:
                st.write(f"✓ {item}")
        
        with col2:
            st.metric("Valor Referencial", format_currency(details["precio"]))
            st.write(f"⏱️ Duración estimada: {details['duracion']}")
            
            # Botón de contacto
            if st.button("📬 Solicitar información", key=f"btn_{service_name}"):
                st.markdown("""
                Para solicitar este servicio, por favor contáctame a través de:
                - 📧 [LinkedIn](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
                - 💼 [Correo directo](mailto:tu_correo@ejemplo.com)
                """)
        
        st.markdown("---")

def main():
    # Título y descripción
    st.title("💼 Servicios Profesionales de Data Science")
    
    # Agregar enlaces de contacto en la barra lateral
    add_sidebar_contact()
    
    st.info("""
    **Nota Importante**: Los valores mostrados son referenciales y pueden variar según los requerimientos específicos de cada proyecto.
    Cada servicio se adapta a las necesidades particulares del cliente y puede incluir funcionalidades adicionales.
    Estos valores no implican presupuesto final, sino una guía para entender el alcance y costo de los servicios ofrecidos.
    Si estás interesado en alguno de los servicios, por favor contáctame para una cotización personalizada.
    """)
    
    # Cargar datos de servicios
    services = load_services_data()
    
    # Selector de categoría
    categoria = st.selectbox(
        "Selecciona una categoría de servicios:",
        list(services.keys())
    )
    
    # Mostrar servicios de la categoría seleccionada
    st.subheader(f"📊 {categoria}")
    for service_name, details in services[categoria].items():
        create_service_card(service_name, details)
    
    # Información adicional
    with st.expander("ℹ️ Información Adicional"):
        st.markdown("""
        ### Proceso de Trabajo
        1. **Reunión inicial**: Entendimiento de necesidades y alcance
        2. **Propuesta detallada**: Incluye cronograma y entregables
        3. **Desarrollo iterativo**: Feedback constante del cliente
        4. **Entrega y capacitación**: Aseguramos la correcta implementación
        
        ### Formas de Trabajo
        - **Proyecto completo**: Desarrollo de inicio a fin
        - **Asesoría por horas**: Para proyectos puntuales
        - **Mantenimiento**: Soporte continuo post-implementación
        
        ### Garantía
        Todos los servicios incluyen:
        - Período de ajustes post-implementación
        - Documentación completa
        - Soporte técnico durante el período acordado
        """)
    
    # Nota final
    st.markdown("""
    ---
    ### 📬 ¿Interesado en algún servicio?
    
    Los precios mostrados son referenciales y pueden variar según los requerimientos específicos.
    Para obtener una cotización personalizada, por favor contáctame a través de:
    
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
    [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Denniels)
    
    **Última actualización de precios**: {}
    """.format(datetime.now().strftime("%d/%m/%Y")))
    
    # Agregar footer al final de la página

    add_page_footer()

if __name__ == "__main__":
    main()
