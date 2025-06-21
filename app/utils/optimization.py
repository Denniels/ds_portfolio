"""
Módulo de optimización simplificado - sin dependencias pesadas
"""
import os
import json
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st

class ResourceOptimizer:
    """
    Clase simplificada para optimización de recursos
    """
    def __init__(self):
        self.start_time = None
        self.metrics = {}

    def start_measurement(self):
        """Inicia la medición de recursos de forma simplificada"""
        self.start_time = time.time()
        return True

    def stop_measurement(self):
        """Detiene la medición y retorna métricas básicas"""
        if self.start_time is None:
            return {'cpu_percent': 0, 'memory_mb': 0, 'elapsed_time': 0}
        
        elapsed = time.time() - self.start_time
        return {
            'cpu_percent': 0.0,  # Simulado
            'memory_mb': 100.0,  # Simulado
            'elapsed_time': elapsed
        }

    def start_monitoring(self):
        """Alias para start_measurement - compatibilidad con páginas existentes"""
        return self.start_measurement()
    
    def stop_monitoring(self):
        """Alias para stop_measurement - compatibilidad con páginas existentes"""
        return self.stop_measurement()

    def get_current_usage(self):
        """Retorna uso actual simulado"""
        return {
            'cpu_percent': 10.0,
            'memory_mb': 150.0,
            'status': 'Optimizado'
        }

class DataManager:
    """
    Gestor de datos simplificado
    """
    def __init__(self, cache_dir=None):
        if cache_dir is None:
            cache_dir = Path(__file__).parent.parent / 'data' / 'cache'
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def save_data(self, data, filename):
        """Guarda datos en caché"""
        try:
            filepath = self.cache_dir / filename
            if isinstance(data, pd.DataFrame):
                data.to_json(filepath, orient='records', date_format='iso')
            else:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            st.warning(f"Error guardando datos: {e}")
            return False

    def load_data(self, filename):
        """Carga datos desde caché"""
        try:
            filepath = self.cache_dir / filename
            if not filepath.exists():
                return None
            
            if filename.endswith('.json'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            st.warning(f"Error cargando datos: {e}")
            return None

    def clear_cache(self):
        """Limpia el caché"""
        try:
            for file in self.cache_dir.glob('*'):
                if file.is_file():
                    file.unlink()
            return True
        except Exception:
            return False

    def get_last_update(self, filename):
        """Devuelve la fecha de última modificación del archivo en caché"""
        filepath = self.cache_dir / filename
        if filepath.exists():
            return filepath.stat().st_mtime
        return None

# Funciones de utilidad simplificadas
def get_memory_usage():
    """Retorna uso de memoria simulado"""
    return {'used': 100.0, 'total': 1000.0, 'percent': 10.0}

def optimize_dataframe(df):
    """Optimiza un DataFrame para usar menos memoria"""
    if not isinstance(df, pd.DataFrame):
        return df
    
    # Optimizaciones básicas
    for col in df.select_dtypes(include=['object']):
        if df[col].nunique() < len(df) * 0.5:
            df[col] = df[col].astype('category')
    
    # Optimizar tipos numéricos
    for col in df.select_dtypes(include=['int64']):
        if df[col].min() >= 0 and df[col].max() <= 255:
            df[col] = df[col].astype('uint8')
        elif df[col].min() >= -128 and df[col].max() <= 127:
            df[col] = df[col].astype('int8')
    
    return df

def monitor_performance(func):
    """Decorador para monitorear rendimiento"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        
        if elapsed > 1.0:  # Solo mostrar si toma más de 1 segundo
            st.info(f"Operación completada en {elapsed:.2f} segundos")
        
        return result
    return wrapper
