"""
Componentes de contacto reutilizables para todas las páginas
"""
import streamlit as st

def add_page_footer():
    """
    Agrega un footer con enlaces de contacto y redes sociales
    al final de cada página
    """
    st.markdown("---")
    
    # Aplicar estilos CSS necesarios para los botones
    st.markdown("""
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
    
    # Crear layout de columnas
    cols = st.columns([1, 2, 1])
    
    # Columna central con botones de contacto
    with cols[1]:
        st.markdown("<h3 style='text-align: center;'>📱 Conecta conmigo</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="display: flex; justify-content: center;">
            <div class="social-buttons">
                <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" class="social-button linkedin">
                    <span class="social-icon">🔗</span> LinkedIn
                </a>
                <a href="https://github.com/Denniels" target="_blank" class="social-button github">
                    <span class="social-icon">💻</span> GitHub
                </a>
            </div>
        </div>
        <p style="text-align: center; margin-top: 10px; font-size: 14px; color: #666;">
            © 2025 Daniel Andrés Mardones Sanhueza | Actualizado: Junio 2025
        </p>
        """, unsafe_allow_html=True)

def add_sidebar_contact():
    """
    Agrega enlaces de contacto al panel lateral
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📱 Contacto")
    
    # Aplicar estilos CSS necesarios para los botones
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
        <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" class="social-button linkedin">
            <span class="social-icon">🔗</span> LinkedIn
        </a>
        <a href="https://github.com/Denniels" target="_blank" class="social-button github">
            <span class="social-icon">💻</span> GitHub
        </a>
    </div>
    """, unsafe_allow_html=True)
