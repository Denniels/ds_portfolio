"""
Utilidades para manejo de coordenadas geográficas
"""
import json
from pathlib import Path
from typing import Dict, Optional
import numpy as np
import streamlit as st

# Rutas de archivos de coordenadas
COORDS_FILE = Path(__file__).parent.parent.parent / "data" / "estaciones_coordenadas.json"
CACHE_FILE = Path(__file__).parent.parent.parent / "data" / "cache_coordenadas_chile.json"

class CoordenadasEstaciones:
    def __init__(self):
        self.coordenadas = {}
        self.cache = {}
        self.load_data()
    
    def load_data(self):
        """Carga datos de coordenadas desde archivos"""
        try:
            # Cargar coordenadas verificadas
            if COORDS_FILE.exists():
                with open(COORDS_FILE, 'r', encoding='utf-8') as f:
                    self.coordenadas = json.load(f)
            
            # Cargar cache
            if CACHE_FILE.exists():
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    self.cache = json.load(f)
        except Exception as e:
            st.error(f"Error cargando datos de coordenadas: {e}")
    
    def save_cache(self):
        """Guarda el cache de coordenadas"""
        try:
            CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Error guardando cache: {e}")
    
    def get_coordinates(self, station_name: str) -> Optional[Dict]:
        """Obtiene coordenadas para una estación"""
        # 1. Verificar cache
        if station_name in self.cache:
            return self.cache[station_name]
        
        # 2. Buscar en coordenadas verificadas
        coords = None
        for cuerpo_agua, data in self.coordenadas.items():
            if station_name in data['estaciones']:
                coords = data['estaciones'][station_name]
                break
            # Si no encuentra exacto, buscar por nombre del cuerpo de agua
            elif cuerpo_agua in station_name.upper():
                base_coords = data['base']
                # Añadir variación para evitar superposición
                coords = {
                    "lat": base_coords["lat"] + np.random.uniform(-0.01, 0.01),
                    "lon": base_coords["lon"] + np.random.uniform(-0.01, 0.01)
                }
                break
        
        # Si encontró coordenadas, guardar en cache
        if coords:
            self.cache[station_name] = coords
            self.save_cache()
        
        return coords

# Instancia global
coordenadas_manager = CoordenadasEstaciones()

def get_station_coordinates(station_name: str) -> Optional[Dict]:
    """Obtiene coordenadas para una estación"""
    coords = coordenadas_manager.get_coordinates(station_name)
    if coords:
        st.success(f"✅ Coordenadas encontradas para: {station_name}")
    return coords
