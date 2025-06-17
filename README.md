# 📊 Portafolio de Data Science | Chile

> Análisis y visualizaciones de datos enfocados en temas relevantes para Chile, desarrollado con Streamlit y herramientas modernas de Data Science.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-Denniels-black.svg)](https://github.com/Denniels/ds_portfolio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Daniel%20Andrés%20Mardones-blue.svg)](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)

## 🌟 Características Principales

- **5 Análisis Especializados**: CO2, calidad del agua, demografía, presupuesto público y currículum profesional
- **Visualizaciones Interactivas**: Mapas dinámicos, gráficos interactivos y dashboards responsivos
- **Optimización de Rendimiento**: Sistema de caché inteligente y preprocesamiento de datos
- **Diseño Responsivo**: Interfaz adaptable a dispositivos móviles y desktop
- **Navegación Simplificada**: Sin menús complejos, acceso directo desde página principal

## 🚀 Inicio Rápido

### Ejecución Local

1. **Clonar el repositorio:**
```bash
git clone https://github.com/Denniels/ds_portfolio.git
cd ds_portfolio
```

2. **Configurar entorno virtual:**
```bash
# Crear entorno virtual
python -m venv .venv_fresh

# Activar entorno (Windows)
.\.venv_fresh\Scripts\Activate.ps1

# Activar entorno (Linux/Mac)
source .venv_fresh/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
# Desde el directorio raíz
python -m streamlit run app/main.py

# O usando ruta absoluta
E:\repos\ds_portfolio\.venv_fresh\Scripts\python.exe -m streamlit run "E:\repos\ds_portfolio\app\main.py"
```

5. **Acceder a la aplicación:**
   - URL Local: http://localhost:8501

### Streamlit Cloud

La aplicación está optimizada para Streamlit Cloud:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ds-portfolio-chile.streamlit.app)

**Para desplegar tu propia versión:**

1. Fork este repositorio en GitHub
2. Conecta tu repositorio a [Streamlit Cloud](https://share.streamlit.io)
3. Configura los siguientes parámetros:
   - **Main file path**: `app/main.py`
   - **Python version**: 3.11
   - **Branch**: `main`

## 📊 Proyectos y Análisis

### 1. 🏭 Análisis de Emisiones CO2
- Visualización temporal de emisiones por sector industrial
- Análisis de tendencias y patrones estacionales
- Comparativas regionales y proyecciones futuras
- **Tecnologías**: Pandas, Plotly, análisis de series temporales

### 2. 💧 Calidad del Agua
- Mapas interactivos de estaciones de monitoreo nacional
- Análisis multivariable de parámetros de calidad
- Visualización geoespacial con Folium
- **Tecnologías**: Folium, Streamlit-Folium, análisis geoespacial

### 3. 👥 Análisis Demográfico
- Procesamiento de datos censales (15M+ registros)
- Tendencias poblacionales y distribución geográfica
- Análisis de patrones demográficos por región
- **Tecnologías**: BigQuery (simulado), análisis estadístico

### 4. 💰 Presupuesto Público
- Análisis del gasto público por ministerios
- Visualizaciones de distribución presupuestaria
- Comparativas históricas y eficiencia fiscal
- **Tecnologías**: Plotly, análisis financiero

### 5. 📄 Currículum Vitae ⭐ **NUEVO**
- Información profesional completa
- Experiencia en Data Science e Ingeniería Industrial
- Proyectos destacados y habilidades técnicas
- **Tecnologías**: Markdown dinámico, diseño responsivo

### 6. 💼 Servicios Profesionales
- Catálogo de servicios de Data Science
- Consultoría en análisis de datos
- Desarrollo de dashboards personalizados

### 7. 💭 Sistema de Feedback
- Recolección de comentarios de usuarios
- Análisis de satisfacción y mejoras
- Interfaz interactiva para sugerencias

## 🛠️ Stack Tecnológico

### Frontend y Visualización
- **Streamlit 1.45+**: Framework principal de la aplicación
- **Plotly**: Gráficos interactivos y dashboards
- **Folium + Streamlit-Folium**: Mapas interactivos
- **HTML/CSS**: Estilos personalizados

### Análisis de Datos
- **Python 3.11**: Lenguaje principal
- **Pandas 2.3+**: Manipulación y análisis de datos
- **NumPy**: Operaciones numéricas optimizadas
- **Matplotlib + Seaborn**: Visualizaciones estadísticas

### Infraestructura y Optimización
- **Psutil**: Monitoreo de recursos del sistema
- **Cachetools**: Sistema de caché personalizado
- **Python-dateutil**: Manejo avanzado de fechas

### Desarrollo y Despliegue
- **Git/GitHub**: Control de versiones
- **Streamlit Cloud**: Despliegue en la nube
- **VS Code**: Entorno de desarrollo

## 🗂️ Estructura del Proyecto

```
ds_portfolio/
├── app/
│   ├── main.py                 # Aplicación principal
│   ├── pages/                  # Páginas individuales
│   │   ├── 01_emisiones_co2.py
│   │   ├── 02_calidad_agua.py
│   │   ├── 03_demografia_bigquery.py
│   │   ├── 04_presupuesto_publico.py
│   │   ├── 05_curriculum.py    # ⭐ NUEVO
│   │   ├── 06_servicios.py
│   │   └── 07_feedback.py
│   ├── utils/                  # Módulos utilitarios
│   │   ├── cache_manager.py
│   │   ├── optimization.py
│   │   ├── contact_components.py
│   │   └── navigation.py
│   ├── components/             # Componentes reutilizables
│   ├── data/                   # Datos y caché
│   └── static/                 # Archivos estáticos
├── notebooks/                  # Jupyter notebooks de análisis
├── docs/                       # Documentación
│   └── curriculum.md           # ⭐ NUEVO
├── .streamlit/                 # Configuración de Streamlit
├── requirements.txt            # Dependencias optimizadas
└── README.md                   # Este archivo
```

## 🚀 Rendimiento y Optimización

### Características de Rendimiento
- ✅ **Caché inteligente**: Datos precargados para carga rápida
- ✅ **Optimización de memoria**: Gestión eficiente de recursos
- ✅ **Lazy loading**: Carga bajo demanda de componentes pesados
- ✅ **Compresión de assets**: CSS y JavaScript optimizados

### Métricas de Rendimiento
- **Tiempo de inicio**: ~10-15 segundos
- **Navegación entre páginas**: ~1-2 segundos
- **Carga de visualizaciones**: ~2-5 segundos
- **Memoria utilizada**: ~200-400 MB

## 🔧 Desarrollo y Contribución

### Configuración de Desarrollo

1. **Instalar dependencias de desarrollo:**
```bash
pip install -r requirements_local.txt
```

2. **Ejecutar en modo desarrollo:**
```bash
streamlit run app/main.py --server.runOnSave true
```

### Estructura de Commits
- `feat:` Nueva funcionalidad
- `fix:` Corrección de errores
- `docs:` Documentación
- `style:` Formato y estilo
- `refactor:` Refactorización

## 📈 Histórico de Actualizaciones

### Versión 2.0 (Junio 2025) ⭐ **ACTUAL**
- ✅ Página de currículum profesional agregada
- ✅ Navegación simplificada sin menús radio
- ✅ Entorno virtual optimizado (.venv_fresh)
- ✅ Dependencias actualizadas (Streamlit 1.45+)
- ✅ Correcciones para despliegue en Streamlit Cloud
- ✅ Sistema de contacto integrado

### Versión 1.0 (2024)
- ✅ 4 análisis principales implementados
- ✅ Sistema de navegación con sidebar
- ✅ Visualizaciones interactivas
- ✅ Optimización de rendimiento básica

## 📞 Contacto y Redes Sociales

### 🧑‍💼 Daniel Andrés Mardones Sanhueza
- **LinkedIn**: [daniel-andres-mardones-sanhueza](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
- **GitHub**: [Denniels](https://github.com/Denniels)
- **Email**: daniel.mardones@integralservicespa.cl
- **Web**: [integralservicespa.cl](https://integralservicespa.cl)

### 💼 Perfil Profesional
- **Data Science**: Transición desde Ingeniería Industrial
- **Experiencia**: +10 años en mantenimiento industrial
- **Especialización**: Análisis predictivo y optimización de procesos
- **Formación**: Ingeniero UTFSM + Data Science Desafío Latam

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

⭐ **Si este proyecto te resulta útil, no olvides darle una estrella en GitHub!**

*Última actualización: Junio 2025 | Versión 2.0*
