"""
Utilidades para manejo de navegación entre páginas de Streamlit
"""

import streamlit as st
import importlib.util
import sys
import os
from pathlib import Path

def navigate_to_page(page_name):
    """
    Navega a la página especificada utilizando st.switch_page si está disponible.
    Si no es posible, guarda la página en session_state para instrucciones manuales.
    
    Args:
        page_name: Nombre del archivo de la página (ej: "01_emisiones_co2.py")
        
    Returns:
        bool: True si la navegación fue exitosa
    """
    # Verificar si estamos ejecutando en Streamlit Cloud o con versión compatible
    direct_navigation_available = False
    
    try:
        # Comprobar si switch_page está disponible
        if hasattr(st, 'switch_page'):
            direct_navigation_available = True
            
            # Preparar la ruta a la página
            if not page_name.startswith("pages/"):
                page_path = f"pages/{page_name}"
            else:
                page_path = page_name
                
            # Intentar navegar
            st.switch_page(page_path)
            return True
    except Exception as e:
        # Si hay un error, mostramos un mensaje de depuración (solo en desarrollo)
        if os.environ.get('STREAMLIT_ENV') == 'development':
            st.error(f"Error en navegación: {e}")
    
    # Si no es posible navegar directamente, guardamos en session_state
    st.session_state["page"] = page_name
    return False


def create_back_button():
    """
    Crea un botón de regreso a la página principal.
    Si st.switch_page está disponible, navega directamente; de lo contrario,
    muestra instrucciones.
    """
    if st.button("🏠 Volver al inicio"):
        try:
            if hasattr(st, 'switch_page'):
                # Navegar directamente a la página principal
                st.switch_page("main_simplified.py")
                return True
        except:
            pass
            
        # Si falla, mostrar instrucciones
        st.info("Para volver al inicio, ejecuta: streamlit run app/main_simplified.py")
        return False
    
    return None
