# 📊 Portafolio de Data Science - Análisis Ambientales Chile

Un portafolio interactivo desarrollado con Streamlit que contiene múltiples aplicaciones de análisis de datos ambientales y visualización.

## 🏗️ Estructura del Proyecto

### 🚀 Aplicación Principal
- **`app/main.py`**: Punto de entrada principal del portafolio con navegación modular
- **`app/apps/`**: Directorio de aplicaciones individuales organizadas de forma modular

### 💧 Aplicación de Calidad del Agua
- **Análisis temporal y estacional** de parámetros de calidad
- **Mapas interactivos** con ubicación de estaciones de monitoreo
- **Evaluación según estándares** internacionales de calidad
- **Datos oficiales** de la Dirección General de Aguas (DGA) de Chile

### 📊 Análisis Disponibles
- **Emisiones de CO2** (basado en datos del RETC)
- **Calidad del agua** en lagos y embalses (basado en datos de la DGA)

## 🚀 Características Principales
- **Portafolio modular** con múltiples aplicaciones
- **Navegación intuitiva** entre diferentes análisis
- **Visualizaciones interactivas** y mapas dinámicos
- **Procesamiento avanzado** de datos oficiales
- **Interface moderna** desarrollada con Streamlit
- Conclusiones y recomendaciones basadas en datos
- Análisis multivariado de parámetros ambientales
- Detección y evaluación de valores críticos

## 📦 Estructura Detallada del Proyecto
```
ds_portfolio/
├── app/                    # 🏠 Aplicación Principal del Portafolio
│   ├── main.py            # 🚀 Punto de entrada principal
│   ├── apps/              # 📁 Aplicaciones modulares
│   │   ├── __init__.py    # 📦 Inicializador del paquete
│   │   ├── water_quality_app.py  # 💧 App calidad del agua
│   │   ├── config.py      # ⚙️ Configuración de parámetros
│   │   └── utils.py       # 🛠️ Utilidades auxiliares
│   └── static/            # 📂 Recursos estáticos
├── notebooks/             # 📓 Análisis y exploración
│   ├── 01_Analisis_Emisiones_CO2_Chile.ipynb
│   └── 02_Analisis_Calidad_Del_Agua.ipynb
├── data/                  # 📊 Datasets organizados
│   ├── raw/              # Datos originales
│   ├── processed/        # Datos procesados
│   └── external/         # Datos externos
├── src/                   # 🔧 Código fuente modular
├── docs/                  # 📚 Documentación completa
├── tests/                 # 🧪 Tests unitarios
└── config/               # ⚙️ Configuración global
```

## 🛠️ Tecnologías Utilizadas
- **Python 3.8+** 🐍 - Lenguaje principal
- **Streamlit** ⚡ - Framework web interactivo
- **Pandas & NumPy** 📊 - Análisis de datos
- **Plotly** 📈 - Visualizaciones interactivas
- **Folium** 🗺️ - Mapas interactivos
- **Jupyter Notebooks** 📓 - Exploración de datos

## 🚦 Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior
- Git (para clonar el repositorio)

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

5. **Ejecutar el portafolio**:
   ```bash
   cd app
   streamlit run main.py
   ```

6. **Acceder a la aplicación**:
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
**Funcionalidades principales:**
- **📊 Análisis Temporal**: Tendencias y patrones estacionales
- **🗺️ Análisis Espacial**: Comparación entre estaciones de monitoreo
- **📈 Evaluación de Calidad**: Clasificación según estándares internacionales
- **🌍 Mapas Interactivos**: Visualización geoespacial con Folium
- **📁 Explorador de Datos**: Tabla interactiva con descarga CSV
- **⚡ Métricas en Tiempo Real**: Dashboard con indicadores clave

**Parámetros monitoreados:**
- pH (rango óptimo: 6.0-8.5)
- Temperatura (rango óptimo: 5-25°C)
- Conductividad Eléctrica (óptimo: <400 µS/cm)
- Oxígeno Disuelto (óptimo: >5 mg/L)
- Turbiedad (óptimo: <10 NTU)
- Sólidos Suspendidos (óptimo: <25 mg/L)

**Fuente de datos:** Dirección General de Aguas (DGA) - Chile

### 🔮 Próximas Aplicaciones
- **📈 Análisis de Mercado Financiero**: ML predictivo para tendencias
- **🛒 Dashboard de Ventas**: Business Intelligence y KPIs
- **🌱 Análisis de Emisiones CO2**: Basado en notebook existente

## 📊 Optimizaciones de Rendimiento
Para optimizar el rendimiento en Streamlit Cloud, la aplicación implementa:
- Muestreo estratificado de datos (reducción a 100,000 registros)
- Gráficos optimizados para consumo eficiente de memoria
- Health checks para mejorar tiempos de carga
- Consulta [docs/DOCUMENTATION.md](docs/DOCUMENTATION.md) para más detalles

## 📚 Documentación
Para más detalles, consultar:
- [project-roadmap.md](project-roadmap.md) - Plan de trabajo y estructura
- [Notebooks](notebooks/) - Ejemplos y tutoriales
- [Docs](docs/) - Documentación detallada
