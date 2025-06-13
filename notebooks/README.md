# 📓 Notebooks de Análisis - Data Science Portfolio

> **Estado**: ✅ **Completamente Integrado** con el sistema modular del portafolio

## 🎯 Propósito

Esta sección contiene notebooks de Jupyter que sirven como **laboratorio de análisis** para el desarrollo de nuevas funcionalidades del portafolio. Los notebooks funcionan como:

1. **🔬 Exploración Inicial**: Análisis exploratorio de nuevos datasets
2. **🧪 Prototipado**: Desarrollo de algoritmos y visualizaciones
3. **📊 Investigación Profunda**: Análisis detallados que complementan las apps web
4. **🚀 Pipeline de Desarrollo**: Desde notebook hasta aplicación Streamlit

## 📓 Notebooks Disponibles

### 1. ✨ **Análisis del Presupuesto Público** (Actualizado Junio 2025)
**[04_Analisis_Presupuesto_Publico.ipynb](04_Analisis_Presupuesto_Publico.ipynb)**

**🔗 Estado**: Integrado y Mejorado - Disponible en dos versiones:
- Versión estable: `budget_analysis_app.py`
- Versión avanzada: `budget_analysis_app_v2.py` (Junio 2025)

**📋 Características Actualizadas**:
- Análisis avanzado de concentración presupuestaria con curvas de Lorenz
- Simulación de evolución temporal para tendencias presupuestarias
- Métricas de concentración (Índice HHI, concentración Top 3/10)
- Exportación de datos en formato CSV
- Sistema mejorado de caché y optimización de rendimiento
- Interfaz renovada con diseño responsivo y explicaciones contextuales

### 2. ✅ **Análisis de Emisiones CO2 en Chile** 
**[01_Analisis_Emisiones_CO2_Chile.ipynb](01_Analisis_Emisiones_CO2_Chile.ipynb)**

**🔗 Estado**: Integrado en la aplicación Streamlit (`co2_emissions_app.py`)

**📋 Características**:
- Análisis de emisiones industriales por región y comuna
- Visualización geoespacial con mapas interactivos
- Tendencias temporales y estacionales
- Identificación de principales emisores sectoriales

**🚀 Acceso vía Streamlit**:
```bash
streamlit run app/main.py
# Seleccionar "🏭 Emisiones CO2 Chile" en el menú
```

### 2. ✅ **Análisis de Calidad del Agua**
**[02_Analisis_Calidad_Del_Agua.ipynb](02_Analisis_Calidad_Del_Agua.ipynb)**

**🔗 Estado**: Integrado en la aplicación Streamlit (`water_quality_app.py`)

**📋 Características**:
- Análisis de parámetros físico-químicos del agua
- Mapas interactivos de estaciones de monitoreo
- Sistema de evaluación según estándares internacionales
- Tendencias temporales de calidad por cuenca hidrográfica

**🚀 Acceso vía Streamlit**:
```bash
streamlit run app/main.py
# Seleccionar "💧 Análisis de Calidad del Agua" en el menú
```

### 3. ✅ **Análisis Demográfico con BigQuery**
**[03_Analisis_BigQuery_Demografia.ipynb](03_Analisis_BigQuery_Demografia.ipynb)**

**🔗 Estado**: Integrado en la aplicación Streamlit (`demographics_app.py`)

**📋 Características**:
- Análisis de datos históricos de nombres en EE.UU. (1910-2013)
- Tendencias de diversidad de nombres a lo largo del tiempo
- Comparativa por género y década
- Visualizaciones interactivas de evolución de nombres populares
- Integración con Google Cloud BigQuery

**🚀 Acceso vía Streamlit**:
```bash
streamlit run app/main.py
# Seleccionar "👤 Análisis Demográfico" en el menú
```

## 🛠️ Herramientas y Tecnologías

### 📊 Análisis de Datos
- **Jupyter Notebooks**: Desarrollo y prototipado
- **Python 3.8+**: Base de desarrollo
- **Pandas/NumPy**: Procesamiento de datos
- **Plotly/Folium**: Visualizaciones interactivas

### 🚀 Deployment
- **Streamlit**: Framework de aplicaciones web
- **Google Cloud**: BigQuery para análisis masivo
- **Git**: Control de versiones
- **Requirements.txt**: Gestión de dependencias

## 📚 Integración con Streamlit

### Pipeline de Desarrollo
1. **Exploración** en Jupyter Notebook
2. **Modularización** del código en funciones
3. **Creación** de app Streamlit correspondiente
4. **Integración** en el portafolio principal

### Estructura de Integración
```
ds_portfolio/
├── notebooks/                # Análisis y prototipos
│   ├── 01_Analisis_*.ipynb
│   ├── 02_Analisis_*.ipynb
│   └── 03_Analisis_*.ipynb
├── app/
│   ├── main.py             # Aplicación principal
│   └── apps/               # Apps modulares
│       ├── co2_emissions_app.py
│       ├── water_quality_app.py
│       └── demographics_app.py
```

## 🔍 Uso y Desarrollo

### Ejecutar Notebooks
1. Activar entorno virtual
```bash
.\ds_portfolio_env\Scripts\activate
```

2. Iniciar Jupyter
```bash
jupyter notebook
```

### Ejecutar Aplicación Streamlit
```bash
streamlit run app/main.py
```

## � Despliegue e Integración

Los análisis desarrollados en estos notebooks pueden desplegarse como aplicaciones interactivas:

### 🔄 Proceso de Integración
1. **Desarrollo en Notebooks**: Prototipado y análisis exploratorio
2. **Refactorización a Módulos**: Conversión a código modular y mantenible
3. **Integración en Streamlit**: Creación de interfaz interactiva
4. **Despliegue en Producción**: Publicación en plataformas cloud

### 📋 Opciones de Despliegue
- **Google Cloud Run**: Para aplicaciones interactivas con Streamlit
- **Google Compute Engine**: VM con Docker (capa gratuita)
- **GitHub Pages**: Para visualizaciones estáticas exportadas

### 📦 Exportación de Visualizaciones
Los notebooks incluyen funcionalidad para exportar visualizaciones como HTML estático o imágenes para su inclusión en GitHub Pages o documentación:

```python
# Ejemplo de exportación de visualización Plotly
fig.write_html("../github_pages/visualizations/presupuesto_distribucion.html")
```

Para instrucciones detalladas sobre las opciones de despliegue, consulta:
- [Despliegue en Google Cloud Run](../docs/roadmap_google_cloud_run.md)
- [Despliegue en VM de Google Cloud](../docs/despliegue_vm_gcp.md)
- [Despliegue en GitHub Pages](../docs/despliegue_github_pages.md)

## �📖 Documentación Adicional

- **[Metodología](../docs/DOCUMENTATION.md)**: Documentación detallada
- **[Deployment](../docs/despliegue_google_cloud_run.md)**: Guía de despliegue
- **[BigQuery](../docs/analisis_demografico_bigquery.md)**: Integración con BigQuery
