"""
Módulo de componentes comunes para todas las páginas
"""
import streamlit as st
from datetime import datetime

def add_contact_links():
    """
    Agrega enlaces de contacto a LinkedIn y GitHub en el sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Contacto")
      # Los estilos ahora se cargan desde el archivo CSS principal
    # st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Contacto")# Mostrar botones con el nuevo diseño
    st.sidebar.markdown("""
    <div class="social-buttons">
        <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" class="social-button linkedin">
            <span class="social-icon">�</span> LINKEDIN
        </a>
        <a href="https://github.com/Denniels" target="_blank" class="social-button github">
            <span class="social-icon">⚡</span> GITHUB
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    # Fecha de actualización
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 Actualizado")
    st.sidebar.markdown(f"{datetime.now().strftime('%d/%m/%Y')}")

def add_footer():
    """
    Agrega un footer con enlaces de contacto en la parte inferior de la página
    """
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; margin-top: 20px; padding: 10px;">
        <p>Desarrollado con ❤️ - Portafolio Data Science 2025</p>        <div class="social-buttons" style="justify-content: center;">
            <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" class="social-button linkedin">
                <span class="social-icon">�</span> LINKEDIN
            </a>
            <a href="https://github.com/Denniels" target="_blank" class="social-button github">
                <span class="social-icon">⚡</span> GITHUB
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
