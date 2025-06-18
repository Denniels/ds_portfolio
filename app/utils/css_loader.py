"""
Utilidad para cargar estilos CSS en páginas de Streamlit
"""
import streamlit as st
from pathlib import Path
import os

def load_css_styles():
    """
    Carga los estilos CSS necesarios para la página actual.
    Esta función debe llamarse al inicio de cada página para asegurar
    que los estilos se apliquen correctamente.
    """
    
    # Determinar si estamos en Streamlit Cloud
    IS_STREAMLIT_CLOUD = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
    
    # Seleccionar archivo CSS según el entorno
    if IS_STREAMLIT_CLOUD:
        css_path = Path(__file__).parent.parent / 'static' / 'css' / 'streamlit_cloud.css'
    else:
        css_path = Path(__file__).parent.parent / 'static' / 'css' / 'style.css'
    
    try:
        if css_path.exists():
            with open(css_path, 'r', encoding='utf-8') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        # Fallback con estilos básicos
        st.markdown("""
        <style>
        /* Fallback CSS para botones sociales */
        .social-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
            margin: 10px 0;
        }
        .social-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            min-width: 120px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        .social-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            text-decoration: none;
            color: white;
        }
        .linkedin {
            background-color: #0077B5;
            border: 2px solid #0077B5;
        }
        .linkedin:hover {
            background-color: #005885;
            border-color: #005885;
        }
        .github {
            background-color: #333;
            border: 2px solid #333;
        }
        .github:hover {
            background-color: #1a1a1a;
            border-color: #1a1a1a;
        }
        .social-icon {
            margin-right: 8px;
            font-size: 16px;
            font-weight: bold;
        }
        
        /* Estilos adicionales para componentes */
        .stMetric {
            background-color: white;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stPlotlyChart {
            background-color: white;
            border-radius: 12px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)

def render_contact_badges():
    """
    Renderiza botones de contacto usando shields.io badges
    para máxima consistencia visual en todas las plataformas
    """
    st.markdown("""
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
    [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Denniels)
    """)

def render_contact_buttons_html():
    """
    Renderiza botones de contacto usando HTML/CSS
    Requiere que load_css_styles() haya sido llamado antes
    """
    st.markdown("""
    <div class="social-buttons">
        <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" class="social-button linkedin">
            <span class="social-icon">💼</span> LINKEDIN
        </a>
        <a href="https://github.com/Denniels" target="_blank" class="social-button github">
            <span class="social-icon">⚡</span> GITHUB
        </a>
    </div>
    """, unsafe_allow_html=True)
