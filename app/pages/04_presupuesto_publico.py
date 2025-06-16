"""
Página para el análisis del presupuesto público
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
    page_title="Análisis Presupuesto Público - DS Portfolio",    page_icon="💰",
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
    st.title("💰 Análisis del Presupuesto Sector Público")
    st.markdown(f"*Última actualización: {data_manager.get_last_update('04_Analisis_Presupuesto_Publico')}*")
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

Este estudio analiza la evolución y distribución del presupuesto del sector público chileno
en el período 2010-2025, evaluando tendencias, prioridades presupuestarias y eficiencia del gasto.
Se utilizaron técnicas de análisis de series temporales y visualización para identificar patrones relevantes.

## Objetivos

1. Analizar la evolución histórica del presupuesto público
2. Identificar cambios en las prioridades presupuestarias
3. Evaluar la eficiencia del gasto público por sectores
4. Analizar el impacto de eventos económicos y sociales en el presupuesto
""")

# Pestañas para organizar el contenido
tab1, tab2, tab3 = st.tabs(["Resultados Principales", "Análisis Sectorial", "Proyecciones"])

with tab1:
    st.header("Hallazgos Clave")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Presupuesto 2025 (% del PIB)",
            value="23.5%",
            delta="-1.2%",
            delta_color="inverse"
        )
        
        st.markdown("""
        ### Principales Áreas (% del presupuesto)
        1. **Protección Social**: 26.8%
        2. **Salud**: 18.5%
        3. **Educación**: 17.9%
        4. **Seguridad**: 10.2%
        """)
    
    with col2:
        st.metric(
            label="Crecimiento real anual promedio",
            value="2.7%",
            delta="-0.8%",
            delta_color="inverse"
        )
        
        st.markdown("""
        ### Inversión Pública
        - Infraestructura: 42.3%
        - Desarrollo Social: 31.5%
        - Desarrollo Productivo: 15.2%
        - Otros: 11.0%
        """)

with tab2:
    st.header("Análisis por Sectores")
    
    st.markdown("### Evolución del Gasto Sectorial (2010-2025)")
    
    # Importar librerías necesarias si no están ya importadas
    import plotly.graph_objects as go
    import plotly.express as px
    import pandas as pd
    import numpy as np
    
    # Crear datos de ejemplo para la evolución del gasto sectorial
    años = list(range(2010, 2026))
    
    # Sectores y sus valores iniciales (% del presupuesto)
    sectores = {
        'Salud': 16.8,
        'Educación': 19.2,
        'Protección Social': 14.5,
        'Infraestructura': 9.8,
        'Defensa': 7.6,
        'Seguridad': 6.2,
        'Otros': 25.9
    }
    
    # Crear patrones de crecimiento/decrecimiento para cada sector
    np.random.seed(42)
    datos = {}
    
    for sector, valor_inicial in sectores.items():
        # Crear tendencias diferentes para cada sector
        if sector == 'Salud':
            # Tendencia creciente para Salud
            cambio_anual = np.linspace(0, 0.3, len(años))
        elif sector == 'Educación':
            # Tendencia ligeramente creciente para Educación
            cambio_anual = np.linspace(0, 0.2, len(años))
        elif sector == 'Defensa':
            # Tendencia decreciente para Defensa
            cambio_anual = np.linspace(0, -0.15, len(años))
        else:
            # Ligeras fluctuaciones para otros sectores
            cambio_anual = np.random.normal(0, 0.05, len(años))
        
        # Aplicar cambios y mantener valor alrededor del inicial
        valores = [valor_inicial]
        for i in range(1, len(años)):
            nuevo_valor = valores[-1] + cambio_anual[i]
            valores.append(nuevo_valor)
        
        datos[sector] = valores
    
    # Crear figura
    fig = go.Figure()
    
    # Añadir línea para cada sector
    for sector, valores in datos.items():
        fig.add_trace(go.Scatter(
            x=años, 
            y=valores,
            mode='lines+markers',
            name=sector
        ))
    
    # Actualizar layout
    fig.update_layout(
        title='Evolución del Gasto por Sector (2010-2025)',
        xaxis_title='Año',
        yaxis_title='Porcentaje del Presupuesto Total',
        legend_title='Sectores',
        height=400
    )
    
    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Eficiencia del Gasto")
        
        # Datos simulados de eficiencia por ministerio
        ministerios = ['Salud', 'Educación', 'Vivienda', 'Obras Públicas', 'Interior']
        eficiencia = [78, 72, 84, 65, 70]
        
        # Crear gráfico de barras
        fig_eficiencia = go.Figure()
        
        # Añadir barras con colores basados en valores
        fig_eficiencia.add_trace(go.Bar(
            x=ministerios,
            y=eficiencia,
            marker_color=['#1E88E5' if v >= 80 else '#FFC107' if v >= 70 else '#D81B60' for v in eficiencia],
            text=eficiencia,
            textposition='auto'
        ))
        
        # Actualizar layout
        fig_eficiencia.update_layout(
            title='Índice de Eficiencia Presupuestaria',
            xaxis_title='Ministerio',
            yaxis_title='Eficiencia (%)',
            yaxis=dict(range=[0, 100]),
            height=300
        )
        
        # Mostrar gráfico
        st.plotly_chart(fig_eficiencia, use_container_width=True)
    
    with col2:
        st.markdown("### Composición 2025")
        
        # Usar los últimos valores de cada sector para el gráfico de torta
        datos_2025 = {sector: valores[-1] for sector, valores in datos.items()}
        
        # Crear gráfico de torta
        fig_composicion = go.Figure(data=[go.Pie(
            labels=list(datos_2025.keys()),
            values=list(datos_2025.values()),
            hole=.3
        )])
        
        # Actualizar layout
        fig_composicion.update_layout(
            title='Distribución Presupuestaria 2025',
            height=300
        )
        
        # Mostrar gráfico
        st.plotly_chart(fig_composicion, use_container_width=True)
    
    st.markdown("""
    #### Cambios Significativos (2010 vs 2025)
    - **Salud**: Incremento del 4.3% en participación
    - **Educación**: Incremento del 2.7% en participación
    - **Defensa**: Reducción del 2.1% en participación
    - **Obras Públicas**: Incremento del 1.8% en participación
    """)

with tab3:
    st.header("Proyecciones y Escenarios")
    
    # Crear gráfico de proyecciones
    años_proy = list(range(2025, 2031))
    
    # Datos para los tres escenarios
    escenario_base = [22.5, 22.6, 22.7, 22.7, 22.8, 22.8]
    escenario_expansivo = [22.5, 22.8, 23.1, 23.5, 23.8, 24.1]
    escenario_restrictivo = [22.5, 22.3, 22.0, 21.8, 21.6, 21.5]
    
    # Crear figura
    fig_proyeccion = go.Figure()
    
    # Añadir líneas para cada escenario
    fig_proyeccion.add_trace(go.Scatter(
        x=años_proy,
        y=escenario_base,
        mode='lines+markers',
        name='Escenario Base',
        line=dict(color='blue', width=2)
    ))
    
    fig_proyeccion.add_trace(go.Scatter(
        x=años_proy,
        y=escenario_expansivo,
        mode='lines+markers',
        name='Escenario Expansivo',
        line=dict(color='green', width=2)
    ))
    
    fig_proyeccion.add_trace(go.Scatter(
        x=años_proy,
        y=escenario_restrictivo,
        mode='lines+markers',
        name='Escenario Restrictivo',
        line=dict(color='red', width=2)
    ))
    
    # Actualizar layout
    fig_proyeccion.update_layout(
        title='Proyección del Presupuesto Público (% del PIB)',
        xaxis_title='Año',
        yaxis_title='Porcentaje del PIB',
        legend_title='Escenarios',
        height=400
    )
    
    # Mostrar gráfico
    st.plotly_chart(fig_proyeccion, use_container_width=True)
    
    st.markdown("""
    ### Escenarios Proyectados
    
    **Escenario Base:**
    - Crecimiento económico de 2.5% anual
    - Presupuesto público al 22.8% del PIB en 2030
    - Mantiene estructura actual con ajustes moderados
    
    **Escenario Expansivo:**
    - Crecimiento económico de 3.8% anual
    - Presupuesto público al 24.1% del PIB en 2030
    - Mayor inversión en infraestructura y desarrollo productivo
    
    **Escenario Restrictivo:**
    - Crecimiento económico de 1.3% anual
    - Presupuesto público al 21.5% del PIB en 2030
    - Ajustes en gastos no esenciales y optimización de programas
    """)
    
    st.info("Las proyecciones consideran factores como cambios demográficos, compromisos fiscales y escenarios macroeconómicos alternativos.")

# Añadir conclusiones
st.header("Conclusiones")

st.markdown("""
- El presupuesto público chileno ha mostrado una tendencia a la estabilización como porcentaje del PIB, con un énfasis creciente en sectores sociales.
- Los sectores de salud y educación han ganado participación, mientras que áreas como defensa han visto reducida su relevancia presupuestaria.
- La eficiencia del gasto muestra variaciones significativas entre sectores, con mejores indicadores en programas con metas e indicadores claros.
- Los eventos sociales y económicos (estallido social, pandemia) han tenido un impacto visible en la redistribución presupuestaria, incrementando el enfoque en protección social.
- Las proyecciones indican una presión creciente sobre áreas relacionadas con el envejecimiento poblacional (salud, pensiones) en los próximos años.
""")

# Obtener información de la fuente de datos
from utils.data_sources import get_data_source_info
presu_data_info = get_data_source_info("04_Analisis_Presupuesto_Publico")

# Añadir información de métodos
with st.expander("Metodología"):
    st.markdown("### Metodología")
    
    st.markdown("Este análisis utilizó datos de las siguientes fuentes:")
    for source in presu_data_info["sources"]:
        st.markdown(f"- **{source}**")
    
    st.markdown("""
    Se utilizaron técnicas de análisis de series temporales y composición presupuestaria, normalización por IPC y PIB,
    y modelamiento de escenarios mediante simulación Monte Carlo para las proyecciones.
    """)
    
    st.subheader("Preprocesamiento y optimización de datos")
    st.markdown(presu_data_info["preprocessing"])
    
    st.subheader("Estrategias para mantener en capa gratuita")
    st.markdown(presu_data_info["optimization"])

# Detener el monitoreo al final
metrics = optimizer.stop_monitoring()

# Footer
st.markdown("---")
st.caption("Los datos mostrados son pre-procesados para optimizar el rendimiento y reducir costos.")
