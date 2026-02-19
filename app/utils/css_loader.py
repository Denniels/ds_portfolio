"""
Utilidad para cargar estilos CSS en páginas de Streamlit
"""
import streamlit as st
from pathlib import Path
import os
from typing import Optional, Dict
from .theme_lifecycle import ThemeLifecycleManager

def load_theme_specific_css(theme_name: str, mode: str) -> Optional[str]:
    """
    Carga el CSS específico para un tema y modo
    
    Args:
        theme_name: Nombre del tema
        mode: Modo del tema ("light" o "dark")
        
    Returns:
        Optional[str]: Contenido CSS o None si no se encuentra
    """
    # Construir el nombre del archivo CSS específico del tema
    theme_css_path = Path(__file__).parent.parent / 'static' / 'css' / 'themes' / f"{theme_name.lower().replace(' ', '_')}_{mode}.css"
    
    try:
        if theme_css_path.exists():
            with open(theme_css_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        return None
    
    return None

def load_base_css() -> str:
    """
    Carga el CSS base que es común para todos los temas
    
    Returns:
        str: CSS base
    """
    base_css = """
    /* Estilos base */
    .main {
        transition: all 0.3s ease;
    }
    
    /* Sidebar */
    .sidebar-header {
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .profile-info h1 {
        margin: 0.5rem 0;
        font-size: 1.5rem;
    }
    
    .profile-role {
        opacity: 0.8;
        font-size: 1rem;
    }
    
    .sidebar-section {
        margin: 1.5rem 0;
    }
    
    .sidebar-links a, .sidebar-nav a {
        display: block;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 4px;
        text-decoration: none;
        transition: all 0.2s ease;
    }
    
    /* Efecto hover para botones y enlaces */
    a:hover, button:hover {
        transform: translateY(-1px);
    }
    
    /* Contenedores y tarjetas */
    .content-card {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    """
    return base_css

def load_environment_css() -> str:
    """
    Carga el CSS específico del entorno (local vs cloud)
    
    Returns:
        str: CSS específico del entorno
    """
    IS_STREAMLIT_CLOUD = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
    
    if IS_STREAMLIT_CLOUD:
        css_path = Path(__file__).parent.parent / 'static' / 'css' / 'streamlit_cloud.css'
    else:
        css_path = Path(__file__).parent.parent / 'static' / 'css' / 'local.css'
    
    try:
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        return ""
    
    return ""

def load_css_styles():
    """
    Carga todos los estilos CSS necesarios para la aplicación.
    Combina los estilos base, específicos del tema y del entorno.
    """
    # Obtener el tema actual
    current_theme = ThemeLifecycleManager.get_current_theme()
    theme_name = current_theme['name']
    mode = current_theme['mode']
    
    # Obtener los colores del tema
    colors = ThemeLifecycleManager.get_theme_colors(theme_name, mode)
    
    # Crear variables CSS para los colores
    color_vars = f"""
    :root {{
        --primary-color: {colors['primary']};
        --secondary-color: {colors['secondary']};
        --background-color: {colors['background']};
        --text-color: {colors['text']};
        --accent-color: {colors['accent']};
        --text-secondary: {'#666666' if mode == 'light' else '#cccccc'};
        --border-color: {'#e0e0e0' if mode == 'light' else '#333333'};
        --hover-color: {'#f5f5f5' if mode == 'light' else '#2a2a2a'};
    }}
    """
      # Combinar todos los estilos
    all_css = "\n".join([
        color_vars,
        load_base_css(),
        load_theme_specific_css(theme_name, mode) or "",
        load_environment_css(),
        # Cargar el CSS para ocultar el menú nativo de Streamlit
        load_hide_streamlit_menu_css()
    ])
    
    # Aplicar estilos
    st.markdown(f'<style>{all_css}</style>', unsafe_allow_html=True)

def load_hide_streamlit_menu_css() -> str:
    """
    Carga el CSS específico para ocultar el menú nativo de Streamlit
    
    Returns:
        str: CSS para ocultar el menú de Streamlit
    """
    css_path = Path(__file__).parent.parent / 'static' / 'css' / 'hide-streamlit-menu.css'
    
    try:
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        return ""
    
    return ""
