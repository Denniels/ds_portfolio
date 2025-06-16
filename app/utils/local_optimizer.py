"""
Optimizador para desarrollo local
"""
import psutil
import time
from datetime import datetime
import streamlit as st

class LocalOptimizer:
    def __init__(self):
        self.start_time = None
        self.metrics = []
        
    def start_measurement(self):
        """Inicia la medición de recursos"""
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss
    
    def stop_measurement(self):
        """Detiene la medición y devuelve métricas para desarrollo local"""
        if not self.start_time:
            return self._get_default_metrics()
        
        duration = time.time() - self.start_time
        current_memory = psutil.Process().memory_info().rss
        memory_used = current_memory - self.start_memory
        memory_gb = current_memory / (1024 ** 3)
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'memory_gb': memory_gb,
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'is_optimized': True,
            'platform': 'local'
        }
        
        self.metrics.append(metrics)
        return metrics
    
    def _get_default_metrics(self):
        """Devuelve métricas por defecto"""
        return {
            'cpu_percent': 0,
            'memory_gb': 0,
            'duration_seconds': 0,
            'is_optimized': True,
            'platform': 'local'
        }
    
    @st.cache_data(ttl=60)
    def get_resource_usage(self):
        """Obtiene uso de recursos local"""
        return {
            'memory_available_gb': psutil.virtual_memory().available / (1024 ** 3),
            'cpu_available': 100 - psutil.cpu_percent(),
            'disk_free_gb': psutil.disk_usage('/').free / (1024 ** 3)
        }
