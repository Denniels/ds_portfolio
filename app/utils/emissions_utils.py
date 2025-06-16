"""
Utilidades para manejo optimizado de datos de emisiones
"""
import pandas as pd
import folium
from pathlib import Path
import json
from datetime import datetime
import streamlit as st

class EmisionesDataManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.cache_dir = self.data_dir / "cache"
        self.static_dir = Path(__file__).parent.parent / "static" / "maps"
        self._ensure_dirs()

    def _ensure_dirs(self):
        """Asegura que existan los directorios necesarios"""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)

    @st.cache_data
    def get_emisiones_data(self):
        """Obtiene datos de emisiones con caché de Streamlit"""
        cache_file = self.cache_dir / "emisiones_anuales.json"
        
        if not cache_file.exists():
            # Datos simulados (se reemplazarían con datos reales en producción)
            data = {
                "años": list(range(2010, 2024)),
                "emisiones": [70.5, 72.3, 74.8, 76.1, 77.5, 79.2, 80.6, 
                            81.8, 82.5, 83.6, 79.8, 80.5, 83.7, 85.2]
            }
            
            # Guardar en caché
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        
        # Cargar desde caché
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        return pd.DataFrame({
            'Año': data['años'],
            'Emisiones_CO2_Mt': data['emisiones']
        })

    @st.cache_data
    def get_emisiones_regionales(self):
        """Obtiene datos regionales con caché de Streamlit"""
        cache_file = self.cache_dir / "emisiones_regionales.json"
        
        if not cache_file.exists():
            # Datos simulados por región
            data = {
                "Metropolitana": {"lat": -33.4489, "lon": -70.6693, "emisiones": 45.2},
                "Valparaíso": {"lat": -33.0458, "lon": -71.6197, "emisiones": 12.8},
                "Biobío": {"lat": -36.8201, "lon": -73.0443, "emisiones": 18.5},
                "Antofagasta": {"lat": -23.6509, "lon": -70.3975, "emisiones": 25.3},
                "O'Higgins": {"lat": -34.1708, "lon": -70.7444, "emisiones": 15.6},
                "Maule": {"lat": -35.4264, "lon": -71.6553, "emisiones": 8.9},
                "Araucanía": {"lat": -38.7359, "lon": -72.5904, "emisiones": 7.4},
                "Los Lagos": {"lat": -41.4693, "lon": -72.9424, "emisiones": 6.8}
            }
            
            # Guardar en caché
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        
        # Cargar desde caché
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        return data

    @st.cache_data
    def generate_emissions_map(self):
        """Genera mapa de emisiones con caché"""
        map_file = self.static_dir / "emisiones_latest.html"
        
        # Si el mapa ya existe y es de hoy, retornarlo
        if map_file.exists():
            last_modified = datetime.fromtimestamp(map_file.stat().st_mtime)
            if last_modified.date() == datetime.now().date():
                with open(map_file, 'r', encoding='utf-8') as f:
                    return f.read()
        
        # Crear nuevo mapa
        data = self.get_emisiones_regionales()
        m = folium.Map(
            location=[-35.6751, -71.5430],  # Centro de Chile
            zoom_start=6,
            tiles='cartodbpositron'
        )
        
        # Añadir marcadores y heatmap
        locations = []
        weights = []
        for region, info in data.items():
            # Marcador con popup
            folium.CircleMarker(
                location=[info['lat'], info['lon']],
                radius=info['emisiones']/2,
                popup=f"{region}<br>Emisiones: {info['emisiones']} Mt CO2",
                color='red' if info['emisiones'] > 20 else 'orange' if info['emisiones'] > 10 else 'green',
                fill=True,
                fill_opacity=0.6
            ).add_to(m)
            
            # Datos para heatmap
            locations.append([info['lat'], info['lon']])
            weights.append(info['emisiones'])
        
        # Añadir heatmap
        folium.plugins.HeatMap(
            locations,
            weights,
            min_opacity=0.3,
            max_val=max(weights),
            radius=25,
            blur=15,
            gradient={0.4: 'blue', 0.65: 'lime', 0.8: 'yellow', 1: 'red'}
        ).add_to(m)
        
        # Añadir leyenda
        legend_html = """
        <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white;
                    padding: 10px; border: 2px solid grey; border-radius: 5px;">
            <h4>Emisiones de CO2 (Mt)</h4>
            <p><i style="background: red; width: 10px; height: 10px; display: inline-block;"></i> > 20 Mt</p>
            <p><i style="background: orange; width: 10px; height: 10px; display: inline-block;"></i> 10-20 Mt</p>
            <p><i style="background: green; width: 10px; height: 10px; display: inline-block;"></i> < 10 Mt</p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Guardar mapa
        m.save(str(map_file))
        
        with open(map_file, 'r', encoding='utf-8') as f:
            return f.read()

    def get_summary_stats(self):
        """Obtiene estadísticas resumen de emisiones"""
        df = self.get_emisiones_data()
        data = self.get_emisiones_regionales()
        
        return {
            "total_actual": df['Emisiones_CO2_Mt'].iloc[-1],
            "cambio_anual": (df['Emisiones_CO2_Mt'].iloc[-1] - df['Emisiones_CO2_Mt'].iloc[-2]) / df['Emisiones_CO2_Mt'].iloc[-2] * 100,
            "max_region": max(data.items(), key=lambda x: x[1]['emisiones'])[0],
            "min_region": min(data.items(), key=lambda x: x[1]['emisiones'])[0]
        }
