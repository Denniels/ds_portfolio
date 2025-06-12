"""
Configuraciones específicas para análisis de emisiones CO2
=========================================================
"""

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

# Escalas de emisiones para categorización
EMISSION_SCALES = {
    'high_emission': 100000,     # > 100k ton CO2
    'medium_emission': 10000,    # 10k - 100k ton CO2
    'low_emission': 1000,        # 1k - 10k ton CO2
    'minimal_emission': 0        # < 1k ton CO2
}

# Colores para escalas de emisión
EMISSION_COLORS = {
    'high': '#dc2626',      # Rojo
    'medium': '#f59e0b',    # Naranja
    'low': '#eab308',       # Amarillo
    'minimal': '#22c55e'    # Verde
}
