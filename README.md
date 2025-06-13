# 📊 Portafolio de Data Science - Análisis de Datos Gubernamentales

> **Estado:** ✅ **Completamente Funcional y Actualizado (Junio 2025)** - Sistema modular con arquitectura escalable, integraciones múltiples y mejoras continuas

Un portafolio interactivo desarrollado con Streamlit que presenta múltiples aplicaciones de análisis de datos gubernamentales, ambientales y demográficos, con visualizaciones avanzadas, mapas interactivos y análisis presupuestario.

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes de Python)
- Git

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/ds_portfolio.git
   cd ds_portfolio
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv ds_portfolio_env
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows
   .\ds_portfolio_env\Scripts\activate
   
   # Linux/Mac
   source ds_portfolio_env/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Ejecución

1. **Iniciar la aplicación**
   ```bash
   streamlit run app/main.py
   ```

2. **Acceder a la interfaz web**
   - Abrir navegador en `http://localhost:8501`
   - Seleccionar una aplicación del menú lateral

### Despliegue

El portafolio está desplegado y accesible en:
🔗 [https://ds-portfolio-482495249955.us-central1.run.app](https://ds-portfolio-482495249955.us-central1.run.app)

#### 🚀 Opciones de Despliegue

1. **Google Cloud Run (Actual)**
   - Despliegue serverless en la capa gratuita
   - Actualizaciones automáticas vía GitHub Actions
   - Escalado automático según demanda
   - Costos optimizados (solo pagas por uso)

2. **Despliegue Local con Docker**
   ```bash
   # Construir imagen Docker
   docker build -t ds-portfolio .
   
   # Ejecutar contenedor
   docker run -p 8080:8080 ds-portfolio
   ```

3. **Características del Despliegue Actual**
   - ✨ CI/CD automatizado con GitHub Actions
   - 🔒 HTTPS y dominio seguro
   - 📱 Interfaz responsive
   - 💰 Optimizado para la capa gratuita de GCP
   - 🔄 Actualizaciones automáticas al hacer push

Consulta las guías detalladas en la carpeta `/docs/` para más información.

## 🎯 Objetivos del Proyecto

Este portafolio está diseñado como una **plataforma evolutiva** para análisis ambientales y demográficos, con un enfoque modular que permite agregar nuevos análisis y funcionalidades de manera incremental.

## 🏗️ Arquitectura del Sistema

### 🚀 Aplicación Principal
- **`app/main.py`**: Hub central del portafolio con navegación intuitiva
- **`app/apps/`**: Aplicaciones modulares independientes  - `budget_analysis_app.py`: Análisis del Presupuesto Público
  - `water_quality_app.py`: Análisis de calidad del agua
  - `co2_emissions_app.py`: Análisis de emisiones CO2
  - `demographics_app.py`: Análisis demográfico con BigQuery
- **`app/apps/modules/`**: Biblioteca de utilidades reutilizables

### 📊 Análisis y Aplicaciones Disponibles

#### 1. **Análisis del Presupuesto Público** ✅ Actualizada (Junio 2025)
- **Nueva versión 2.0**: Visualizaciones mejoradas y análisis avanzados
- **Análisis interactivo** del Presupuesto del Sector Público de Chile
- **Curvas de Lorenz** y análisis de concentración presupuestaria
- **Simulación de evolución temporal** para análisis de tendencias
- **Métricas de concentración**: Índice HHI y porcentajes acumulados
- **Exportación de datos** en formato CSV para análisis complementarios
- **Integración con API** de datos.gob.cl con sistema de caché optimizado
- **Rutas**: 
  - `app/apps/budget_analysis_app.py` (versión estable)
  - `app/apps/budget_analysis_app_v2.py` (versión mejorada)

#### 2. **Calidad del Agua en Chile** ✅ Operativa
- **Análisis temporal** de parámetros físico-químicos
- **Mapas interactivos** con geocodificación inteligente
- **Sistema de evaluación** según estándares internacionales
- **Dashboard interactivo** con métricas en tiempo real
- **Datos oficiales** de la Dirección General de Aguas (DGA)
- **Ruta**: `app/apps/water_quality_app.py`

#### 2. **Emisiones CO2 por Región** ✅ Operativa  
- **Análisis sectorial** de emisiones industriales
- **Visualizaciones geográficas** por región
- **Tendencias temporales** y patrones estacionales
- **Datos oficiales** del Registro RETC Chile
- **Ruta**: `app/apps/co2_emissions_app.py`

#### 3. **Análisis Demográfico con BigQuery** ✅ Operativo
- **Exploración de datos de nombres** históricos (1910-2013)
- **Análisis de tendencias** por género y década
- **Visualizaciones interactivas** de evolución de nombres populares
- **Integración con Google Cloud** usando BigQuery
- **Visualizaciones exportables** en formatos HTML y PNG
- **Ruta**: `app/apps/demographics_app.py`

### 📈 Roadmap de Expansión
- 🔄 **Próximo**: Análisis de Calidad del Aire
- 🔄 **En planificación**: Dashboard Financiero
- 🔄 **Futuro**: Análisis de Biodiversidad

## 🛠️ Características Técnicas

### 🎨 **Interfaz Moderna**
- **Framework**: Streamlit 1.24+
- **Visualizaciones**: Plotly, Folium
- **Responsive Design**: Optimizado para móvil/desktop
- **Navegación**: Sistema de tabs y menú lateral

### 🔧 **Arquitectura Modular**
- **Componentes reutilizables** en `app/apps/modules/`
- **Configuraciones centralizadas** para fácil mantenimiento
- **Sistema de coordenadas inteligente** con cache automático
- **Carga de datos optimizada** con validación automática

### ☁️ **Integración con Cloud**
- **BigQuery** para análisis de grandes conjuntos de datos
- **Exportación de visualizaciones** en múltiples formatos
- **Manejo seguro de credenciales** con variables de entorno
- **Opciones de despliegue** documentadas para Google Cloud y GitHub Pages

### 🚀 **Opciones de Despliegue**
- **Google Cloud Run**: Despliegue serverless con Docker
- **Google Compute Engine**: VM con capa gratuita e2-micro
- **GitHub Pages**: Documentación y visualizaciones estáticas
- **Estrategia híbrida**: Combinación de plataformas para óptimo rendimiento

## 📚 Documentación

- **Notebooks de Análisis**: `/notebooks/`
- **Documentación Técnica**: `/docs/`
- **Guías de Despliegue**:
  - [Despliegue en Google Cloud Run](/docs/roadmap_google_cloud_run.md)
  - [Despliegue en VM de Google Cloud](/docs/despliegue_vm_gcp.md)
  - [Despliegue en GitHub Pages](/docs/despliegue_github_pages.md)
- **Guías de Usuario**: Integradas en cada aplicación
- **Metodología**: Documentada en cada módulo

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, revisa las guías de contribución en `CONTRIBUTING.md`.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

Si tienes preguntas o encuentras problemas, por favor abre un issue en el repositorio.
