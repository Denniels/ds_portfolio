"""
Optimizador simplificado para desarrollo local
"""
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
        return True
        
    def stop_measurement(self):
        """Detiene la medición y retorna métricas simuladas"""
        if self.start_time is None:
            return {
                'cpu_percent': 15.0,
                'memory_gb': 0.5,
                'cpu_cost': 0.000001,
                'memory_cost': 0.000002,
                'request_cost': 0.000001
            }
        
        elapsed = time.time() - self.start_time
        
        # Métricas simuladas para desarrollo local
        metrics = {
            'cpu_percent': min(50.0, 10.0 + elapsed * 2),
            'memory_gb': min(2.0, 0.3 + elapsed * 0.1),
            'elapsed_time': elapsed,
            'cpu_cost': elapsed * 0.000001,
            'memory_cost': elapsed * 0.000002,
            'request_cost': 0.000001
        }
        
        self.metrics.append(metrics)
        return metrics
        
    def get_current_metrics(self):
        """Retorna métricas actuales simuladas"""
        return {
            'cpu_percent': 12.5,
            'memory_gb': 0.4,
            'status': 'Local Development'
        }
    
    def start_monitoring(self):
        """Alias para start_measurement - compatibilidad"""
        return self.start_measurement()
    
    def stop_monitoring(self):
        """Alias para stop_measurement - compatibilidad"""
        return self.stop_measurement()

    def get_current_usage(self):
        """Retorna uso actual simulado"""
        return {
            'cpu_percent': 12.5,
            'memory_gb': 0.4,
            'status': 'Local Development'
        }
