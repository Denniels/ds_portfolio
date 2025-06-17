"""
Sistema de datos optimizado para Streamlit Community Cloud
Maneja datos precargados y fallbacks para la capa gratuita
"""

import streamlit as st
import json
import pandas as pd
from pathlib import Path
import os

class StreamlitCloudDataManager:
    """Gestor de datos optimizado para Streamlit Community Cloud"""
    
    def __init__(self, base_path=None):
        # Detectar entorno y configurar rutas
        self.is_cloud = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
        
        if base_path is None:
            # En Streamlit Cloud la estructura es diferente
            if self.is_cloud:
                self.base_path = Path(__file__).parent.parent / 'data' / 'cache'
            else:
                self.base_path = Path(__file__).parent / 'data' / 'cache'
        else:
            self.base_path = Path(base_path)
    
    @st.cache_data
    def load_co2_data(_self):
        """
        Carga datos de CO2 con fallbacks robustos para Streamlit Cloud
        """
        try:
            # Intentar cargar datos reales
            return _self._load_real_data()
        except Exception as e:
            st.warning(f"⚠️ Datos reales no disponibles: {str(e)}")
            st.info("📊 Usando datos de ejemplo para demostración")
            return _self._generate_demo_data()
    
    def _load_real_data(self):
        """Carga datos reales desde archivos JSON"""
        
        # Rutas de archivos
        files = {
            'emisiones_anuales': self.base_path / 'emisiones_anuales.json',
            'emisiones_regionales': self.base_path / 'emisiones_regionales.json', 
            'metadata': self.base_path / 'cache_metadata.json'
        }
        
        # Verificar que todos los archivos existan
        missing_files = [name for name, path in files.items() if not path.exists()]
        if missing_files:
            raise FileNotFoundError(f"Archivos faltantes: {missing_files}")
        
        # Cargar datos
        data = {}
        for name, path in files.items():
            with open(path, 'r', encoding='utf-8') as f:
                data[name] = json.load(f)
        
        # Validar datos
        if not data['emisiones_regionales'] or not data['emisiones_anuales']:
            raise ValueError("Datos vacíos o inválidos")
        
        return data
    
    def _generate_demo_data(self):
        """Genera datos de demostración cuando los reales no están disponibles"""
        
        # Datos de demostración basados en patrones reales de Chile
        demo_emisiones_regionales = {
            "Metropolitana": {
                "lat": -33.4489,
                "lon": -70.6693,
                "emisiones": 8500000,  # 8.5 Mt CO2
                "region_original": "Región Metropolitana"
            },
            "Antofagasta": {
                "lat": -23.6509,
                "lon": -70.3975,
                "emisiones": 2200000,  # 2.2 Mt CO2
                "region_original": "Antofagasta"
            },
            "Valparaíso": {
                "lat": -33.0472,
                "lon": -71.6127,
                "emisiones": 1800000,  # 1.8 Mt CO2
                "region_original": "Valparaíso"
            },
            "Biobío": {
                "lat": -36.8201,
                "lon": -73.0444,
                "emisiones": 1500000,  # 1.5 Mt CO2
                "region_original": "Biobío"
            },
            "O'Higgins": {
                "lat": -34.1701,
                "lon": -70.7400,
                "emisiones": 800000,   # 0.8 Mt CO2
                "region_original": "O'Higgins"
            }
        }
        
        demo_emisiones_anuales = {
            "2023": sum(region["emisiones"] for region in demo_emisiones_regionales.values())
        }
        
        demo_metadata = {
            "version": "demo",
            "generado_en": "2025-06-17",
            "tipo": "datos_demostración",
            "fuentes_datos": ["Datos sintéticos para demostración"],
            "ultima_actualizacion": "Demo - 17 junio 2025"
        }
        
        return {
            'emisiones_anuales': demo_emisiones_anuales,
            'emisiones_regionales': demo_emisiones_regionales,
            'metadata': demo_metadata
        }
    
    def get_stats(self, data):
        """Calcula estadísticas de los datos"""
        
        emisiones_regionales = data['emisiones_regionales']
        emisiones_anuales = data['emisiones_anuales']
        
        if not emisiones_regionales:
            return {}
        
        # Calcular estadísticas
        emisiones_list = [region['emisiones'] for region in emisiones_regionales.values()]
        total_emisiones = sum(emisiones_list)
        
        # Región con mayor y menor emisión
        region_mayor = max(emisiones_regionales.items(), key=lambda x: x[1]['emisiones'])
        region_menor = min(emisiones_regionales.items(), key=lambda x: x[1]['emisiones'])
        
        return {
            'total_emisiones_ton': total_emisiones,
            'total_regiones': len(emisiones_regionales),
            'total_instalaciones': 150,  # Estimado
            'region_mayor_emision': {
                'nombre': region_mayor[0],
                'emisiones': region_mayor[1]['emisiones']
            },
            'region_menor_emision': {
                'nombre': region_menor[0], 
                'emisiones': region_menor[1]['emisiones']
            }
        }
    
    def to_dataframe(self, data):
        """Convierte datos regionales a DataFrame para análisis"""
        
        emisiones_regionales = data['emisiones_regionales']
        
        data_list = []
        for region, info in emisiones_regionales.items():
            data_list.append({
                'Region': region,
                'lat': info['lat'],
                'lon': info['lon'], 
                'emisiones': info['emisiones'],
                'emisiones_mt': round(info['emisiones'] / 1000000, 2)
            })
        
        return pd.DataFrame(data_list)

# Función de conveniencia para uso en páginas
def get_co2_data_manager():
    """Retorna instancia del gestor de datos configurada"""
    return StreamlitCloudDataManager()

# Función específica para cargar datos CO2
@st.cache_data
def load_co2_data():
    """Función simplificada para cargar datos de CO2"""
    manager = get_co2_data_manager()
    return manager.load_co2_data()
