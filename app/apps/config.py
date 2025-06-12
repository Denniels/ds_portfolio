"""
Configuración para la aplicación de Calidad del Agua
"""

# URLs de datos
DATA_SOURCES = {
    'water_quality': "https://datos.gob.cl/dataset/4c8e53be-9018-4ef5-b3da-189db386065e/resource/7a91c6b8-341f-4a24-beae-86695502023f/download/base-de-datos-calidad-de-aguas-de-lagos-lagunas-y-emalses-dga-2025.xlsx"
}

# Parámetros de calidad del agua y sus rangos óptimos
WATER_QUALITY_PARAMETERS = {
    'Temperatura Temperatura muestra °C': {
        'name': 'Temperatura',
        'unit': '°C',
        'optimal_range': (10, 25),
        'description': 'Temperatura del agua'
    },
    'Ph a 25°C': {
        'name': 'pH',
        'unit': '',
        'optimal_range': (6.5, 8.5),
        'description': 'Potencial de hidrógeno (acidez/basicidad)'
    },
    'Conductividad Específica (µS/cm a 25°C)': {
        'name': 'Conductividad',
        'unit': 'µS/cm',
        'optimal_range': (100, 800),
        'description': 'Capacidad de conducir electricidad'
    },
    'Oxigeno Disuelto (% Saturacion)': {
        'name': 'Oxígeno Disuelto',
        'unit': '% Sat.',
        'optimal_range': (80, 120),
        'description': 'Porcentaje de saturación de oxígeno'
    },
    'Turbiedad (NTU)': {
        'name': 'Turbiedad',
        'unit': 'NTU',
        'optimal_range': (0, 5),
        'description': 'Claridad del agua'
    },
    'Solidos Suspendidos Totales ': {
        'name': 'Sólidos Suspendidos',
        'unit': 'mg/L',
        'optimal_range': (0, 25),
        'description': 'Partículas en suspensión'
    }
}

# Clasificación de calidad
QUALITY_CLASSIFICATION = {
    'Ph a 25°C': {
        'Excelente': (6.5, 8.5),
        'Buena': (6.0, 9.0),
        'Regular': (5.5, 9.5),
        'Deficiente': (0, 5.5)
    },
    'Oxigeno Disuelto (% Saturacion)': {
        'Excelente': (90, 120),
        'Buena': (70, 90),
        'Regular': (50, 70),
        'Deficiente': (0, 50)
    },
    'Turbiedad (NTU)': {
        'Excelente': (0, 1),
        'Buena': (1, 5),
        'Regular': (5, 25),
        'Deficiente': (25, 1000)
    },
    'Conductividad Específica (µS/cm a 25°C)': {
        'Excelente': (100, 500),
        'Buena': (500, 800),
        'Regular': (800, 1200),
        'Deficiente': (1200, 10000)
    }
}

# Colores para visualizaciones
COLORS = {
    'primary': '#0891b2',
    'secondary': '#06b6d4',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6'
}

# Configuración de mapas (coordenadas aproximadas de Chile)
MAP_CONFIG = {
    'chile_center': [-33.4489, -70.6693],
    'chile_zoom': 6,
    'default_zoom': 8
}

# Estaciones de demostración con coordenadas aproximadas
DEMO_STATIONS = {
    "EMBALSE RAPEL EN SECTOR BRAZO ALHUE": {"lat": -34.1, "lon": -71.2},
    "LAGO VILLARRICA EN SECTOR MOLCO": {"lat": -39.3, "lon": -72.1},
    "LAGO RIÑIHUE EN RIÑIHUE": {"lat": -39.8, "lon": -72.4},
    "LAGUNA GRANDE DE SAN PEDRO": {"lat": -18.1, "lon": -69.8},
    "EMBALSE EL YESO": {"lat": -33.7, "lon": -70.1},
    "LAGO LLANQUIHUE EN PUERTO VARAS": {"lat": -41.3, "lon": -72.9}
}

# Coordenadas de regiones chilenas para mapas de emisiones
CHILE_REGIONS = {
    "Arica y Parinacota": {"lat": -18.4783, "lon": -70.3126, "zoom": 8},
    "Tarapacá": {"lat": -20.2140, "lon": -70.1522, "zoom": 8},
    "Antofagasta": {"lat": -23.6509, "lon": -70.3975, "zoom": 7},
    "Atacama": {"lat": -27.3668, "lon": -70.3323, "zoom": 7},
    "Coquimbo": {"lat": -29.9533, "lon": -71.3436, "zoom": 8},
    "Valparaíso": {"lat": -33.0472, "lon": -71.6127, "zoom": 8},
    "Metropolitana": {"lat": -33.4489, "lon": -70.6693, "zoom": 9},
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

# Sectores económicos principales para emisiones CO2
CO2_EMISSION_SECTORS = {
    "Generación Eléctrica": {"color": "#dc2626", "icon": "bolt"},
    "Industria": {"color": "#7c3aed", "icon": "factory"},
    "Transporte": {"color": "#059669", "icon": "truck"},
    "Minería": {"color": "#d97706", "icon": "hammer"},
    "Petroquímica": {"color": "#be185d", "icon": "oil-can"},
    "Otros": {"color": "#6b7280", "icon": "industry"}
}

# Tipos de contaminantes
POLLUTANT_TYPES = {
    "CO2": {"name": "Dióxido de Carbono", "color": "#ef4444"},
    "CH4": {"name": "Metano", "color": "#f59e0b"},
    "N2O": {"name": "Óxido Nitroso", "color": "#8b5cf6"},
    "CO": {"name": "Monóxido de Carbono", "color": "#06b6d4"},
    "NOx": {"name": "Óxidos de Nitrógeno", "color": "#10b981"}
}
