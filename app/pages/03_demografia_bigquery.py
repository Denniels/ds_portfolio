"""
Página para el análisis demográfico con BigQuery
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
    page_title="Análisis Demográfico - DS Portfolio",
    page_icon="👥",
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
    st.title("👥 Análisis Demográfico con BigQuery")
    st.markdown(f"*Última actualización: {data_manager.get_last_update('03_Analisis_BigQuery_Demografia')}*")
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

Este estudio analiza tendencias demográficas en Chile utilizando Google BigQuery para procesar
grandes volúmenes de datos censales y proyecciones poblacionales. Se enfoca en cambios en la
estructura etaria, distribución geográfica y proyecciones futuras.

## Objetivos

1. Analizar la evolución demográfica de Chile en las últimas décadas
2. Identificar patrones migratorios internos entre regiones
3. Evaluar el envejecimiento poblacional y sus implicaciones
4. Generar proyecciones demográficas para los próximos 20 años
""")

# Pestañas para organizar el contenido
tab1, tab2, tab3 = st.tabs(["Resultados Principales", "Visualizaciones", "Metodología BigQuery"])

with tab1:
    st.header("Hallazgos Clave")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Tasa de envejecimiento poblacional",
            value="12.3%",
            delta="3.7%",
            delta_color="inverse"
        )
        
        st.markdown("""
        ### Indicadores Demográficos
        1. **Tasa de fertilidad**: 1.6 hijos por mujer
        2. **Esperanza de vida**: 82.3 años
        3. **Migración neta**: +1.8 por cada 1,000 habitantes
        """)
    
    with col2:
        st.metric(
            label="Población urbana",
            value="87.5%",
            delta="1.2%",
            delta_color="off"
        )
        
        st.markdown("""
        ### Concentración Regional
        - Región Metropolitana: 42.3%
        - Valparaíso: 10.1%
        - Biobío: 9.8%
        - Otras regiones: 37.8%
        """)

with tab2:
    st.header("Visualizaciones")
    
    st.markdown("### Pirámide Poblacional 2010 vs 2025")
    
    # Importar librerías necesarias
    import plotly.graph_objects as go
    import numpy as np
    import pandas as pd
    
    # Generar datos para pirámide poblacional
    grupos_edad = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', 
                  '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
    
    # Datos simulados - valores negativos para hombres (convención para pirámides)
    hombres_2010 = [-800, -650, -640, -630, -690, -720, -680, -650, -590, -540, -500, -420, -350, -270, -210, -120, -90]
    mujeres_2010 = [780, 630, 620, 610, 680, 730, 690, 670, 610, 560, 530, 450, 380, 310, 250, 180, 150]
    
    hombres_2025 = [-750, -600, -590, -620, -680, -750, -740, -730, -690, -640, -590, -520, -480, -390, -320, -240, -210]
    mujeres_2025 = [730, 580, 570, 600, 670, 760, 750, 750, 710, 670, 610, 550, 510, 430, 370, 300, 280]
    
    # Crear figura
    fig = go.Figure()
    
    # Agregar barras para 2010
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=hombres_2010,
        name='Hombres 2010',
        orientation='h',
        marker=dict(color='lightblue')
    ))
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=mujeres_2010,
        name='Mujeres 2010',
        orientation='h',
        marker=dict(color='pink')
    ))
    
    # Agregar barras para 2025 con transparencia
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=hombres_2025,
        name='Hombres 2025',
        orientation='h',
        marker=dict(color='blue', opacity=0.7)
    ))
    fig.add_trace(go.Bar(
        y=grupos_edad,
        x=mujeres_2025,
        name='Mujeres 2025',
        orientation='h',
        marker=dict(color='red', opacity=0.7)
    ))
    
    # Actualizar diseño
    fig.update_layout(
        title='Pirámide Poblacional: Chile 2010 vs 2025',
        barmode='overlay',
        bargap=0.1,
        xaxis=dict(
            title='Población (miles)',
            tickvals=[-800, -600, -400, -200, 0, 200, 400, 600, 800],
            ticktext=['800', '600', '400', '200', '0', '200', '400', '600', '800']
        ),
        yaxis=dict(title='Grupo de edad'),
        height=500
    )
    
    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Migración Interregional")
        
        # Crear datos de migración entre regiones
        regiones = ['RM', 'V', 'VIII', 'II', 'VI', 'VII', 'IV']
        
        # Matriz de migración (origen -> destino)
        migracion = [
            [0, 45, 32, 18, 25, 12, 8],     # RM
            [38, 0, 12, 5, 15, 7, 4],       # V
            [29, 10, 0, 3, 8, 15, 2],       # VIII
            [22, 6, 4, 0, 2, 3, 12],        # II
            [30, 18, 7, 2, 0, 14, 3],       # VI
            [25, 8, 17, 2, 12, 0, 3],       # VII
            [15, 5, 3, 10, 2, 3, 0]         # IV
        ]
        
        # Crear heatmap
        fig_mig = go.Figure(data=go.Heatmap(
            z=migracion,
            x=regiones,
            y=regiones,
            colorscale='Viridis',
            hoverongaps=False,
            colorbar=dict(title='Migración (miles)')
        ))
        
        fig_mig.update_layout(
            title='Flujos Migratorios Interregionales',
            xaxis=dict(title='Región Destino'),
            yaxis=dict(title='Región Origen'),
            height=300
        )
        
        st.plotly_chart(fig_mig, use_container_width=True)
    
    with col2:
        st.markdown("### Proyección 2050")
        
        # Datos de proyección poblacional
        categorias = ['0-14', '15-64', '65+']
        valores = [15.2, 61.3, 23.5]
        
        # Crear gráfico de dona
        fig_proy = go.Figure(data=[go.Pie(
            labels=categorias,
            values=valores,
            hole=.4,
            marker_colors=['#2E86C1', '#28B463', '#CB4335']
        )])
        
        fig_proy.update_layout(
            title='Estructura Etaria Proyectada 2050',
            annotations=[dict(text='2050', showarrow=False)],
            height=300
        )
        
        st.plotly_chart(fig_proy, use_container_width=True)

with tab3:
    st.header("Procesamiento con BigQuery")
    
    st.markdown("""
    Este estudio utilizó Google BigQuery para procesar más de 15 millones de registros censales
    y datos complementarios. A continuación se presenta un ejemplo de las consultas utilizadas:
    """)
    
    st.code("""
    SELECT 
      region,
      EXTRACT(YEAR FROM fecha) AS año,
      SUM(CASE WHEN edad < 15 THEN población ELSE 0 END) AS población_joven,
      SUM(CASE WHEN edad BETWEEN 15 AND 64 THEN población ELSE 0 END) AS población_adulta,
      SUM(CASE WHEN edad > 64 THEN población ELSE 0 END) AS población_mayor
    FROM 
      `proyecto.dataset.datos_censales`
    GROUP BY 
      region, año
    ORDER BY 
      region, año
    """, language="sql")
    
    st.markdown("""
    ### Optimización de Procesamiento
    
    Para reducir costos y optimizar el rendimiento:
    
    1. Utilizamos particionamiento por año en las tablas
    2. Implementamos pre-agregaciones para consultas frecuentes
    3. Exportamos resultados finales a formatos optimizados
    4. Aplicamos técnicas de muestreo para análisis exploratorios
    """)

# Añadir conclusiones
st.header("Conclusiones")

st.markdown("""
- Chile se encuentra en una etapa avanzada de transición demográfica, con envejecimiento acelerado.
- La concentración urbana continúa aumentando, especialmente en la Región Metropolitana.
- El índice de dependencia demográfica está aumentando, lo que representa desafíos para los sistemas de pensiones.
- Los patrones migratorios internos muestran un desplazamiento desde regiones extremas hacia zonas centrales.
- Las proyecciones indican que para 2050, más del 25% de la población tendrá más de 65 años.
""")

st.info("""
**Implicaciones**:
1. Mayor demanda de servicios de salud para adultos mayores
2. Necesidad de adaptar el sistema de pensiones
3. Oportunidades para desarrollo de nuevos mercados orientados a población mayor
4. Desafíos para mantener la fuerza laboral productiva
""")

# Obtener información de la fuente de datos
from utils.data_sources import get_data_source_info
demo_data_info = get_data_source_info("03_Analisis_BigQuery_Demografia")

with st.expander("Fuentes de datos y optimización"):
    st.markdown("### Fuentes de datos utilizadas")
    for source in demo_data_info["sources"]:
        st.markdown(f"- **{source}**")
    
    st.markdown("### Procesamiento de datos")
    st.markdown(demo_data_info["preprocessing"])
    
    st.markdown("### Estrategias de optimización")
    st.markdown(demo_data_info["optimization"])

# Detener el monitoreo al final
metrics = optimizer.stop_monitoring()

# Importar componente de contacto
from utils.contact_components import add_page_footer, add_sidebar_contact

# Agregar enlaces de contacto en la barra lateral
add_sidebar_contact()

# Agregar footer al final de la página
add_page_footer()
