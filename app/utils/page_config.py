"""
Configuración compartida para todas las páginas
"""
import streamlit as st
from pathlib import Path
from config import apply_styles_only, init_theme

def setup_page(title: str, icon: str = "📊", layout: str = "wide"):
    """
    Configura una página con estilos y temas consistentes
    
    Args:
        title (str): Título de la página
        icon (str): Emoji o ícono para la página
        layout (str): Layout de la página ("wide" o "centered")
    """
    # Configuración de la página
    st.set_page_config(
        page_title=f"{title} - DS Portfolio",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    # Inicializar tema
    init_theme()
    
    # Aplicar estilos compartidos
    apply_styles_only()
    
    # Inyectar CSS específico para páginas secundarias
    css_content = """
    <style>
        /* Asegurar consistencia en todas las páginas */
        .stApp {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        
        /* Mejorar visibilidad de textos */
        p, li {
            color: var(--text-color);
            font-size: 1rem;
            line-height: 1.6;
        }
        
        /* Estilizar encabezados */
        h1, h2, h3 {
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* Destacar bloques de información */
        .info-block {
            background: var(--glass-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        /* Mejorar visibilidad de enlaces */
        a {
            color: var(--accent-color);
            text-decoration: none;
            transition: color 0.3s;
        }
        
        a:hover {
            color: var(--secondary-color);
            text-decoration: underline;
        }
    </style>
    """
    st.markdown(css_content, unsafe_allow_html=True)
