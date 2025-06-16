"""
Utilidades para gestionar y mostrar el CV en la aplicación
"""

import streamlit as st
from pathlib import Path
import base64
from datetime import datetime

def get_cv_download_link():
    """
    Crea links de descarga para el CV en formato Markdown
    """
    cv_path = Path(__file__).parent.parent.parent / "docs" / "curriculum.md"
    
    if not cv_path.exists():
        return None
    
    # Leer el archivo markdown
    with open(cv_path, 'r', encoding='utf-8') as file:
        cv_content = file.read()
    
    # Crear link de descarga para MD
    b64_md = base64.b64encode(cv_content.encode()).decode()
    md_href = f'<a href="data:file/markdown;base64,{b64_md}" download="DanielMardones_CV.md">📥 Descargar CV (Markdown)</a>'
    
    return cv_content, md_href

def display_cv():
    """
    Muestra el CV en la aplicación Streamlit
    """
    st.title("📄 Curriculum Vitae")
    
    try:
        cv_content, download_link = get_cv_download_link()
        if cv_content and download_link:
            # Crear columnas para los botones de descarga y redes sociales
            col1, col2, col3 = st.columns([1,1,1])
            
            with col1:
                st.markdown(download_link, unsafe_allow_html=True)
            with col2:
                st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)")
            with col3:
                st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Denniels)")
            
            # Mostrar fecha de última actualización
            st.caption(f"Última actualización: {datetime.now().strftime('%d/%m/%Y')}")
            
            # Mostrar CV
            st.markdown(cv_content)
            
            # Añadir nota sobre contacto
            st.info("💡 Disponible para proyectos y oportunidades que combinen mantenimiento industrial con análisis de datos.", icon="📬")
        else:
            st.error("No se pudo cargar el CV. Por favor, inténtalo más tarde.")
    except Exception as e:
        st.error(f"Error al cargar el CV: {str(e)}")
        st.info("Puedes ver mi perfil completo en [LinkedIn](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)")
