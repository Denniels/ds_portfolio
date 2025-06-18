"""
Página para el análisis demográfico de Chile
Integración completa con datos del notebook 03_Analisis_Demografia.ipynb
"""

import streamlit as st
import sys
from pathlib import Path
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

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

def load_demografia_data():
    """Cargar datos del análisis demográfico desde el archivo JSON generado por el notebook"""
    try:
        data_file = Path(__file__).parent.parent / 'data' / 'cache' / 'demografia_data.json'
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            st.error("❌ Archivo de datos no encontrado. Ejecute primero el notebook 03_Analisis_Demografia.ipynb")
            return None
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return None

# Iniciar monitoreo
optimizer = ResourceOptimizer()
optimizer.start_monitoring()

# Inicializar gestor de datos
data_manager = DataManager()

# Cargar datos del notebook
demo_data = load_demografia_data()

# Título y descripción
col1, col2 = st.columns([0.85, 0.15])
with col1:
    st.title("👥 Análisis Demográfico de Chile")
    if demo_data:
        fecha_actualizacion = demo_data['metadata']['fecha_actualizacion'][:10]
        st.markdown(f"*Última actualización: {fecha_actualizacion}*")
    else:
        st.markdown(f"*Última actualización: {data_manager.get_last_update('03_Analisis_Demografia')}*")
with col2:
    # Importar la función de navegación
    from utils.navigation import create_back_button
    create_back_button()

if demo_data is None:
    st.error("❌ No se pudieron cargar los datos del análisis demográfico.")
    st.info("💡 Para generar los datos, ejecute el notebook `03_Analisis_Demografia.ipynb` en el directorio `notebooks/`")
    st.stop()

# Extraer datos para facilitar el acceso
metadata = demo_data['metadata']
datos = demo_data['datos']
conclusiones = demo_data['conclusiones']

# Contenido principal
st.markdown(f"""
## 📊 Análisis Demográfico de Chile

### 🌍 Fuente de Datos
**{metadata['fuente_datos']}** - Período de análisis: **{metadata['periodo_analisis']}**

Este estudio analiza la evolución demográfica de Chile utilizando datos oficiales del Banco Mundial,
con respaldo de estadísticas del INE Chile. Se enfoca en tendencias poblacionales, crecimiento demográfico
y proyecciones futuras hasta 2030.

### 🎯 Objetivos del Análisis
1. **Analizar evolución poblacional** histórica de Chile (2010-2023)
2. **Identificar tendencias** de crecimiento demográfico
3. **Generar proyecciones** poblacionales hasta 2030
4. **Calcular métricas** de densidad poblacional y crecimiento
5. **Proporcionar insights** para planificación de políticas públicas
""")

# Pestañas para organizar el contenido
tab1, tab2, tab3, tab4 = st.tabs(["📊 Resultados Principales", "📈 Visualizaciones", "🔮 Proyecciones", "📋 Metodología"])

with tab1:
    st.header("🔍 Hallazgos Clave")
    
    # Métricas principales
    estadisticas = datos['estadisticas_resumen']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Población Actual",
            value=f"{estadisticas['poblacion_actual']:,}",
            help="Población total de Chile según el último año de datos disponibles"
        )
    
    with col2:
        st.metric(
            label="📈 Crecimiento Total",
            value=f"{estadisticas['crecimiento_porcentual']}%",
            help=f"Crecimiento poblacional total en el período {metadata['periodo_analisis']}"
        )
    
    with col3:
        st.metric(
            label="🏘️ Densidad Poblacional",
            value=f"{estadisticas['densidad_poblacional']} hab/km²",
            help="Habitantes por kilómetro cuadrado (área total de Chile: 756,102 km²)"
        )
    
    with col4:
        if 'modelo_estadisticas' in datos:
            r2_score = datos['modelo_estadisticas']['r2_score']
            st.metric(
                label="🎯 Precisión Modelo",
                value=f"{r2_score:.1%}",
                help="Coeficiente de determinación R² del modelo de proyección"
            )
    
    # Indicadores adicionales
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 **Indicadores Demográficos Clave**")
        
        crecimiento_absoluto = estadisticas['crecimiento_total_periodo']
        años_analisis = len(datos['poblacion_historica'])
        crecimiento_anual_promedio = crecimiento_absoluto / años_analisis
        
        st.markdown(f"""
        - **🌍 Fuente de datos**: {metadata['fuente_datos']}
        - **📅 Período analizado**: {metadata['periodo_analisis']}
        - **📊 Registros procesados**: {metadata['total_registros']} años
        - **👥 Crecimiento absoluto**: {crecimiento_absoluto:,} habitantes
        - **📈 Crecimiento anual promedio**: {crecimiento_anual_promedio:,.0f} habitantes/año
        - **🏘️ Superficie territorial**: 756,102 km²
        """)
    
    with col2:
        st.markdown("### 🔍 **Resumen Ejecutivo**")
        st.markdown(conclusiones['resumen_ejecutivo'])
        
        st.markdown("### 💡 **Principales Hallazgos**")
        for hallazgo in conclusiones['hallazgos_principales']:
            icono = "✅" if hallazgo['impacto'] == 'positivo' else "⚠️" if hallazgo['impacto'] == 'neutral' else "🔻"
            st.markdown(f"**{icono} {hallazgo['categoria']}**: {hallazgo['descripcion']}")

with tab2:
    st.header("📈 Visualizaciones Interactivas")
    
    # 1. Evolución poblacional histórica
    st.subheader("📊 Evolución de la Población Total")
    
    # Crear DataFrame para visualización
    df_poblacion = pd.DataFrame(datos['poblacion_historica'])
    
    fig_evolution = px.line(
        df_poblacion,
        x='año',
        y='poblacion_total',
        title='Evolución de la Población Total de Chile (2010-2023)',
        labels={
            'año': 'Año',
            'poblacion_total': 'Población Total (habitantes)'
        },
        markers=True
    )
    
    fig_evolution.update_traces(
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8, color='#ff7f0e')
    )
    
    fig_evolution.update_layout(
        height=500,
        yaxis=dict(tickformat=','),
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # 2. Análisis de crecimiento por quinquenios
    st.subheader("📊 Crecimiento por Períodos")
    
    # Calcular crecimiento por quinquenios
    quinquenios = [
        (2010, 2014, "2010-2014"),
        (2015, 2019, "2015-2019"), 
        (2020, 2023, "2020-2023")
    ]
    
    quinquenio_data = []
    for inicio, fin, label in quinquenios:
        data_periodo = df_poblacion[
            (df_poblacion['año'] >= inicio) & 
            (df_poblacion['año'] <= fin)
        ]
        
        if len(data_periodo) > 1:
            pob_inicio = data_periodo['poblacion_total'].iloc[0]
            pob_fin = data_periodo['poblacion_total'].iloc[-1]
            crecimiento = pob_fin - pob_inicio
            años = data_periodo['año'].iloc[-1] - data_periodo['año'].iloc[0]
            
            quinquenio_data.append({
                'periodo': label,
                'crecimiento_absoluto': crecimiento,
                'crecimiento_anual_promedio': crecimiento / años if años > 0 else 0
            })
    
    if quinquenio_data:
        df_quinquenios = pd.DataFrame(quinquenio_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_quinquenios = px.bar(
                df_quinquenios,
                x='periodo',
                y='crecimiento_absoluto',
                title='Crecimiento Poblacional por Períodos',
                labels={
                    'periodo': 'Período',
                    'crecimiento_absoluto': 'Crecimiento (habitantes)'
                },
                color='crecimiento_absoluto',
                color_continuous_scale='Viridis'
            )
            
            fig_quinquenios.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_quinquenios, use_container_width=True)
        
        with col2:
            fig_anual = px.bar(
                df_quinquenios,
                x='periodo',
                y='crecimiento_anual_promedio',
                title='Crecimiento Anual Promedio por Período',
                labels={
                    'periodo': 'Período',
                    'crecimiento_anual_promedio': 'Crecimiento Anual (hab/año)'
                },
                color='crecimiento_anual_promedio',
                color_continuous_scale='Blues'
            )
            
            fig_anual.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_anual, use_container_width=True)
    
    # 3. Comparación de densidad poblacional
    st.subheader("🌍 Comparación de Densidad Poblacional Regional")
    
    # Datos de referencia para contexto regional
    contexto_regional = {
        'Chile': estadisticas['densidad_poblacional'],
        'Argentina': 16.0,
        'Brasil': 25.0,
        'Uruguay': 19.8,
        'Perú': 25.0,
        'Colombia': 45.0
    }
    
    df_contexto = pd.DataFrame(
        list(contexto_regional.items()), 
        columns=['País', 'Densidad (hab/km²)']
    )
    
    fig_contexto = px.bar(
        df_contexto,
        x='País',
        y='Densidad (hab/km²)',
        title='Densidad Poblacional - Comparación Regional',
        color='Densidad (hab/km²)',
        color_continuous_scale='RdYlBu_r'
    )
    
    # Destacar Chile
    colors = ['red' if pais == 'Chile' else 'lightblue' for pais in df_contexto['País']]
    fig_contexto.update_traces(marker_color=colors)
    
    fig_contexto.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_contexto, use_container_width=True)

with tab3:
    st.header("🔮 Proyecciones Demográficas 2024-2030")
    
    if 'proyecciones' in datos:
        proyecciones = datos['proyecciones']
        
        # Combinar datos históricos y proyecciones
        df_historico = pd.DataFrame(datos['poblacion_historica'])
        df_proyecciones = pd.DataFrame(proyecciones)
        
        # Agregar tipo de dato
        df_historico['tipo'] = 'Histórico'
        df_proyecciones['tipo'] = 'Proyectado'
        df_proyecciones.rename(columns={'poblacion_proyectada': 'poblacion_total'}, inplace=True)
        
        # Combinar
        df_combined = pd.concat([
            df_historico[['año', 'poblacion_total', 'tipo']],
            df_proyecciones[['año', 'poblacion_total', 'tipo']]
        ], ignore_index=True)
        
        # Visualización histórico vs proyectado
        fig_projection = px.line(
            df_combined,
            x='año',
            y='poblacion_total',
            color='tipo',
            title='Evolución Histórica y Proyecciones Poblacionales (2010-2030)',
            labels={
                'año': 'Año',
                'poblacion_total': 'Población (habitantes)',
                'tipo': 'Tipo de Dato'
            },
            markers=True
        )
        
        # Personalizar colores
        colors = {'Histórico': '#1f77b4', 'Proyectado': '#ff7f0e'}
        for trace in fig_projection.data:
            trace.line.color = colors[trace.name]
            if trace.name == 'Proyectado':
                trace.line.dash = 'dash'
        
        # Línea vertical para separar histórico de proyectado
        fig_projection.add_vline(
            x=2023.5,
            line_dash="dot",
            line_color="gray",
            annotation_text="Inicio proyecciones"
        )
        
        fig_projection.update_layout(height=600, yaxis=dict(tickformat=','))
        st.plotly_chart(fig_projection, use_container_width=True)
        
        # Métricas de proyección
        col1, col2, col3 = st.columns(3)
        
        pob_2023 = df_historico['poblacion_total'].iloc[-1]
        pob_2030 = proyecciones[-1]['poblacion_proyectada']
        crecimiento_proyectado = pob_2030 - pob_2023
        crecimiento_porcentual_proj = (crecimiento_proyectado / pob_2023) * 100
        
        with col1:
            st.metric(
                label="👥 Población 2030",
                value=f"{pob_2030:,}",
                help="Población proyectada para el año 2030"
            )
        
        with col2:
            st.metric(
                label="📈 Crecimiento 2023-2030",
                value=f"{crecimiento_proyectado:,}",
                delta=f"{crecimiento_porcentual_proj:.1f}%",
                help="Crecimiento absoluto y porcentual proyectado"
            )
        
        with col3:
            crecimiento_anual_proj = crecimiento_proyectado / 7
            st.metric(
                label="📊 Crecimiento Anual Promedio",
                value=f"{crecimiento_anual_proj:,.0f}",
                help="Habitantes promedio por año (2023-2030)"
            )
        
        # Tabla de proyecciones
        st.subheader("📋 Tabla de Proyecciones Detalladas")
        
        df_proyecciones_display = pd.DataFrame(proyecciones)
        df_proyecciones_display['Población Proyectada'] = df_proyecciones_display['poblacion_proyectada'].apply(lambda x: f"{x:,}")
        df_proyecciones_display = df_proyecciones_display[['año', 'Población Proyectada']].rename(columns={'año': 'Año'})
        
        st.dataframe(df_proyecciones_display, use_container_width=True, hide_index=True)
        
        # Información del modelo
        if 'modelo_estadisticas' in datos:
            modelo_stats = datos['modelo_estadisticas']
            
            st.markdown("### 🎯 **Información del Modelo Predictivo**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                - **📊 Coeficiente R²**: {modelo_stats['r2_score']:.4f}
                - **📈 Pendiente**: {modelo_stats['pendiente']:,.0f} hab/año
                - **🎯 Precisión**: {'Excelente' if modelo_stats['r2_score'] > 0.95 else 'Buena' if modelo_stats['r2_score'] > 0.9 else 'Aceptable'}
                """)
            
            with col2:
                st.markdown(f"""
                - **🔧 Tipo de modelo**: Regresión lineal
                - **📅 Datos de entrenamiento**: {metadata['periodo_analisis']}
                - **🔮 Horizonte de proyección**: 2024-2030
                """)
    else:
        st.warning("⚠️ No hay datos de proyecciones disponibles. Ejecute el notebook completo para generar las proyecciones.")

with tab4:
    st.header("📋 Metodología y Fuentes de Datos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌍 **Fuentes de Datos Utilizadas**")
        st.markdown(f"""
        **Fuente Principal**: {metadata['fuente_datos']}
        - ✅ Datos oficiales sin credenciales requeridas
        - ✅ API REST estable y confiable
        - ✅ Cobertura internacional estándar
        - ✅ Datos actualizados regularmente
        
        **Período de análisis**: {metadata['periodo_analisis']}
        
        **Registros procesados**: {metadata['total_registros']} años de datos
        
        **Última actualización**: {metadata['fecha_actualizacion'][:10]}
        """)
        
        st.markdown("### 🔄 **Estrategia de Respaldo**")
        st.markdown("""
        1. **API del Banco Mundial** (primera opción)
        2. **Datos INE Chile** (respaldo confiable)
        3. **Datos de emergencia** (garantía mínima)
        
        Esta aproximación asegura que el análisis **siempre funcione**.
        """)
    
    with col2:
        st.markdown("### 🔬 **Metodología de Análisis**")
        st.markdown("""
        #### **1. Extracción de Datos**
        - Conexión automática con API del Banco Mundial
        - Validación de calidad y completitud
        - Respaldo automático si falla la conexión
        
        #### **2. Análisis Exploratorio**
        - Estadísticas descriptivas fundamentales
        - Identificación de tendencias temporales
        - Cálculo de métricas demográficas
        
        #### **3. Visualización**
        - Gráficos interactivos con Plotly
        - Análisis por períodos y quinquenios
        - Comparaciones regionales e internacionales
        
        #### **4. Modelado Predictivo**
        - Regresión lineal para proyecciones
        - Validación con métricas R²
        - Horizonte de 7 años (2024-2030)
        """)
        
        st.markdown("### 💡 **Ventajas de Esta Implementación**")
        st.markdown("""
        - 🔓 **Sin credenciales**: No requiere configuración compleja
        - ⚡ **Siempre funcional**: Múltiples niveles de respaldo
        - 📈 **Datos reales**: Fuentes oficiales cuando disponibles
        - ☁️ **Cloud-ready**: Compatible con Streamlit Community Cloud
        - 🧹 **Mantenible**: Código limpio y documentado
        """)
    
    # Recomendaciones
    st.markdown("---")
    st.markdown("### 📋 **Recomendaciones Basadas en el Análisis**")
    
    cols = st.columns(len(conclusiones['recomendaciones']))
    for i, recomendacion in enumerate(conclusiones['recomendaciones']):
        with cols[i]:
            st.info(f"💡 {recomendacion}")

# Footer con información técnica
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
📊 Análisis generado desde notebook: {metadata['notebook_origen']} | 
🌍 Fuente: {metadata['fuente_datos']} | 
📅 Última actualización: {metadata['fecha_actualizacion'][:10]}
</div>
""", unsafe_allow_html=True)

# Detener el monitoreo al final
metrics = optimizer.stop_monitoring()

# Importar componente de contacto
from utils.contact_components import add_page_footer, add_sidebar_contact

# Agregar enlaces de contacto en la barra lateral
add_sidebar_contact()

# Agregar footer al final de la página
add_page_footer()
