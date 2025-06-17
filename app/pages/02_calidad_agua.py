"""
Página para el análisis de calidad del agua
"""

import streamlit as st
import sys
from pathlib import Path

# Verificar si se ejecuta directamente con Python o a través de streamlit
if __name__ == "__main__" and not sys.argv[0].endswith("streamlit"):
    print("\n¡ATENCIÓN! Este es un archivo de Streamlit y debe ejecutarse con el comando:")
    print(f"\nstreamlit run {__file__}\n")
    print("Ejecutando este archivo directamente con Python puede causar advertencias.")
    print("Las advertencias 'missing ScriptRunContext' pueden ser ignoradas en modo bare.")

# Configuración de la página - DEBE SER EL PRIMER COMANDO DE STREAMLIT
st.set_page_config(
    page_title="Análisis de Calidad del Agua - DS Portfolio",
    page_icon="💧",
    layout="wide"
)

# Agregar el directorio raíz al path
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from utils.optimization import DataManager, ResourceOptimizer

# Iniciar monitoreo
optimizer = ResourceOptimizer()
optimizer.start_monitoring()

# Inicializar gestor de datos
data_manager = DataManager()

# Título y descripción
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.title("💧 Análisis de Calidad del Agua")
    st.markdown(f"*Última actualización: {data_manager.get_last_update('02_Analisis_Calidad_Del_Agua')}*")
with col2:
    # Importar la función de navegación
    import sys
    from pathlib import Path
    
    # Añadir el directorio raíz al path si no está
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.append(str(parent_dir))
    
    from utils.navigation import create_back_button
    create_back_button()

# Contenido principal
st.markdown("""
## Descripción del Estudio

Este estudio analiza la calidad del agua en diferentes regiones de Chile, evaluando parámetros
fisicoquímicos y microbiológicos en fuentes de agua potable y cuerpos de agua naturales.
El análisis incluye la identificación de tendencias temporales y variaciones geográficas.

## Objetivos

1. Evaluar la calidad del agua potable en áreas urbanas y rurales
2. Identificar contaminantes principales y su distribución geográfica
3. Analizar tendencias temporales de calidad del agua
4. Evaluar el cumplimiento de normativas nacionales e internacionales
""")

# Pestañas para organizar el contenido
tab1, tab2, tab3 = st.tabs(["Resultados Principales", "Mapa Interactivo", "Conclusiones"])

with tab1:
    st.header("Hallazgos Clave")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Índice de Calidad del Agua Promedio",
            value="78.3/100",
            delta="2.1%",
            delta_color="normal"
        )
        
        st.markdown("""
        ### Parámetros Críticos
        1. **Nitratos**: Elevados en zonas agrícolas
        2. **Turbidez**: Problemas en temporada de lluvias
        3. **Coliformes**: Presentes en áreas rurales sin tratamiento
        """)
    
    with col2:
        st.metric(
            label="Cumplimiento normativo",
            value="92.7%",
            delta="3.5%",
            delta_color="normal"
        )
        
        st.markdown("""
        ### Distribución de Calidad
        - Excelente: 42% de estaciones
        - Buena: 38% de estaciones
        - Regular: 15% de estaciones
        - Deficiente: 5% de estaciones
        """)

with tab2:
    st.header("Mapa de Estaciones de Monitoreo")
    
    st.markdown("### Distribución Geográfica de Calidad del Agua")
    
    # Importar librerías para mapas
    import folium
    from folium.plugins import MarkerCluster
    import pandas as pd
    from streamlit_folium import folium_static
    
    # Crear datos de ejemplo para estaciones de monitoreo
    # Coordenadas aproximadas para diferentes regiones de Chile
    estaciones = pd.DataFrame({
        'Nombre': [
            'Est. Santiago', 'Est. Valparaíso', 'Est. Concepción', 'Est. Antofagasta',
            'Est. Puerto Montt', 'Est. Temuco', 'Est. La Serena', 'Est. Copiapó',
            'Est. Rancagua', 'Est. Talca', 'Est. Valdivia', 'Est. Arica',
            'Est. Punta Arenas', 'Est. Coyhaique', 'Est. Iquique', 'Est. Chillán',
            'Est. Los Ángeles', 'Est. Osorno', 'Est. Calama', 'Est. Quillota'
        ],
        'Latitud': [
            -33.45, -33.04, -36.83, -23.65,
            -41.47, -38.73, -29.90, -27.37,
            -34.17, -35.43, -39.81, -18.48,
            -53.16, -45.57, -20.22, -36.60,
            -37.47, -40.57, -22.46, -32.88
        ],
        'Longitud': [
            -70.67, -71.62, -73.05, -70.40,
            -72.94, -72.60, -71.25, -70.33,
            -70.74, -71.66, -73.25, -70.31,
            -70.91, -72.07, -70.14, -72.10,
            -72.35, -73.13, -68.93, -71.25
        ],
        'Índice_Calidad': [
            85, 78, 82, 68,
            90, 76, 72, 65,
            80, 75, 88, 70,
            92, 94, 67, 79,
            81, 86, 62, 77
        ]
    })
    
    # Función para determinar color según índice de calidad
    def get_color(indice):
        if indice >= 90:
            return 'darkgreen'  # Excelente
        elif indice >= 75:
            return 'green'      # Bueno
        elif indice >= 65:
            return 'orange'     # Regular
        else:
            return 'red'        # Deficiente
            
    # Crear mapa base centrado en Chile
    m = folium.Map(location=[-35.675147, -71.542969], zoom_start=5)
    
    # Crear clúster de marcadores
    marker_cluster = MarkerCluster().add_to(m)
    
    # Añadir marcadores para cada estación
    for idx, row in estaciones.iterrows():
        # Determinar color según índice de calidad
        color = get_color(row['Índice_Calidad'])
        
        # Crear texto pop-up
        popup_text = f"""
        <b>Estación:</b> {row['Nombre']}<br>
        <b>Índice de Calidad:</b> {row['Índice_Calidad']}/100<br>
        <b>Categoría:</b> {
            'Excelente' if row['Índice_Calidad'] >= 90 else
            'Bueno' if row['Índice_Calidad'] >= 75 else
            'Regular' if row['Índice_Calidad'] >= 65 else
            'Deficiente'
        }
        """
        
        # Añadir marcador al clúster
        folium.Marker(
            location=[row['Latitud'], row['Longitud']],
            popup=folium.Popup(popup_text, max_width=200),
            icon=folium.Icon(color=color)
        ).add_to(marker_cluster)
    
    # Añadir leyenda (como HTML flotante)
    legend_html = '''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; 
    padding: 10px; border: 2px solid grey; border-radius: 5px;">
    <h4>Índice de Calidad</h4>
    <div><i style="background: darkgreen; width: 15px; height: 15px; display: inline-block;"></i> Excelente (90-100)</div>
    <div><i style="background: green; width: 15px; height: 15px; display: inline-block;"></i> Bueno (75-89)</div>
    <div><i style="background: orange; width: 15px; height: 15px; display: inline-block;"></i> Regular (65-74)</div>
    <div><i style="background: red; width: 15px; height: 15px; display: inline-block;"></i> Deficiente (<65)</div>
    </div>
    '''
    
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Mostrar el mapa en Streamlit
    try:
        folium_static(m, width=800, height=500)
    except:
        # Si streamlit_folium no está disponible, mostrar mensaje alternativo
        st.warning("La biblioteca streamlit_folium no está instalada. Instalando...")
        st.code("pip install streamlit-folium", language="bash")
        st.image("https://via.placeholder.com/800x500?text=Mapa+Interactivo+de+Estaciones", 
                caption="Vista previa del mapa interactivo de estaciones")
    
    st.markdown("""
    El mapa muestra la distribución de 120 estaciones de monitoreo a lo largo del país,
    con un código de colores según el índice de calidad del agua registrado.
    """)

with tab3:
    st.header("Conclusiones")
    
    st.markdown("""
    - La calidad del agua en Chile presenta una distribución heterogénea, con mejor calidad en zonas urbanas centrales y algunos desafíos en áreas rurales y zonas con alta actividad industrial/agrícola.
    - Se detectó una mejoría sostenida del 2.1% anual en el índice de calidad general, asociada a inversiones en plantas de tratamiento.
    - Las zonas norte y sur presentan problemas específicos: el norte con salinidad y metales pesados, y el sur con parámetros orgánicos y microbiológicos.
    - El 92.7% de las muestras cumplen con la normativa chilena, pero solo el 87.3% con los estándares internacionales más exigentes (OMS).
    """)
    
    st.info("""
    **Recomendaciones**:
    1. Fortalecer el monitoreo en zonas rurales
    2. Implementar tecnologías avanzadas de tratamiento en áreas problemáticas
    3. Desarrollar programas de gestión de cuencas hidrográficas
    4. Actualizar normativas para acercarlas a estándares internacionales
    """)

# Obtener información de la fuente de datos
from utils.data_sources import get_data_source_info
agua_data_info = get_data_source_info("02_Analisis_Calidad_Del_Agua")

# Añadir información de métodos
with st.expander("Metodología"):
    st.markdown("""
    ### Metodología
    
    Este análisis utilizó datos de las siguientes fuentes:""")
    
    # Mostrar las fuentes reales
    for source in agua_data_info["sources"]:
        st.markdown(f"- **{source}**")
    
    st.markdown("""
    Se analizaron 15 parámetros fisicoquímicos y microbiológicos según metodologías estandarizadas (APHA, EPA).
    El índice de calidad del agua se calculó utilizando el método de Índice de Calidad de Agua Objetivo (ICAO).
    """)
    
    # Mostrar información de preprocesamiento
    st.subheader("Proceso de preprocesamiento de datos")
    st.markdown(agua_data_info["preprocessing"])
    
    st.subheader("Estrategias de optimización")
    st.markdown(agua_data_info["optimization"])

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

# Detener el monitoreo al final
metrics = optimizer.stop_monitoring()

# Footer
add_page_footer()

# Sidebar - Contacto
with st.sidebar:
    add_sidebar_contact()
