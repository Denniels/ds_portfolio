"""
Aplicación principal del portafolio de Data Science
"""
import streamlit as st
from utils.navigation import create_nav_menu, init_navigation
from components.theme_switcher import render_theme_switcher
from utils.theme_selector import initialize_theme, apply_theme
# Asegurar que se apliquen los estilos globales (CSS) y tema
from config import apply_styles_only, init_theme as config_init_theme
from pathlib import Path
import os

# Configuración inicial de la página
st.set_page_config(
    page_title="Data Science Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar el tema global de `config` y aplicar estilos compartidos
try:
    config_init_theme()
    apply_styles_only()
except Exception:
    # Si falla la carga de estilos, continuar sin interrumpir la app
    pass

# Ocultar la navegación nativa de Streamlit (evita doble barra lateral)
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        [data-testid="stSidebarNavItems"] { display: none !important; }
        section[data-testid="stSidebar"] > div:first-child > div:first-child ul { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# Inicializar navegación y tema
init_navigation()
initialize_theme()

# Aplicar tema actual
current_theme = st.session_state.get('current_theme', 'Ocean Breeze')
is_dark = st.session_state.get('is_dark_mode', False)
apply_theme(theme_name=current_theme, is_dark=is_dark)

# Crear el menú de navegación
with st.sidebar:
    # Logo y título con manejo de errores para la imagen
    logo_path = Path(__file__).parent / "static" / "images" / "logo.png"
    
    try:
        if logo_path.exists():
            st.image(str(logo_path), width=100)
        else:
            # Si no existe el logo, mostrar un título estilizado
            st.markdown("""
                <div style="text-align: center; margin-bottom: 1rem;">
                    <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                    <div style="font-size: 1.5rem; font-weight: bold; background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        DS Portfolio
                    </div>
                </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.write("DS Portfolio")
    
    st.title("Daniel Mardones")
    st.caption("Desarrollador Python & Data Scientist")
    
    # Menú de navegación
    create_nav_menu()
    
    # Separador
    st.markdown("<div class='nav-separator'></div>", unsafe_allow_html=True)
    
    # Selector de tema
    render_theme_switcher()

# Contenido principal
st.title("Bienvenido a mi Portafolio de Data Science")
st.write("Explora mis proyectos y análisis usando el menú lateral.")

# Sección de destacados
st.header("📌 Proyectos Destacados")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        ### 📊 Análisis de Emisiones CO2
        Estudio detallado de las emisiones de CO2 en Chile
        
        [Ver proyecto →](/?page=emisiones_co2)
    """)

with col2:
    st.markdown("""
        ### 🏠 Predictor Inmobiliario
        Modelo ML para predicción de precios de propiedades
        
        [Ver proyecto →](/?page=predictor_inmobiliario)
    """)

with col3:
    st.markdown("""
        ### 💧 Calidad del Agua
        Análisis de la calidad del agua en Chile
        
        [Ver proyecto →](/?page=calidad_agua)
    """)

# Sección de estadísticas
st.header("📈 Estadísticas del Portfolio")

stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)

with stats_col1:
    st.metric(
        label="Proyectos Completados",
        value="12",
        delta="↑ 2 este mes"
    )

with stats_col2:
    st.metric(
        label="Precisión Promedio ML",
        value="95.3%",
        delta="↑ 2.1%"
    )

with stats_col3:
    st.metric(
        label="Datasets Analizados",
        value="24",
        delta="↑ 3 nuevos"
    )

with stats_col4:
    st.metric(
        label="Visualizaciones",
        value="156",
        delta="↑ 12%"
    )
