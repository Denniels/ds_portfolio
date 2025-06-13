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

## � Despliegue y Exportación

Estas utilidades también incluyen funciones para exportar resultados y visualizaciones para despliegue:

### Exportación para GitHub Pages
```python
from utils.export_utils import export_map_for_github_pages

# Exportar mapa para GitHub Pages
export_map_for_github_pages(mapa, "mapa_estaciones_calidad_agua.html", 
                           thumbnail=True, optimize=True)
```

### Preparación para Despliegue Cloud
```python
from utils.cloud_utils import prepare_data_for_cloud

# Optimizar datos para despliegue
df_optimized = prepare_data_for_cloud(df_original)
```

Para instrucciones detalladas sobre el despliegue de las visualizaciones y aplicaciones:
- [Despliegue en Google Cloud Run](../../docs/roadmap_google_cloud_run.md)
- [Despliegue en VM de GCP](../../docs/despliegue_vm_gcp.md)
- [Despliegue en GitHub Pages](../../docs/despliegue_github_pages.md)

## �🛠️ Mantenimiento

- Cache de geocodificación se almacena localmente
- Logs de progreso se muestran en consola
- Configuración optimizada para APIs gratuitas
