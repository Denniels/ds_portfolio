"""
Simulador de optimización para Streamlit Cloud
"""
import time
import random
from datetime import datetime
import streamlit as st

class StreamlitCloudOptimizer:
    """
    Simulador de métricas y optimización para Streamlit Cloud
    """
    def __init__(self):
        self.start_time = None
        self.metrics = []
        
    def start_measurement(self):
        """Inicia la medición simulada de recursos"""
        self.start_time = time.time()
    
    def stop_measurement(self):
        """Detiene la medición y devuelve métricas simuladas para Streamlit Cloud"""
        if not self.start_time:
            return self._get_default_metrics()
        
        duration = time.time() - self.start_time
        
        # Simular uso de recursos optimizado para Streamlit Cloud
        memory_gb = random.uniform(0.15, 0.25)  # Menos memoria que local
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'memory_gb': memory_gb,
            'cpu_percent': random.uniform(10, 25),  # CPU optimizado
            'memory_percent': random.uniform(20, 35),  # Memoria optimizada
            'is_optimized': True,
            'platform': 'streamlit_cloud'
        }
        
        self.metrics.append(metrics)
        return metrics
    
    def _get_default_metrics(self):
        """Devuelve métricas por defecto"""
        return {
            'cpu_percent': 15,
            'memory_gb': 0.2,
            'duration_seconds': 0,
            'is_optimized': True,
            'platform': 'streamlit_cloud'
        }
    
    @st.cache_data(ttl=60)
    def get_resource_usage(self):
        """Obtiene uso de recursos simulado para Streamlit Cloud"""
        return {
            'memory_available_gb': random.uniform(0.7, 0.9),
            'cpu_available': random.uniform(70, 85),
            'disk_free_gb': random.uniform(0.8, 1.2)
        }
