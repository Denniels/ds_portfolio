# Módulos organizados para el portafolio de Data Science
"""
Estructura modular para facilitar el mantenimiento:

- data_loaders.py: Funciones de carga y procesamiento de datos
- map_utils.py: Utilidades para mapas interactivos  
- chart_utils.py: Funciones para gráficos y visualizaciones
- water_quality.py: Específico para calidad del agua
- emissions.py: Específico para emisiones CO2
- config.py: Configuraciones centralizadas
"""

from .data_loaders import *
from .map_utils import *
from .chart_utils import *
from .water_quality import *
from .emissions import *
from .config import *
