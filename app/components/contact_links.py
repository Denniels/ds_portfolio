"""
Módulo de componentes comunes para todas las páginas - Versión unificada con badges
"""
import streamlit as st
from datetime import datetime

def add_contact_links():
    """
    Agrega enlaces de contacto a LinkedIn y GitHub en el sidebar usando badges
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Contacto")
    
    # Mostrar botones usando badges para máxima consistencia
    st.sidebar.markdown("""
    <div style="display: flex; flex-direction: column; gap: 5px; align-items: center;">
        <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank">
            <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
        </a>
        <a href="https://github.com/Denniels" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Fecha de actualización
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Actualizado")
    st.sidebar.markdown(f"{datetime.now().strftime('%d/%m/%Y')}")

def add_footer():
    """
    Agrega un footer con enlaces de contacto en la parte inferior de la página usando badges
    """
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; padding: 10px;">
        <p>Desarrollado con ❤️ - Portafolio Data Science 2025</p>
        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
            <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
            </a>
            <a href="https://github.com/Denniels" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
