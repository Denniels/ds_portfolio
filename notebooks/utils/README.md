# 🛠️ Utilidades para Notebooks - Sistema Integrado

> **Estado**: ✅ **Integrado** con el sistema modular de `app/apps/modules/`

## 🎯 Propósito

Este directorio contiene utilidades especializadas para notebooks que complementan y extienden las funcionalidades del sistema modular principal. Estas herramientas están diseñadas para:

1. **🔬 Investigación avanzada** en notebooks
2. **🧪 Prototipado** de nuevas funcionalidades  
3. **📊 Análisis especializados** específicos de Chile
4. **🗺️ Geocodificación inteligente** para datos ambientales

## 📁 Contenido del Directorio

### 🗺️ `geocodificador_chile.py` - **Sistema de Geocodificación Inteligente**

**🔗 Estado**: ✅ Integrado con `app/apps/modules/geo_utils.py`

**🎯 Funcionalidades**:
- **Extracción automática** de topónimos chilenos
- **Múltiples fuentes** de geocodificación (Nominatim, Google, MapBox)
- **Validación geográfica** específica para territorio chileno
- **Cache local persistente** para optimización de consultas
- **Generación automática** de mapas interactivos
- **Manejo robusto** de errores y timeouts

**💻 Uso en Notebooks**:
```python
# Importación directa desde notebooks
from utils.geocodificador_chile import GeocodificadorChile

# Inicializar geocodificador
geocoder = GeocodificadorChile()

# Geocodificar DataFrame completo
df_with_coords = geocoder.geocodificar_dataframe(
    df, 
    columna_nombre='GLS_ESTACION',
    cache_file='cache_estaciones.json'
)

# Generar mapa interactivo
mapa = geocoder.generar_mapa_estaciones(df_with_coords)
mapa.save('mapa_estaciones.html')
```

**🔧 Integración con Sistema Modular**:
```python
# Las funcionalidades también están disponibles en el sistema principal
from app.apps.modules.geo_utils import get_station_coordinates
from app.apps.modules.map_utils import create_interactive_water_quality_map

# Coordenadas obtenidas automáticamente
coords = get_station_coordinates("LAGO VILLARRICA EN PELAGIAL")
```

### 📊 `visualizaciones_helper.py` - **Asistente de Visualizaciones**

**🔗 Estado**: ✅ Migrado a `app/apps/modules/chart_utils.py`

**🎯 Funcionalidades Originales** (ahora en módulos principales):
- Gráficos temporales interactivos
- Mapas de calor de correlaciones  
- Visualizaciones geoespaciales
- Dashboards personalizados

## 🔄 Flujo de Trabajo Integrado

### 📋 **Workflow Recomendado**

1. **🔬 Investigación en Notebooks**:
```python
# Usar utilidades específicas para exploración
from utils.geocodificador_chile import GeocodificadorChile
from utils import visualizaciones_helper

# Desarrollo y experimentación libre
geocoder = GeocodificadorChile()
estaciones_geo = geocoder.explorar_patrones_geograficos(df)
```

2. **🧪 Prototipado Avanzado**:
```python
# Probar nuevas funcionalidades antes de migrar a módulos
def nueva_funcionalidad_experimental(data):
    # Código experimental aquí
    return resultado

# Test en notebook antes de production
resultado = nueva_funcionalidad_experimental(mi_data)
```

3. **🚀 Migración a Producción**:
```python
# Una vez validado, migrar a sistema modular
# app/apps/modules/nueva_funcionalidad.py
def funcionalidad_produccion(data):
    # Código limpio y optimizado
    return resultado
```

## 🔧 Configuración y Dependencias

### ✅ **Prerrequisitos**
- **Python 3.8+** con entorno virtual activo
- **Conexión a internet** para APIs de geocodificación
- **Librerías especializadas**:

```bash
# Instalación de dependencias específicas
pip install geopy folium geopandas requests beautifulsoup4
pip install nominatim geojson shapely fiona
```

### ⚙️ **Configuración de APIs** (Opcional)

Para mayor precisión en geocodificación, configurar APIs:

```python
# Configuración en notebook o script
import os

# Google Geocoding API (opcional, mayor precisión)
os.environ['GOOGLE_API_KEY'] = 'tu_api_key_aqui'

# MapBox API (opcional, alternativa robusta)  
os.environ['MAPBOX_TOKEN'] = 'tu_mapbox_token_aqui'

# Nominatim es gratuito y funciona sin configuración
```

## 📈 Integración con Sistema Principal

### 🔗 **Conexión Bidireccional**

```python
# Desde notebooks: usar utilidades de producción
import sys
sys.path.append('../app')

from apps.modules.data_loaders import load_water_quality_data
from apps.modules.geo_utils import get_station_coordinates
from apps.modules.chart_utils import create_temporal_chart

# Desde sistema principal: usar utilidades experimentales
# app/apps/modules/experimental.py
import sys
sys.path.append('../../notebooks/utils')

from geocodificador_chile import GeocodificadorChile
```

### 📊 **Casos de Uso Comunes**

1. **🗺️ Geocodificación Masiva**:
```python
# Para procesar grandes datasets de estaciones
geocoder = GeocodificadorChile()
df_completo = geocoder.procesar_dataset_completo(
    'datos_estaciones_nacionales.csv',
    columna_estacion='nombre_estacion',
    batch_size=100
)
```

2. **📍 Validación de Coordenadas**:
```python
# Verificar precisión de coordenadas existentes
coords_validadas = geocoder.validar_coordenadas_existentes(df)
reporte_precision = geocoder.generar_reporte_calidad()
```

3. **🎯 Análisis de Cobertura Geográfica**:
```python
# Identificar gaps en monitoreo ambiental
gaps_geograficos = geocoder.analizar_cobertura_territorial(
    df_estaciones, 
    regiones_chile
)
```

## 🚀 Próximas Utilidades

### 🔮 **En Desarrollo**
- **🌐 API_client_chile.py**: Cliente para APIs gubernamentales chilenas
- **🧮 estadisticas_ambientales.py**: Funciones estadísticas especializadas
- **🏞️ topografia_chile.py**: Análisis de elevación y topografía

### 📋 **Roadmap**
1. **Geocodificación v2.0**: Integración con catastro nacional
2. **APIs Gubernamentales**: Conectores automáticos para datos oficiales
3. **ML Utils**: Utilidades para machine learning ambiental

---

> **💡 Consejo**: Estas utilidades están optimizadas para el contexto chileno y datos ambientales. Para uso general, considere las funciones en `app/apps/modules/`.
