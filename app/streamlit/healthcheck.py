"""
Módulo para monitorear la salud de la aplicación Streamlit
"""
import streamlit as st
from pathlib import Path
import os
import psutil
import json
import sys
import pkg_resources

def check_dependencies():
    """
    Verifica las versiones de dependencias críticas
    """
    try:
        required_packages = {
            'numpy': '1.25.0',
            'pandas': '2.1.0',
            'scikit-learn': '1.3.0',
            'streamlit': '1.28.0'
        }
        
        issues = []
        for package, min_version in required_packages.items():
            try:
                installed = pkg_resources.get_distribution(package)
                if pkg_resources.parse_version(installed.version) < pkg_resources.parse_version(min_version):
                    issues.append(f"{package} {installed.version} (requiere >= {min_version})")
            except pkg_resources.DistributionNotFound:
                issues.append(f"{package} no instalado")
        
        if issues:
            st.warning(f"Dependencias con versiones incompatibles: {', '.join(issues)}")
            return False
        return True
    except Exception as e:
        st.error(f"Error al verificar dependencias: {str(e)}")
        return False

def check_python_version():
    """
    Verifica la versión de Python
    """
    min_version = (3, 9)
    max_version = (3, 11, 9)
    current = sys.version_info[:2]
    
    if current < min_version:
        st.error(f"Versión de Python {sys.version} demasiado antigua. Mínimo requerido: {'.'.join(map(str, min_version))}")
        return False
    elif current > max_version:
        st.error(f"Versión de Python {sys.version} demasiado nueva. Máximo soportado: {'.'.join(map(str, max_version))}")
        return False
    return True

def check_app_health():
    """
    Verifica el estado de salud de la aplicación
    """
    try:
        # Verificar versión de Python
        if not check_python_version():
            return False
            
        # Verificar dependencias
        if not check_dependencies():
            return False
            
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
