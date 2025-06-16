"""
Gestor de caché optimizado para GCP
"""
import streamlit as st
from pathlib import Path
import json
import gzip
import time
from datetime import datetime, timedelta
import hashlib

class CacheManager:
    def __init__(self, cache_dir: Path = None):
        """
        Inicializa el gestor de caché
        
        Args:
            cache_dir: Directorio base para el caché. Si es None, usa app/data/cache
        """
        self.base_dir = cache_dir or Path(__file__).parent.parent / "data"
        self.cache_dir = self.base_dir / "cache"
        self.static_dir = self.base_dir / "static"
        
        # Asegurar que existan los directorios
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        """Crea los directorios necesarios si no existen"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)
        
        # Directorios específicos
        (self.static_dir / "estaciones").mkdir(exist_ok=True)
        (self.static_dir / "regiones").mkdir(exist_ok=True)
    
    @st.cache_data(ttl=3600)  # 1 hora de caché
    def get_emissions_data(self):
        """
        Obtiene datos de emisiones con caché de Streamlit
        """
        cache_file = self.cache_dir / "emisiones_anuales.json"
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # Manejo de error si el archivo no existe o está corrupto
            st.error("Error cargando datos de emisiones")
            return None
    
    @st.cache_data(ttl=86400)  # 24 horas de caché
    def get_regional_data(self):
        """
        Obtiene datos regionales con caché de Streamlit
        """
        cache_file = self.cache_dir / "emisiones_regionales.json"
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            st.error("Error cargando datos regionales")
            return None
    
    @st.cache_data(ttl=604800)  # 7 días de caché
    def get_station_coordinates(self):
        """
        Obtiene coordenadas de estaciones con caché de larga duración
        """
        coords_file = self.static_dir / "estaciones" / "coordenadas.json"
        
        try:
            with open(coords_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            st.error("Error cargando coordenadas de estaciones")
            return None
    
    def save_to_cache(self, data, cache_key: str, compress: bool = False):
        """
        Guarda datos en caché
        
        Args:
            data: Datos a guardar
            cache_key: Nombre del archivo sin extensión
            compress: Si se debe comprimir el archivo
        """
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if compress:
            cache_file = cache_file.with_suffix('.json.gz')
            with gzip.open(cache_file, 'wt', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    
    def save_static_data(self, data, category: str, name: str):
        """
        Guarda datos estáticos
        
        Args:
            data: Datos a guardar
            category: Categoría (estaciones/regiones)
            name: Nombre del archivo sin extensión
        """
        file_path = self.static_dir / category / f"{name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_cache_stats(self):
        """
        Obtiene estadísticas del caché
        """
        stats = {
            "cache_size": 0,
            "num_files": 0,
            "last_update": None
        }
        
        for file in self.cache_dir.glob("**/*"):
            if file.is_file():
                stats["num_files"] += 1
                stats["cache_size"] += file.stat().st_size
                stats["last_update"] = max(
                    stats["last_update"] or 0,
                    file.stat().st_mtime
                )
        
        if stats["last_update"]:
            stats["last_update"] = datetime.fromtimestamp(stats["last_update"])
        
        return stats

# Ejemplo de uso:
# cache_manager = CacheManager()
# emissions_data = cache_manager.get_emissions_data()
# regional_data = cache_manager.get_regional_data()
# coordinates = cache_manager.get_station_coordinates()
