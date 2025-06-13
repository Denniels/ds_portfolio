# 📓 Notebooks de Análisis - Data Science Portfolio

> **Estado**: ✅ **Completamente Integrado** con el sistema modular del portafolio

## 🎯 Propósito

Esta sección contiene notebooks de Jupyter que sirven como **laboratorio de análisis** para el desarrollo de nuevas funcionalidades del portafolio. Los notebooks funcionan como:

1. **🔬 Exploración Inicial**: Análisis exploratorio de nuevos datasets
2. **🧪 Prototipado**: Desarrollo de algoritmos y visualizaciones
3. **📊 Investigación Profunda**: Análisis detallados que complementan las apps web
4. **🚀 Pipeline de Desarrollo**: Desde notebook hasta aplicación Streamlit

## 📓 Notebooks Disponibles

### 1. ✅ **Análisis de Emisiones CO2 en Chile** 
**[01_Analisis_Emisiones_CO2_Chile.ipynb](01_Analisis_Emisiones_CO2_Chile.ipynb)**

**🔗 Estado**: Integrado en la aplicación Streamlit (`co2_emissions_app.py`)

**📋 Características**:
- Análisis de emisiones industriales por región y comuna
- Visualización geoespacial con mapas interactivos
- Tendencias temporales y estacionales
- Identificación de principales emisores sectoriales

### 2. ✅ **Análisis de Calidad del Agua**
**[02_Analisis_Calidad_Del_Agua.ipynb](02_Analisis_Calidad_Del_Agua.ipynb)**

**🔗 Estado**: Integrado en la aplicación Streamlit (`water_quality_app.py`)

**📋 Características**:
- Análisis de parámetros físico-químicos del agua
- Mapas interactivos de estaciones de monitoreo
- Sistema de evaluación según estándares internacionales
- Tendencias temporales de calidad por cuenca hidrográfica

### 3. ✅ **Análisis Demográfico con BigQuery**
**[03_Analisis_BigQuery_Demografia.ipynb](03_Analisis_BigQuery_Demografia.ipynb)**

**🔗 Estado**: Implementado como notebook independiente con visualizaciones exportables

**📋 Características**:
- Análisis de datos históricos de nombres en EE.UU. (1910-2013)
- Tendencias de diversidad de nombres a lo largo del tiempo
- Comparativa por género y década
- Visualizaciones interactivas de evolución de nombres populares
- Integración con Google Cloud BigQuery

**🔧 Tecnologías**: 
- BigQuery, Python, Pandas, Plotly
- Sistema de exportación de visualizaciones a HTML/PNG

**📊 Visualizaciones**: 
- Disponibles en la carpeta [visualizaciones/](visualizaciones/)
- [Ver visualización interactiva](visualizaciones/tendencias_nombres.html)

## 🛠️ Utilidades y Herramientas

- **[export_bigquery_viz.ipynb](export_bigquery_viz.ipynb)**: Notebook para exportar visualizaciones del análisis demográfico
- **[actualizar_visualizaciones.py](actualizar_visualizaciones.py)**: Script para actualizar visualizaciones
- **[visualizaciones_helper.py](visualizaciones_helper.py)**: Funciones auxiliares para visualizaciones
