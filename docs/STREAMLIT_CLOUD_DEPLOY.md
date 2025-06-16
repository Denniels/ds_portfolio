# Guía de Despliegue en Streamlit Cloud

Este documento describe los pasos para desplegar el portafolio de análisis de datos ambientales en Streamlit Cloud.

## 📋 Requisitos Previos

1. Cuenta en GitHub con el repositorio
2. Cuenta en [Streamlit Cloud](https://share.streamlit.io)
3. Requirements.txt actualizado
4. Archivos de configuración optimizados

## 🚀 Pasos para el Despliegue

### 1. Preparar el Repositorio

Asegúrate de que tu repositorio tiene la siguiente estructura:
```
ds_portfolio/
├── app/
│   ├── main.py
│   ├── pages/
│   ├── utils/
│   └── data/
├── requirements.txt
└── .streamlit/
    └── config.toml
```

### 2. Verificar Requirements.txt

```txt
streamlit==1.24.0
pandas==1.5.3
numpy==1.24.3
plotly==5.15.0
folium==0.14.0
streamlit-folium==0.12.0
```

### 3. Configurar Secrets (si es necesario)

En Streamlit Cloud:
1. Ve a ⚙️ Settings
2. Secrets Management
3. Añade las variables necesarias

### 4. Desplegar en Streamlit Cloud

1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Click en "New app"
3. Seleccionar el repositorio
4. Configurar:
   - Python version: 3.9
   - Main file path: app/main.py
   - Requirements: requirements.txt

## 🔧 Optimizaciones para Streamlit Cloud

### 1. Caché de Datos
```python
@st.cache_data(ttl=3600)
def load_data():
    # Tu código de carga de datos
```

### 2. Manejo de Memoria
```python
def optimize_dataframe(df):
    # Reducir tipos de datos
    for col in df.select_dtypes(['float64']):
        df[col] = df[col].astype('float32')
    return df
```

### 3. Carga Lazy
```python
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

## 📊 Monitoreo

### Métricas a Observar
- Uso de memoria
- Tiempo de carga
- Errores de ejecución
- Tiempo de respuesta

### Dashboard de Rendimiento
```python
def show_performance_metrics():
    st.sidebar.markdown("### 📊 Métricas")
    st.sidebar.metric("Memoria", f"{get_memory_usage():.1f} MB")
    st.sidebar.metric("Tiempo de Carga", f"{get_load_time():.2f}s")
```

## 🛠️ Mantenimiento

### Actualizaciones
- Mantener requirements.txt actualizado
- Revisar logs periódicamente
- Monitorear uso de recursos

### Backup
- Mantener datos críticos en caché
- Implementar fallbacks para datos externos
- Documentar cambios importantes

## 🚨 Solución de Problemas

### Problemas Comunes
1. **Error de Memoria**: Reducir tamaño de datos
2. **Timeout**: Implementar caching
3. **Dependencias**: Verificar versions

### Logs y Debugging
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_info():
    logger.info("Iniciando carga de datos...")
```

## 📝 Notas Importantes

1. Mantener datos bajo 1GB
2. Usar caché estratégicamente
3. Minimizar operaciones pesadas
4. Implementar manejo de errores
5. Documentar cambios
