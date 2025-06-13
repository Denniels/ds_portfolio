"""
Configuración específica para despliegue en Cloud Run
"""
import os
from datetime import timedelta

# Configuración de caché
CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hora por defecto
MEMORY_CACHE_SIZE = 500  # MB

# Ajustes de rendimiento
STREAMLIT_SERVER_WORKERS = 1
STREAMLIT_SERVER_TIMEOUT = 60  # segundos

# Rutas específicas para Cloud
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials/default.json')

# Configuración de APIs externas
API_TIMEOUT = 15  # segundos
API_MAX_RETRIES = 3
API_BACKOFF_FACTOR = 0.5

# Configuración de visualizaciones
MAX_POINTS_VISUALIZATION = 5000  # Limitar puntos en visualizaciones pesadas

# Configuración de logs
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Configuración de manejo de memoria
OPTIMIZE_MEMORY = True  # Activar optimizaciones de memoria para entorno cloud

class CloudConfig:
    """Clase de configuración para despliegue en la nube"""
    
    @staticmethod
    def optimize_dataframe(df):
        """Optimiza el uso de memoria de un DataFrame para entorno cloud"""
        if not OPTIMIZE_MEMORY:
            return df
            
        # Convertir tipos para optimizar memoria
        for col in df.select_dtypes(include=['float64']).columns:
            df[col] = df[col].astype('float32')
            
        for col in df.select_dtypes(include=['int64']).columns:
            df[col] = df[col].astype('int32')
            
        return df
        
    @staticmethod
    def get_api_retry_config():
        """Retorna configuración de reintentos para APIs externas"""
        return {
            'total': API_MAX_RETRIES,
            'backoff_factor': API_BACKOFF_FACTOR,
            'status_forcelist': [500, 502, 503, 504]
        }
