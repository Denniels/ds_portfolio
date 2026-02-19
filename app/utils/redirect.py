"""
Implementa una función para forzar la navegación entre páginas en Streamlit
"""
import streamlit as st
from pathlib import Path
import os

def create_redirect_button(label, target_page, key=None, full_width=True, primary=False):
    """
    Crea un botón que redirige usando streamlit.switch_page y fallbacks
    
    Args:
        label (str): Texto para el botón
        target_page (str): Página de destino (sin extensión, puede incluir o no "pages/")
        key (str, optional): Clave única para el botón
        full_width (bool): Si el botón debe ocupar todo el ancho disponible
        primary (bool): Si debe ser un botón primario con estilo destacado
    """
    # Asegurarse que el target esté en formato correcto
    if target_page.endswith('.py'):
        target_page = target_page[:-3]
    
    # Si no empieza con 'pages/' y no es 'main', añadir el prefijo
    if not target_page.startswith('pages/') and target_page != 'main':
        full_path = f"pages/{target_page}"
    else:
        full_path = target_page
    
    # Asegurarnos que tenemos la extensión .py para switch_page
    full_path_with_extension = f"{full_path}.py" if not full_path.endswith('.py') else full_path
    
    # Dependiendo del tipo de botón, ajustar parámetros
    button_type = "primary" if primary else "secondary"
    width_option = True if full_width else False
    
    # Crear el botón
    if st.button(label, key=key, type=button_type, use_container_width=width_option):        # Usar st.switch_page (método estándar de Streamlit)
        try:
            st.switch_page(full_path_with_extension)
        except:
            # Fallback silencioso con meta refresh
            html_refresh = f"""
                <meta http-equiv="refresh" content="0;URL='/{full_path}'" />
            """
            st.markdown(html_refresh, unsafe_allow_html=True)
            st.stop()
