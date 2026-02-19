"""
Estilos compartidos para mantener consistencia visual en todas las páginas
"""
import streamlit as st
from pathlib import Path
import os

def apply_shared_styles():
    """
    Aplica estilos CSS compartidos a todas las páginas.
    Debe ser llamado DESPUÉS de st.set_page_config().
    """
    try:
        # Cargar estilos desde el archivo CSS externo
        css_path = Path(__file__).parent.parent / "static/styles/main.css"
        if css_path.exists():
            with open(css_path) as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        else:
            st.error("No se encontró el archivo de estilos main.css")
    except Exception as e:
        print(f"Error al cargar CSS: {e}")
