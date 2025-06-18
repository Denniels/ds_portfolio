"""
MVP - Generador de Reportes Automáticos
Página dedicada del primer producto comercial
"""
import streamlit as st
import pandas as pd
import json
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import base64
from pathlib import Path
import sys

# Configuración de la página
st.set_page_config(
    page_title="Generador de Reportes Automáticos - MVP",
    page_icon="🤖",
    layout="wide"
)

# Cargar estilos CSS
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from utils.css_loader import load_css_styles
load_css_styles()

# Importar componente de contacto
try:
    from utils.contact_components import add_page_footer, add_sidebar_contact
except ImportError:
    def add_page_footer():
        st.markdown("---")
        st.markdown("© 2025 DS Portfolio")
    def add_sidebar_contact():
        st.sidebar.markdown("---")

# Importar conectores de API
try:
    from utils.api_connectors import APIConnector, DataValidator, ReportTemplates
except ImportError:
    st.warning("⚠️ Módulo de conectores API no disponible. Funcionalidad limitada.")
    APIConnector = None
    DataValidator = None
    ReportTemplates = None

class DataIngestionManager:
    """Maneja la ingesta de datos desde múltiples fuentes"""
    
    @staticmethod
    def load_csv_data(uploaded_file):
        """Carga datos desde archivo CSV"""
        try:
            df = pd.read_csv(uploaded_file)
            return df, "✅ CSV cargado exitosamente"
        except Exception as e:
            return None, f"❌ Error cargando CSV: {str(e)}"
    
    @staticmethod
    def load_excel_data(uploaded_file):
        """Carga datos desde archivo Excel"""
        try:
            df = pd.read_excel(uploaded_file)
            return df, "✅ Excel cargado exitosamente"
        except Exception as e:
            return None, f"❌ Error cargando Excel: {str(e)}"
    
    @staticmethod
    def load_json_data(uploaded_file):
        """Carga datos desde archivo JSON"""
        try:
            json_data = json.load(uploaded_file)
            
            # Si es un array de objetos, convertir directamente
            if isinstance(json_data, list):
                df = pd.json_normalize(json_data)
            # Si es un objeto, intentar normalizar
            elif isinstance(json_data, dict):
                # Si tiene una clave que contiene un array, usar esa
                array_keys = [k for k, v in json_data.items() if isinstance(v, list)]
                if array_keys:
                    df = pd.json_normalize(json_data[array_keys[0]])
                else:
                    # Convertir objeto a DataFrame
                    df = pd.json_normalize([json_data])
            else:
                return None, "❌ Formato JSON no soportado"
                
            return df, "✅ JSON cargado exitosamente"
        except Exception as e:
            return None, f"❌ Error cargando JSON: {str(e)}"
    
    @staticmethod
    def load_api_data(url, headers=None, params=None):
        """Carga datos desde API REST"""
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Normalizar datos JSON a DataFrame
            if isinstance(data, list):
                df = pd.json_normalize(data)
            elif isinstance(data, dict):
                # Buscar arrays en el JSON
                array_keys = [k for k, v in data.items() if isinstance(v, list)]
                if array_keys:
                    df = pd.json_normalize(data[array_keys[0]])
                else:
                    df = pd.json_normalize([data])
            else:
                return None, "❌ Respuesta API no válida"
                
            return df, f"✅ API consultada exitosamente ({len(df)} registros)"
        except requests.exceptions.RequestException as e:
            return None, f"❌ Error en API: {str(e)}"
        except Exception as e:
            return None, f"❌ Error procesando API: {str(e)}"

class ReportGenerator:
    """Genera reportes automáticos con IA"""
    
    @staticmethod
    def generate_data_summary(df):
        """Genera resumen estadístico de los datos"""
        summary = {
            "total_records": len(df),
            "total_columns": len(df.columns),
            "missing_values": df.isnull().sum().sum(),
            "numeric_columns": len(df.select_dtypes(include=['number']).columns),
            "categorical_columns": len(df.select_dtypes(include=['object']).columns),
            "memory_usage": f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB"
        }
        return summary
    
    @staticmethod
    def generate_insights(df):
        """Genera insights automáticos del dataset"""
        insights = []
        
        # Insights básicos
        insights.append(f"📊 Dataset contiene {len(df):,} registros y {len(df.columns)} columnas")
        
        # Análisis de valores faltantes
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 10:
            insights.append(f"⚠️ {missing_pct:.1f}% de valores faltantes detectados")
        elif missing_pct > 0:
            insights.append(f"ℹ️ {missing_pct:.1f}% de valores faltantes (nivel aceptable)")
        else:
            insights.append("✅ No se detectaron valores faltantes")
        
        # Análisis de columnas numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            insights.append(f"📈 {len(numeric_cols)} columnas numéricas disponibles para análisis")
            
            # Buscar outliers en columnas numéricas
            for col in numeric_cols[:3]:  # Solo primeras 3 columnas
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = len(df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)])
                if outliers > 0:
                    insights.append(f"🔍 {outliers} posibles outliers en columna '{col}'")
        
        # Análisis temporal
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            insights.append(f"📅 {len(date_cols)} columnas temporales detectadas")
        
        # Análisis de cardinalidad
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols[:3]:  # Solo primeras 3 columnas
            unique_vals = df[col].nunique()
            if unique_vals < 10:
                insights.append(f"🏷️ Columna '{col}' tiene {unique_vals} categorías únicas")
            elif unique_vals > len(df) * 0.8:
                insights.append(f"🆔 Columna '{col}' parece ser un identificador único")
        
        return insights
    
    @staticmethod
    def create_automatic_visualizations(df):
        """Crea visualizaciones automáticas basadas en los datos"""
        visualizations = []
        
        # Gráfico de distribución para columnas numéricas
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = numeric_cols[0]  # Tomar primera columna numérica
            fig = px.histogram(df, x=col, title=f"Distribución de {col}")
            visualizations.append(("Distribución", fig))
        
        # Gráfico de barras para columnas categóricas
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols[:2]:  # Máximo 2 gráficos categóricos
            if df[col].nunique() <= 20:  # Solo si tiene pocas categorías
                value_counts = df[col].value_counts().head(10)
                fig = px.bar(x=value_counts.values, y=value_counts.index, 
                           orientation='h', title=f"Top 10 valores en {col}")
                visualizations.append((f"Top {col}", fig))
        
        # Correlación si hay múltiples columnas numéricas
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto",
                          title="Matriz de Correlación")
            visualizations.append(("Correlación", fig))
        
        return visualizations

def show_pricing_section():
    """Muestra la sección de pricing del producto"""
    st.markdown("## 💰 Planes de Pricing")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📦 Plan Básico
        **$99/mes**
        
        ✅ 5 reportes/mes  
        ✅ CSV, Excel, JSON  
        ✅ Insights automáticos  
        ✅ 3 visualizaciones  
        ✅ Export PDF  
        
        *Ideal para pequeñas empresas*
        """)
        if st.button("Seleccionar Básico", key="basic", use_container_width=True):
            st.info("💳 Sistema de pagos en desarrollo")
    
    with col2:
        st.markdown("""
        ### 🚀 Plan Pro
        **$299/mes**
        
        ✅ 25 reportes/mes  
        ✅ Todas las fuentes + APIs  
        ✅ Insights avanzados con IA  
        ✅ Visualizaciones ilimitadas  
        ✅ Export PDF + PowerPoint  
        ✅ Templates personalizados  
        ✅ Soporte prioritario  
        
        *Recomendado para empresas medianas*
        """)
        if st.button("Seleccionar Pro ⭐", key="pro", type="primary", use_container_width=True):
            st.info("💳 Sistema de pagos en desarrollo")
    
    with col3:
        st.markdown("""
        ### 🏢 Plan Enterprise
        **$799/mes**
        
        ✅ 100 reportes/mes  
        ✅ API completa  
        ✅ White label  
        ✅ Integraciones custom  
        ✅ Soporte dedicado  
        ✅ SLA garantizado  
        
        *Para grandes corporaciones*
        """)
        if st.button("Contactar Ventas", key="enterprise", use_container_width=True):
            st.info("📞 Contacta para pricing personalizado")

def show_data_ingestion():
    """Muestra la interfaz de ingesta de datos"""
    st.markdown("## 📊 Carga de Datos")
      # Tabs para diferentes fuentes de datos
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📁 Archivos", "🌐 API REST", "🔗 URLs", "⚡ APIs Populares", "📋 Datos Demo"])
    
    data_manager = DataIngestionManager()
    df = None
    status_message = ""
    
    with tab1:
        st.markdown("### Cargar desde Archivo")
        uploaded_file = st.file_uploader(
            "Selecciona tu archivo de datos",
            type=['csv', 'xlsx', 'xls', 'json'],
            help="Formatos soportados: CSV, Excel (.xlsx, .xls), JSON"
        )
        
        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df, status_message = data_manager.load_csv_data(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                df, status_message = data_manager.load_excel_data(uploaded_file)
            elif file_extension == 'json':
                df, status_message = data_manager.load_json_data(uploaded_file)
            
            st.success(status_message)
    
    with tab2:
        st.markdown("### Cargar desde API REST")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            api_url = st.text_input(
                "URL de la API",
                placeholder="https://api.ejemplo.com/datos",
                help="Ingresa la URL completa de tu API REST"
            )
        
        with col2:
            st.markdown("#### APIs Demo")
            if st.button("🌍 Countries API", use_container_width=True):
                api_url = "https://restcountries.com/v3.1/all"
                st.session_state.api_url = api_url
            if st.button("📊 JSON Placeholder", use_container_width=True):
                api_url = "https://jsonplaceholder.typicode.com/users"
                st.session_state.api_url = api_url
        
        # Headers opcionales
        with st.expander("⚙️ Configuración Avanzada"):
            headers_text = st.text_area(
                "Headers (JSON format)",
                placeholder='{"Authorization": "Bearer token", "Content-Type": "application/json"}',
                help="Headers adicionales en formato JSON"
            )
            
            params_text = st.text_area(
                "Parámetros (JSON format)", 
                placeholder='{"limit": 100, "page": 1}',
                help="Parámetros de consulta en formato JSON"
            )
        
        if st.button("🔄 Consultar API", type="primary"):
            if api_url:
                try:
                    headers = json.loads(headers_text) if headers_text else None
                    params = json.loads(params_text) if params_text else None
                    
                    with st.spinner("Consultando API..."):
                        df, status_message = data_manager.load_api_data(api_url, headers, params)
                    
                    if df is not None:
                        st.success(status_message)
                    else:
                        st.error(status_message)
                        
                except json.JSONDecodeError:
                    st.error("❌ Error en formato JSON de headers o parámetros")
            else:
                st.warning("⚠️ Ingresa una URL válida")
    
    with tab3:
        st.markdown("### Cargar desde URL de Archivo")
        
        file_url = st.text_input(
            "URL del archivo",
            placeholder="https://ejemplo.com/datos.csv",
            help="URL directa a archivo CSV, Excel o JSON"
        )
        
        if st.button("📥 Descargar desde URL", type="primary"):
            if file_url:
                try:
                    with st.spinner("Descargando archivo..."):
                        response = requests.get(file_url, timeout=30)
                        response.raise_for_status()
                        
                        # Detectar tipo de archivo por extensión o Content-Type
                        content_type = response.headers.get('content-type', '')
                        
                        if 'csv' in file_url.lower() or 'text/csv' in content_type:
                            df = pd.read_csv(io.StringIO(response.text))
                            status_message = "✅ CSV descargado exitosamente"
                        elif 'json' in file_url.lower() or 'application/json' in content_type:
                            data = response.json()
                            df = pd.json_normalize(data if isinstance(data, list) else [data])
                            status_message = "✅ JSON descargado exitosamente"
                        else:
                            st.error("❌ Tipo de archivo no soportado desde URL")
                            
                    if df is not None:
                        st.success(status_message)
                        
                except Exception as e:
                    st.error(f"❌ Error descargando archivo: {str(e)}")
            else:                st.warning("⚠️ Ingresa una URL válida")
    
    with tab5:
        st.markdown("### APIs Populares de Negocio")
        st.info("💡 Conecta con fuentes de datos reales de tu empresa")
        
        if APIConnector:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Marketing & Analytics")
                if st.button("📈 Google Analytics", use_container_width=True):
                    with st.spinner("Cargando datos de Google Analytics..."):
                        df = APIConnector.get_google_analytics_sample()
                        status_message = "✅ Datos de Google Analytics cargados (sample)"
                        st.success(status_message)
                
                if st.button("📱 Facebook Ads", use_container_width=True):
                    with st.spinner("Cargando datos de Facebook Ads..."):
                        df = APIConnector.get_facebook_ads_sample()
                        status_message = "✅ Datos de Facebook Ads cargados (sample)"
                        st.success(status_message)
                
                if st.button("📧 HubSpot", use_container_width=True):
                    with st.spinner("Cargando datos de HubSpot..."):
                        df = APIConnector.get_hubspot_sample()
                        status_message = "✅ Datos de HubSpot cargados (sample)"
                        st.success(status_message)
            
            with col2:
                st.markdown("#### 💰 Ventas & Finanzas")
                if st.button("🤝 Salesforce", use_container_width=True):
                    with st.spinner("Cargando datos de Salesforce..."):
                        df = APIConnector.get_salesforce_sample()
                        status_message = "✅ Datos de Salesforce cargados (sample)"
                        st.success(status_message)
                
                if st.button("💳 Stripe Payments", use_container_width=True):
                    with st.spinner("Cargando datos de Stripe..."):
                        df = APIConnector.get_stripe_sample()
                        status_message = "✅ Datos de Stripe cargados (sample)"
                        st.success(status_message)
            
            st.markdown("---")
            with st.expander("🔐 Configurar APIs Reales"):
                st.markdown("""
                **Para conectar con APIs reales:**
                1. Obtén tus credenciales API de cada plataforma
                2. Configura los tokens de acceso
                3. Define los endpoints y parámetros
                4. ¡Automatiza tus reportes!
                
                *En el Plan Pro tendrás acceso a configuración de APIs reales.*
                """)
        else:
            st.error("Módulo de conectores API no disponible")
    
    with tab4:
        st.markdown("### Datos de Demostración")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📈 Ventas Demo", use_container_width=True):
                # Generar datos demo de ventas
                dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
                df = pd.DataFrame({
                    'fecha': dates,
                    'ventas': np.random.normal(1000, 200, len(dates)),
                    'region': np.random.choice(['Norte', 'Centro', 'Sur'], len(dates)),
                    'producto': np.random.choice(['A', 'B', 'C'], len(dates)),
                    'vendedor': np.random.choice(['Juan', 'María', 'Carlos', 'Ana'], len(dates))
                })
                status_message = "✅ Datos demo de ventas cargados"
                st.success(status_message)
        
        with col2:
            if st.button("👥 Clientes Demo", use_container_width=True):
                # Generar datos demo de clientes
                df = pd.DataFrame({
                    'cliente_id': range(1, 101),
                    'edad': np.random.normal(35, 10, 100),
                    'ingresos': np.random.normal(50000, 15000, 100),
                    'ciudad': np.random.choice(['Santiago', 'Valparaíso', 'Concepción'], 100),
                    'segmento': np.random.choice(['Premium', 'Standard', 'Basic'], 100),
                    'churn': np.random.choice([0, 1], 100, p=[0.8, 0.2])
                })
                status_message = "✅ Datos demo de clientes cargados"
                st.success(status_message)
        
        with col3:
            if st.button("💰 Finanzas Demo", use_container_width=True):
                # Generar datos demo financieros
                months = pd.date_range(start='2024-01-01', periods=12, freq='M')
                df = pd.DataFrame({
                    'mes': months,
                    'ingresos': np.random.normal(100000, 20000, 12),
                    'gastos': np.random.normal(80000, 15000, 12),
                    'utilidad': lambda x: x['ingresos'] - x['gastos']
                })
                df['utilidad'] = df['ingresos'] - df['gastos']
                df['roi'] = (df['utilidad'] / df['gastos']) * 100
                status_message = "✅ Datos demo financieros cargados"
                st.success(status_message)
    
    return df, status_message

def main():
    """Función principal del MVP"""
    
    # Header principal
    st.markdown("# 🤖 Generador de Reportes Automáticos")
    st.markdown("### *MVP - Transforma tus datos en insights accionables con IA*")
    
    # Descripción del producto
    st.markdown("""
    **🚀 Primera solución comercial del portafolio** - Automatiza la creación de reportes ejecutivos 
    profesionales usando IA avanzada. Soporta múltiples fuentes de datos y genera insights 
    narrativos automáticamente.
    """)
    
    # Sidebar con información
    add_sidebar_contact()
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🎯 Estado MVP")
        st.success("✅ En desarrollo activo")
        
        st.markdown("### 🔧 Funcionalidades")
        st.markdown("""
        - ✅ Carga CSV, Excel, JSON
        - ✅ Ingesta API REST
        - ✅ Insights automáticos con IA
        - ✅ Visualizaciones dinámicas
        - 🚧 Export PDF (próximamente)
        - 🚧 Templates industria
        """)
        
        st.markdown("### 💡 Demo Disponible")
        st.info("Prueba todas las funcionalidades con datos demo o tus propios archivos")
    
    # Pricing destacado
    with st.expander("💰 Ver Planes de Pricing", expanded=False):
        show_pricing_section()
    
    st.markdown("---")
    
    # Sección principal: Carga de datos
    df, status_message = show_data_ingestion()
      # Si hay datos cargados, mostrar análisis
    if df is not None and not df.empty:
        st.markdown("---")
        
        # Validar datos
        if DataValidator:
            is_valid, validation_issues = DataValidator.validate_dataframe(df)
            
            if validation_issues:
                with st.expander("⚙️ Validación de Datos"):
                    for issue in validation_issues:
                        st.markdown(f"• {issue}")
                    
                    # Sugerencias de tipos de datos
                    suggestions = DataValidator.suggest_data_types(df)
                    if suggestions:
                        st.markdown("**💡 Sugerencias de mejora:**")
                        for suggestion in suggestions:
                            st.markdown(f"• {suggestion}")
        
        st.markdown("## 📊 Análisis Automático")
        
        # Templates de reporte
        if ReportTemplates:
            st.markdown("### 📋 Seleccionar Template de Reporte")
            
            template_options = {
                "Análisis General": None,
                "📊 Marketing Digital": ReportTemplates.get_marketing_template(),
                "💰 Ventas": ReportTemplates.get_sales_template(),
                "💵 Financiero": ReportTemplates.get_financial_template(),
                "⚙️ Operacional": ReportTemplates.get_operations_template()
            }
            
            selected_template = st.selectbox(
                "Tipo de reporte",
                options=list(template_options.keys()),
                help="Selecciona un template específico para tu industria"
            )
            
            if selected_template != "Análisis General":
                template = template_options[selected_template]
                st.info(f"📋 Template seleccionado: **{template['title']}**")
                
                with st.expander("Ver estructura del template"):
                    st.markdown("**Secciones incluidas:**")
                    for section in template['sections']:
                        st.markdown(f"• {section}")
        
        # Mostrar preview de datos
        with st.expander("👀 Preview de Datos", expanded=True):
            st.dataframe(df.head(10), use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Registros", len(df))
            with col2:
                st.metric("Columnas", len(df.columns))
            with col3:
                st.metric("Tamaño", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        
        # Generar insights automáticos
        report_generator = ReportGenerator()
        
        # Resumen estadístico
        st.markdown("### 📈 Resumen Estadístico")
        summary = report_generator.generate_data_summary(df)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Registros", f"{summary['total_records']:,}")
        with col2:
            st.metric("Columnas Numéricas", summary['numeric_columns'])
        with col3:
            st.metric("Columnas Categóricas", summary['categorical_columns'])
        with col4:
            st.metric("Valores Faltantes", summary['missing_values'])
        
        # Insights automáticos
        st.markdown("### 🧠 Insights Automáticos con IA")
        insights = report_generator.generate_insights(df)
        
        for insight in insights:
            st.markdown(f"• {insight}")
        
        # Visualizaciones automáticas
        st.markdown("### 📊 Visualizaciones Automáticas")
        visualizations = report_generator.create_automatic_visualizations(df)
        
        if visualizations:
            for title, fig in visualizations:
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No se pudieron generar visualizaciones automáticas para este dataset")
        
        # Botón para generar reporte completo
        st.markdown("### 📄 Generar Reporte Completo")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("📊 Reporte Ejecutivo", type="primary", use_container_width=True):
                st.info("🚧 Generación de PDF en desarrollo")
        
        with col2:
            if st.button("📈 Reporte Técnico", use_container_width=True):
                st.info("🚧 Disponible en Plan Pro")
        
        with col3:
            if st.button("💼 Reporte Custom", use_container_width=True):
                st.info("🚧 Disponible en Plan Enterprise")
    
    else:
        # Mostrar beneficios mientras no hay datos
        st.markdown("---")
        st.markdown("## ✨ Beneficios del Generador de Reportes")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🎯 Para tu Negocio
            - ⚡ **Ahorra 10+ horas** por reporte
            - 📊 **Insights que importan** con IA
            - 🎨 **Reportes profesionales** automáticos
            - 📱 **Múltiples formatos** de export
            - 🔄 **Actualizaciones** en tiempo real
            """)
        
        with col2:
            st.markdown("""
            ### 🚀 Características Técnicas
            - 🔗 **APIs REST** y webhooks
            - 📁 **CSV, Excel, JSON** nativo
            - 🧠 **GPT-4** para narrativa
            - 📊 **Plotly** visualizaciones
            - ☁️ **Cloud-ready** escalable
            """)
    
    # Call to action
    st.markdown("---")
    st.markdown("## 🤝 ¿Listo para Automatizar tus Reportes?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📞 Contactar para Demo Personalizado", type="primary", use_container_width=True):
            st.balloons()
            st.success("¡Excelente! Usa los enlaces de contacto abajo para agendar tu demo.")
    
    # Footer
    add_page_footer()

# Agregar numpy para datos demo
import numpy as np

if __name__ == "__main__":
    main()
