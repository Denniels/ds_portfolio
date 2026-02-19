"""
Componentes de contacto reutilizables para todas las páginas
"""
import streamlit as st
import os
from pathlib import Path
from PIL import Image
import io
import requests

def add_custom_button(text, url, icon="🔗"):
    """
    Crea un botón personalizado con animación y efecto glassmorphism
    """
    return f"""
    <a href="{url}" target="_blank" rel="noopener noreferrer" class="sidebar-button animate-fade-in">
        <span style="margin-right: 8px;">{icon}</span> {text}
    </a>
    """

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
            <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
            </a>
            <a href="https://github.com/Denniels" target="_blank" rel="noopener noreferrer">
                <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
            </a>
        </div>
        <p style="text-align: center; margin-top: 10px; font-size: 14px; color: #666;">
            © 2025 Daniel Andrés Mardones Sanhueza | Actualizado: Junio 2025
        </p>
        """, unsafe_allow_html=True)

def add_sidebar_contact():
    """
    Agrega enlaces de contacto al panel lateral
    """
    # Cargar imagen de perfil
    profile_image_path = Path(__file__).parent.parent / "static" / "emoji_python_developer.png"
    if profile_image_path.exists():
        st.sidebar.image(str(profile_image_path), width=80)
    else:
        st.sidebar.markdown("👨‍💻", unsafe_allow_html=True)
    
    st.sidebar.title("Daniel Mardones")
    st.sidebar.caption("Python Developer")

def add_contact_buttons_legacy():
    """
    Función legacy para botones HTML/CSS (requiere CSS cargado)
    """
    st.markdown("""
    <div class="social-buttons">
        <a href="https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777" target="_blank" rel="noopener noreferrer" class="social-button linkedin">
            <span class="social-icon">💼</span> LINKEDIN
        </a>
        <a href="https://github.com/Denniels" target="_blank" rel="noopener noreferrer" class="social-button github">
            <span class="social-icon">⚡</span> GITHUB
        </a>
    </div>
    """, unsafe_allow_html=True)

def load_image(image_path, fallback_url=None, width=None):
    """
    Carga una imagen desde una ruta local o URL de fallback.
    """
    try:
        # Intentar cargar imagen local
        if os.path.exists(image_path):
            image = Image.open(image_path)
            if width:
                # Mantener la proporción al redimensionar
                aspect_ratio = image.height / image.width
                height = int(width * aspect_ratio)
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            return image
        
        # Si no existe localmente, intentar fallback URL
        elif fallback_url:
            response = requests.get(fallback_url, timeout=5)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                if width:
                    aspect_ratio = image.height / image.width
                    height = int(width * aspect_ratio)
                    image = image.resize((width, height), Image.Resampling.LANCZOS)
                return image
    except Exception as e:
        st.warning(f"No se pudo cargar la imagen: {str(e)}")
    
    return None

def add_profile_image_sidebar():
    """
    Agrega la imagen de perfil al sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Daniel Mardones")
    
    # Cargar imagen de perfil
    current_dir = os.path.dirname(__file__)
    app_dir = os.path.dirname(current_dir)
    profile_image_path = os.path.join(app_dir, "static", "emoji_python_developer.png")
    
    profile_image = load_image(
        profile_image_path,
        fallback_url="https://via.placeholder.com/100x100/1f77b4/ffffff?text=👨‍💻",
        width=100
    )
    
    # Mostrar imagen centrada en el sidebar
    if profile_image:
        st.sidebar.image(profile_image, width=100)
    else:
        st.sidebar.markdown('<div style="font-size: 60px; text-align: center;">👨‍💻</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <p style="text-align: center; font-size: 14px; color: #666; margin-top: 5px;">
        Data Science Enthusiast<br>
        Python Developer
    </p>
    """, unsafe_allow_html=True)

def add_complete_sidebar():
    """
    Agrega todos los componentes al sidebar en el orden correcto
    """
    # 1. Imagen de perfil y info personal
    add_profile_image_sidebar()
    
    # 2. Selector de paleta de colores (opcional)
    try:
        from utils.color_palette_manager import create_color_palette_selector
        create_color_palette_selector()
    except ImportError:
        pass
    
    # 3. Enlaces de contacto
    st.sidebar.markdown("### 📱 Contacto")
    
    # Crear contenedor para botones personalizados
    st.sidebar.markdown("""
    <div class="glass-container animate-fade-in" style="margin-top: 1rem;">
    """ + \
    add_custom_button("LinkedIn", "https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777", "💼") + \
    add_custom_button("GitHub", "https://github.com/Denniels", "⚡") + \
    add_custom_button("Portfolio", "https://integralservicespa.cl", "🌐") + \
    "</div>", unsafe_allow_html=True)

# Alias para compatibilidad con importaciones existentes
def mostrar_enlaces_contacto():
    """Alias para add_page_footer()"""
    add_page_footer()

def agregar_enlaces_sidebar():
    """Alias para add_complete_sidebar()"""
    add_complete_sidebar()
