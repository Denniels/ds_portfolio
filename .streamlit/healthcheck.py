"""
Módulo de monitoreo de salud para la aplicación Streamlit
"""
import streamlit as st
import psutil
import time
from pathlib import Path
import logging

def check_app_health():
    """Monitorea la salud de la aplicación y registra métricas"""
    try:
        # Configurar logging
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='.streamlit/app.log'
        )
        
        # Métricas básicas
        memory_usage = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        cpu_percent = psutil.Process().cpu_percent()
        
        # Verificar umbrales
        if memory_usage > 1000:  # 1GB
            logging.warning(f"Alto uso de memoria: {memory_usage:.2f}MB")
            st.warning("La aplicación está experimentando alta carga de memoria")
        
        if cpu_percent > 80:
            logging.warning(f"Alto uso de CPU: {cpu_percent}%")
            st.warning("La aplicación está experimentando alta carga de CPU")
        
        return True
    except Exception as e:
        logging.error(f"Error en health check: {str(e)}")
        return False

def cleanup_session():
    """Limpia recursos de la sesión"""
    try:
        # Limpiar caché si es muy grande
        cache_info = st.runtime.get_instance().cache_info
        if cache_info.current_size > 1000:  # MB
            st.runtime.get_instance().clear_cache()
        
        # Limpiar variables de sesión antiguas
        for key in list(st.session_state.keys()):
            if key.startswith('tmp_'):
                del st.session_state[key]
    except Exception as e:
        logging.error(f"Error en cleanup: {str(e)}")

def init_session():
    """Inicializa la sesión con configuraciones óptimas"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.render_count = 0
        st.session_state.last_cleanup = time.time()
        cleanup_session()
