"""
Punto de Entrada Legacy para Utilidades del Portafolio
======================================================

Este archivo mantiene retrocompatibilidad re-exportando funciones desde 
la nueva arquitectura modular. Para nuevos desarrollos, usar directamente
los módulos especializados en /modules/

Migración completada: todas las funciones ahora están organizadas en módulos especializados:
- data_loaders.py: Carga y procesamiento de datos
- water_quality.py: Análisis de calidad del agua  
- emissions.py: Análisis de emisiones CO2
- chart_utils.py: Gráficos y visualizaciones
- map_utils.py: Mapas interactivos
- config/: Configuraciones especializadas
"""

# Re-exportar funciones desde módulos especializados para retrocompatibilidad
from apps.modules.data_loaders import (
    load_water_quality_data,
    process_water_data,
    load_emissions_data,
    diagnose_excel_structure,
    convert_numeric_columns
)

from apps.modules.water_quality import (
    create_demo_water_data,
    calculate_water_quality_index,
    get_water_quality_summary_statistics,
    filter_water_data
)

from apps.modules.emissions import (
    create_demo_emissions_data,
    process_real_emissions_data,
    classify_emission_level,
    get_emission_color
)

from apps.modules.chart_utils import (
    create_temporal_chart,
    create_station_comparison_chart,
    create_correlation_heatmap,
    create_seasonal_analysis_chart,
    create_distribution_chart
)

from apps.modules.map_utils import (
    create_interactive_water_quality_map,
    create_interactive_emissions_map
)

from apps.modules.config import (
    COLORS,
    MAP_CONFIG,
    DEMO_STATIONS
)

from apps.modules.water_quality_config import (
    WATER_QUALITY_PARAMETERS,
    QUALITY_CLASSIFICATION
)

from apps.modules.emissions_config import (
    CO2_EMISSION_SECTORS,
    POLLUTANT_TYPES,
    EMISSION_SCALES,
    EMISSION_COLORS
)

# Mantener función de estadísticas con nombre legacy
def get_summary_statistics(df, parameters):
    """Alias para retrocompatibilidad - usa get_water_quality_summary_statistics"""
    from apps.modules.water_quality import get_water_quality_summary_statistics
    return get_water_quality_summary_statistics(df, parameters)

# Información de la migración
__version__ = "2.0.0"
__migration_date__ = "2025-06-11"
__note__ = """
Todas las funciones han sido migradas a módulos especializados.
Este archivo mantiene compatibilidad hacia atrás.
Para nuevo código, usar imports directos desde /modules/
"""
