# Guía de Despliegue en Streamlit Community Cloud

## 📁 Estructura de Archivos para el Despliegue

```plaintext
ds_portfolio/
├── app/                        # Directorio principal de la aplicación
│   ├── main.py                # Punto de entrada principal
│   ├── pages/                 # Páginas de la aplicación
│   │   ├── 01_emisiones_co2.py
│   │   ├── 02_calidad_agua.py
│   │   ├── 03_demografia_bigquery.py
│   │   ├── 04_presupuesto_publico.py
│   │   ├── 05_curriculum.py
│   │   ├── 06_servicios.py
│   │   └── 07_feedback.py
│   ├── utils/                 # Utilidades
│   │   ├── cache_manager.py
│   │   ├── cloud_cost_simulator.py
│   │   ├── content_manager.py
│   │   ├── data_sources.py
│   │   ├── emissions_utils.py
│   │   ├── feedback_utils.py
│   │   ├── menu_utils.py
│   │   └── optimization.py
│   ├── data/                  # Datos y recursos
│   │   ├── cache/            # Caché de datos
│   │   │   ├── emisiones_anuales.json
│   │   │   └── emisiones_regionales.json
│   │   ├── feedback/         # Datos de feedback
│   │   │   └── comments.json
│   │   ├── preprocessed/     # Datos procesados
│   │   │   ├── demograficos_procesados.json
│   │   │   └── presupuesto_procesado.json
│   │   └── texts/           # Contenido estático
│   │       └── content.json
│   ├── static/               # Recursos estáticos
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── images/
│   │   └── maps/
│   └── config/              # Configuraciones
│       ├── environment.json
│       ├── menu_config.json
│       └── platform_config.json
├── .streamlit/              # Configuración de Streamlit
│   └── config.toml
└── requirements.txt        # Dependencias del proyecto
```

## 📋 Archivos Esenciales para el Despliegue

### 1. requirements.txt
```txt
streamlit==1.24.0
pandas==1.5.3
numpy==1.24.3
plotly==5.15.0
folium==0.14.0
streamlit-folium==0.12.0
python-dotenv==1.0.0
psutil==5.9.5
pathlib==1.0.1
pillow==9.5.0
requests==2.31.0
geopandas==0.13.2
matplotlib==3.7.1
seaborn==0.12.2
openpyxl==3.1.2
```

### 2. .streamlit/config.toml
```toml
[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false

[theme]
primaryColor = "#3B82F6"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F4F6"
textColor = "#1F2937"
font = "sans serif"

[browser]
gatherUsageStats = false
```

### 3. app/main.py (Punto de entrada)
```python
import streamlit as st
import os

# Configuración específica para Streamlit Cloud
os.environ['IS_STREAMLIT_CLOUD'] = 'true'

# Importar el resto de la aplicación
from utils.streamlit_cloud_optimizer import StreamlitCloudOptimizer
```

## 🚀 Pasos para el Despliegue

1. **Preparar el Repositorio**
   ```bash
   # Estructura mínima requerida
   git clone https://github.com/tu-usuario/ds_portfolio.git
   cd ds_portfolio
   # Asegurarse de tener solo los archivos necesarios
   ```

2. **Verificar datos preprocesados**
   - Comprimir datos grandes
   - Convertir imágenes a WebP
   - Eliminar archivos temporales

3. **Configurar en Streamlit Cloud**
   - Ir a https://share.streamlit.io
   - Conectar con GitHub
   - Seleccionar repositorio
   - Configurar:
     * Main file path: `app/main.py`
     * Python version: 3.9
     * Requirements: `requirements.txt`

## 🔧 Optimizaciones Específicas

### 1. Datos Preprocesados
```python
# app/utils/data_sources.py
PREPROCESSED_DATA = {
    'emisiones': 'data/preprocessed/emisiones.parquet.gz',
    'agua': 'data/preprocessed/calidad_agua.parquet.gz',
    'demografia': 'data/preprocessed/demografia.parquet.gz'
}
```

### 2. Caché Optimizado
```python
# app/utils/cache_manager.py
@st.cache_data(ttl=3600, max_entries=20)
def load_optimized_data(source):
    return pd.read_parquet(PREPROCESSED_DATA[source])
```

### 3. Recursos Estáticos
```python
# app/utils/static_manager.py
STATIC_RESOURCES = {
    'images': 'static/images/',
    'css': 'static/css/style.min.css',
    'maps': 'static/maps/'
}
```

## 📊 Límites y Consideraciones

### Límites de Streamlit Community Cloud
- RAM: 1GB
- CPU: Compartida
- Tiempo de ejecución: Limitado
- Almacenamiento: ~200MB recomendado

### Optimizaciones Recomendadas
1. **Datos**
   - Mantener la estructura actual de archivos JSON
   - Conservar la organización de carpetas data/
   - No comprimir los JSON existentes (ya están optimizados)
   - Mantener el sistema de caché actual
   - Conservar el feedback local

2. **Imágenes**
   - Convertir a WebP
   - Optimizar resolución
   - Usar lazy loading

3. **Recursos**
   - Minimizar CSS/JS
   - Comprimir assets
   - Eliminar recursos no usados

## 🔍 Verificación Pre-Despliegue

1. **Verificar Tamaños**
   ```bash
   # Desde la raíz del proyecto
   du -sh app/data/preprocessed/*
   du -sh app/static/*
   ```

2. **Probar Localmente**
   ```bash
   streamlit run app/main.py
   ```

3. **Verificar Dependencias**
   ```bash
   pip freeze > requirements.txt
   # Eliminar dependencias innecesarias
   ```

## 📝 Mantenimiento

### Monitoreo
- Revisar logs en Streamlit Cloud
- Monitorear uso de recursos
- Verificar tiempos de carga

### Actualizaciones
1. Hacer cambios en rama de desarrollo
2. Probar localmente
3. Hacer merge a main
4. Verificar despliegue automático

## 🚨 Solución de Problemas

### Problemas Comunes
1. **Error de Memoria**
   - Reducir tamaño de datos
   - Implementar paginación
   - Optimizar carga de recursos

2. **Tiempo de Carga**
   - Verificar caché
   - Optimizar queries
   - Reducir tamaño de assets

3. **Dependencias**
   - Verificar versiones compatibles
   - Eliminar dependencias no usadas
   - Usar alternativas más ligeras

## ✅ Checklist Final

- [ ] Estructura de archivos correcta
- [ ] requirements.txt actualizado
- [ ] Datos preprocesados y optimizados
- [ ] Configuración de Streamlit correcta
- [ ] Recursos estáticos optimizados
- [ ] Caché implementado
- [ ] Tests locales exitosos
- [ ] Documentación actualizada
