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
    
    # Estilos CSS para los botones de redes sociales
    st.sidebar.markdown("""
    <style>
    .social-buttons {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    .social-button {
        display: flex;
        align-items: center;
        text-decoration: none;
        color: white;
        padding: 8px 12px;
        border-radius: 5px;
        font-weight: bold;
        transition: opacity 0.3s;
    }
    .social-button:hover {
        opacity: 0.8;
    }
    .linkedin {
        background-color: #0077B5;
    }
    .github {
        background-color: #333;
    }
    .social-icon {
        margin-right: 8px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Mostrar botones
    st.sidebar.markdown("""
    <div class="social-buttons">
        <a href="https://www.linkedin.com/in/tu-perfil-linkedin/" target="_blank" class="social-button linkedin">
            <span class="social-icon">🔗</span> LinkedIn
        </a>
        <a href="https://github.com/tu-usuario-github" target="_blank" class="social-button github">
            <span class="social-icon">💻</span> GitHub
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
        <p>Desarrollado con ❤️ - Portafolio Data Science 2025</p>
        <div class="social-buttons" style="justify-content: center;">
            <a href="https://www.linkedin.com/in/tu-perfil-linkedin/" target="_blank" class="social-button linkedin">
                <span class="social-icon">🔗</span> LinkedIn
            </a>
            <a href="https://github.com/tu-usuario-github" target="_blank" class="social-button github">
                <span class="social-icon">💻</span> GitHub
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
