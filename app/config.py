"""
Archivo de configuración global para la aplicación de Streamlit
Este archivo será importado automáticamente por todas las páginas
"""

import streamlit as st
import sys
from pathlib import Path

def init_theme():
    """Inicializa el tema global y sus variables en session_state"""
    # Inicializar todas las variables del tema de una vez
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'light'
    
    if 'theme_name' not in st.session_state:
        st.session_state.theme_name = 'Azul Clásico'
    
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = {
            'mode': st.session_state.theme_mode,
            'name': st.session_state.theme_name
        }
    
    if 'theme_needs_reload' not in st.session_state:
        st.session_state.theme_needs_reload = False

def get_theme_css(mode, theme_name):
    """Genera el CSS dinámico para el tema seleccionado"""
    from utils.theme_manager import get_theme_config
    
    theme = get_theme_config(mode, theme_name)
    return f"""
    :root {{
        --primary-color: {theme['primary_color']};
        --background-color: {theme['background_color']};
        --text-color: {theme['text_color']};
        --secondary-color: {theme['secondary_color']};
        --accent-color: {theme['accent_color']};
        --card-bg: {theme['card_bg']};
        --glass-background: {theme['background_color']}ee;
        --border-color: {theme['border_color']};
        --glass-blur: 10px;
        --transition-speed: 0.3s;
        --text-secondary: {theme['text_color']}99;
    }}
    """

def apply_styles_only():
    """
    Aplica estilos CSS y configuración del tema.
    Para usar DESPUÉS de st.set_page_config()
    """
    try:
        # Asegurarse que utils está en el path
        app_dir = Path(__file__).parent
        if str(app_dir) not in sys.path:
            sys.path.append(str(app_dir))
        
        # Aplicar CSS base
        css_files = [
            "static/css/variables.css",     # Variables globales
            "static/css/style.css",         # Estilos principales
        ]
        
        # Cargar CSS base
        for css_file in css_files:
            css_path = Path(app_dir) / css_file
            if css_path.exists():
                with open(css_path) as f:
                    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
        # Aplicar CSS del tema actual
        theme_css = get_theme_css(
            st.session_state.get('theme_mode', 'light'),
            st.session_state.get('theme_name', 'Azul Clásico')
        )
        st.markdown(f'<style>{theme_css}</style>', unsafe_allow_html=True)
        
        return True
    
    except Exception as e:
        print(f"Error al cargar CSS: {e}")
        return False
