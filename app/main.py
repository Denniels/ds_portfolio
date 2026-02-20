"""
Aplicación principal del portafolio de Data Science
"""
import streamlit as st
from utils.navigation import create_nav_menu, init_navigation, navigate_to
from components.theme_switcher import render_theme_switcher
from utils.theme_selector import initialize_theme, apply_theme
from utils.page_setup import add_page_title
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

# Banner principal de la página de inicio
add_page_title(
    "Bienvenido a mi Portafolio de Data Science",
    "Explora proyectos de análisis de datos, modelos ML y visualizaciones interactivas.",
    "📊"
)

# ── Estilos exclusivos para las tarjetas de estudios ────────────────────────
st.markdown("""
<style>
.study-card {
    background: var(--card-bg, #ffffff);
    border: 1px solid var(--border-color, rgba(0,0,0,0.08));
    border-radius: 14px;
    padding: 1.6rem 1.4rem 1.2rem 1.4rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
    min-height: 185px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.study-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.13);
}
.study-card-accent {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    border-radius: 14px 14px 0 0;
}
.study-card-icon {
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
    display: block;
    line-height: 1;
}
.study-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-color, #1a202c);
    margin: 0.2rem 0 0.5rem 0;
}
.study-card-desc {
    font-size: 0.88rem;
    color: var(--text-secondary, #4a5568);
    line-height: 1.5;
    margin: 0;
    flex-grow: 1;
}
.study-card-tag {
    display: inline-block;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
    color: #fff;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    padding: 2px 10px;
    border-radius: 20px;
    margin-bottom: 0.7rem;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ── Sección de estudios ──────────────────────────────────────────────────────
st.markdown("## 🔬 Estudios Realizados")
st.caption("Proyectos de análisis de datos con visualizaciones interactivas")
st.markdown("")

ESTUDIOS = [
    {
        "icono":   "🌍",
        "titulo":  "Análisis de Emisiones CO2",
        "desc":    "Estudio detallado de las emisiones de gases de efecto invernadero en Chile, con visualizaciones temporales y por sector industrial.",
        "tag":     "Medio ambiente",
        "pagina":  "pages/01_emisiones_co2.py",
    },
    {
        "icono":   "💧",
        "titulo":  "Calidad del Agua",
        "desc":    "Análisis de parámetros fisicoquímicos y microbiológicos en fuentes hídricas de Chile, tendencias y comparativas regionales.",
        "tag":     "Recursos hídricos",
        "pagina":  "pages/02_calidad_agua.py",
    },
    {
        "icono":   "👥",
        "titulo":  "Análisis Demográfico",
        "desc":    "Exploración de datos poblacionales de Chile usando BigQuery: distribución etaria, crecimiento y densidad por región.",
        "tag":     "Demografía",
        "pagina":  "pages/03_demografia.py",
    },
    {
        "icono":   "💰",
        "titulo":  "Presupuesto Público",
        "desc":    "Análisis de la ejecución del gasto gubernamental, evolución histórica y comparativa entre ministerios y programas.",
        "tag":     "Finanzas públicas",
        "pagina":  "pages/04_presupuesto_publico.py",
    },
]

col1, col2 = st.columns(2, gap="medium")
for i, estudio in enumerate(ESTUDIOS):
    with (col1 if i % 2 == 0 else col2):
        st.markdown(f"""
        <div class="study-card">
            <div class="study-card-accent"></div>
            <div>
                <span class="study-card-icon">{estudio['icono']}</span>
                <span class="study-card-tag">{estudio['tag']}</span>
                <p class="study-card-title">{estudio['titulo']}</p>
                <p class="study-card-desc">{estudio['desc']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Ver estudio →  {estudio['icono']}", key=f"btn_estudio_{i}", use_container_width=True):
            st.switch_page(estudio['pagina'])

# ── Sección de estadísticas ───────────────────────────────────────────────────
st.markdown("")
st.markdown("## 📈 Estadísticas del Portfolio")

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
