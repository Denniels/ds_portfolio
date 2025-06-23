"""
Archivo de configuración global para la aplicación de Streamlit
Este archivo será importado automáticamente por todas las páginas
"""

import streamlit as st
import sys
from pathlib import Path

def apply_styles_only():
    """
    Aplica solo los estilos CSS sin configurar la página.
    Para usar DESPUÉS de st.set_page_config()
    """
    try:
        # Asegurarse que utils está en el path para todas las páginas
        app_dir = Path(__file__).parent
        if str(app_dir) not in sys.path:
            sys.path.append(str(app_dir))
            
        # Importar y aplicar estilos compartidos sin configurar la página
        from utils.shared_styles import apply_shared_styles
        apply_shared_styles()
          # Aplicar tema seleccionado si existe en la sesión
        try:
            from utils.theme_manager import apply_theme_styles
            
            # Verificar si ya existe un tema seleccionado
            if 'theme_mode' in st.session_state and 'theme_name' in st.session_state:
                # Aplicar el tema guardado sin mostrar el selector
                # (el selector se mostrará en main.py para evitar duplicación)
                apply_theme_styles(st.session_state.theme_mode, st.session_state.theme_name)
        except Exception as e:
            print(f"Error al cargar tema: {e}")
        
        return True
    except Exception as e:
        print(f"Error al cargar CSS compartido: {e}")
        return False
