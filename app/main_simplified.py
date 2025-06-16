"""
Portafolio de Data Science - Aplicación Principal Optimizada
"""

import streamlit as st
import os
from pathlib import Path
from utils.optimization import DataManager, ResourceOptimizer, format_cost, format_resource
from utils.navigation import navigate_to_page

# Configuración de la página principal
st.set_page_config(
    page_title="Portafolio Data Science Optimizado",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar monitorio de recursos
optimizer = ResourceOptimizer()
optimizer.start_monitoring()

# Inicializar el gestor de datos
data_manager = DataManager()

# Asegurar que existen los directorios de páginas
pages_dir = Path(__file__).parent / "pages"
pages_dir.mkdir(exist_ok=True)

# Función para asegurar que una página existe
def ensure_page(page_name, content, overwrite=False):
    page_path = pages_dir / page_name
    if not page_path.exists() or overwrite:
        with open(page_path, "w", encoding="utf-8") as f:
            f.write(content)

# Título y descripción
st.title("📊 Portafolio de Ciencia de Datos")
st.markdown("Versión optimizada con preprocesamiento y monitoreo de recursos.")

# Información sobre la URL de acceso correcta
st.info("""
### ⚠️ Nota sobre la URL de acceso
Si ves "No se puede acceder a este sitio" al usar la URL mostrada en la terminal:
- Usa **http://localhost:8080** o **http://127.0.0.1:8080** en lugar de 0.0.0.0:8080
- Esta aplicación siempre debe accederse mediante localhost, no con 0.0.0.0
""", icon="⚠️")

# Añadir destacado sobre cómo acceder a los estudios
st.success("""
### 🔍 Cómo acceder a los estudios detallados

Para ver cualquiera de los análisis completos, tienes dos opciones:
1. **Haz clic en los enlaces de la barra lateral** para acceder directamente a cada estudio 👈
2. O pulsa el botón "Ver análisis completo" debajo de cada sección
""")

# Sección de Perfil Profesional
with st.expander("ℹ️ Sobre mí y este portafolio", expanded=True):
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Imagen de perfil personalizada relacionada con ciencia de datos
        profile_image_path = "app/static/images/data_science_profile_small.png"
        # Verificar si la imagen existe, si no, mostrar un mensaje
        try:
            st.image(profile_image_path, width=150)
            
            # Añadir información sobre herramientas
            st.caption("**Tecnologías:**")
            cols = st.columns(3)
            icons = {
                "Python": "🐍",
                "Pandas": "🔢",
                "SQL": "📊"
            }
            
            for idx, (tech, icon) in enumerate(icons.items()):
                with cols[idx % 3]:
                    st.markdown(f"{icon} {tech}")
                    
        except Exception:
            st.warning("Imagen de perfil no encontrada. Ejecutando: `python app/utils/generate_profile_image.py`")
            st.image("https://via.placeholder.com/150?text=DS", width=150)
        
    with col2:        st.markdown("""        ## Daniel Andrés Mardones Sanhueza
        ### Especialista en Mantenimiento Industrial & Entusiasta del Data Science
        
        Profesional con más de 10 años de experiencia en mantenimiento y automatización industrial, actualmente **expandiendo mis conocimientos hacia el análisis de datos**. Combino mi experiencia práctica en resolución de problemas industriales con nuevas habilidades en análisis de datos para aportar soluciones innovadoras.
        
        Este portafolio demuestra mi capacidad para:
        - Analizar datos gubernamentales complejos
        - Crear visualizaciones interactivas
        - Implementar soluciones cloud-native
        - Optimizar recursos computacionales
        
        ### Enlaces Profesionales:
        - 🔗 [LinkedIn](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
        - 💻 [GitHub](https://github.com/Denniels)
        - 📄 [Curriculum Vitae](/docs/curriculum.md)
        
        ### Objetivos de este portafolio:
        
        1. **Demostrar mis habilidades técnicas** con Python, Streamlit, y servicios cloud
        2. **Presentar análisis basados en datos reales** con conclusiones profesionales
        3. **Mostrar implementaciones optimizadas** que operan dentro de la capa gratuita de GCP
        4. **Evidenciar mi capacidad para trabajar** con datos complejos y extraer insights relevantes
        
        Los proyectos que encontrarás aquí utilizan datos reales de Chile y muestran mi enfoque analítico y técnico, desarrollado de manera autodidacta y aplicado a problemas del mundo real.
        """)

# Sección principal
st.markdown("## Análisis disponibles")

# Grid de análisis
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Análisis Medioambiental")
    
    # Emisiones CO2
    with st.container():
        st.markdown("#### 🏭 Emisiones de CO2 en Chile")
        last_update = data_manager.get_last_update("01_Analisis_Emisiones_CO2_Chile")
        st.markdown(f"*Última actualización: {last_update}*")
        if st.button("Ver análisis completo", key="emisiones_co2"):
            page = "01_emisiones_co2.py"
            # Intentar navegación directa
            if not navigate_to_page(page):
                st.info(f"Por favor, ejecuta: streamlit run pages/{page}")
        
        st.markdown("""
        Análisis detallado de las emisiones de CO₂ en Chile entre 2010-2023, 
        evaluando su evolución, distribución por sectores y comparación regional.
        """)
    
    # Calidad del Agua
    with st.container():
        st.markdown("#### 💧 Calidad del Agua")
        last_update = data_manager.get_last_update("02_Analisis_Calidad_Del_Agua")
        st.markdown(f"*Última actualización: {last_update}*")
        if st.button("Ver análisis completo", key="calidad_agua"):
            page = "02_calidad_agua.py"
            # Intentar navegación directa
            if not navigate_to_page(page):
                st.info(f"Por favor, ejecuta: streamlit run pages/{page}")
        
        st.markdown("""
        Evaluación de la calidad del agua en diferentes regiones de Chile,
        analizando parámetros fisicoquímicos y microbiológicos.
        """)

with col2:
    st.markdown("### Análisis Socioeconómico")    # Demografía
    with st.container():
        st.markdown("#### 👥 Análisis demográfico")
        last_update = data_manager.get_last_update("03_Analisis_BigQuery_Demografia")
        st.markdown(f"*Última actualización: {last_update}*")
        if st.button("Ver análisis completo", key="demografia"):
            page = "03_demografia_bigquery.py"
            # Intentar navegación directa
            if not navigate_to_page(page):
                st.info(f"Por favor, ejecuta: streamlit run pages/{page}")
        
        st.markdown("""
        Análisis de tendencias demográficas en Chile utilizando BigQuery para procesar
        grandes volúmenes de datos censales y proyecciones poblacionales.
        """)    # Presupuesto Público
    with st.container():
        st.markdown("#### 💰 Presupuesto Público")
        last_update = data_manager.get_last_update("04_Analisis_Presupuesto_Publico")
        st.markdown(f"*Última actualización: {last_update}*")
        if st.button("Ver análisis completo", key="presupuesto"):
            page = "04_presupuesto_publico.py"
            # Intentar navegación directa
            if not navigate_to_page(page):
                st.info(f"Por favor, ejecuta: streamlit run pages/{page}")
        
        st.markdown("""
        Evaluación de la evolución y distribución del presupuesto del sector público chileno
        en el período 2010-2025.
        """)

# Importar información de fuentes de datos
from utils.data_sources import get_data_source_info

# Información de optimización
metrics = optimizer.get_resource_summary()

with st.sidebar:
    # Perfil técnico resumido
    st.markdown("### 💻 Perfil Técnico")
    
    with st.container():
        st.markdown("""
        #### Habilidades Técnicas:
        - **Lenguajes**: Python (5+ años), SQL
        - **Análisis de Datos**: Pandas, NumPy, Matplotlib
        - **Visualización**: Plotly, Seaborn, Streamlit
        - **Cloud**: Google Cloud Platform (capa gratuita)
        - **Optimización**: Preprocesamiento, caché, monitoreo
        """)
        
        with st.expander("Ver stack tecnológico completo"):
            st.markdown("""
            - **Bases de Datos**: SQLite, PostgreSQL, BigQuery
            - **ETL**: Scripts personalizados en Python, Pandas
            - **Control de Versiones**: Git, GitHub
            - **Despliegue**: Streamlit Cloud, Google Cloud Run
            - **Geoespacial**: GeoPandas, Folium
            - **Desarrollo Web**: Básico de HTML/CSS, Flask
            """)
    
    # Información sobre optimización de datos
    with st.expander("🔍 Estrategias de Optimización"):
        st.markdown("""
        Este portafolio implementa varias técnicas para garantizar que todos los datos 
        estén siempre disponibles manteniendo el uso dentro de la **capa gratuita** de GCP:
        
        1. **Preprocesamiento completo**: Todos los datos son preprocesados y almacenados 
           en formatos optimizados (CSV.gz, WebP, JSON compacto)
        
        2. **Caché multinivel**: 
           - Decorador `@st.cache_data` en todas las funciones de carga
           - Almacenamiento en memoria para consultas frecuentes
           - Sistema de versionado de caché para actualizaciones
        
        3. **Ejecución programada**: Scripts automatizados extraen y procesan datos 
           periódicamente para mantener la información actualizada
        
        4. **Monitoreo de recursos**: Sistema integrado de seguimiento de uso de 
           CPU, memoria y estimación de costos para garantizar la operación dentro 
           del límite gratuito
        """)
    
    st.markdown("---")
      # Añadir flecha indicativa
    st.markdown("""
    ### 👇 Ejecuta las apps desde aquí 👇
    *Haz clic en los enlaces de la navegación para acceder directamente a cada estudio*
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Métricas de Recursos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Costo Total Estimado",
            format_cost(metrics.get('total_cost', 0))
        )
        st.metric(
            "Total de CPU",
            format_resource(metrics.get('total_cpu_seconds', 0), "vCPU-s")
        )
    
    with col2:
        st.metric(
            "Memoria Total",
            format_resource(metrics.get('total_memory_gib_seconds', 0), "GiB-s")
        )
        st.metric(
            "Solicitudes Totales",
            str(metrics.get('total_requests', 0))
        )
    
    if st.checkbox("Mostrar detalles de costos", value=False):
        st.markdown("#### Desglose de Costos")
        st.markdown(f"""
        - Costo promedio por solicitud: {format_cost(metrics.get('average_cost_per_request', 0))}
        - Última actualización: {metrics.get('last_updated', 'No disponible')}
        """)
        
        # Proyección a GCP
        st.markdown("#### Proyección GCP")
        monthly_requests = metrics.get('total_requests', 0) * 30  # estimación mensual
        st.markdown(f"""
        Uso mensual estimado:
        - Solicitudes: {monthly_requests:,}
        - % del límite gratuito: {(monthly_requests / 2_000_000) * 100:.2f}%
        """)
    
    st.markdown("### ℹ️ Información de Optimización")
    st.markdown("""
    Esta versión de la aplicación utiliza:
    - Preprocesamiento de datos
    - Caché optimizado
    - Monitoreo de recursos
    - Simulación de costos GCP
    """)

# Sección de habilidades técnicas
st.markdown("---")
st.header("🛠️ Habilidades técnicas y enfoque profesional")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tecnologías y habilidades")
    st.markdown("""
    Este portafolio demuestra mi experiencia con las siguientes tecnologías:
    
    - **Python**: 5+ años de experiencia con análisis y visualización de datos
    - **Frameworks**: Streamlit, Pandas, NumPy, Matplotlib, Plotly, Scikit-learn
    - **Cloud**: Google Cloud Platform (optimizado para la capa gratuita)
    - **Bases de datos**: BigQuery, SQL, procesamiento eficiente de datos
    - **Optimización**: Técnicas de preprocesamiento, caché, y monitoreo de recursos
    """)
    
    # Mostrar barras de habilidades
    st.markdown("### Nivel de experiencia")
    
    for skill, level in [
        ("Python", 0.92), 
        ("Análisis de datos", 0.88), 
        ("Streamlit", 0.85),
        ("GCP", 0.75), 
        ("Visualización", 0.90)
    ]:
        st.markdown(f"**{skill}**")
        st.progress(level)

with col2:
    st.subheader("Enfoque profesional")
    st.markdown("""
    Mi aproximación al análisis de datos se caracteriza por:
    
    - **Basado en evidencia**: Conclusiones extraídas directamente de los datos, 
      minimizando sesgos personales.
      
    - **Costo-eficiente**: Desarrollo optimizado para operar en capas gratuitas 
      de servicios cloud, demostrando eficiencia técnica y económica.
      
    - **Datos reales**: Trabajo con datasets del mundo real para proporcionar 
      análisis con aplicaciones prácticas y relevantes.
      
    - **Comunicación clara**: Transformación de análisis técnicos complejos 
      en visualizaciones y conclusiones comprensibles.
    """)
    
    # Call to action
    st.info("""
    **¿Por qué elegir este enfoque?**
    
    La combinación de análisis de datos riguroso con optimización de recursos demuestra
    mi capacidad para entregar valor analítico sin generar costos excesivos - una habilidad
    esencial en empresas de cualquier tamaño que buscan maximizar el retorno de sus
    inversiones en análisis de datos.
    """)

# Footer
st.markdown("---")
st.markdown("""
💡 *Los datos mostrados son preprocesados para optimizar el rendimiento y reducir costos. 
Todos los análisis se ejecutan con recursos optimizados para mantenerse dentro de la capa gratuita de GCP.*
""")

# Detener el monitoreo al finalizar
metrics = optimizer.stop_monitoring()

# Código para manejar la navegación entre páginas
if "page" in st.session_state:
    # Mostrar la página que el usuario quiere ver
    page_to_run = st.session_state["page"]
    
    # Intentar usar navegación directa una vez más
    try:
        # Intentar navegar directamente a la página
        if hasattr(st, 'switch_page'):
            st.switch_page(f"pages/{page_to_run}")
        else:
            # Si no está disponible, mostrar mensaje
            st.markdown("---")
            st.markdown("### 🔄 Navegación")
            st.markdown(f"**Para ver el análisis solicitado, ejecuta:**")
            st.code(f"streamlit run app/pages/{page_to_run}", language="bash")
            
            # Botones para acceso rápido a todas las páginas
            st.markdown("### 🚀 Acceso rápido a estudios")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏭 Emisiones CO2", use_container_width=True):
                    navigate_to_page("01_emisiones_co2.py")
                if st.button("👥 Demografía", use_container_width=True):
                    navigate_to_page("03_demografia_bigquery.py")
            with col2:
                if st.button("💧 Calidad Agua", use_container_width=True):
                    navigate_to_page("02_calidad_agua.py")
                if st.button("💰 Presupuesto", use_container_width=True):
                    navigate_to_page("04_presupuesto_publico.py")
    except Exception as e:
        st.error(f"Error al intentar navegar: {e}")
        st.info(f"Ejecuta este comando para ver el análisis: streamlit run app/pages/{page_to_run}")
    
    # Mantener el estado para que el usuario pueda verlo hasta que navegue
    # (no eliminamos st.session_state["page"] para que siga visible)

# Sección sobre transición profesional
st.markdown("---")
st.header("🌱 Mi Transición a la Industria de Datos")

st.markdown("""
### De otras industrias al análisis de datos

Mi trayectoria profesional no ha sido tradicional en la industria tecnológica. Durante años, he trabajado en otros 
sectores mientras desarrollaba paralelamente mis habilidades en análisis de datos y Python de forma autodidacta. 
**Nunca he trabajado en un entorno real de producción de datos**, pero he aplicado estos conocimientos en proyectos personales 
y en mi propio emprendimiento.

#### Mi objetivo actual:
Integrarme profesionalmente en la industria de los datos, aportando:

- Una **perspectiva multidisciplinaria** basada en mi experiencia en diferentes sectores
- **Habilidades técnicas sólidas** desarrolladas durante más de 5 años de aprendizaje autodidacta
- **Enfoque práctico** para resolver problemas del mundo real con datos
- **Optimización de recursos** para maximizar el valor mientras se minimizan los costos

Este portafolio es mi carta de presentación, demostrando que puedo analizar datos complejos, extraer insights valiosos 
y presentarlos de manera accesible y técnicamente eficiente.
""")

# Enlaces de contacto
cols = st.columns(4)
with cols[0]:
    st.button("📧 Contacto", key="contacto")
with cols[1]:
    st.button("🔗 LinkedIn", key="linkedin")
with cols[2]:
    st.button("💻 GitHub", key="github")
with cols[3]:
    st.button("📄 CV", key="cv")

# Footer final
st.markdown("---")
st.caption("Desarrollado con Python y Streamlit | Optimizado para la capa gratuita de GCP")
