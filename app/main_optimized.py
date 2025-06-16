"""
Versión optimizada de la aplicación principal del portafolio.
"""

import streamlit as st
import importlib.util
import sys
from pathlib import Path
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos locales
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir))

from utils.optimization import DataManager
from components.resource_metrics import display_resource_metrics, track_page_view

# Configuración de la página principal
st.set_page_config(
    page_title="Portafolio Data Science Optimizado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Inicializar el tracking de recursos
    optimizer = track_page_view()
    
    # Inicializar el gestor de datos
    data_manager = DataManager()
    
    # Configuración del header
    st.title("📊 Portafolio de Data Science")
    st.markdown("""
    Versión optimizada con pre-procesamiento y monitoreo de recursos, esta es la fomra de mostrar mis habilidades con los datos.
    """)
    
    # Mostrar métricas de recursos
    display_resource_metrics()
    
    # Sección principal
    st.markdown("## 📈 Análisis Disponibles")
    
    # Grid de análisis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Análisis Medioambiental")
        
        # Emisiones CO2
        with st.container():
            st.markdown("#### 🏭 Emisiones CO2 en Chile")
            last_update = data_manager.get_last_update("01_Analisis_Emisiones_CO2_Chile")
            st.markdown(f"*Última actualización: {last_update}*")
            st.button("Ver análisis completo", key="emisiones_co2", 
                     on_click=lambda: st.switch_page("pages/01_emisiones_co2.py"))
            
            st.markdown("""
            Análisis detallado de las emisiones de CO₂ en Chile entre 2010-2023, 
            evaluando su evolución, distribución por sectores y comparación regional.
            """)
        
        # Calidad del Agua
        with st.container():
            st.markdown("#### 💧 Calidad del Agua")
            last_update = data_manager.get_last_update("02_Analisis_Calidad_Del_Agua")
            st.markdown(f"*Última actualización: {last_update}*")
            st.button("Ver análisis completo", key="calidad_agua", 
                     on_click=lambda: st.switch_page("pages/02_calidad_agua.py"))
            
            st.markdown("""
            Evaluación de la calidad del agua en diferentes regiones de Chile,
            analizando parámetros fisicoquímicos y microbiológicos.
            """)
    
    with col2:
        st.markdown("### Análisis Socioeconómico")
        
        # Demografía
        with st.container():
            st.markdown("#### 👥 Análisis Demográfico")
            last_update = data_manager.get_last_update("03_Analisis_BigQuery_Demografia")
            st.markdown(f"*Última actualización: {last_update}*")
            st.button("Ver análisis completo", key="demografia", 
                     on_click=lambda: st.switch_page("pages/03_demografia_bigquery.py"))
            
            st.markdown("""
            Análisis de tendencias demográficas en Chile utilizando BigQuery para procesar
            grandes volúmenes de datos censales y proyecciones poblacionales.
            """)
        
        # Presupuesto Público
        with st.container():
            st.markdown("#### 💰 Presupuesto Público")
            last_update = data_manager.get_last_update("04_Analisis_Presupuesto_Publico")
            st.markdown(f"*Última actualización: {last_update}*")
            st.button("Ver análisis completo", key="presupuesto", 
                     on_click=lambda: st.switch_page("pages/04_presupuesto_publico.py"))
            
            st.markdown("""
            Evaluación de la evolución y distribución del presupuesto del sector público chileno
            en el período 2010-2025.
            """)
    
    # Información de optimización
    st.sidebar.markdown("""
    ### ℹ️ Información de Optimización
    
    Esta versión de la aplicación utiliza:
    - Pre-procesamiento de datos
    - Caché optimizado
    - Monitoreo de recursos
    - Simulación de costos GCP
    """)
    
    # Detener el tracking al finalizar
    metrics = optimizer.stop_monitoring()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    💡 *Los datos mostrados son pre-procesados para optimizar el rendimiento y reducir costos y asi podemer mantener el portafolio visible.*
    """)

if __name__ == "__main__":
    main()
