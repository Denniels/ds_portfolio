# Utils para Notebooks de Análisis Ambiental

Este directorio contiene utilidades especializadas para el análisis de datos ambientales en Chile.

## 📁 Contenido

### `geocodificador_chile.py`
Geocodificador inteligente específicamente diseñado para estaciones de monitoreo ambiental en Chile.

**Características:**
- Extracción automática de topónimos
- Múltiples fuentes de geocodificación
- Validación geográfica específica para Chile
- Cache local para eficiencia
- Generación de mapas interactivos

**Uso básico:**
```python
from utils.geocodificador_chile import GeocodificadorChile

geocoder = GeocodificadorChile()
df_geocodificado = geocoder.geocodificar_dataframe(df, columna_nombre='GLS_ESTACION')
mapa = geocoder.generar_mapa_estaciones(df_geocodificado)
```

## 🚀 Instalación de Dependencias

```bash
pip install geopy folium geopandas
```

## 📊 Integración con Notebooks

Los archivos en este directorio están diseñados para integrarse perfectamente con:
- `01_Analisis_Emisiones_CO2_Chile.ipynb`
- `02_Analisis_Calidad_Del_Agua.ipynb`

## 🛠️ Mantenimiento

- Cache de geocodificación se almacena localmente
- Logs de progreso se muestran en consola
- Configuración optimizada para APIs gratuitas
