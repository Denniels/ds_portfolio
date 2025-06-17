"""
Módulo de optimización de recursos y gestión de datos para la aplicación
"""
import os
import json
import pandas as pd
import numpy as np
import time
import psutil
from datetime import datetime, timedelta
from pathlib import Path
import streamlit as st

class ResourceOptimizer:
    """
    Clase para monitorear y optimizar el uso de recursos
    """
    def __init__(self):
        self.start_time = None
        self.start_memory = None
        self.metrics = []
        
        # Detectar entorno
        self.is_streamlit_cloud = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
        self.is_cloud_run = os.getenv('CLOUD_RUN_SERVICE', 'false').lower() == 'true'
        
        # Usar diferentes métricas según plataforma
        if self.is_streamlit_cloud:
            self.platform = "streamlit_cloud"
        elif self.is_cloud_run:
            self.platform = "cloud_run"
        else:
            self.platform = "local"
            
    def start_monitoring(self):
        """Inicia la monitorización de recursos"""
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss
        
    def get_metrics(self):
        """Obtiene métricas actuales sin detener el monitoreo"""
        if not self.start_time:
            return self._default_metrics()
            
        duration = time.time() - self.start_time
        current_memory = psutil.Process().memory_info().rss
        memory_increase = current_memory - self.start_memory
        memory_gb = current_memory / (1024 ** 3)
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': round(duration, 2),
            'memory_gb': round(memory_gb, 4),
            'memory_increase_mb': round(memory_increase / (1024 ** 2), 2),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'platform': self.platform
        }
        
        self.metrics.append(metrics)
        return metrics
        
    def stop_monitoring(self):
        """Detiene el monitoreo y retorna las métricas finales"""
        metrics = self.get_metrics()
        self.start_time = None
        self.start_memory = None
        return metrics
        
    def _default_metrics(self):
        """Devuelve métricas por defecto"""
        return {
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': 0,
            'memory_gb': 0,
            'memory_increase_mb': 0,
            'cpu_percent': 0,
            'memory_percent': 0,
            'platform': self.platform
        }
    
    @st.cache_data(ttl=60)
    def get_resource_usage(self):
        """Obtiene uso de recursos del sistema"""
        return {
            'memory_available_gb': round(psutil.virtual_memory().available / (1024 ** 3), 2),
            'cpu_available': round(100 - psutil.cpu_percent(), 1),
            'disk_free_gb': round(psutil.disk_usage('/').free / (1024 ** 3), 1)
        }
        
    def optimize_dataframe(self, df):
        """
        Optimiza el uso de memoria de un DataFrame
        
        Args:
            df (pd.DataFrame): DataFrame a optimizar
            
        Returns:
            pd.DataFrame: DataFrame optimizado
        """
        if df is None or df.empty:
            return df
            
        # Copia para no modificar el original
        result = df.copy()
        
        # Optimizar tipos numéricos
        for col in result.select_dtypes(include=['int']).columns:
            c_min = result[col].min()
            c_max = result[col].max()
            
            # Seleccionar el tipo más pequeño posible
            if c_min >= 0:
                if c_max < 255:
                    result[col] = result[col].astype(np.uint8)
                elif c_max < 65535:
                    result[col] = result[col].astype(np.uint16)
                elif c_max < 4294967295:
                    result[col] = result[col].astype(np.uint32)
            else:
                if c_min > -128 and c_max < 127:
                    result[col] = result[col].astype(np.int8)
                elif c_min > -32768 and c_max < 32767:
                    result[col] = result[col].astype(np.int16)
                elif c_min > -2147483648 and c_max < 2147483647:
                    result[col] = result[col].astype(np.int32)
        
        # Optimizar floats
        for col in result.select_dtypes(include=['float']).columns:
            result[col] = result[col].astype(np.float32)
            
        # Convertir strings a categorías cuando sea apropiado
        for col in result.select_dtypes(include=['object']).columns:
            num_unique = result[col].nunique()
            if num_unique < len(result) * 0.5:  # Si menos del 50% son valores únicos
                result[col] = result[col].astype('category')
                
        return result

class DataManager:
    """
    Clase para gestionar la carga y procesamiento de datos
    """
    def __init__(self):
        # Determinar entorno
        self.is_streamlit_cloud = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
        self.is_cloud_run = os.getenv('CLOUD_RUN_SERVICE', 'false').lower() == 'true'
        
        # Definir rutas según entorno
        if self.is_streamlit_cloud:
            self.data_dir = Path('/app/data')
            self.notebooks_dir = Path('/app/notebooks')
        elif self.is_cloud_run:
            self.data_dir = Path('/app/data')
            self.notebooks_dir = Path('/app/notebooks')
        else:
            # En desarrollo local, usar rutas relativas
            self.data_dir = Path(__file__).parent.parent.parent / 'data'
            self.notebooks_dir = Path(__file__).parent.parent.parent / 'notebooks'
            
        # Asegurarse de que existe el directorio de datos
        os.makedirs(self.data_dir, exist_ok=True)
            
        # Definir subdirectorios
        self.raw_data_dir = self.data_dir / 'raw'
        self.processed_data_dir = self.data_dir / 'processed'
        self.results_data_dir = self.data_dir / 'results'
        
        # Crear directorios si no existen
        os.makedirs(self.raw_data_dir, exist_ok=True)
        os.makedirs(self.processed_data_dir, exist_ok=True)
        os.makedirs(self.results_data_dir, exist_ok=True)
        
        # Inicializar optimizador
        self.optimizer = ResourceOptimizer()
        
    @st.cache_data(ttl=3600)
    def load_data(self, file_path, file_type='csv', optimize=True):
        """
        Carga datos desde un archivo
        
        Args:
            file_path (str): Ruta al archivo
            file_type (str): Tipo de archivo ('csv', 'excel', 'json', 'pickle')
            optimize (bool): Si se debe optimizar el DataFrame
            
        Returns:
            pd.DataFrame: DataFrame con los datos
        """
        # Convertir string a Path si es necesario
        if isinstance(file_path, str):
            file_path = Path(file_path)
            
        # Si es una ruta relativa, añadir la ruta base
        if not file_path.is_absolute():
            # Intentar en cada directorio hasta encontrar el archivo
            if (self.processed_data_dir / file_path).exists():
                file_path = self.processed_data_dir / file_path
            elif (self.raw_data_dir / file_path).exists():
                file_path = self.raw_data_dir / file_path
            elif (self.results_data_dir / file_path).exists():
                file_path = self.results_data_dir / file_path
            elif (self.data_dir / file_path).exists():
                file_path = self.data_dir / file_path
        
        # Verificar que el archivo existe
        if not file_path.exists():
            st.error(f"No se encontró el archivo: {file_path}")
            return None
            
        try:
            # Cargar según el tipo de archivo
            if file_type.lower() == 'csv':
                df = pd.read_csv(file_path)
            elif file_type.lower() in ['excel', 'xlsx', 'xls']:
                df = pd.read_excel(file_path)
            elif file_type.lower() == 'json':
                df = pd.read_json(file_path)
            elif file_type.lower() == 'pickle':
                df = pd.read_pickle(file_path)
            else:
                st.error(f"Tipo de archivo no soportado: {file_type}")
                return None
                
            # Optimizar si se solicita
            if optimize:
                df = self.optimizer.optimize_dataframe(df)
                
            return df
        except Exception as e:
            st.error(f"Error al cargar el archivo {file_path}: {e}")
            return None
    
    def save_data(self, df, file_path, file_type='csv'):
        """
        Guarda datos en un archivo
        
        Args:
            df (pd.DataFrame): DataFrame a guardar
            file_path (str): Ruta al archivo
            file_type (str): Tipo de archivo ('csv', 'excel', 'json', 'pickle')
            
        Returns:
            bool: True si se guardó correctamente
        """
        # Convertir string a Path si es necesario
        if isinstance(file_path, str):
            file_path = Path(file_path)
            
        # Si es una ruta relativa, añadir la ruta base
        if not file_path.is_absolute():
            file_path = self.results_data_dir / file_path
        
        # Crear directorio si no existe
        os.makedirs(file_path.parent, exist_ok=True)
        
        try:
            # Guardar según el tipo de archivo
            if file_type.lower() == 'csv':
                df.to_csv(file_path, index=False)
            elif file_type.lower() in ['excel', 'xlsx', 'xls']:
                df.to_excel(file_path, index=False)
            elif file_type.lower() == 'json':
                df.to_json(file_path, orient='records')
            elif file_type.lower() == 'pickle':
                df.to_pickle(file_path)
            else:
                st.error(f"Tipo de archivo no soportado: {file_type}")
                return False
                
            return True
        except Exception as e:
            st.error(f"Error al guardar el archivo {file_path}: {e}")
            return False
    
    def get_last_update(self, notebook_name):
        """
        Obtiene la fecha de última actualización de un notebook
        
        Args:
            notebook_name (str): Nombre del notebook (sin extensión)
            
        Returns:
            str: Fecha de última actualización en formato DD/MM/YYYY
        """
        # Buscar notebook
        notebook_path = None
        for path in self.notebooks_dir.glob(f"{notebook_name}*.ipynb"):
            notebook_path = path
            break
            
        if notebook_path and notebook_path.exists():
            # Obtener fecha de modificación
            mod_time = datetime.fromtimestamp(notebook_path.stat().st_mtime)
            return mod_time.strftime("%d/%m/%Y")
        else:
            # Si no encuentra el notebook, usar la fecha actual
            return datetime.now().strftime("%d/%m/%Y")
