# 📊 Portafolio de Data Science - Análisis Ambientales y Demográficos

> **Estado:** ✅ **Completamente Funcional** - Sistema modular con arquitectura escalable e integración con BigQuery

Un portafolio interactivo desarrollado con Streamlit que presenta múltiples aplicaciones de análisis de datos ambientales y demográficos con visualizaciones avanzadas y mapas interactivos.

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

## 🎯 Objetivos del Proyecto

Este portafolio está diseñado como una **plataforma evolutiva** para análisis ambientales y demográficos, con un enfoque modular que permite agregar nuevos análisis y funcionalidades de manera incremental.

## 🏗️ Arquitectura del Sistema

### 🚀 Aplicación Principal
- **`app/main.py`**: Hub central del portafolio con navegación intuitiva
- **`app/apps/`**: Aplicaciones modulares independientes
  - `water_quality_app.py`: Análisis de calidad del agua
  - `co2_emissions_app.py`: Análisis de emisiones CO2
  - `demographics_app.py`: Análisis demográfico con BigQuery
- **`app/apps/modules/`**: Biblioteca de utilidades reutilizables

### 📊 Análisis y Aplicaciones Disponibles

#### 1. **Calidad del Agua en Chile** ✅ Operativa
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

## 📚 Documentación

- **Notebooks de Análisis**: `/notebooks/`
- **Documentación Técnica**: `/docs/`
- **Guías de Usuario**: Integradas en cada aplicación
- **Metodología**: Documentada en cada módulo

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, revisa las guías de contribución en `CONTRIBUTING.md`.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

Si tienes preguntas o encuentras problemas, por favor abre un issue en el repositorio.
