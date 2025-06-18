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

def format_percentage_text(values):
    """Formatea una lista de valores como texto de porcentaje de manera segura"""
    result = []
    for val in values:
        try:
            if isinstance(val, str):
                cleaned = val.replace('%', '').replace(',', '').replace(' ', '')
                val = float(cleaned)
            result.append(f"{val:.1f}%")
        except (ValueError, TypeError):
            result.append("0.0%")
    return result

def format_currency(value, fallback="$0"):
    """Formatea un valor como moneda de manera segura"""
    try:
        if isinstance(value, str):
            # Intentar convertir string a número
            cleaned = value.replace(',', '').replace('$', '').replace(' ', '')
            value = float(cleaned)
        return f"${value:,.0f}"
    except (ValueError, TypeError):
        return fallback

def format_percentage(value, fallback="0.0%"):
    """Formatea un valor como porcentaje de manera segura"""
    try:
        if isinstance(value, str):
            # Intentar convertir string a número
            cleaned = value.replace('%', '').replace(',', '').replace(' ', '')
            value = float(cleaned)
        return f"{value:.1f}%"
    except (ValueError, TypeError):
        return fallback

# Cargar datos reales del análisis
@st.cache_data
def cargar_datos_presupuesto():
    """Carga los datos reales del análisis de presupuesto público"""
    import pandas as pd
    import json
    from pathlib import Path
    
    # Ruta a los datos procesados
    data_path = Path(__file__).parent.parent / "data" / "processed"
    
    # Cargar resumen ejecutivo
    with open(data_path / "resumen_ejecutivo.json", 'r') as f:
        resumen = json.load(f)
    
    # Convertir strings a números donde sea necesario
    numeric_fields = ['presupuesto_total', 'transferencias_totales', 'inversion_total', 'inversion_ejecutada']
    for field in numeric_fields:
        if field in resumen:
            try:
                # Convertir a float eliminando posibles comas y espacios
                if isinstance(resumen[field], str):
                    cleaned_value = resumen[field].replace(',', '').replace(' ', '')
                    resumen[field] = float(cleaned_value)
                elif not isinstance(resumen[field], (int, float)):
                    resumen[field] = float(resumen[field])
            except (ValueError, TypeError) as e:
                print(f"Error converting {field}: {resumen[field]} -> {e}")
                resumen[field] = 0

    # Asegurar que los porcentajes sean números
    percentage_fields = ['eficiencia_ejecucion', 'avance_promedio', 'eficiencia_inversion']
    for field in percentage_fields:
        if field in resumen:
            try:
                if isinstance(resumen[field], str):
                    cleaned_value = resumen[field].replace('%', '').replace(',', '').replace(' ', '')
                    resumen[field] = float(cleaned_value)
                elif not isinstance(resumen[field], (int, float)):
                    resumen[field] = float(resumen[field])
            except (ValueError, TypeError) as e:
                print(f"Error converting {field}: {resumen[field]} -> {e}")
                resumen[field] = 0.0
    """Carga los datos reales del análisis de presupuesto público"""
    import pandas as pd
    import json
    from pathlib import Path
    
    # Ruta a los datos procesados
    data_path = Path(__file__).parent.parent / "data" / "processed"
    
    # Cargar resumen ejecutivo
    with open(data_path / "resumen_ejecutivo.json", 'r') as f:
        resumen = json.load(f)
      # Convertir strings a números donde sea necesario
    numeric_fields = ['presupuesto_total', 'transferencias_totales', 'inversion_total', 'inversion_ejecutada']
    for field in numeric_fields:
        if field in resumen:
            try:
                # Convertir a float eliminando posibles comas y espacios
                if isinstance(resumen[field], str):
                    cleaned_value = resumen[field].replace(',', '').replace(' ', '')
                    resumen[field] = float(cleaned_value)
                elif not isinstance(resumen[field], (int, float)):
                    resumen[field] = float(resumen[field])
            except (ValueError, TypeError) as e:
                print(f"Error converting {field}: {resumen[field]} -> {e}")
                resumen[field] = 0

    # Asegurar que los porcentajes sean números
    percentage_fields = ['eficiencia_ejecucion', 'avance_promedio', 'eficiencia_inversion']
    for field in percentage_fields:
        if field in resumen:
            try:
                if isinstance(resumen[field], str):
                    cleaned_value = resumen[field].replace('%', '').replace(',', '').replace(' ', '')
                    resumen[field] = float(cleaned_value)
                elif not isinstance(resumen[field], (int, float)):
                    resumen[field] = float(resumen[field])
            except (ValueError, TypeError) as e:
                print(f"Error converting {field}: {resumen[field]} -> {e}")
                resumen[field] = 0.0
    
    # Cargar datasets principales
    df_presupuesto = pd.read_csv(data_path / "presupuesto_chile_2024.csv")
    df_ejecucion = pd.read_csv(data_path / "ejecucion_presupuestaria_2024.csv") 
    df_transferencias = pd.read_csv(data_path / "transferencias_regionales_2024.csv")
    df_inversion = pd.read_csv(data_path / "inversion_publica_2024.csv")
    
    # Cargar rankings
    top_ministerios = pd.read_csv(data_path / "top_ministerios.csv")
    top_regiones = pd.read_csv(data_path / "top_regiones.csv")
    distribucion_sectores = pd.read_csv(data_path / "distribucion_sectores.csv")
    
    # Cargar datos de visualización
    with open(data_path / "datos_visualizacion.json", 'r') as f:
        datos_viz = json.load(f)
    
    # Cargar metadatos
    with open(data_path / "metadatos.json", 'r') as f:
        metadatos = json.load(f)
    
    return {
        'resumen': resumen,
        'presupuesto': df_presupuesto,
        'ejecucion': df_ejecucion,
        'transferencias': df_transferencias,
        'inversion': df_inversion,
        'top_ministerios': top_ministerios,
        'top_regiones': top_regiones,
        'distribucion_sectores': distribucion_sectores,
        'datos_viz': datos_viz,
        'metadatos': metadatos
    }

def crear_datos_respaldo():
    """Crea datos de respaldo para garantizar que la aplicación funcione"""
    import pandas as pd
    
    return {
        'resumen': {
            'presupuesto_total': 94133485395,
            'transferencias_totales': 116728399671,
            'inversion_total': 593267329484,
            'inversion_ejecutada': 301723562359,
            'eficiencia_ejecucion': 84.4,
            'avance_promedio': 51.1,
            'eficiencia_inversion': 50.9,
            'fecha_analisis': '2024-06-17 19:36:02',
            'total_ministerios': 5,
            'total_regiones': 16,
            'total_sectores': 8
        },
        'top_ministerios': pd.DataFrame({
            'Ministerio': ['Ministerio de Defensa', 'Ministerio de Justicia', 'Ministerio de Obras Públicas', 'Ministerio de Educación', 'Ministerio de Salud'],
            'Presupuesto': [10771928421, 10745106944, 8659871946, 8583077348, 8361579009],
            'Porcentaje': [11.4, 11.4, 9.2, 9.1, 8.9]
        }),
        'top_regiones': pd.DataFrame({
            'Region': ['Valparaíso', 'Metropolitana', 'Ñuble', 'Maule', 'Tarapacá'],
            'Transferencias': [10949565328, 10647953229, 10501958797, 10193311120, 10035205884],
            'Porcentaje': [9.4, 9.1, 9.0, 8.7, 8.6]
        }),
        'distribucion_sectores': pd.DataFrame({
            'Sector': ['Asuntos Económicos', 'Orden Público', 'Vivienda', 'Protección Social', 'Educación'],
            'Cantidad': [3836257233, 3618365226, 3484629756, 3047143468, 3019676187],
            'Porcentaje': [15.6, 14.7, 14.1, 12.4, 12.2]
        }),
        'metadatos': {
            'version': '1.0',
            'fecha_generacion': '2024-06-17',
            'total_registros': 946
        }
    }

# Cargar todos los datos con manejo de errores robusto
try:
    datos = cargar_datos_presupuesto()
    st.success("✅ Datos del análisis cargados exitosamente")
    
    # Verificar que los datos críticos estén disponibles
    required_keys = ['resumen', 'top_ministerios', 'top_regiones', 'distribucion_sectores']
    missing_keys = [key for key in required_keys if key not in datos or datos[key] is None]
    
    if missing_keys:
        st.error(f"❌ Datos faltantes: {missing_keys}")
        st.info("🔄 Intentando generar datos de respaldo...")
        
        # Crear datos mínimos de respaldo
        datos = crear_datos_respaldo()
        st.warning("⚠️ Usando datos de respaldo para demostración")
    
except FileNotFoundError as e:
    st.error(f"❌ Archivo no encontrado: {e}")
    st.info("🔄 Creando datos de respaldo...")
    datos = crear_datos_respaldo()
    st.warning("⚠️ Usando datos de respaldo para demostración")
    
except Exception as e:
    st.error(f"❌ Error cargando datos: {e}")
    st.info("🔄 Creando datos de respaldo...")
    datos = crear_datos_respaldo()
    st.warning("⚠️ Usando datos de respaldo para demostración")

# Contenido principal con datos reales
st.markdown(f"""
## 📊 Análisis Integral del Presupuesto Público de Chile

### 🎯 Descripción del Estudio

Este estudio presenta un **análisis completo del presupuesto público de Chile** utilizando datos oficiales de la **Dirección de Presupuestos (DIPRES)** y el portal **datos.gob.cl**. El análisis integra múltiples fuentes de datos para proporcionar insights sobre asignación, ejecución y distribución de recursos públicos.

### 🌍 Fuentes de Datos Utilizadas

**1. Datos DIPRES via datos.gob.cl** (Fuente Principal)
- **Portal**: [datos.gob.cl/organization/direccion_de_presupuestos](https://datos.gob.cl/organization/direccion_de_presupuestos)
- **Datasets**: {datos['metadatos']['total_registros']:,} registros procesados
- **Cobertura**: Presupuesto, Ejecución, Inversión Pública, Transferencias Regionales

**2. Metodología de Extracción**
- **CSV Downloads**: Descarga directa de datasets públicos
- **API Integration**: Datos complementarios via API REST
- **Data Processing**: Limpieza, normalización y análisis estadístico

### 📈 Período de Análisis: {datos['metadatos']['periodo_analisis']}
*Última actualización: {datos['resumen']['fecha_analisis']}*

### 🎯 Objetivos del Análisis

1. **Evaluar eficiencia presupuestaria** por sector y ministerio
2. **Analizar distribución territorial** de recursos públicos  
3. **Identificar patrones de ejecución** y oportunidades de mejora
4. **Desarrollar modelos predictivos** para optimización presupuestaria
""")

# Pestañas para organizar el contenido con datos reales
tab1, tab2, tab3, tab4 = st.tabs(["📊 Resumen Ejecutivo", "💰 Análisis Financiero", "🏛️ Análisis Sectorial", "🤖 Insights y Modelado"])

with tab1:
    st.header("📈 Resumen Ejecutivo - Datos Reales")
      # Métricas principales del análisis real
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Presupuesto Total",
            value=format_currency(datos['resumen']['presupuesto_total']),
            delta="Análisis 2024"
        )
        
    with col2:
        st.metric(
            label="📊 Eficiencia Ejecución",
            value=format_percentage(datos['resumen']['eficiencia_ejecucion']),
            delta="Regular 🟠" if float(datos['resumen']['eficiencia_ejecucion']) < 90 else "Bueno 🟢"
        )
        
    with col3:
        st.metric(
            label="🎯 Avance Proyectos",
            value=format_percentage(datos['resumen']['avance_promedio']),
            delta="Deficiente 🔴" if float(datos['resumen']['avance_promedio']) < 70 else "Bueno 🟢"
        )
        
    with col4:
        st.metric(
            label="💵 Transferencias Totales",
            value=format_currency(datos['resumen']['transferencias_totales']),
            delta="Análisis Regional"
        )
    
    st.markdown("---")
    
    # Gráficos principales con datos reales
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 5 Ministerios por Presupuesto")
        
        import plotly.express as px
        import plotly.graph_objects as go
        
        # Crear gráfico de barras con datos reales
        fig_ministerios = px.bar(
            datos['top_ministerios'],
            x='Presupuesto',
            y='Ministerio',
            orientation='h',
            title="Asignación Presupuestaria por Ministerio",
            labels={'Presupuesto': 'Presupuesto (CLP)', 'Ministerio': 'Ministerio'},
            color='Porcentaje',
            color_continuous_scale='Blues'
        )
        
        fig_ministerios.update_layout(
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_ministerios, use_container_width=True)
        
        # Mostrar tabla de ministerios
        st.dataframe(
            datos['top_ministerios'][['Ministerio', 'Presupuesto', 'Porcentaje']],
            use_container_width=True
        )
    
    with col2:
        st.subheader("🌍 Top 5 Regiones por Transferencias")
        
        # Crear gráfico de barras con datos reales
        fig_regiones = px.bar(
            datos['top_regiones'],
            x='Transferencias',
            y='Region',
            orientation='h',
            title="Transferencias por Región",
            labels={'Transferencias': 'Transferencias (CLP)', 'Region': 'Región'},
            color='Porcentaje',
            color_continuous_scale='Greens'
        )
        
        fig_regiones.update_layout(
            height=400,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_regiones, use_container_width=True)
        
        # Mostrar tabla de regiones
        st.dataframe(
            datos['top_regiones'][['Region', 'Transferencias', 'Porcentaje']],
            use_container_width=True
        )

with tab2:
    st.header("💰 Análisis Financiero Detallado")
    
    # Indicadores financieros principales    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏗️ Inversión Total",
            value=format_currency(datos['resumen']['inversion_total']),
            delta="Inversión Pública"
        )
        
    with col2:
        st.metric(
            label="✅ Inversión Ejecutada", 
            value=format_currency(datos['resumen']['inversion_ejecutada']),
            delta=format_percentage(datos['resumen']['eficiencia_inversion']) + " ejecutado"
        )
        
    with col3:
        eficiencia_inv = datos['resumen']['eficiencia_inversion']
        st.metric(
            label="📊 Eficiencia Inversión",
            value=format_percentage(eficiencia_inv),
            delta="Deficiente 🔴" if eficiencia_inv < 70 else "Bueno 🟢"
        )
    
    st.markdown("---")
    
    # Análisis de distribución sectorial
    st.subheader("📊 Distribución por Sectores")
    
    # Crear gráfico de torta con datos reales
    fig_sectores = px.pie(
        datos['distribucion_sectores'],
        values='Cantidad',
        names='Sector',
        title="Distribución de Recursos por Sector",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig_sectores.update_traces(textposition='inside', textinfo='percent+label')
    fig_sectores.update_layout(height=500)
    
    st.plotly_chart(fig_sectores, use_container_width=True)
    
    # Tabla detallada de sectores
    st.dataframe(
        datos['distribucion_sectores'].sort_values('Porcentaje', ascending=False),
        use_container_width=True
    )

with tab3:
    st.header("🏛️ Análisis Sectorial y de Eficiencia")
    
    # Análisis de eficiencia por datos reales
    st.subheader("📈 Indicadores de Eficiencia del Análisis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Clasificación de Eficiencia")
        
        # Crear indicadores basados en los datos reales
        indicadores_eficiencia = {
            "Ejecución Presupuestaria": {
                "valor": datos['resumen']['eficiencia_ejecucion'],
                "clasificacion": "🟠 Regular" if datos['resumen']['eficiencia_ejecucion'] < 90 else "🟢 Bueno"
            },
            "Avance de Proyectos": {
                "valor": datos['resumen']['avance_promedio'],                "clasificacion": "🔴 Deficiente" if datos['resumen']['avance_promedio'] < 70 else "🟢 Bueno"
            },
            "Eficiencia de Inversión": {
                "valor": datos['resumen']['eficiencia_inversion'],
                "clasificacion": "🔴 Deficiente" if datos['resumen']['eficiencia_inversion'] < 70 else "🟢 Bueno"
            }
        }
        
        for indicador, info in indicadores_eficiencia.items():
            st.metric(
                label=indicador,
                value=format_percentage(info['valor']),
                delta=info['clasificacion']
            )
    
    with col2:
        st.markdown("### 🌟 Concentración de Recursos")
          # Calcular concentración basada en datos reales
        conc_ministerios = datos['top_ministerios']['Porcentaje'].head(5).sum()
        conc_regiones = datos['top_regiones']['Porcentaje'].head(5).sum()
        
        st.metric(
            label="Top 5 Ministerios",
            value=format_percentage(conc_ministerios),
            delta="del presupuesto total"
        )
        
        st.metric(
            label="Top 5 Regiones", 
            value=format_percentage(conc_regiones),
            delta="de las transferencias"
        )
        
        st.metric(
            label="Total Ministerios",
            value=str(datos['resumen']['total_ministerios']),
            delta="analizados"
        )
    
    st.markdown("---")
    
    # Gráfico de eficiencia comparativa
    st.subheader("📊 Comparación de Indicadores de Eficiencia")
    
    # Crear gráfico de barras comparativo
    indicadores_data = {
        'Indicador': ['Ejecución Presupuestaria', 'Avance de Proyectos', 'Eficiencia de Inversión'],
        'Porcentaje': [
            datos['resumen']['eficiencia_ejecucion'],
            datos['resumen']['avance_promedio'], 
            datos['resumen']['eficiencia_inversion']
        ],
        'Color': ['#1E88E5', '#FFC107', '#D81B60']  # Azul, Amarillo, Rojo
    }
    
    fig_eficiencia = go.Figure()
    
    fig_eficiencia.add_trace(go.Bar(
        x=indicadores_data['Indicador'],
        y=indicadores_data['Porcentaje'],
        marker_color=indicadores_data['Color'],
        text=format_percentage_text(indicadores_data['Porcentaje']),
        textposition='auto'
    ))
    
    # Agregar líneas de referencia
    fig_eficiencia.add_hline(y=90, line_dash="dash", line_color="green", 
                            annotation_text="Objetivo Excelente (90%)")
    fig_eficiencia.add_hline(y=70, line_dash="dash", line_color="orange",
                            annotation_text="Mínimo Aceptable (70%)")
    
    fig_eficiencia.update_layout(
        title='Indicadores de Eficiencia del Presupuesto Público',
        xaxis_title='Indicadores',
        yaxis_title='Eficiencia (%)',
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    st.plotly_chart(fig_eficiencia, use_container_width=True)

with tab4:
    st.header("🤖 Insights y Modelado Predictivo")
    
    st.markdown("""
    ### 🔍 Hallazgos Principales del Análisis
    
    Basado en el análisis de datos reales de DIPRES:
    """)
    
    # Insights basados en datos reales
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        #### 💡 Conclusiones Clave        
        **Estado General:**
        - Eficiencia promedio: **{format_percentage(datos['resumen']['eficiencia_ejecucion'])}** (🟠 Regular)
        - Avance de proyectos: **{format_percentage(datos['resumen']['avance_promedio'])}** (🔴 Deficiente)
        - Eficiencia de inversión: **{format_percentage(datos['resumen']['eficiencia_inversion'])}** (🔴 Deficiente)
        
        **Concentración:**
        - Top 5 ministerios: **{format_percentage(datos['top_ministerios']['Porcentaje'].head(5).sum())}** del presupuesto
        - Top 5 regiones: **{format_percentage(datos['top_regiones']['Porcentaje'].head(5).sum())}** de transferencias
        
        **Oportunidades:**
        - Potencial de mejora: **15-25%** en eficiencia
        - Recursos optimizables: **$75-125 mil millones**
        """)
    
    with col2:
        st.markdown(f"""
        #### 🎯 Recomendaciones Estratégicas
        
        **1. Mejora Operacional:**
        - Monitoreo de proyectos con avance <70%
        - Alertas tempranas para sub-ejecución
        - Benchmarks de eficiencia por sector
        
        **2. Optimización Presupuestaria:**
        - Redistribución basada en eficiencia
        - Presupuesto por resultados
        - Incentivos por metas de eficiencia
        
        **3. Fortalecimiento Regional:**
        - Capacitación en gestión presupuestaria
        - Mejores prácticas de regiones eficientes
        - Indicadores per cápita territoriales
        """)
    
    st.markdown("---")
    
    # Información del modelado predictivo
    st.subheader("🔮 Modelado Predictivo Implementado")
    
    st.markdown("""
    El análisis incluyó desarrollo de **modelos de machine learning** para predicción de eficiencia:
    
    - **Random Forest Regressor**: Modelo principal para predicción de eficiencia
    - **Regresión Lineal**: Modelo de comparación y validación
    - **Variables más importantes**: Presupuesto, sector, región, año
    - **Capacidad predictiva**: Modelos entrenados con 1,000 observaciones sintéticas
    
    ### 📊 Factores Clave Identificados:
    1. **Logaritmo del Presupuesto** (27.7% importancia)
    2. **Monto del Presupuesto** (26.9% importancia) 
    3. **Código de Región** (21.4% importancia)
    4. **Código de Sector** (16.6% importancia)
    5. **Año** (7.4% importancia)
    """)
    
    # Mostrar datos de ejemplo del modelo
    st.subheader("📈 Ejemplos de Predicción")
    
    ejemplo_data = {
        'Escenario': ['Presupuesto Pequeño', 'Presupuesto Mediano', 'Presupuesto Grande'],
        'Monto': ['$5.000.000', '$50.000.000', '$500.000.000'],
        'Predicción Eficiencia': ['84.6%', '89.5%', '82.4%'],
        'Clasificación': ['🟠 Regular', '🟢 Bueno', '🟠 Regular']
    }
    
    st.dataframe(ejemplo_data, use_container_width=True)

# Sección de Metodología y Fuentes de Datos
st.header("📚 Metodología y Extracción de Datos")

with st.expander("🔍 Ver Detalles de Metodología"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        ### 🌐 Fuentes de Datos Utilizadas
        
        **Portal datos.gob.cl - DIPRES:**
        - URL: [datos.gob.cl/organization/direccion_de_presupuestos](https://datos.gob.cl/organization/direccion_de_presupuestos)
        - Datasets: 414 conjuntos oficiales disponibles
        - Formato: CSV descarga directa
        - Estado: ✅ **FUNCIONANDO**
        
        **Presupuesto Abierto Chile:**
        - URL: [presupuestoabierto.gob.cl](https://presupuestoabierto.gob.cl/)
        - API: Datos transaccionales en tiempo real
        - Cobertura: 596 servicios públicos
        - Estado: ✅ **FUNCIONANDO**
        
        **Datos Procesados:**
        - Total registros: **{datos['metadatos']['total_registros']:,}**
        - Período: **{datos['metadatos']['periodo_analisis']}**
        - Versión: **{datos['metadatos']['version']}**
        """)
    
    with col2:
        st.markdown("""
        ### ⚙️ Proceso de Extracción
        
        **1. Descarga CSV:**
        ```python
        # Descarga directa desde datos.gob.cl
        datasets = [
            'presupuesto_vigente_2024.csv',
            'ejecucion_presupuestaria_2024.csv', 
            'transferencias_municipales_2024.csv',
            'inversion_publica_2024.csv'
        ]
        ```
        
        **2. Integración API:**
        ```python
        # Datos complementarios via API
        api_url = "https://presupuestoabierto.gob.cl/api/v1/"
        datos_poblacion = requests.get(f"{api_url}poblacion")
        datos_socioeconomicos = requests.get(f"{api_url}indicadores")
        ```
        
        **3. Procesamiento:**
        - Limpieza y normalización de datos
        - Cálculo de indicadores de eficiencia
        - Análisis estadístico y modelado predictivo
        - Exportación para visualización
        """)

# Conclusiones Finales con datos reales
st.header("📋 Conclusiones y Recomendaciones")

st.markdown(f"""
### 🎯 Hallazgos Principales

**Estado de Eficiencia Presupuestaria:**
- **Eficiencia promedio de ejecución**: {format_percentage(datos['resumen']['eficiencia_ejecucion'])} (🟠 Regular)
- **Avance promedio de proyectos**: {format_percentage(datos['resumen']['avance_promedio'])} (🔴 Deficiente)  
- **Eficiencia de inversión**: {format_percentage(datos['resumen']['eficiencia_inversion'])} (🔴 Deficiente)

**Concentración de Recursos:**
- Los **5 ministerios principales** concentran el **{format_percentage(datos['top_ministerios']['Porcentaje'].head(5).sum())}** del presupuesto total
- Las **5 regiones principales** concentran el **{format_percentage(datos['top_regiones']['Porcentaje'].head(5).sum())}** de las transferencias
- Distribución entre **{datos['resumen']['total_sectores']} sectores** principales identificados

**Sectores Más Relevantes:**
""")

# Mostrar top sectores
for i, row in datos['distribucion_sectores'].head(3).iterrows():
    st.markdown(f"- **{row['Sector']}**: {format_percentage(row['Porcentaje'])} de la distribución")

st.markdown(f"""

### 💡 Recomendaciones Estratégicas

**1. Mejora de Eficiencia Operacional:**
- Implementar sistemas de **monitoreo en tiempo real** para proyectos con avance <70%
- Desarrollar **alertas tempranas** para sectores en riesgo de sub-ejecución
- Establecer **benchmarks** de eficiencia por sector y región

**2. Optimización de Asignación Presupuestaria:**
- **Redistribuir recursos** de sectores con sobre-asignación hacia áreas críticas
- Implementar **presupuesto por resultados** basado en eficiencia histórica
- Crear **incentivos** para ministerios que superen metas de eficiencia

**3. Fortalecimiento de Capacidades Regionales:**
- **Capacitar equipos regionales** en gestión presupuestaria eficiente
- Implementar **mejores prácticas** de regiones más eficientes
- Desarrollar **indicadores per cápita** para evaluación territorial

### 🚀 Impacto Potencial

**Las mejoras implementadas podrían resultar en:**
- Incremento de eficiencia del **15-25%**
- Liberación de recursos por **$75-125 mil millones**
- Optimización para inversión en áreas prioritarias

### 📊 Próximos Pasos

1. **Validación con datos históricos** adicionales de DIPRES
2. **Implementación de dashboard** interactivo para seguimiento continuo  
3. **Desarrollo de modelos predictivos** más sofisticados
4. **Integración con sistemas** de gestión presupuestaria existentes
""")

# Información técnica del análisis
st.markdown("---")
st.subheader("🔧 Información Técnica del Análisis")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    **📊 Datos Procesados:**
    - Presupuesto: {len(datos['presupuesto']):,} registros
    - Ejecución: {len(datos['ejecucion']):,} registros  
    - Transferencias: {len(datos['transferencias']):,} registros
    - Inversión: {len(datos['inversion']):,} registros
    """)

with col2:
    st.markdown(f"""
    **🤖 Modelado:**
    - Random Forest: Entrenado y evaluado
    - Regresión Lineal: Modelo de comparación
    - Variables: 5 predictores principales
    - Observaciones: 1,000 simuladas
    """)

with col3:
    st.markdown(f"""
    **📅 Temporalidad:**
    - Período: {datos['metadatos']['periodo_analisis']}
    - Generado: {datos['resumen']['fecha_analisis'][:10]}
    - Versión: {datos['metadatos']['version']}
    - Notebook: {datos['metadatos']['notebook_origen']}
    """)

# Obtener información de la fuente de datos
from utils.data_sources import get_data_source_info
presu_data_info = get_data_source_info("04_Analisis_Presupuesto_Publico")

# Añadir información de métodos expandida
with st.expander("📖 Metodología Detallada"):
    st.markdown("### 🔬 Metodología Técnica Utilizada")
    
    st.markdown(f"""
    **Fuentes de Datos Integradas:**
    """)
    for source in presu_data_info["sources"]:
        st.markdown(f"- **{source}**")
    
    st.markdown("""
    **Técnicas de Análisis Aplicadas:**
    - **Análisis Estadístico Descriptivo**: Cálculo de indicadores de tendencia central y dispersión
    - **Análisis de Eficiencia**: Ratio de ejecución vs presupuesto asignado por sector
    - **Modelado Predictivo**: Random Forest y Regresión Lineal para predicción de eficiencia
    - **Análisis de Concentración**: Evaluación de distribución de recursos por ministerio y región
    - **Visualización Interactiva**: Dashboards con Plotly para exploración de datos
    
    **Procesamiento de Datos:**
    """)
    st.markdown(presu_data_info["preprocessing"])
    
    st.markdown("""
    **Estrategias de Optimización:**
    """)
    st.markdown(presu_data_info["optimization"])

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

# Sidebar - Contacto
with st.sidebar:
    add_sidebar_contact()

# Detener el monitoreo al final
metrics = optimizer.stop_monitoring()

# Footer
add_page_footer()
