"""
Script de configuración compartida para todas las páginas
Este archivo se ejecuta automáticamente al inicio de cada página
"""
import streamlit as st
import sys
from pathlib import Path

# Asegurarse que utils está en el path para todas las páginas
app_dir = Path(__file__).parent.parent
if str(app_dir) not in sys.path:
    sys.path.append(str(app_dir))

# Importar y aplicar estilos compartidos
from utils.shared_styles import apply_shared_styles
apply_shared_styles()
