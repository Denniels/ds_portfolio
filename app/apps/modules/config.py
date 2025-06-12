"""
Configuraciones centralizadas para el portafolio de Data Science
================================================================
"""

# URLs de datos
DATA_SOURCES = {
    'water_quality': "https://datos.gob.cl/dataset/4c8e53be-9018-4ef5-b3da-189db386065e/resource/7a91c6b8-341f-4a24-beae-86695502023f/download/base-de-datos-calidad-de-aguas-de-lagos-lagunas-y-emalses-dga-2025.xlsx"
}

# Configuración de mapas
MAP_CONFIG = {
    'chile_center': [-35.6751, -71.5430],  # Centro de Chile continental
    'chile_zoom': 6,
    'default_zoom': 8
}

# Colores para visualizaciones
COLORS = {
    'primary': '#0891b2',
    'secondary': '#06b6d4', 
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'red_scale': ['#fef2f2', '#fee2e2', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626'],
    'blue_scale': ['#eff6ff', '#dbeafe', '#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb']
}

# Coordenadas de regiones chilenas
CHILE_REGIONS = {
    "Arica y Parinacota": {"lat": -18.4783, "lon": -70.3126, "zoom": 8},
    "Tarapacá": {"lat": -20.2140, "lon": -70.1522, "zoom": 8},
    "Antofagasta": {"lat": -23.6509, "lon": -70.3975, "zoom": 7},
    "Atacama": {"lat": -27.3668, "lon": -70.3323, "zoom": 7},
    "Coquimbo": {"lat": -29.9533, "lon": -71.3436, "zoom": 8},
    "Valparaíso": {"lat": -33.0472, "lon": -71.6127, "zoom": 8},
    "Metropolitana de Santiago": {"lat": -33.4489, "lon": -70.6693, "zoom": 9},
    "O'Higgins": {"lat": -34.5755, "lon": -71.0022, "zoom": 8},
    "Maule": {"lat": -35.4264, "lon": -71.6554, "zoom": 8},
    "Ñuble": {"lat": -36.6063, "lon": -72.1034, "zoom": 8},
    "Biobío": {"lat": -36.8201, "lon": -73.0444, "zoom": 8},
    "Araucanía": {"lat": -38.9489, "lon": -72.3311, "zoom": 8},
    "Los Ríos": {"lat": -39.8196, "lon": -73.2424, "zoom": 8},
    "Los Lagos": {"lat": -41.4693, "lon": -72.9318, "zoom": 7},
    "Aysén": {"lat": -45.5719, "lon": -72.0635, "zoom": 6},
    "Magallanes": {"lat": -53.1638, "lon": -70.9171, "zoom": 5}
}

# Estaciones de demostración para calidad del agua
DEMO_STATIONS = {
    "LAGO VILLARRICA EN PELAGIAL VILLARRICA": {"lat": -39.2553317, "lon": -72.0857331},
    "EMBALSE RAPEL EN SECTOR BRAZO ALHUE": {"lat": -34.0415858, "lon": -71.5888203},
    "LAGUNA GRANDE DE SAN PEDRO EN SECTOR SUR": {"lat": -36.8582915, "lon": -73.1102597},
    "LAGO LLANQUIHUE EN PUERTO VARAS": {"lat": -41.1429898, "lon": -72.8062011},
    "LAGO RANCO EN FUTRONO": {"lat": -40.3216708, "lon": -72.4813502},
    "EMBALSE LA PALOMA EN BOCATOMA": {"lat": -30.7382785, "lon": -71.0203132},
    "LAGO CHAPO EN SECTOR HORNOPIREN": {"lat": -41.4511111, "lon": -72.5000000},
    "LAGO RIÑIHUE EN RIÑIHUE": {"lat": -39.7833333, "lon": -72.4500000},
    "EMBALSE COLBUN EN PARED PRESA": {"lat": -35.6866667, "lon": -71.4144444},
    "LAGO CALAFQUEN EN SECTOR COÑARIPE": {"lat": -39.5527778, "lon": -72.1541667}
}
