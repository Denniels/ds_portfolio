"""
Configuraciones específicas para análisis de calidad del agua
============================================================
"""

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
