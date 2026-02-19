"""
Página de Productos Comerciales del Portafolio Data Science
"""
import streamlit as st
from pathlib import Path
import sys

# Importar configuración de página
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from utils.page_setup import setup_page, add_page_title
from utils.product_styles import get_product_card_styles, product_card_template
from utils.product_components import show_product_card

# Configurar página
st = setup_page(
    title="Soluciones Data Science",
    icon="💡"
)

# Título y descripción de la página
add_page_title(
    "Soluciones Innovadoras",
    "Transformando datos en valor para tu negocio",
    "💡"
)

# <div class="product-description">
#             <h3>🎯 Automatiza tus Reportes con IA</h3>
            
#             Potencia la toma de decisiones empresariales con informes generados 
#             automáticamente. Nuestra solución transforma datos complejos en 
#             visualizaciones claras y narrativas impactantes.
            
#             🚀 Ahorra hasta 80% del tiempo en creación de informes.
#         </div>



# Inyectar estilos CSS al inicio
st.markdown(get_product_card_styles(), unsafe_allow_html=True)

st.write("## 🚀 Soluciones Disponibles")

col1, col2 = st.columns(2)

with col1:
    show_product_card(
        title="Generador de Informes",
        description='Generador de Informes Inteligente',
        icon="📊",
        status="demo",
        features=[
            "Creación automática de informes en minutos",
            "Integración con múltiples fuentes de datos",
            "Narrativas inteligentes con GPT-4",
            "Visualizaciones profesionales automáticas",
            "Templates personalizados por industria",
            "Exportación a PDF, PPT y más"
        ],
        tech_stack=[
            "Python + Streamlit",
            "OpenAI GPT-4",
            "Pandas + Plotly",
            "FastAPI"
        ],
        demo_path="09_generador_reportes.py"
    )


        # <div class="product-description">
        #     <h3>💎 Inversiones Inmobiliarias Inteligentes</h3>
            
        #     Toma decisiones de inversión respaldadas por IA con predicciones 
        #     de precio de alta precisión. Identifica las mejores oportunidades 
        #     del mercado antes que la competencia.
            
        #     📈 95% de precisión en valoraciones.
        # </div>

with col2:
    show_product_card(
        title="Predictor Inmobiliario",
        description='Predictor Inmoviliario Avanzado',
        icon="🏠",
        status="demo",
        features=[
            "Predicciones de precio con 95% de precisión",
            "Análisis en tiempo real del mercado",
            "Mapas interactivos de valoración",
            "Recomendaciones personalizadas",
            "Informes profesionales detallados",
            "Alertas de oportunidades"
        ],
        tech_stack=[
            "Python + Scikit-learn",
            "XGBoost + LightGBM",
            "Pandas + GeoPandas",
            "Folium + Leaflet"
        ],
        demo_path="10_predictor_inmobiliario.py"
    )

st.write("## 🔨 Próximas Innovaciones")

col1, col2 = st.columns(2)


# <div class="product-description">
#             <h3>📈 Marketing Optimizado con IA</h3>
            
#             Maximiza el retorno de tus campañas publicitarias con decisiones 
#             basadas en datos. Optimiza presupuestos y mejora conversiones 
#             automáticamente.
            
#             💡 Incrementa ROI hasta un 40%.
#         </div>

with col1:
    show_product_card(
        title="Optimizador de Marketing",
        description='Marketing Optimizado con IA',
        icon="📈",
        status="dev",
        features=[
            "Optimización automática de ROI",
            "Predicción avanzada de conversiones",
            "Distribución inteligente de presupuesto",
            "Segmentación predictiva de audiencia",
            "Integración con plataformas principales",
            "Dashboard personalizado en tiempo real"
        ],
        tech_stack=[
            "Python + FastAPI",
            "TensorFlow",
            "Google Ads API",
            "MongoDB"
        ]
    )


# <div class="product-description">
#             <h3>🎯 Escucha Social Inteligente</h3>
            
#             Comprende el sentimiento de tus clientes en tiempo real con NLP 
#             avanzado. Detecta tendencias emergentes y anticípate a las 
#             necesidades del mercado.
            
#             ⚡ Monitoreo 24/7 en múltiples idiomas.
#         </div>


with col2:
    show_product_card(
        title="Análisis de Sentimiento",
        description='Análisis de Sentimiento Avanzado',
        icon="🎯",
        status="concept",
        features=[
            "Análisis multilingüe en tiempo real",
            "Detección automática de tendencias",
            "Sistema de alertas inteligentes",
            "Integración con redes sociales",
            "Visualizaciones interactivas",
            "API para integración personalizada"
        ],
        tech_stack=[
            "Python + Django",
            "BERT + Transformers",
            "Redis",
            "PostgreSQL"
        ]
    )

# Footer con información de contacto
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: rgba(255, 255, 255, 0.05); border-radius: 1rem; margin-top: 2rem;'>
    <h3 style='margin-bottom: 1rem;'>¿Listo para transformar tu negocio?</h3>
    <p style='font-size: 1.1rem; opacity: 0.9;'>
        Descubre cómo nuestras soluciones pueden impulsar tu empresa. 
        Agenda una demo personalizada y ve el poder de la IA en acción.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.button("🤝 Agenda una Demo Personalizada", use_container_width=True, type="primary")
