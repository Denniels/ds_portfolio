"""Utilidades para el manejo de rutas del proyecto"""
from pathlib import Path

# Rutas base
ROOT_DIR = Path(__file__).parent.parent
APP_DIR = ROOT_DIR / 'app'
DATA_DIR = APP_DIR / 'data'
PREPROCESSED_DIR = DATA_DIR / 'preprocessed'
METRICS_DIR = DATA_DIR / 'metrics'

# Crear directorios necesarios
PREPROCESSED_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR.mkdir(parents=True, exist_ok=True)

def get_notebook_dir():
    """Retorna la ruta al directorio de notebooks"""
    return ROOT_DIR / 'notebooks'

def get_preprocessed_dir():
    """Retorna la ruta al directorio de datos preprocesados"""
    return PREPROCESSED_DIR

def get_metrics_dir():
    """Retorna la ruta al directorio de métricas"""
    return METRICS_DIR
