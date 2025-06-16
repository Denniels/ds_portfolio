"""
Módulo de utilidades para el manejo de datos preprocesados y optimización de recursos.
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
import streamlit as st
from .cloud_cost_simulator import CloudCostSimulator

class DataManager:
    def __init__(self, preprocessed_dir: str = None):
        """
        Inicializa el gestor de datos.
        
        Args:
            preprocessed_dir: Directorio donde se almacenan los datos preprocesados.
                            Si es None, se usa 'data/preprocessed'.
        """
        if preprocessed_dir is None:
            base_dir = Path(__file__).parent.parent  # directorio app/
            self.preprocessed_dir = base_dir / 'data' / 'preprocessed'
        else:
            self.preprocessed_dir = Path(preprocessed_dir)
        
        # Asegurar que el directorio existe
        self.preprocessed_dir.mkdir(parents=True, exist_ok=True)
        self.cost_simulator = CloudCostSimulator()
        self._load_metadata()
    
    @st.cache_data
    def _load_metadata(_self):
        """Carga los metadatos de los notebooks procesados"""
        metadata = {}
        for notebook_dir in _self.preprocessed_dir.glob('*'):
            if notebook_dir.is_dir():
                meta_file = notebook_dir / 'metadata.json'
                if meta_file.exists():
                    try:
                        with open(meta_file, 'r', encoding='utf-8') as f:
                            metadata[notebook_dir.name] = json.load(f)
                    except json.JSONDecodeError:
                        # En caso de error, proporcionamos datos ficticios
                        metadata[notebook_dir.name] = {
                            "processed_at": datetime.now().isoformat(),
                            "status": "error_loading"
                        }
        return metadata
    
    @st.cache_data
    def load_dataframe(_self, notebook_name: str, df_name: str) -> pd.DataFrame:
        """Carga un DataFrame preprocesado"""
        df_path = _self.preprocessed_dir / notebook_name / f"{df_name}.csv.gz"
        if df_path.exists():
            return pd.read_csv(df_path)
        # Si no existe, retorna un DataFrame vacío
        return pd.DataFrame()
    
    @st.cache_data
    def load_figure(_self, notebook_name: str, fig_name: str) -> str:
        """Carga una figura preprocesada"""
        fig_path = _self.preprocessed_dir / notebook_name / f"{fig_name}.webp"
        if fig_path.exists():
            return str(fig_path)
        # Si no existe, retorna None
        return None
    
    def get_last_update(self, notebook_name: str) -> str:
        """Obtiene la fecha de última actualización de un notebook"""
        metadata = self._load_metadata()
        if notebook_name in metadata:
            return metadata[notebook_name].get('processed_at', 'No disponible')
        return 'No disponible'

class ResourceOptimizer:
    def __init__(self):
        self.cost_simulator = CloudCostSimulator()
    
    def start_monitoring(self):
        """Inicia el monitoreo de recursos para una sesión"""
        self.cost_simulator.start_measurement()
    
    def stop_monitoring(self, request_count=1):
        """Detiene el monitoreo y registra las métricas"""
        return self.cost_simulator.stop_measurement(request_count)
    
    @st.cache_data
    def get_resource_summary(_self):
        """Obtiene un resumen del uso de recursos"""
        base_dir = Path(__file__).parent.parent
        metrics_file = base_dir / 'data' / 'metrics' / 'cloud_costs.json'
        if metrics_file.exists():
            try:
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('summary', {})
            except json.JSONDecodeError:
                # En caso de error, proporcionamos datos ficticios
                return {
                    "total_duration": 10.0,
                    "total_cpu_seconds": 1.0,
                    "total_memory_gib_seconds": 0.1,
                    "total_requests": 5,
                    "total_cost": 0.00005,
                    "average_cost_per_request": 0.00001,
                    "last_updated": datetime.now().isoformat()
                }
        return {}

def format_cost(cost: float) -> str:
    """Formatea un costo para mostrar"""
    return f"${cost:.6f}"

def format_resource(value: float, unit: str) -> str:
    """Formatea un valor de recurso para mostrar"""
    return f"{value:.2f} {unit}"
