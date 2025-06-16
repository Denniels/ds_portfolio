import time
import psutil
import json
from pathlib import Path
from datetime import datetime

class CloudCostSimulator:
    # Precios de GCP Cloud Run (aproximados)
    GCP_PRICES = {
        'cpu': 0.00002400,  # por vCPU-segundo
        'memory': 0.00000250,  # por GiB-segundo
        'requests': 0.40,  # por millón de requests
        'network': 0.12,  # por GB
    }
    
    def __init__(self, output_dir='app/data/metrics'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.start_time = None
        self.metrics = []
        
    def start_measurement(self):
        """Inicia la medición de recursos"""
        self.start_time = time.time()
        self.start_cpu_percent = psutil.cpu_percent()
        self.start_memory = psutil.Process().memory_info().rss
        
    def stop_measurement(self, request_count=1):
        """Detiene la medición y calcula los costos simulados"""
        if not self.start_time:
            raise RuntimeError("Measurement not started")
        
        duration = time.time() - self.start_time
        cpu_percent = psutil.cpu_percent()
        memory_bytes = psutil.Process().memory_info().rss
        
        # Convertir métricas a unidades de GCP
        cpu_seconds = duration * (cpu_percent / 100)  # vCPU-segundos
        memory_gib_seconds = (memory_bytes / (1024**3)) * duration  # GiB-segundos
        
        # Calcular costos
        costs = {
            'cpu_cost': cpu_seconds * self.GCP_PRICES['cpu'],
            'memory_cost': memory_gib_seconds * self.GCP_PRICES['memory'],
            'request_cost': (request_count / 1_000_000) * self.GCP_PRICES['requests'],
        }
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': duration,
            'cpu_seconds': cpu_seconds,
            'memory_gib_seconds': memory_gib_seconds,
            'request_count': request_count,
            'costs': costs,
            'total_cost': sum(costs.values())
        }
        
        self.metrics.append(metrics)
        self._save_metrics()
        
        return metrics
    
    def _save_metrics(self):
        """Guarda las métricas en un archivo JSON"""
        metrics_file = self.output_dir / 'cloud_costs.json'
        
        # Calcular resumen
        summary = {
            'total_duration': sum(m['duration_seconds'] for m in self.metrics),
            'total_cpu_seconds': sum(m['cpu_seconds'] for m in self.metrics),
            'total_memory_gib_seconds': sum(m['memory_gib_seconds'] for m in self.metrics),
            'total_requests': sum(m['request_count'] for m in self.metrics),
            'total_cost': sum(m['total_cost'] for m in self.metrics),
            'average_cost_per_request': sum(m['total_cost'] for m in self.metrics) / sum(m['request_count'] for m in self.metrics),
            'last_updated': datetime.now().isoformat()
        }
        
        data = {
            'metrics': self.metrics,
            'summary': summary
        }
        
        with open(metrics_file, 'w') as f:
            json.dump(data, f, indent=2)

# Ejemplo de uso en un decorador
def measure_cloud_costs(simulator):
    def decorator(func):
        def wrapper(*args, **kwargs):
            simulator.start_measurement()
            result = func(*args, **kwargs)
            metrics = simulator.stop_measurement()
            return result
        return wrapper
    return decorator
