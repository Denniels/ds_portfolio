"""
Módulo para monitorear la salud de la aplicación Streamlit
"""
import streamlit as st
from pathlib import Path
import os
import psutil
import json

def check_app_health():
    """
    Verifica el estado de salud de la aplicación
    """
    try:
        # Verificar espacio en disco
        disk = psutil.disk_usage('/')
        if disk.percent > 95:  # Si el uso del disco es mayor al 95%
            st.warning("Espacio en disco bajo. Algunas funcionalidades podrían no estar disponibles.")
            
        # Verificar memoria
        memory = psutil.virtual_memory()
        if memory.percent > 90:  # Si el uso de memoria es mayor al 90%
            st.warning("Memoria del sistema baja. El rendimiento podría verse afectado.")
            
        # Verificar archivos críticos
        required_files = [
            'config/menu_config.json',
            'config/contact_config.json',
            'data/servicios.json'
        ]
        
        app_dir = Path(__file__).parent.parent
        missing_files = []
        
        for file in required_files:
            if not (app_dir / file).exists():
                missing_files.append(file)
                
        if missing_files:
            st.error(f"Archivos críticos faltantes: {', '.join(missing_files)}")
            return False
            
        return True
        
    except Exception as e:
        st.error(f"Error al verificar la salud de la aplicación: {str(e)}")
        return False

def init_session():
    """
    Inicializa variables de sesión y verifica integridad
    """
    if 'initialized' not in st.session_state:
        st.session_state['initialized'] = True
        st.session_state['startup_time'] = os.times()
        
def cleanup_session():
    """
    Limpia recursos y variables de sesión
    """
    if 'initialized' in st.session_state:
        del st.session_state['initialized']
        del st.session_state['startup_time']
