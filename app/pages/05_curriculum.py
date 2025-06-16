"""
Página del CV en el portafolio
"""
import streamlit as st
from utils.cv_utils import display_cv
from pathlib import Path

st.set_page_config(
    page_title="CV - Daniel Mardones",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"  # Para dar más espacio al CV
)

# Configurar el estilo de la página
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .stMarkdown h1 {
        text-align: center;
    }
    
    .download-buttons {
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Mostrar el CV
display_cv()
