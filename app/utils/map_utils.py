"""
Utilidades para la generación y manejo de mapas estáticos
"""
import folium
import geopandas as gpd
import pandas as pd
from pathlib import Path
import json
from datetime import datetime
import os

def generar_mapa_emisiones():
    """
    Genera un mapa estático de emisiones de CO2 en Chile
    """
    # Crear directorio para mapas estáticos si no existe
    static_maps_dir = Path(__file__).parent.parent / "static" / "maps"
    static_maps_dir.mkdir(parents=True, exist_ok=True)
    
    # Cargar datos de emisiones (simulados para ejemplo)
    regiones = {
        "Metropolitana": {"lat": -33.4489, "lon": -70.6693, "emisiones": 45.2},
        "Valparaíso": {"lat": -33.0458, "lon": -71.6197, "emisiones": 12.8},
        "Biobío": {"lat": -36.8201, "lon": -73.0443, "emisiones": 18.5},
        "Antofagasta": {"lat": -23.6509, "lon": -70.3975, "emisiones": 25.3},
        # ... más regiones
    }
    
    # Crear mapa base
    m = folium.Map(
        location=[-33.4489, -70.6693],
        zoom_start=5,
        tiles='cartodbpositron'
    )
    
    # Añadir marcadores de emisiones
    for region, data in regiones.items():
        # Color basado en nivel de emisiones
        color = 'red' if data['emisiones'] > 20 else 'orange' if data['emisiones'] > 10 else 'green'
        
        folium.CircleMarker(
            location=[data['lat'], data['lon']],
            radius=data['emisiones']/2,  # Tamaño proporcional a emisiones
            popup=f"{region}<br>Emisiones: {data['emisiones']} Mt CO2",
            color=color,
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
    
    # Añadir leyenda
    legend_html = """
    <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px;">
        <h4>Emisiones de CO2 (Mt)</h4>
        <p><i style="background: red; width: 10px; height: 10px; display: inline-block;"></i> > 20 Mt</p>
        <p><i style="background: orange; width: 10px; height: 10px; display: inline-block;"></i> 10-20 Mt</p>
        <p><i style="background: green; width: 10px; height: 10px; display: inline-block;"></i> < 10 Mt</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Guardar mapa
    timestamp = datetime.now().strftime("%Y%m")
    map_path = static_maps_dir / f"emisiones_co2_{timestamp}.html"
    m.save(str(map_path))
    
    # Guardar metadata
    metadata = {
        "fecha_generacion": datetime.now().isoformat(),
        "archivo": str(map_path),
        "tamaño_kb": os.path.getsize(map_path) / 1024,
        "regiones_incluidas": list(regiones.keys())
    }
    
    with open(static_maps_dir / f"emisiones_co2_{timestamp}_metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return str(map_path)

def obtener_mapa_actual():
    """
    Obtiene la ruta al mapa más reciente o genera uno nuevo si es necesario
    """
    static_maps_dir = Path(__file__).parent.parent / "static" / "maps"
    
    # Buscar mapa del mes actual
    timestamp = datetime.now().strftime("%Y%m")
    map_path = static_maps_dir / f"emisiones_co2_{timestamp}.html"
    
    if map_path.exists():
        return str(map_path)
    else:
        return generar_mapa_emisiones()

def cargar_mapa_emisiones(force_refresh=False):
    """
    Carga el mapa de emisiones, generando uno nuevo si es necesario
    """
    if force_refresh:
        return generar_mapa_emisiones()
    else:
        return obtener_mapa_actual()
