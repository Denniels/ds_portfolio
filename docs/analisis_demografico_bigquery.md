# Análisis Demográfico con BigQuery Public Datasets

Este documento describe el análisis implementado en el notebook `03_Analisis_BigQuery_Demografia.ipynb` que explora datos demográficos históricos de nombres en Estados Unidos usando la plataforma BigQuery de Google Cloud.

## 📑 Descripción del Análisis

El notebook utiliza el conjunto de datos público `bigquery-public-data.usa_names.usa_1910_2013` que contiene registros históricos de nombres de bebés nacidos en Estados Unidos entre 1910 y 2013. A través de consultas SQL avanzadas y visualizaciones interactivas, se analizan tendencias demográficas y patrones en la elección de nombres.

## 🔍 Características Principales

### 1. Integración con Google Cloud BigQuery
- Configura la autenticación segura con credenciales
- Ejecuta consultas SQL directamente contra el servicio BigQuery
- Extrae y procesa grandes volúmenes de datos de forma eficiente

### 2. Análisis Demográfico Avanzado
- **Evolución temporal**: Tendencias de popularidad por década
- **Análisis por género**: Comparativas de nombres masculinos y femeninos
- **Diversidad nominal**: Cambios en la variedad de nombres a lo largo del tiempo

### 3. Visualizaciones Interactivas
- **Gráficos de tendencias**: Evolución de nombres populares
- **Paneles comparativos**: Patrones de género y generacionales
- **Exportación de visualizaciones**: Formatos HTML (interactivo) y PNG (estático)

## 💻 Uso e Implementación

### Requisitos
1. Cuenta en Google Cloud Platform con acceso a BigQuery
2. Credenciales configuradas adecuadamente
3. Python 3.7+ con las bibliotecas necesarias instaladas

### Ejecución
1. Configurar las credenciales de GCP
2. Ejecutar el notebook completo
3. Explorar las visualizaciones interactivas
4. Opcionalmente, exportar las visualizaciones a formatos estáticos

## 📊 Visualizaciones Generadas

Las visualizaciones generadas se guardan en la carpeta `notebooks/visualizaciones/`:
- **[tendencias_nombres.html](../notebooks/visualizaciones/tendencias_nombres.html)**: Versión interactiva
- **tendencias_nombres.png**: Versión estática para GitHub

## 📚 Referencias

- [BigQuery Public Datasets](https://cloud.google.com/bigquery/public-data)
- [USA Names Dataset Documentation](https://cloud.google.com/bigquery/docs/samples/bigquery-query-names-dataset)
- [Plotly Documentation](https://plotly.com/python/)
- [Google Cloud Authentication Guide](https://cloud.google.com/docs/authentication)
