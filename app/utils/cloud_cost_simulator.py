import time
import psutil
import json
from pathlib import Path
from datetime import datetime

class CloudCostSimulator:
    """
    Simulador local de costos que NO se conecta a GCP.
    Solo simula localmente para fines de demostración.
    """
    
    # Precios simulados (no conecta con GCP)
    SIMULATION_PRICES = {
        'cpu': 0.00002400,  # simulado, no real
        'memory': 0.00000250,  # simulado, no real
        'requests': 0.40,  # simulado, no real
        'network': 0.12,  # simulado, no real
    }
    
    def __init__(self, output_dir='data/metrics'):
        """
        Inicializa el simulador en modo completamente local.
        No realiza ninguna conexión con GCP.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.start_time = None
        self.metrics = []
        self.is_local = True  # Siempre en modo local
        
        # Crear archivo de advertencia
        self._create_warning_file()
        
    def _create_warning_file(self):
        """
        Crea un archivo de advertencia para documentar que esto es solo una simulación
        """
        warning_file = self.output_dir / "SIMULATION_ONLY.txt"
        warning_text = """
        ¡ADVERTENCIA! - SIMULACIÓN LOCAL ÚNICAMENTE
        
        Este es un simulador de costos que opera COMPLETAMENTE EN MODO LOCAL.
        - NO se conecta a Google Cloud Platform
        - NO genera costos reales
        - NO requiere credenciales de GCP
        - Todos los valores son simulados para fines de demostración
        
        Los costos mostrados son estimaciones aproximadas basadas en:
        1. Uso local de CPU
        2. Uso local de memoria
        3. Contadores locales de solicitudes
        
        NO USE ESTOS VALORES PARA DECISIONES FINANCIERAS REALES.
        
        Última actualización: {}
        """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        with open(warning_file, 'w', encoding='utf-8') as f:
            f.write(warning_text)
    
    def start_measurement(self):
        """Inicia la medición local de recursos (sin conexión a GCP)"""
        self.start_time = time.time()
        self.start_cpu_percent = psutil.cpu_percent()
        self.start_memory = psutil.Process().memory_info().rss
    
    def stop_measurement(self, request_count=1):
        """
        Detiene la medición y calcula los costos simulados.
        Todos los cálculos son locales y simulados.
        """
        if not self.start_time:
            return {
                'cpu_percent': 0,
                'memory_gb': 0,
                'cpu_cost': 0,
                'memory_cost': 0,
                'request_cost': 0,
                'total_cost': 0,
                'is_simulation': True
            }
        
        duration = time.time() - self.start_time
        cpu_percent = psutil.cpu_percent()
        memory_bytes = psutil.Process().memory_info().rss
        
        # Cálculos simulados (no reales)
        memory_gb = memory_bytes / (1024**3)
        cpu_cost = (duration * (cpu_percent / 100)) * self.SIMULATION_PRICES['cpu']
        memory_cost = (memory_gb * duration) * self.SIMULATION_PRICES['memory']
        request_cost = (request_count / 1_000_000) * self.SIMULATION_PRICES['requests']
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': cpu_percent,
            'memory_gb': memory_gb,
            'cpu_cost': cpu_cost,
            'memory_cost': memory_cost,
            'request_cost': request_cost,
            'total_cost': cpu_cost + memory_cost + request_cost,
            'is_simulation': True,  # Indicador explícito de que es una simulación
            'warning': "Estos son costos simulados, NO reales"
        }
        
        self.metrics.append(metrics)
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
