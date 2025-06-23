"""
Página de Productos Comerciales del Portafolio Data Science
Transformando expertise técnico en soluciones comerciales
"""
import streamlit as st

# Importar configuración global
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import apply_styles_only
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Importar navegación robusta
import sys
from pathlib import Path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))
from utils.navigation import navigate_to

# Configuración de la página
st.set_page_config(
    page_title="Productos Comerciales - DS Portfolio",
    page_icon="🚀",
    layout="wide"
)

# Aplicar estilos compartidos después de configurar la página
apply_styles_only()

# Cargar estilos CSS
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar utils
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
    # Fallback por si no encuentra el módulo
    def add_page_footer():
        st.markdown("---")
        st.markdown("© 2025 DS Portfolio")
    def add_sidebar_contact():
        st.sidebar.markdown("---")

def load_productos_data():
    """Carga los datos de productos comerciales"""
    productos = {        "mvp": [
            {
                "nombre": "🤖 Generador de Reportes Automáticos",
                "estado": "En Desarrollo",
                "descripcion": "IA que transforma datos brutos en reportes ejecutivos profesionales con insights automáticos",
                "precio_basico": 99,
                "precio_pro": 299,
                "precio_enterprise": 799,
                "lanzamiento": "Julio 2025",
                "demo_disponible": True,
                "caracteristicas": [
                    "Automatización total con IA",
                    "Compatible con Excel, CSV, APIs",
                    "Insights narrativos con GPT-4",
                    "Gráficos automáticos profesionales",
                    "Templates por industria",
                    "Exportación PDF/PowerPoint"
                ],
                "mercado_objetivo": "Gerencias, consultoras, startups, agencias",
                "roi_cliente": "90% ahorro de tiempo vs reportes manuales",
                "url": "pages/09_generador_reportes.py"
            },
            {
                "nombre": "🏠 Predictor Inmobiliario Chile",
                "estado": "MVP Disponible",
                "descripcion": "ML para tasaciones precisas usando datos de propiedades en tiempo real",
                "precio_basico": 50,
                "precio_pro": 120,
                "precio_enterprise": 500,
                "lanzamiento": "Junio 2025",
                "demo_disponible": True,
                "caracteristicas": [
                    "Ensemble ML de alta precisión",
                    "Análisis de tendencias por comuna",
                    "Propiedades comparables",
                    "Alertas y recomendaciones",
                    "Exportación de informes PDF",
                    "API REST para integraciones"
                ],
                "mercado_objetivo": "Inmobiliarias, tasadores, inversionistas, bancos",
                "roi_cliente": "70% reducción tiempo de tasación",
                "url": "pages/10_predictor_inmobiliario.py"
            }
        ],
        "pipeline": [            {
                "nombre": "📊 Predictor de Churn de Clientes",
                "estado": "Planificado Q4 2025",
                "descripcion": "ML que identifica clientes en riesgo y recomienda acciones de retención",
                "precio_range": "$200-1,200/mes",
                "mercado": "E-commerce, SaaS, telecoms"
            },
            {
                "nombre": "📱 Monitor de Reputación Digital",
                "estado": "Planificado Q4 2025", 
                "descripcion": "NLP que monitorea menciones y analiza sentimiento en tiempo real",
                "precio_range": "$149-899/mes",
                "mercado": "Marcas, políticos, crisis management"
            },
            {
                "nombre": "📋 Analizador Licitaciones ChileCompra",
                "estado": "Planificado Q1 2026",
                "descripcion": "IA que identifica oportunidades en licitaciones públicas",
                "precio_range": "$300-2,000/mes",
                "mercado": "Consultoras, constructoras, proveedores"
            }
        ]
    }
    return productos

def mostrar_metricas_overview():
    """Muestra métricas generales de la estrategia comercial"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Productos en Roadmap",
            value="10",
            delta="Validados comercialmente"
        )
    
    with col2:
        st.metric(
            label="💰 ARR Potencial",
            value="$486K-2.1M",
            delta="Proyección 3 años"
        )
    
    with col3:
        st.metric(
            label="⚡ Time to Market",
            value="2-4 meses",
            delta="Promedio por producto"
        )
    
    with col4:
        st.metric(
            label="📈 ROI Proyectado",
            value="300-800%",
            delta="En 24 meses"
        )

def mostrar_producto_mvp(producto_mvp):
    """Muestra el producto MVP en desarrollo con detalle"""
    st.markdown("## 🚀 Producto Principal - MVP")
    
    # Header del producto
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {producto_mvp['nombre']}")
        st.markdown(f"**Estado:** `{producto_mvp['estado']}` | **Lanzamiento:** {producto_mvp['lanzamiento']}")
        st.write(producto_mvp['descripcion'])
        
        # ROI y mercado objetivo
        st.markdown("#### 🎯 Propuesta de Valor")
        col_roi1, col_roi2 = st.columns(2)
        with col_roi1:
            st.info(f"**ROI Cliente:** {producto_mvp['roi_cliente']}")
        with col_roi2:
            st.info(f"**Mercado:** {producto_mvp['mercado_objetivo']}")
    
    with col2:
        # Pricing card
        st.markdown("#### 💰 Planes de Pricing")
        pricing_data = {
            "Plan": ["Básico", "Pro", "Enterprise"],
            "Precio": [f"${producto_mvp['precio_basico']}", f"${producto_mvp['precio_pro']}", f"${producto_mvp['precio_enterprise']}"],
            "Target": ["Small Biz", "Medium Biz", "Large Corp"]
        }
        st.table(pd.DataFrame(pricing_data))        # Demo button
        if producto_mvp['demo_disponible']:
            if st.button("🎮 Probar Generador de Reportes", type="primary", use_container_width=True):
                st.balloons()
                st.success("🚀 ¡Demo integrada! Ve a la página 'Generador Reportes' para probar con datos ficticios")
                navigate_to("09_generador_reportes")
    
    # Características técnicas
    st.markdown("#### ⚙️ Características Técnicas")
    cols_features = st.columns(3)
    for i, feature in enumerate(producto_mvp['caracteristicas']):
        with cols_features[i % 3]:
            st.markdown(f"✅ {feature}")

def mostrar_pipeline_productos(pipeline):
    """Muestra los productos en pipeline"""
    st.markdown("## 📋 Pipeline de Productos")
    st.markdown("*Productos planificados para los próximos 12-18 meses*")
    
    for i, producto in enumerate(pipeline):
        with st.expander(f"{producto['nombre']} - {producto['estado']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(producto['descripcion'])
                st.markdown(f"**🎯 Mercado Objetivo:** {producto['mercado']}")
            
            with col2:
                st.markdown(f"**💰 Pricing:** {producto['precio_range']}")
                st.markdown(f"**📅 Estado:** {producto['estado']}")

def mostrar_roadmap_visual():
    """Muestra un roadmap visual de productos"""
    st.markdown("## 🗺️ Roadmap Visual 2025-2026")
    
    # Datos para el roadmap
    roadmap_data = {
        "Producto": [
            "Generador Reportes", "Monitor Reputación", "Predictor Churn",
            "Predictor Inmobiliario", "Licitaciones ChileCompra"
        ],
        "Q3_2025": [100, 0, 0, 0, 0],
        "Q4_2025": [100, 80, 60, 0, 0],
        "Q1_2026": [100, 100, 100, 40, 30],
        "Q2_2026": [100, 100, 100, 80, 70]
    }
    
    df_roadmap = pd.DataFrame(roadmap_data)
    
    # Crear gráfico de roadmap
    fig = go.Figure()
    
    quarters = ["Q3_2025", "Q4_2025", "Q1_2026", "Q2_2026"]
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"]
    
    for i, producto in enumerate(df_roadmap["Producto"]):
        y_values = [df_roadmap.loc[i, q] for q in quarters]
        fig.add_trace(go.Scatter(
            x=quarters,
            y=y_values,
            mode='lines+markers',
            name=producto,
            line=dict(width=3, color=colors[i]),
            marker=dict(size=8)        ))
    fig.update_layout(
        title={
            'text': "Roadmap de Desarrollo de Productos (%)",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#2F4F4F'}
        },
        xaxis_title="Trimestre",
        yaxis_title="Progreso de Desarrollo (%)",
        height=500,  # Mayor altura
        width=800,   # Ancho fijo para evitar problemas de escala
        hovermode='x unified',
        template='plotly_white',
        margin=dict(l=60, r=40, t=100, b=60)  # Márgenes mejorados
    )
    
    # Mejorar el formato de los ejes y líneas
    fig.update_traces(
        line=dict(width=3),     # Línea más gruesa
        marker=dict(size=8)     # Marcadores más grandes
    )
    
    # Configuración avanzada para la visualización
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            'displayModeBar': True,
            'responsive': True,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'roadmap_productos',
                'height': 600,
                'width': 1200,
                'scale': 2  # Mayor resolución
            }
        }
    )

def mostrar_metricas_comerciales():
    """Muestra métricas y proyecciones comerciales"""
    st.markdown("## 📊 Proyecciones Comerciales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de ARR proyectado
        arr_data = {
            "Año": [2025, 2026, 2027],
            "ARR_Conservador": [50000, 200000, 500000],
            "ARR_Optimista": [100000, 500000, 1500000]
        }
        
        fig_arr = go.Figure()
        fig_arr.add_trace(go.Scatter(
            x=arr_data["Año"],
            y=arr_data["ARR_Conservador"],
            mode='lines+markers',
            name='Escenario Conservador',
            line=dict(color='#FF6B6B', width=3)
        ))
        fig_arr.add_trace(go.Scatter(
            x=arr_data["Año"],
            y=arr_data["ARR_Optimista"],
            mode='lines+markers',
            name='Escenario Optimista',
            line=dict(color='#4ECDC4', width=3)        ))
        fig_arr.update_layout(
            title={
                'text': "Proyección ARR (Annual Recurring Revenue)",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': '#2F4F4F'}
            },
            xaxis_title="Año",
            yaxis_title="ARR (USD)",
            height=450,  # Mayor altura
            template='plotly_white',
            margin=dict(l=50, r=40, t=80, b=50),  # Márgenes adecuados
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        # Mejoras adicionales para el gráfico
        fig_arr.update_traces(
            line=dict(width=3),      # Líneas más gruesas
            marker=dict(size=8)      # Marcadores más grandes
        )
        
        # Configuración avanzada para la visualización
        st.plotly_chart(
            fig_arr, 
            use_container_width=True,
            config={
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'proyeccion_arr',
                    'height': 500,
                    'width': 900,
                    'scale': 2  # Mayor resolución
                }
            }
        )
    
    with col2:
        # Distribución de productos por categoría
        categorias_data = {
            "Categoría": ["Automatización", "Predicción", "Monitoreo", "Análisis"],
            "Productos": [3, 3, 2, 2],
            "ARR_Potencial": [400000, 600000, 300000, 200000]        }
        fig_pie = px.pie(
            values=categorias_data["ARR_Potencial"],
            names=categorias_data["Categoría"],
            title="Distribución ARR por Categoría",
            color_discrete_sequence=px.colors.qualitative.Bold,  # Paleta de colores más vistosa
            template='plotly_white',
            hole=0.4,  # Crear gráfico de dona para mejor visualización
            height=450  # Mayor altura
        )
        
        # Mejoras adicionales para el gráfico de pastel
        fig_pie.update_layout(
            title={
                'text': "Distribución ARR por Categoría",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 18, 'color': '#2F4F4F'}
            },
            margin=dict(l=40, r=40, t=80, b=40),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,  # Posición debajo del gráfico
                xanchor="center",
                x=0.5
            )
        )
        
        # Añadir etiquetas con valores
        fig_pie.update_traces(
            textinfo='percent+label',
            textposition='inside',
            insidetextfont=dict(color='white', size=14)
        )
        
        # Configuración avanzada para la visualización
        st.plotly_chart(
            fig_pie, 
            use_container_width=True,
            config={
                'displayModeBar': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'distribucion_arr',
                    'height': 500,
                    'width': 900,
                    'scale': 2  # Mayor resolución
                }
            }
        )

def mostrar_estrategia_comercial():
    """Muestra la estrategia go-to-market"""
    st.markdown("## 🎯 Estrategia Go-to-Market")
    
    tab1, tab2, tab3 = st.tabs(["🚀 Lanzamiento", "📈 Crecimiento", "🌐 Escalamiento"])
    
    with tab1:
        st.markdown("### Fase 1: MVP Launch (Q3 2025)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Objetivos")
            st.markdown("""
            - ✅ MVP Generador de Reportes funcional
            - ✅ 10 beta customers validados
            - ✅ Product-market fit confirmado
            - ✅ $5,000 MRR alcanzado
            """)
        
        with col2:
            st.markdown("#### 📋 Acciones Clave")
            st.markdown("""
            - 🔧 Desarrollo MVP (4-6 semanas)
            - 🎮 Demo interactivo en Streamlit
            - 💳 Integración sistema de pagos
            - 📧 Outreach directo LinkedIn
            """)
    
    with tab2:
        st.markdown("### Fase 2: Growth (Q4 2025)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Objetivos")
            st.markdown("""
            - ✅ 50 clientes pagantes activos
            - ✅ 2 productos en producción
            - ✅ $15,000 MRR alcanzado
            - ✅ NPS >50 customer satisfaction
            """)
        
        with col2:
            st.markdown("#### 📋 Acciones Clave")
            st.markdown("""
            - 📊 Optimización conversion funnel
            - 🤖 Launch Monitor Reputación
            - 📝 Content marketing strategy
            - 🤝 Programa de referidos
            """)
    
    with tab3:
        st.markdown("### Fase 3: Scale (2026)")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Objetivos")
            st.markdown("""
            - ✅ 200+ clientes enterprise
            - ✅ 5 productos en producción
            - ✅ $100,000+ MRR alcanzado
            - ✅ Equipo de 3-5 personas
            """)
        
        with col2:
            st.markdown("#### 📋 Acciones Clave")
            st.markdown("""
            - 🏢 Enterprise sales program
            - 🌎 Expansión internacional
            - 🔗 Platform integrations
            - 💼 Partnership strategy
            """)

def main():
    """Función principal de la página"""
    
    # Header principal
    st.markdown("# 🚀 Productos Comerciales")
    st.markdown("### *Transformando expertise en Data Science en soluciones comerciales de alto valor*")
    
    # Descripción introductoria
    st.markdown("""
    Esta sección presenta la transformación estratégica del portafolio técnico en una plataforma comercial, 
    con productos de **IA y Data Science** diseñados para resolver problemas reales de negocio con 
    **ROI medible y comprobable**.
    """)
    
    # Sidebar con información adicional
    add_sidebar_contact()
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📊 Estado del Portfolio")
        st.info("Transformación a productos comerciales en progreso")
        
        st.markdown("### 🎯 MVP Actual")
        st.success("Generador de Reportes Automáticos - En desarrollo")
        
        st.markdown("### 📈 Métricas Clave")
        st.metric("Productos Roadmap", "10")
        st.metric("ARR Potencial", "$486K-2.1M")        
        st.metric("Tiempo MVP", "30-45 días")
    
    # Métricas overview
    mostrar_metricas_overview()
    st.markdown("---")
    
    # Cargar datos de productos
    productos_data = load_productos_data()
    
    # Mostrar producto MVP
    # Si hay más de un producto en la lista, mostrar el predictor inmobiliario
    if len(productos_data["mvp"]) > 1:
        # Buscar el producto inmobiliario
        predictor_inmobiliario = next((p for p in productos_data["mvp"] if "Predictor Inmobiliario" in p["nombre"]), productos_data["mvp"][0])
        mostrar_producto_mvp(predictor_inmobiliario)
    else:
        # Si solo hay un producto, mostrar ese
        mostrar_producto_mvp(productos_data["mvp"][0])
    
    st.markdown("---")
    
    # Pipeline de productos
    mostrar_pipeline_productos(productos_data["pipeline"])
    
    st.markdown("---")
    
    # Roadmap visual
    mostrar_roadmap_visual()
    
    st.markdown("---")
    
    # Métricas comerciales
    mostrar_metricas_comerciales()
    
    st.markdown("---")
    
    # Estrategia comercial
    mostrar_estrategia_comercial()
    
    st.markdown("---")
    
    # Call to action
    st.markdown("## 💡 ¿Interesado en Colaborar?")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        **🤝 Oportunidades de Colaboración:**
        - 💼 **Clientes Early Adopters** para beta testing
        - 🚀 **Inversionistas** para acelerar desarrollo  
        - 👥 **Partners Técnicos** para co-desarrollo
        - 🎯 **Clientes Enterprise** para productos custom
        """)
        
        if st.button("📞 Contactar para Colaboración", type="primary", use_container_width=True):
            st.balloons()
            st.success("¡Excelente! Usa los enlaces de contacto abajo para conectar.")
    
    # Footer con contactos
    add_page_footer()

# Ejecutar página principal
if __name__ == "__main__":
    main()
