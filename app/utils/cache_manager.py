"""
Gestor de caché para la aplicación
"""
import os
import json
import pickle
from pathlib import Path
from datetime import datetime, timedelta
import hashlib

class CacheManager:
    """
    Clase para gestionar el caché de la aplicación
    """
    def __init__(self, cache_dir=None):
        """
        Inicializa el gestor de caché
        
        Args:
            cache_dir (Path, optional): Directorio para almacenar el caché. 
                                        Por defecto None, lo que crea un directorio en /tmp
        """
        if cache_dir is None:
            self.cache_dir = Path('/tmp/streamlit_cache')
        else:
            self.cache_dir = Path(cache_dir)
            
        # Asegurarse de que el directorio existe
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear subdirectorios para diferentes tipos de caché
        self.data_cache_dir = self.cache_dir / 'data'
        self.data_cache_dir.mkdir(exist_ok=True)
        
        self.map_cache_dir = self.cache_dir / 'maps'
        self.map_cache_dir.mkdir(exist_ok=True)
        
        # Archivo de metadatos
        self.metadata_file = self.cache_dir / 'cache_metadata.json'
        if not self.metadata_file.exists():
            self._init_metadata()
    
    def _init_metadata(self):
        """Inicializa el archivo de metadatos del caché"""
        metadata = {
            'created_at': datetime.now().isoformat(),
            'entries': {}
        }
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _get_cache_key(self, key, namespace=None):
        """
        Genera una clave única de caché
        
        Args:
            key (str): Clave principal
            namespace (str, optional): Espacio de nombres para agrupar cachés. Por defecto None.
            
        Returns:
            str: Clave única para usar en el sistema de archivos
        """
        if namespace:
            combined_key = f"{namespace}:{key}"
        else:
            combined_key = key
        
        # Generar hash para evitar problemas con nombres de archivo
        return hashlib.md5(combined_key.encode()).hexdigest()
    
    def save_data(self, data, key, namespace=None, expires=None):
        """
        Guarda datos en caché
        
        Args:
            data: Datos a guardar (debe ser serializable)
            key (str): Clave de caché
            namespace (str, optional): Espacio de nombres. Por defecto None.
            expires (int, optional): Tiempo de expiración en segundos. Por defecto None (no expira).
            
        Returns:
            bool: True si se guardó correctamente
        """
        cache_key = self._get_cache_key(key, namespace)
        file_path = self.data_cache_dir / f"{cache_key}.pickle"
        
        try:
            # Guardar datos
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            
            # Actualizar metadatos
            self._update_metadata(cache_key, key, namespace, expires)
            return True
        except Exception as e:
            print(f"Error al guardar en caché: {e}")
            return False
    
    def load_data(self, key, namespace=None, default=None):
        """
        Carga datos desde caché
        
        Args:
            key (str): Clave de caché
            namespace (str, optional): Espacio de nombres. Por defecto None.
            default: Valor por defecto si no existe caché o ha expirado
            
        Returns:
            Datos cargados o valor por defecto
        """
        cache_key = self._get_cache_key(key, namespace)
        file_path = self.data_cache_dir / f"{cache_key}.pickle"
        
        # Verificar si existe y no ha expirado
        if file_path.exists() and not self._is_expired(cache_key):
            try:
                with open(file_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error al cargar desde caché: {e}")
                return default
        return default
    
    def _update_metadata(self, cache_key, original_key, namespace, expires):
        """Actualiza los metadatos para una entrada de caché"""
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            expiry_time = None
            if expires:
                expiry_time = (datetime.now() + timedelta(seconds=expires)).isoformat()
            
            metadata['entries'][cache_key] = {
                'key': original_key,
                'namespace': namespace,
                'created_at': datetime.now().isoformat(),
                'expires_at': expiry_time
            }
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"Error al actualizar metadatos: {e}")
    
    def _is_expired(self, cache_key):
        """Verifica si una entrada de caché ha expirado"""
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            entry = metadata['entries'].get(cache_key)
            if not entry:
                return True
            
            if entry.get('expires_at'):
                expiry_time = datetime.fromisoformat(entry['expires_at'])
                return datetime.now() > expiry_time
            
            return False
        except Exception as e:
            print(f"Error al verificar expiración: {e}")
            return True
    
    def clear_cache(self, namespace=None):
        """
        Limpia el caché
        
        Args:
            namespace (str, optional): Si se proporciona, solo limpia las entradas de ese namespace
        """
        try:
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            entries_to_remove = []
            
            for cache_key, entry in metadata['entries'].items():
                if namespace is None or entry.get('namespace') == namespace:
                    # Eliminar archivo
                    file_path = self.data_cache_dir / f"{cache_key}.pickle"
                    if file_path.exists():
                        os.remove(file_path)
                    entries_to_remove.append(cache_key)
            
            # Actualizar metadatos
            for key in entries_to_remove:
                metadata['entries'].pop(key, None)
            
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error al limpiar caché: {e}")
            return False
    
    def get_cache_size(self, namespace=None):
        """
        Obtiene el tamaño total del caché
        
        Args:
            namespace (str, optional): Si se proporciona, solo cuenta las entradas de ese namespace
            
        Returns:
            int: Tamaño en bytes
        """
        total_size = 0
        
        if namespace:
            # Si se especifica un namespace, cargar metadatos para filtrar
            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)
            
            for cache_key, entry in metadata['entries'].items():
                if entry.get('namespace') == namespace:
                    file_path = self.data_cache_dir / f"{cache_key}.pickle"
                    if file_path.exists():
                        total_size += file_path.stat().st_size
        else:
            # Si no hay namespace, sumar tamaño de todos los archivos
            for file_path in self.data_cache_dir.glob('*.pickle'):
                total_size += file_path.stat().st_size
        
        return total_size
