# 📊 Portafolio de Data Science - Análisis Ambientales y Demográficos

> **Estado:** ✅ **Completamente Funcional** - Sistema modular con arquitectura escalable e integración con BigQuery

Un portafolio interactivo desarrollado con Streamlit que presenta múltiples aplicaciones de análisis de datos ambientales y demográficos con visualizaciones avanzadas y mapas interactivos.

## 🎯 Objetivos del Proyecto

Este portafolio está diseñado como una **plataforma evolutiva** para análisis ambientales y demográficos, con un enfoque modular que permite agregar nuevos análisis y funcionalidades de manera incremental.

## 🏗️ Arquitectura del Sistema

### 🚀 Aplicación Principal
- **`app/main.py`**: Hub central del portafolio con navegación intuitiva
- **`app/apps/`**: Aplicaciones modulares independientes
- **`app/apps/modules/`**: Biblioteca de utilidades reutilizables

### 📊 Análisis y Aplicaciones

#### 1. **Calidad del Agua en Chile** ✅ Operativa
- **Análisis temporal** de parámetros físico-químicos
- **Mapas interactivos** con geocodificación inteligente
- **Sistema de evaluación** según estándares internacionales
- **Dashboard interactivo** con métricas en tiempo real
- **Datos oficiales** de la Dirección General de Aguas (DGA)

#### 2. **Emisiones CO2 por Región** ✅ Operativa  
- **Análisis sectorial** de emisiones industriales
- **Visualizaciones geográficas** por región
- **Tendencias temporales** y patrones estacionales
- **Datos oficiales** del Registro RETC Chile

#### 3. **Análisis Demográfico con BigQuery** ✅ Operativo
- **Exploración de datos de nombres** históricos (1910-2013)
- **Análisis de tendencias** por género y década
- **Visualizaciones interactivas** de evolución de nombres populares
- **Integración con Google Cloud** usando BigQuery
- **Visualizaciones exportables** en formatos HTML y PNG

### 📈 Roadmap de Expansión
- 🔄 **Próximo**: Análisis de Calidad del Aire
- 🔄 **En planificación**: Dashboard Financiero
- 🔄 **Futuro**: Análisis de Biodiversidad

## 🚀 Características del Sistema

### 🎨 **Interfaz Moderna**
- **Dashboard intuitivo** con navegación centralizada
- **Visualizaciones interactivas** usando Plotly y Folium
- **Responsive design** optimizado para diferentes dispositivos
- **Feedback en tiempo real** sobre el estado del sistema

### 🔧 **Arquitectura Modular**
- **Componentes reutilizables** en `app/apps/modules/`
- **Configuraciones centralizadas** para fácil mantenimiento
- **Sistema de coordenadas inteligente** con cache automático
- **Carga de datos optimizada** con validación automática

### ☁️ **Integración con Cloud**
- **BigQuery** para análisis de grandes conjuntos de datos
- **Exportación de visualizaciones** en múltiples formatos
- **Manejo seguro de credenciales** con variables de entorno

## 📦 Estructura Actualizada del Proyecto
```
ds_portfolio/
├── 🏠 app/                          # Aplicación Principal Streamlit
│   ├── main.py                      # 🚀 Hub central del portafolio
│   ├── apps/                        # 📁 Aplicaciones modulares
│   │   ├── __init__.py              # 📦 Inicializador del paquete
│   │   ├── water_quality_app.py     # 💧 Análisis calidad del agua
│   │   ├── co2_emissions_app.py     # 🏭 Análisis emisiones CO2
│   │   ├── demography_analysis_app.py # 👥 Análisis demográfico
│   │   ├── config.py                # ⚙️ Configuración de apps
│   │   ├── utils.py                 # 🛠️ Utilidades generales
│   │   └── modules/                 # 🔧 Biblioteca modular
│   │       ├── __init__.py          # 📦 Inicializador módulos
│   │       ├── config.py            # ⚙️ Configuraciones centrales
│   │       ├── data_loaders.py      # 📥 Cargadores de datos
│   │       ├── geo_utils.py         # 🗺️ Utilidades geográficas
│   │       ├── map_utils.py         # 🗺️ Mapas interactivos
│   │       ├── chart_utils.py       # 📊 Gráficos y visualizaciones
│   │       ├── water_quality.py     # 💧 Lógica calidad agua
│   │       ├── emissions.py         # 🏭 Lógica emisiones
│   │       ├── demography.py        # 👥 Lógica análisis demográfico
│   │       └── *_config.py          # ⚙️ Configs específicas
│   ├── data/                        # 📊 Datos de aplicación
│   │   ├── estaciones_coordenadas.json    # 🗺️ Coordenadas verificadas
│   │   └── cache_coordenadas_chile.json   # 🔄 Cache dinámico
│   └── static/                      # 📂 Recursos estáticos
├── 📓 notebooks/                    # Análisis y exploración
│   ├── 01_Analisis_Emisiones_CO2_Chile.ipynb
│   ├── 02_Analisis_Calidad_Del_Agua.ipynb
│   ├── 03_Analisis_Demografico.ipynb
│   ├── utils/                       # 🛠️ Utilidades para notebooks
│   │   ├── README.md                # 📚 Documentación utils
│   │   └── geocodificador_chile.py  # 🗺️ Geocodificador especializado
│   └── README.md                    # 📚 Documentación notebooks
├── 📊 data/                         # Datasets organizados
│   ├── raw/                         # 📥 Datos originales
│   ├── processed/                   # 🔄 Datos procesados
│   ├── external/                    # 🌐 Datos externos
│   └── results/                     # 📤 Resultados exportados
├── 🔧 src/                          # Código fuente adicional
├── 📚 docs/                         # Documentación completa
├── 🧪 tests/                        # Tests unitarios
├── 🛠️ config/                       # Configuración global
├── 🤖 models/                       # Modelos ML (futuro)
├── 🌍 ds_portfolio_env/             # Entorno virtual
└── 📋 *.md                          # Documentación del proyecto
```

## 🛠️ Stack Tecnológico

### 🐍 **Backend y Análisis**
- **Python 3.8+** - Lenguaje principal
- **Pandas & NumPy** - Manipulación y análisis de datos
- **Streamlit** - Framework web interactivo
- **Jupyter Notebooks** - Exploración y prototipado

### 📊 **Visualizaciones**
- **Plotly** - Gráficos interactivos avanzados
- **Folium** - Mapas web interactivos
- **Matplotlib/Seaborn** - Gráficos estadísticos

### 🗺️ **Geoespacial**
- **GeoPandas** - Análisis geoespacial
- **Geocoding APIs** - Conversión de direcciones a coordenadas
- **OpenStreetMap & CartoDB** - Capas base de mapas

### ☁️ **Cloud y Big Data**
- **Google Cloud Platform** - Infraestructura en la nube
- **BigQuery** - Análisis de grandes volúmenes de datos
- **APIs de Google** - Integración y autenticación segura

### 🔧 **Infraestructura**
- **Git & GitHub** - Control de versiones
- **Virtual Environment** - Gestión de dependencias
- **Modular Architecture** - Escalabilidad y mantenimiento

## 🚦 Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior
- Git (para clonar el repositorio)
- Cuenta de Google Cloud con acceso a BigQuery (para análisis demográficos)

### Pasos de Instalación
1. **Clonar el repositorio**:
   ```bash
   git clone <repository-url>
   cd ds_portfolio
   ```

2. **Crear entorno virtual**:
   ```bash
   python -m venv ds_portfolio_env
   ```

3. **Activar entorno virtual**:
   ```bash
   # Windows PowerShell
   .\ds_portfolio_env\Scripts\Activate.ps1
   
   # Windows CMD
   .\ds_portfolio_env\Scripts\activate.bat
   
   # Linux/Mac
   source ds_portfolio_env/bin/activate
   ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar credenciales de Google Cloud** (si se utiliza el análisis demográfico):
   - Seguir instrucciones en la [documentación de Google Cloud](https://cloud.google.com/docs/authentication/getting-started)

6. **Ejecutar el portafolio**:
   ```bash
   cd app
   streamlit run main.py
   ```

7. **Acceder a la aplicación**:
   - Abrir navegador en: `http://localhost:8501`

## 🎯 Navegación y Uso del Portafolio

### 🏠 Página de Inicio
- **Vista general** del portafolio con estadísticas
- **Tarjetas informativas** de cada aplicación disponible
- **Acceso directo** a aplicaciones desde botones
- **Información técnica** sobre tecnologías utilizadas

### 🧭 Sistema de Navegación
- **Sidebar dinámico** para selección de aplicaciones
- **Estado de aplicaciones**: Disponibles y próximamente
- **Navegación fluida** entre diferentes módulos
- **Enlaces útiles** a documentación y recursos

### 💧 Aplicación de Calidad del Agua

#### **🎯 Funcionalidades Principales**
- **📊 Dashboard Interactivo**: Métricas en tiempo real con KPIs ambientales
- **🗺️ Mapas Georreferenciados**: Sistema avanzado de geocodificación para Chile
- **📈 Análisis Temporal**: Tendencias estacionales y patrones históricos  
- **🔍 Explorador de Datos**: Tabla interactiva con filtros avanzados
- **📤 Exportación**: Descarga de datos procesados en CSV/Excel

#### **🧪 Parámetros Monitoreados**
| Parámetro | Rango Óptimo | Unidad | Estándar |
|-----------|--------------|--------|----------|
| **pH** | 6.0 - 8.5 | unidades | WHO/OMS |
| **Temperatura** | 5 - 25°C | °C | Ambiental |
| **Conductividad** | < 400 | µS/cm | Dulce |
| **Oxígeno Disuelto** | > 80% | % Saturación | Biológico |
| **Turbiedad** | < 10 | NTU | Claridad |
| **Sólidos Suspendidos** | < 25 | mg/L | Físico |

#### **🏛️ Fuente de Datos**
- **Organismo**: Dirección General de Aguas (DGA) - Chile
- **Cobertura**: Lagos, lagunas y embalses nacionales
- **Frecuencia**: Monitoreo continuo con datos históricos
- **Validación**: Controles de calidad automatizados

### 🏭 Aplicación de Emisiones CO2

#### **📊 Análisis Disponibles**
- **🗺️ Distribución Regional**: Mapas coropléticos por región administrativa
- **🏗️ Análisis Sectorial**: Clasificación por tipo de industria
- **📈 Tendencias Temporales**: Evolución de emisiones en el tiempo
- **🎯 Identificación de Hotspots**: Zonas de mayor concentración

#### **📋 Datos del RETC**
- **Fuente**: Registro de Emisiones y Transferencias de Contaminantes
- **Alcance**: Emisiones industriales reportadas oficialmente
- **Sectores**: Minería, manufactura, energía, química, otros
- **Años**: Serie temporal desde 2013 hasta presente

### 👥 Aplicación de Análisis Demográfico

#### **📊 Funcionalidades Principales**
- **📈 Análisis de Tendencias**: Evolución de nombres por década y género
- **🗺️ Mapas de Calor**: Distribución geográfica de nombres populares
- **📊 Gráficos Interactivos**: Visualización de cambios en la popularidad de nombres
- **🔄 Exportación de Resultados**: Descarga de análisis se esta trabajando en implementar una forma para poder descargar en formatos HTML y PNG las visualizaciones.

#### **📅 Rango de Datos**
- **Desde**: 1910
- **Hasta**: 2013
- **Frecuencia**: Anual

#### **🔗 Integración con BigQuery**
- **Consulta de Datos**: Acceso a grandes volúmenes de datos históricos
- **Autenticación Segura**: Uso de credenciales de Google Cloud
- **Manejo de Errores**: Validación y control de errores en consultas

## 📊 Estado del Sistema y Optimizaciones

### ✅ **Componentes Operativos**
- **🚀 Aplicación Principal**: Funcionando completamente
- **💧 Calidad del Agua**: Sistema completo con mapas y análisis
- **🏭 Emisiones CO2**: Dashboard interactivo operativo
- **👥 Análisis Demográfico**: Integración con BigQuery y visualizaciones operativas
- **🗺️ Sistema de Mapas**: Geocodificación inteligente implementada
- **📊 Visualizaciones**: Gráficos interactivos optimizados

### ⚡ **Optimizaciones de Rendimiento**
- **📦 Cache Inteligente**: Coordenadas geográficas cacheadas automáticamente
- **🔄 Carga Lazy**: Datos cargados bajo demanda para eficiencia
- **🗜️ Compresión de Datos**: Optimización de memoria para datasets grandes
- **⚡ Streamlit Optimizado**: Configuración para mejor performance en cloud

### 🎯 **Planes de Expansión**
1. **📈 Próximo Release**: 
   - Análisis de Calidad del Aire (PM2.5, PM10, O3)
   - Dashboard de Biodiversidad Marina
   
2. **🔮 Roadmap Futuro**:
   - Machine Learning para predicciones ambientales
   - API REST para integración externa
   - Dashboard de alertas ambientales en tiempo real

## 📚 Documentación Complementaria

Para información detallada sobre componentes específicos:

- **[📓 Notebooks README](notebooks/README.md)** - Guía de análisis exploratorios
- **[🛠️ Utils README](notebooks/utils/README.md)** - Utilidades especializadas
- **[📊 PROYECTO_COMPLETADO.md](PROYECTO_COMPLETADO.md)** - Estado detallado del proyecto
- **[🔧 REFACTORIZACION_COMPLETADA.md](REFACTORIZACION_COMPLETADA.md)** - Cambios técnicos implementados
