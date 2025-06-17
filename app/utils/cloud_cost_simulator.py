"""
Simulador de costos y métricas para Google Cloud Run
"""
import time
import random
from datetime import datetime
import streamlit as st

class CloudCostSimulator:
    """
    Simulador de métricas y costos para aplicaciones en Google Cloud Run
    """
    def __init__(self):
        self.start_time = None
        self.metrics = []
        self.cost_per_gb_memory_hour = 0.00001875  # $0.00001875 por GB-segundo
        self.cost_per_cpu_hour = 0.00002400        # $0.00002400 por CPU-segundo
        self.total_cost = 0.0
        
    def start_measurement(self):
        """Inicia la medición simulada de recursos y costos"""
        self.start_time = time.time()
    
    def stop_measurement(self):
        """Detiene la medición y devuelve métricas simuladas para Cloud Run"""
        if not self.start_time:
            return self._get_default_metrics()
        
        duration = time.time() - self.start_time
        
        # Simular uso de recursos optimizado para Cloud Run
        memory_gb = random.uniform(0.2, 0.3)
        cpu_percent = random.uniform(15, 30)
        
        # Calcular costo simulado
        memory_cost = memory_gb * self.cost_per_gb_memory_hour * (duration / 3600)
        cpu_cost = (cpu_percent / 100) * self.cost_per_cpu_hour * (duration / 3600)
        request_cost = 0.0000004  # $0.0000004 por solicitud
        
        total_request_cost = request_cost
        total_cost = memory_cost + cpu_cost + total_request_cost
        self.total_cost += total_cost
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'memory_gb': memory_gb,
            'cpu_percent': cpu_percent,
            'memory_percent': random.uniform(25, 40),
            'cost': {
                'memory_cost_usd': memory_cost,
                'cpu_cost_usd': cpu_cost,
                'request_cost_usd': total_request_cost,
                'total_cost_usd': total_cost,
                'accumulated_cost_usd': self.total_cost
            },
            'is_optimized': True,
            'platform': 'cloud_run'
        }
        
        self.metrics.append(metrics)
        return metrics
    
    def _get_default_metrics(self):
        """Devuelve métricas por defecto"""
        return {
            'cpu_percent': 20,
            'memory_gb': 0.25,
            'duration_seconds': 0,
            'cost': {
                'memory_cost_usd': 0,
                'cpu_cost_usd': 0,
                'request_cost_usd': 0,
                'total_cost_usd': 0,
                'accumulated_cost_usd': self.total_cost
            },
            'is_optimized': True,
            'platform': 'cloud_run'
        }
    
    @st.cache_data(ttl=60)
    def get_resource_usage(self):
        """Obtiene uso de recursos simulado para Cloud Run"""
        return {
            'memory_available_gb': random.uniform(0.6, 0.8),
            'cpu_available': random.uniform(65, 80),
            'disk_free_gb': random.uniform(0.9, 1.5),
            'estimated_monthly_cost': self.estimate_monthly_cost()
        }
    
    def estimate_monthly_cost(self):
        """Estima el costo mensual basado en el uso actual"""
        # Simular un costo mensual realista para una app en Cloud Run
        base_cost = random.uniform(5, 15)
        usage_multiplier = 1 + (self.total_cost * 1000)  # Amplificar el efecto del uso
        return min(base_cost * usage_multiplier, 50)  # Limitar a un máximo de $50
