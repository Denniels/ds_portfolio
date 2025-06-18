# 📊 Portafolio de Data Science | Chile

> Análisis y visualizaciones de datos enfocados en temas relevantes para Chile, desarrollado con Streamlit y datos oficiales del gobierno.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45+-red.svg)](https://streamlit.io/)
[![GitHub](https://img.shields.io/badge/GitHub-Denniels-black.svg)](https://github.com/Denniels/ds_portfolio)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Daniel%20Andrés%20Mardones-blue.svg)](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)

## 🌟 Características Principales

- **5 Análisis Especializados**: CO2, calidad del agua, demografía, presupuesto público y currículum profesional
- **✅ Análisis CO2 con Datos Reales**: Estudio exhaustivo del RETC 2023 - 15+ Mt de emisiones CO2 oficiales de Chile
- **Pipeline Completo**: Desde Jupyter notebooks hasta aplicación web con datos oficiales del MMA
- **Visualizaciones Interactivas**: Mapas dinámicos, gráficos interactivos y dashboards responsivos
- **Notebooks Jupyter**: Análisis detallados con código documentado y reproducible
- **Optimización de Rendimiento**: Sistema de caché inteligente y preprocesamiento de datos
- **Diseño Responsivo**: Interfaz adaptable a dispositivos móviles y desktop
- **Datos Oficiales**: Fuentes gubernamentales verificadas (RETC, MMA Chile)

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

4. **Generar datos de CO2 (IMPORTANTE):**
```bash
# Ejecutar el notebook de análisis CO2 para generar los datos reales
cd notebooks
jupyter notebook 01_Analisis_Emisiones_CO2_Chile.ipynb
# Ejecutar todas las celdas para generar los archivos JSON en app/data/cache/
```

5. **Ejecutar la aplicación:**
```bash
# Desde el directorio raíz
python -m streamlit run app/main.py

# O usando ruta absoluta
E:\repos\ds_portfolio\.venv_fresh\Scripts\python.exe -m streamlit run "E:\repos\ds_portfolio\app\main.py"
```

5. **Acceder a la aplicación:**
   - URL Local: http://localhost:8501

### Streamlit Cloud ⭐ **LISTO PARA DESPLIEGUE**

La aplicación está **100% optimizada** para Streamlit Cloud con datos reales:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ds-portfolio-chile.streamlit.app)

**Para desplegar tu propia versión:**

1. Fork este repositorio en GitHub
2. **⚠️ IMPORTANTE:** Ejecuta localmente el notebook `01_Analisis_Emisiones_CO2_Chile.ipynb` para generar los datos
3. Commit y push los archivos JSON generados en `app/data/cache/`
4. Conecta tu repositorio a [Streamlit Cloud](https://share.streamlit.io)
5. Configura los siguientes parámetros:
   - **Main file path**: `app/main.py`
   - **Python version**: 3.11
   - **Branch**: `main`

**Archivos necesarios para Streamlit Cloud:**
```
app/data/cache/
├── ✅ emisiones_anuales.json       (Datos anuales RETC)
├── ✅ emisiones_regionales.json    (16 regiones de Chile)
├── ✅ cache_metadata.json          (Metadatos del análisis)
└── maps/
    ├── ✅ regiones_chile_simplificadas.geojson
    └── ✅ regiones_chile_mobile.geojson
```

## 📊 Proyectos y Análisis

### 1. 🏭 Análisis de Emisiones CO2 ⭐ **CON DATOS REALES**
- **Fuente oficial**: Registro de Emisiones y Transferencias de Contaminantes (RETC) 2023
- **Cobertura**: 15+ Mt CO₂, 16 regiones, 50 instalaciones principales
- **Pipeline completo**: Desde datos crudos hasta visualizaciones interactivas
- **Análisis geoespacial**: Mapas de Chile con coordenadas reales
- **Tipos de emisiones**: EFD (Fugitivas Difusas), EFP (Fugitivas Puntuales), TR (Transferencias)
- **Tecnologías**: Pandas, Plotly, Folium, análisis estadístico exploratorio

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

## � Análisis CO2 con Datos Reales - Destacado

### 📊 **Pipeline Completo de Datos Oficiales**

El análisis de emisiones CO2 utiliza **datos oficiales del gobierno chileno**:

#### **Fuentes de Datos:**
- **RETC 2023**: Registro de Emisiones y Transferencias de Contaminantes
- **Ministerio del Medio Ambiente**: Datos gubernamentales verificados
- **3 Datasets oficiales**: EFD, EFP, TR (>1M registros procesados)

#### **Cobertura del Análisis:**
- ✅ **15.0 Mt CO₂**: Total de emisiones registradas oficialmente
- ✅ **16 Regiones**: Cobertura completa de Chile continental  
- ✅ **50 Instalaciones**: Principales emisores identificados
- ✅ **Región Metropolitana**: 7.5 Mt CO₂ (49.9% del total nacional)

#### **Pipeline Técnico:**
```
📄 Datos RETC     →    🔬 Notebook Jupyter    →    📊 Streamlit App
├── 3 CSV files         ├── Análisis EDA             ├── Visualizaciones reales
├── +1M registros       ├── Limpieza de datos        ├── Mapas interactivos
└── Datos oficiales     ├── Detección outliers       └── Conclusiones basadas
                        └── Exporta JSON                 en datos oficiales
```

#### **Tecnologías Aplicadas:**
- **Análisis Estadístico**: Pandas, NumPy, análisis exploratorio
- **Visualización**: Plotly, Folium, mapas interactivos
- **Optimización**: Sistema de caché, compresión de datos
- **Geoespacial**: Coordenadas reales, geometrías simplificadas

> 🎯 **Resultado**: Aplicación web que presenta análisis real y verificable de las emisiones CO₂ en Chile, no simulaciones.

---

## �🛠️ Stack Tecnológico

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
│   │   ├── 01_emisiones_co2.py    # ⭐ CON DATOS REALES RETC
│   │   ├── 02_calidad_agua.py
│   │   ├── 03_demografia_bigquery.py
│   │   ├── 04_presupuesto_publico.py
│   │   ├── 05_curriculum.py        # ⭐ NUEVO
│   │   ├── 06_servicios.py
│   │   └── 07_feedback.py
│   ├── utils/                  # Módulos utilitarios
│   │   ├── cache_manager.py
│   │   ├── optimization.py
│   │   ├── contact_components.py
│   │   └── navigation.py
│   ├── components/             # Componentes reutilizables
│   ├── data/                   # Datos y caché
│   │   └── cache/              # ⭐ DATOS REALES CO2
│   │       ├── emisiones_anuales.json
│   │       ├── emisiones_regionales.json
│   │       ├── cache_metadata.json
│   │       └── maps/
│   └── static/                 # Archivos estáticos
├── notebooks/                  # Jupyter notebooks de análisis
│   ├── 01_Analisis_Emisiones_CO2_Chile.ipynb  # ⭐ GENERA DATOS REALES
│   ├── 02_Analisis_Calidad_Del_Agua.ipynb
│   ├── 03_Analisis_Demografia.ipynb
│   └── 04_Analisis_Presupuesto_Publico.ipynb
├── data/                       # Datos fuente
│   └── raw/                    # Datasets RETC originales
│       ├── retc_emisiones_aire_2023.csv
│       ├── ruea-efd-2023-ckan.csv
│       ├── ruea-efp-2023-ckan.csv
│       └── ruea-tr-2023-ckan.csv
├── docs/                       # Documentación
│   └── curriculum.md           # ⭐ NUEVO
├── .streamlit/                 # Configuración de Streamlit
├── requirements.txt            # Dependencias optimizadas
├── PIPELINE_CO2_CONECTADO_EXITOSO.md  # ⭐ DOCUMENTACIÓN PIPELINE
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

### Versión 2.1 (Junio 2025) ⭐ **ACTUAL**
- ✅ **Pipeline CO2 conectado**: Datos reales del RETC 2023 integrados
- ✅ **15+ Mt CO₂ analizados**: Emisiones oficiales por región
- ✅ **Mapas interactivos reales**: Coordenadas oficiales de Chile
- ✅ **Análisis geoespacial**: 16 regiones con datos verificados
- ✅ **Pipeline robusto**: Notebook → JSON → Streamlit
- ✅ **Optimizado para producción**: Listo para Streamlit Cloud
- ✅ **Documentación completa**: Guías de despliegue actualizadas

### Versión 2.0 (Junio 2025)
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

## 🎯 Estado del Proyecto

### ✅ **Listo para Producción**
- **Pipeline CO2:** 100% conectado con datos reales RETC 2023
- **Optimización:** Archivos JSON comprimidos (~50KB total)
- **Validación:** Probado localmente y listo para Streamlit Cloud
- **Documentación:** Guías completas de despliegue disponibles

### 📁 **Archivos de Documentación Adicionales**
- `PIPELINE_CO2_CONECTADO_EXITOSO.md` - Estado del pipeline implementado
- `GUIA_DESPLIEGUE_STREAMLIT_CLOUD.md` - Instrucciones detalladas de despliegue
- `INFORME_PIPELINE_CO2_VERIFICACION.md` - Análisis inicial del problema resuelto
- `app/data/README.md` - Documentación específica de los datos

### � **Próximo Paso: Desplegar**
```bash
# 1. Verificar que tienes los datos generados
ls app/data/cache/

# 2. Commit y push (si no está hecho)
git add .
git commit -m "feat: ready for Streamlit Cloud with real CO2 data"
git push origin main

# 3. Ir a share.streamlit.io y desplegar
```

## �📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

⭐ **Si este proyecto te resulta útil, no olvides darle una estrella en GitHub!**

🎯 **Estado:** ✅ **LISTO PARA DESPLIEGUE EN STREAMLIT CLOUD CON DATOS REALES**

*Última actualización: 17 de junio de 2025 | Versión 2.1 - Pipeline CO2 Conectado*
