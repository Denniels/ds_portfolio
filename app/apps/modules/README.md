# 🔧 Módulos del Sistema - Data Science Portfolio

> **Estado**: ✅ **Sistema Modular Completo** - Arquitectura escalable y mantenible

## 🎯 Filosofía del Sistema Modular

Este directorio implementa una **arquitectura modular** que separa las responsabilidades en componentes reutilizables, facilitando:

1. **🔄 Reutilización**: Funciones utilizables por múltiples aplicaciones
2. **🧪 Testabilidad**: Módulos independientes fáciles de probar
3. **📈 Escalabilidad**: Agregar nuevas funcionalidades sin afectar existentes
4. **🛠️ Mantenibilidad**: Código organizado y fácil de mantener

## 📚 Módulos Disponibles

### ⚙️ **config.py** - Configuraciones Centralizadas
```python
# Configuraciones principales del sistema
MAP_CONFIG = {
    'chile_center': [-35.6751, -71.5430],
    'chile_zoom': 6,
    'default_zoom': 8
}

COLORS = {
    'primary': '#0891b2',
    'secondary': '#06b6d4',
    # ... paleta completa
}

DEMO_STATIONS = {
    "LAGO VILLARRICA EN PELAGIAL VILLARRICA": {"lat": -39.2553, "lon": -72.0857},
    # ... coordenadas verificadas
}
```

**🎯 Uso**:
```python
from apps.modules.config import MAP_CONFIG, COLORS, DEMO_STATIONS
```

### 📥 **data_loaders.py** - Cargadores de Datos
```python
def load_water_quality_data():
    """Carga datos de calidad del agua con validación automática"""
    
def load_emissions_data():
    """Carga datos de emisiones CO2 con procesamiento"""
    
def validate_data_quality(df):
    """Valida calidad e integridad de datasets"""
```

**🎯 Uso**:
```python
from apps.modules.data_loaders import load_water_quality_data

data, is_official = load_water_quality_data()
```

### 🗺️ **geo_utils.py** - Utilidades Geográficas
```python
class CoordenadasEstaciones:
    """Sistema inteligente de coordenadas con cache"""
    
def get_station_coordinates(station_name: str):
    """Obtiene coordenadas usando múltiples fuentes"""
    
def load_coordinates_cache():
    """Maneja cache persistente de coordenadas"""
```

**🎯 Uso**:
```python
from apps.modules.geo_utils import get_station_coordinates

coords = get_station_coordinates("LAGO LLANQUIHUE EN PUERTO VARAS")
```

### 🗺️ **map_utils.py** - Mapas Interactivos
```python
def create_interactive_water_quality_map(df, filters):
    """Crea mapas Folium con estaciones y datos"""
    
def create_interactive_emissions_map(df, region_col, emissions_col):
    """Mapas de emisiones por región"""
```

**🎯 Uso**:
```python
from apps.modules.map_utils import create_interactive_water_quality_map

mapa = create_interactive_water_quality_map(df, filtros)
```

### 📊 **chart_utils.py** - Gráficos y Visualizaciones
```python
def create_temporal_chart(df, parameter, station=None):
    """Gráficos temporales interactivos con Plotly"""
    
def create_station_comparison_chart(df, parameters, stations):
    """Comparaciones entre estaciones"""
    
def create_quality_distribution_chart(df, parameter):
    """Distribuciones de calidad"""
```

**🎯 Uso**:
```python
from apps.modules.chart_utils import create_temporal_chart

chart = create_temporal_chart(df, 'pH', 'LAGO_VILLARRICA')
```

### 💧 **water_quality.py** - Lógica de Calidad del Agua
```python
def create_demo_water_data():
    """Genera datos de demostración realistas"""
    
def calculate_water_quality_index(df, parameters):
    """Calcula índice de calidad del agua"""
    
def get_water_quality_summary_statistics(df, parameters):
    """Estadísticas resumidas por parámetro"""
    
def filter_water_data(df, filters):
    """Filtrado avanzado de datos"""
```

### 🏭 **emissions.py** - Lógica de Emisiones CO2
```python
def classify_emission_level(emission_value):
    """Clasifica nivel de emisión"""
    
def get_emission_color(emission_value):
    """Obtiene color para visualización"""
    
def calculate_emission_statistics(df):
    """Estadísticas de emisiones"""
```

### ⚙️ **water_quality_config.py** - Configuración Específica
```python
WATER_QUALITY_PARAMETERS = {
    'Ph a 25°C': {
        'name': 'pH',
        'unit': 'unidades',
        'optimal_range': (6.0, 8.5),
        'description': 'Potencial de hidrógeno'
    },
    # ... más parámetros
}

QUALITY_CLASSIFICATION = {
    'Ph a 25°C': {
        'Excelente': (6.5, 8.0),
        'Buena': (6.0, 8.5),
        'Regular': (5.5, 9.0),
        'Deficiente': (0, 14)
    }
    # ... más clasificaciones
}
```

### 🏭 **emissions_config.py** - Configuración de Emisiones
```python
EMISSION_COLORS = {
    'Muy Bajo': '#4ade80',
    'Bajo': '#84cc16', 
    'Medio': '#eab308',
    'Alto': '#f97316',
    'Muy Alto': '#dc2626'
}

EMISSION_THRESHOLDS = {
    'co2_ton': [0, 100, 500, 2000, 10000]
}
```

## 🔗 Sistema de Interconexiones

### 📋 **Dependencias entre Módulos**
```
config.py (base)
    ↓
data_loaders.py ← geo_utils.py ← map_utils.py
    ↓                ↓             ↓
water_quality.py → chart_utils.py → apps
    ↓                ↓
emissions.py → water_quality_config.py
                    ↓
               emissions_config.py
```

### 🔄 **Flujo de Datos Típico**
1. **📥 Carga**: `data_loaders.py` obtiene datos oficiales
2. **🗺️ Geocodificación**: `geo_utils.py` asigna coordenadas
3. **🧮 Procesamiento**: `water_quality.py` o `emissions.py` procesan datos
4. **📊 Visualización**: `chart_utils.py` y `map_utils.py` generan gráficos
5. **🎨 Presentación**: Apps de Streamlit integran todo

## 🚀 Patrón de Uso Recomendado

### 🎯 **Para Nuevas Aplicaciones**
```python
# app/apps/nueva_app.py
import streamlit as st
from modules.data_loaders import load_new_dataset
from modules.chart_utils import create_custom_chart
from modules.map_utils import create_custom_map
from modules.config import COLORS, MAP_CONFIG

def nueva_aplicacion():
    st.title("Nueva Aplicación")
    
    # Usar cargadores de datos
    data = load_new_dataset()
    
    # Usar utilidades de visualización
    chart = create_custom_chart(data)
    mapa = create_custom_map(data)
    
    # Presentar con configuración centralizada
    st.plotly_chart(chart, use_container_width=True)
    st_folium(mapa, width=800, height=600)
```

### 🔧 **Para Nuevos Módulos**
```python
# app/apps/modules/nuevo_modulo.py
"""
Nuevo módulo siguiendo convenciones del sistema
"""
import pandas as pd
import streamlit as st
from .config import COLORS, CONFIG_PARAM
from .data_loaders import base_data_loader

def nueva_funcionalidad(data, parametros):
    """
    Nueva funcionalidad del sistema
    
    Args:
        data: DataFrame con datos
        parametros: Dict con configuración
        
    Returns:
        resultado: Resultado procesado
    """
    # Implementación usando convenciones del sistema
    return resultado
```

## 📈 Mejores Prácticas

### ✅ **Convenciones de Código**
- **📝 Docstrings**: Toda función pública debe tener documentación
- **🏷️ Type Hints**: Usar typing para parámetros y retornos
- **🚨 Error Handling**: Manejo robusto de errores con feedback a usuario
- **⚡ Performance**: Cache cuando sea apropiado
- **🧪 Testeable**: Funciones puras cuando sea posible

### 🔧 **Estructura de Función Estándar**
```python
def funcion_modular(data: pd.DataFrame, parametros: Dict) -> Dict:
    """
    Descripción clara de la función
    
    Args:
        data: DataFrame con datos de entrada
        parametros: Configuración de la función
        
    Returns:
        Dict con resultados procesados
        
    Raises:
        ValueError: Si los datos no son válidos
    """
    try:
        # Validación de entrada
        if data.empty:
            st.warning("No hay datos para procesar")
            return {}
            
        # Procesamiento principal
        resultado = procesar_datos(data, parametros)
        
        # Feedback al usuario
        st.success(f"Procesados {len(data)} registros exitosamente")
        
        return resultado
        
    except Exception as e:
        st.error(f"Error en procesamiento: {str(e)}")
        return {}
```

## 🔮 Roadmap de Expansión

### 📋 **Próximos Módulos Planificados**
- **🤖 ml_utils.py**: Utilidades de machine learning
- **📊 api_clients.py**: Clientes para APIs gubernamentales
- **🔒 security_utils.py**: Utilidades de seguridad y validación
- **📤 export_utils.py**: Exportación a múltiples formatos
- **⚡ performance_utils.py**: Optimizaciones de rendimiento

### 🎯 **Mejoras Continuas**
- **📊 Métricas de rendimiento**: Monitoreo de performance
- **🧪 Testing automatizado**: Cobertura de tests
- **📚 Documentación auto-generada**: Docs desde docstrings
- **🔄 CI/CD Integration**: Automatización de despliegue

---

> **💡 Filosofía**: "Escribe una vez, usa en muchos lugares" - Cada módulo debe ser independiente pero integrable con el ecosistema completo.
