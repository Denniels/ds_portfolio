"""
Configuración unificada de página para todas las páginas de la aplicación
"""
import streamlit as st
from pathlib import Path
from .navigation import create_nav_menu, init_navigation
from .theme_selector import initialize_theme, apply_theme
from components.theme_switcher import render_theme_switcher
from config import apply_styles_only, init_theme as config_init_theme

def setup_page(title="", icon="📊", show_navigation=True):
    """
    Configura una página con todos los elementos comunes
    
    Args:
        title (str): Título de la página
        icon (str): Ícono de la página
        show_navigation (bool): Si se debe mostrar la navegación
    """
    # Configuración inicial
    st.set_page_config(
        page_title=f"DS Portfolio | {title}" if title else "DS Portfolio",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inicializar tema global y cargar CSS compartido para toda la app
    try:
        config_init_theme()
        apply_styles_only()
    except Exception:
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
    if show_navigation:
        init_navigation()
    initialize_theme()
    
    # Aplicar tema actual
    current_theme = st.session_state.get('current_theme', 'Ocean Breeze')
    is_dark = st.session_state.get('is_dark_mode', False)
    apply_theme(theme_name=current_theme, is_dark=is_dark)
    
    # Configurar sidebar
    if show_navigation:
        with st.sidebar:
            # Logo y título
            logo_path = Path(__file__).parent.parent / "static" / "images" / "logo.png"
            try:
                if logo_path.exists():
                    st.image(str(logo_path), width=100)
                else:
                    # Título estilizado como fallback
                    st.markdown("""
                        <div style="text-align: center; margin-bottom: 1rem;">
                            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
                            <div style="font-size: 1.5rem; font-weight: bold; background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                                DS Portfolio
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            except Exception:
                st.write("DS Portfolio")
            
            st.title("Daniel Mardones")
            st.caption("Desarrollador Python & Data Scientist")
            
            # Menú de navegación
            create_nav_menu()
            
            # Separador
            st.markdown("<div class='nav-separator'></div>", unsafe_allow_html=True)
            
            # Selector de tema
            render_theme_switcher()
    
    return st

def add_page_title(title, description="", icon=""):
    """
    Agrega un título de página con estilo consistente
    
    Args:
        title (str): Título principal
        description (str): Descripción o subtítulo opcional
        icon (str): Ícono opcional para el título
    """
    st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="
                margin: 0;
                display: flex;
                align-items: center;
                gap: 0.5rem;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">
                {f'<span style="font-size: 2.5rem;">{icon}</span>' if icon else ''}
                <span>{title}</span>
            </h1>
            {f'<p style="font-size: 1.1rem; opacity: 0.7; margin-top: 0.5rem;">{description}</p>' if description else ''}
            <div style="
                height: 2px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                margin: 1rem 0;
            "></div>
        </div>
    """, unsafe_allow_html=True)

def create_card(title, content, icon="", is_featured=False):
    """
    Crea una tarjeta estilizada
    
    Args:
        title (str): Título de la tarjeta
        content (str): Contenido de la tarjeta
        icon (str): Ícono opcional
        is_featured (bool): Si la tarjeta debe destacarse
    """
    gradient = """
        linear-gradient(135deg,
            rgba(var(--primary-color-rgb), 0.2),
            rgba(var(--secondary-color-rgb), 0.2)
        )
    """ if is_featured else """
        linear-gradient(135deg,
            rgba(var(--primary-color-rgb), 0.05),
            rgba(var(--secondary-color-rgb), 0.05)
        )
    """
    
    border = "2px solid var(--primary-color)" if is_featured else "1px solid rgba(255,255,255,0.1)"
    
    st.markdown(f"""
        <div style="
            background: {gradient};
            backdrop-filter: blur(10px);
            border: {border};
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                opacity: {1 if is_featured else 0};
            "></div>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                {f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ''}
                <h3 style="margin: 0;">{title}</h3>
            </div>
            <div>{content}</div>
        </div>
    """, unsafe_allow_html=True)

def add_page_footer():
    """Agrega el footer común a todas las páginas"""
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <div style="opacity: 0.7; margin-bottom: 1rem;">
                Desarrollado por Daniel Mardones
            </div>
            <div style="display: flex; justify-content: center; gap: 1rem;">
                <a href="https://github.com/Denniels" target="_blank" title="GitHub"
                   style="color: var(--text-color); text-decoration: none;">
                    <i class="fab fa-github fa-2x"></i>
                </a>
                <a href="www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" title="LinkedIn"
                   style="color: var(--text-color); text-decoration: none;">
                    <i class="fab fa-linkedin fa-2x"></i>
                </a>
                <a href="mailto:daniel.mardones@integralservicespa.cl" title="Email"
                   style="color: var(--text-color); text-decoration: none;">
                    <i class="fas fa-envelope fa-2x"></i>
                </a>
            </div>
            <div style="margin-top: 1rem; opacity: 0.5;">
                © 2025 Data Science Portfolio
            </div>
        </div>
    """, unsafe_allow_html=True)
