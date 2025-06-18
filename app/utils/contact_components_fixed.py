"""
Componentes de contacto reutilizables para todas las páginas
"""
import streamlit as st

def add_page_footer():
    """
    Agrega un footer con enlaces de contacto y redes sociales
    al final de cada página usando badges para máxima consistencia
    """
    st.markdown("---")
    
    # Crear layout de columnas
    cols = st.columns([1, 2, 1])
    
    # Columna central con botones de contacto
    with cols[1]:
        st.markdown("<h3 style='text-align: center;'>📱 Conecta conmigo</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
            <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
            </a>
            <a href="https://github.com/Denniels" target="_blank">
                <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
            </a>
        </div>
        <p style="text-align: center; margin-top: 10px; font-size: 14px; color: #666;">
            © 2025 Daniel Andrés Mardones Sanhueza | Actualizado: Junio 2025
        </p>
        """, unsafe_allow_html=True)

def add_sidebar_contact():
    """
    Agrega enlaces de contacto al panel lateral usando badges
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Contacto")
    
    # Mostrar botones usando badges para consistencia
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

def add_contact_buttons_legacy():
    """
    Función legacy para botones HTML/CSS (requiere CSS cargado)
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
