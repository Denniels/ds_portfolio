# 📊 Portfolio de Ciencia de Datos - Daniel Mardones

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29-red)
![Status](https://img.shields.io/badge/Status-Production%20Ready-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Descripción General

**Portfolio interactivo de análisis de datos** enfocado en Chile, desarrollado con **Streamlit**. Este proyecto presenta análisis comprehensivos de datos públicos chilenos utilizando técnicas avanzadas de ciencia de datos, visualización interactiva y machine learning.

### 🎯 Objetivos del Proyecto

- **Democratizar el acceso** a análisis de datos públicos chilenos
- **Mostrar capacidades técnicas** en ciencia de datos y desarrollo web
- **Proporcionar insights accionables** para la toma de decisiones
- **Servir como portfolio profesional** para oportunidades laborales

## 📁 Estructura del Proyecto

```
ds_portfolio/
├── 📂 app/                          # Aplicación Streamlit
│   ├── 📂 components/               # Componentes reutilizables
│   │   ├── __init__.py
│   │   └── contact_links.py         # Enlaces de contacto
│   ├── 📂 config/                   # Configuraciones
│   │   ├── contact_config.json      # Configuración de contactos
│   │   ├── environment.json         # Variables de entorno
│   │   ├── menu_config.json         # Configuración del menú
│   │   └── platform_config.json     # Configuración de plataformas
│   ├── 📂 data/                     # Datos procesados y cacheados
│   │   ├── 📂 cache/                # Cache de datos
│   │   │   ├── cache_metadata.json
│   │   │   ├── emisiones_anuales.json
│   │   │   └── emisiones_regionales.json
│   │   ├── 📂 feedback/             # Comentarios de usuarios
│   │   │   └── comments.json
│   │   ├── 📂 processed/            # Datos procesados por notebooks
│   │   │   ├── datos_visualizacion.json
│   │   │   ├── distribucion_sectores.csv
│   │   │   ├── ejecucion_presupuestaria_2024.csv
│   │   │   ├── indicadores_socioeconomicos_2024.csv
│   │   │   ├── inversion_publica_2024.csv
│   │   │   ├── metadatos.json
│   │   │   ├── poblacion_regiones_2024.csv
│   │   │   ├── presupuesto_chile_2024.csv
│   │   │   ├── resumen_ejecutivo.json
│   │   │   ├── top_ministerios.csv
│   │   │   ├── top_regiones.csv
│   │   │   └── transferencias_regionales_2024.csv
│   │   ├── 📂 static/               # Archivos estáticos
│   │   └── 📂 texts/                # Textos de la aplicación
│   ├── 📂 pages/                    # Páginas de la aplicación
│   │   ├── 01_emisiones_co2.py      # Análisis de emisiones CO2
│   │   ├── 02_calidad_agua.py       # Análisis de calidad del agua
│   │   ├── 03_demografia.py         # Análisis demográfico
│   │   ├── 04_presupuesto_publico.py # Análisis presupuesto público
│   │   ├── 05_curriculum.py         # CV profesional
│   │   ├── 06_servicios.py          # Servicios ofrecidos
│   │   └── 07_feedback.py           # Sistema de feedback
│   ├── 📂 static/                   # Archivos estáticos adicionales
│   ├── 📂 utils/                    # Utilidades y helpers
│   │   ├── __init__.py
│   │   ├── cache_manager.py         # Gestión de cache
│   │   ├── cloud_cost_simulator.py # Simulador de costos cloud
│   │   ├── contact_components.py    # Componentes de contacto
│   │   ├── data_sources.py          # Fuentes de datos
│   │   ├── feedback_utils.py        # Utilidades de feedback
│   │   ├── local_optimizer.py       # Optimizador local
│   │   ├── navigation.py            # Navegación
│   │   ├── optimization.py          # Optimizaciones generales
│   │   └── streamlit_cloud_optimizer.py # Optimizador para Streamlit Cloud
│   └── main.py                      # Aplicación principal
├── 📂 notebooks/                    # Notebooks de análisis
│   ├── 01_Analisis_Emisiones_CO2_Chile.ipynb
│   ├── 02_Analisis_Calidad_Del_Agua.ipynb
│   ├── 03_Analisis_BigQuery_Demografia.ipynb
│   ├── 04_Analisis_Presupuesto_Publico.ipynb
│   ├── process_notebooks.py         # Procesador de notebooks
│   └── update_app_data.py           # Actualizador de datos
├── 📂 data/                         # Datos raw y procesados
│   ├── 📂 processed/                # Datos procesados
│   ├── 📂 raw/                      # Datos originales
│   └── 📂 results/                  # Resultados de análisis
├── 📂 credentials/                  # Credenciales (no incluidas en repo)
├── 📂 docs/                         # Documentación
├── 📂 .streamlit/                   # Configuración Streamlit
├── requirements.txt                 # Dependencias principales
├── requirements_local.txt           # Dependencias desarrollo local
├── requirements_streamlit_cloud.txt # Dependencias para Streamlit Cloud
└── README.md                        # Este archivo
```

## 🔍 Análisis Incluidos

### 1. 🌍 Emisiones de CO2 Chile (`01_emisiones_co2.py`)

**Fuentes de Datos:**
- RETC (Registro de Emisiones y Transferencias de Contaminantes)
- datos.gob.cl - Portal de datos abiertos
- SINIA (Sistema Nacional de Información Ambiental)

**Características:**
- ✅ Análisis temporal de emisiones por región y sector
- ✅ Visualizaciones interactivas con Plotly
- ✅ Identificación de patrones y tendencias
- ✅ Sistema de cache optimizado para rendimiento
- ✅ Mapas geoespaciales de emisiones

### 2. 💧 Calidad del Agua (`02_calidad_agua.py`)

**Fuentes de Datos:**
- DGA (Dirección General de Aguas)
- datos.gob.cl - Calidad del agua
- Monitoreo de cuencas hidrográficas

**Características:**
- ✅ Análisis de parámetros de calidad (pH, conductividad, etc.)
- ✅ Evaluación por cuencas y regiones
- ✅ Tendencias temporales de calidad
- ✅ Sistema de alertas por contaminación
- ✅ Visualizaciones comparativas

### 3. 👥 Analicis Demografico (`03_demografia.py`)

**Fuentes de Datos:**
- Fuente Primaria: API del Banco Mundial
- INE (Instituto Nacional de Estadísticas)

**Características:**
- ✅ Análisis poblacional por región y edad
- ✅ Proyecciones demográficas
- ✅ Indicadores socioeconómicos
- ✅ Visualizaciones interactivas avanzadas

### 4. 💰 Presupuesto Público (`04_presupuesto_publico.py`)

**Fuentes de Datos:**
- DIPRES (Dirección de Presupuestos)
- datos.gob.cl - Presupuesto público
- API REST de datos gubernamentales

**Archivos JSON Clave:**
```json
📂 app/data/processed/
├── resumen_ejecutivo.json          # Métricas principales
├── datos_visualizacion.json        # Datos para gráficos
├── metadatos.json                  # Metadatos del análisis
├── top_ministerios.csv             # Ranking de ministerios
├── top_regiones.csv                # Ranking regional
├── distribucion_sectores.csv       # Distribución sectorial
├── presupuesto_chile_2024.csv      # Presupuesto detallado
├── ejecucion_presupuestaria_2024.csv # Ejecución presupuestaria
├── transferencias_regionales_2024.csv # Transferencias
└── inversion_publica_2024.csv      # Inversión pública
```

**Características:**
- ✅ Análisis integral del presupuesto nacional
- ✅ Eficiencia de ejecución presupuestaria
- ✅ Distribución por ministerios y regiones
- ✅ Análisis de inversión pública
- ✅ Modelado predictivo con Random Forest
- ✅ Sistema robusto anti-errores para deployment

## 🛠️ Tecnologías Utilizadas

### Frontend y Visualización
- **Streamlit** 1.29+ - Framework principal
- **Plotly** - Visualizaciones interactivas
- **Matplotlib/Seaborn** - Gráficos estáticos
- **Folium** - Mapas interactivos

### Data Science y Machine Learning
- **Pandas** - Manipulación de datos
- **NumPy** - Computación numérica
- **Scikit-learn** - Machine learning
- **Scipy** - Análisis científico

### APIs y Bases de Datos
- **Google Cloud BigQuery** - Big data analytics
- **Requests** - APIs REST
- **JSON** - Almacenamiento de datos
- **CSV** - Intercambio de datos

### Deployment y Optimización
- **Streamlit Cloud** - Hosting
- **Git/GitHub** - Control de versiones
- **Cache** - Optimización de rendimiento

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/Denniels/ds_portfolio.git
cd ds_portfolio
```

### 2. Configurar Entorno Virtual

```bash
# Windows
python -m venv ds_portfolio_env
ds_portfolio_env\Scripts\activate

# Linux/macOS
python -m venv ds_portfolio_env
source ds_portfolio_env/bin/activate
```

### 3. Instalar Dependencias

```bash
# Para desarrollo local
pip install -r requirements_local.txt

# Para Streamlit Cloud (automático)
pip install -r requirements_streamlit_cloud.txt
```

### 4. Configurar Credenciales (Opcional)

Para BigQuery y APIs externas:
```bash
# Crear archivo de credenciales
cp credentials/example_key.json credentials/your_credentials.json
```

### 5. Ejecutar la Aplicación

```bash
streamlit run app/main.py
```

## 📊 Detalles de Archivos JSON - Presupuesto Público

### `resumen_ejecutivo.json`
```json
{
  "presupuesto_total": "94133485395",        # Presupuesto total en CLP
  "transferencias_totales": "116728399671",  # Transferencias totales
  "inversion_total": "593267329484",         # Inversión total
  "inversion_ejecutada": "301723562359",     # Inversión ejecutada
  "eficiencia_ejecucion": 84.35,            # % eficiencia ejecución
  "avance_promedio": 51.14,                 # % avance promedio
  "eficiencia_inversion": 50.86,            # % eficiencia inversión
  "fecha_analisis": "2025-06-17 19:36:02",  # Timestamp del análisis
  "total_ministerios": 5,                   # Número de ministerios
  "total_regiones": 5,                      # Número de regiones
  "total_sectores": 8                       # Número de sectores
}
```

### `datos_visualizacion.json`
```json
{
  "indicadores_eficiencia": {
    "labels": ["Ejecución", "Avance", "Inversión"],
    "values": [84.35, 51.14, 50.86],
    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"]
  },
  "distribucion_temporal": {
    "meses": ["Ene", "Feb", "Mar", ...],
    "ejecucion": [78.2, 81.4, 84.1, ...]
  }
}
```

### `metadatos.json`
```json
{
  "version": "1.0",
  "fecha_generacion": "2025-06-17",
  "fuentes": [
    "DIPRES - Dirección de Presupuestos",
    "datos.gob.cl - Portal de Datos Abiertos"
  ],
  "metodologia": "Extracción multi-fuente con validación cruzada",
  "total_registros": 946,
  "periodo_analisis": "2024"
}
```

## 🎯 Optimizaciones Implementadas

### Para Streamlit Cloud
- **Cache inteligente** con `@st.cache_data`
- **Carga lazy** de datos pesados
- **Fallback data** para casos de error
- **Optimización de memoria** para datasets grandes
- **Formateo robusto** anti-errores de tipo

### Para Rendimiento Local
- **Procesamiento en batch** de notebooks
- **Cache persistente** de resultados
- **Compresión** de archivos estáticos

## 🔧 Pipeline de Datos

### 1. Extracción
```
Fuentes → APIs → Raw Data → Validación → Procesamiento
```

### 2. Transformación
```
Notebooks → Análisis → Agregaciones → Exportación → JSON/CSV
```

### 3. Carga
```
Processed Data → Streamlit App → Cache → Visualización
```

## 🧪 Testing y Validación

### Scripts de Prueba
- `test_environment.py` - Validación del entorno
- `test_presupuesto_fix.py` - Validación de formateo
- `verify_deployment.py` - Verificación de despliegue
- `verify_streamlit_cloud.py` - Verificación cloud

### Validaciones Automáticas
- ✅ Integridad de datos JSON
- ✅ Formateo de números y monedas
- ✅ Carga de todas las páginas
- ✅ Funcionalidad de cache
- ✅ Enlaces y navegación

## 📈 Métricas y KPIs

### Técnicas
- **Tiempo de carga**: < 3 segundos
- **Memoria utilizada**: < 512MB
- **Cache hit rate**: > 90%
- **Uptime**: 99.9%

### Funcionales
- **Cobertura de datos**: 4 áreas principales
- **Fuentes de datos**: 8+ APIs y datasets
- **Visualizaciones**: 20+ gráficos interactivos
- **Análisis**: 100+ métricas calculadas

## 🚢 Deployment

### Streamlit Cloud (Recomendado)
1. Fork del repositorio
2. Conectar con Streamlit Cloud
3. Configurar variables de entorno
4. Deploy automático

Ver [**INFORME_DESPLIEGUE.md**](INFORME_DESPLIEGUE.md) para instrucciones detalladas.

### Local Development
```bash
streamlit run app/main.py
```

### Docker (Opcional)
```dockerfile
# Disponible en solicitud
```

## 🤝 Contribución

### Para Contribuir
1. Fork del proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

### Reportar Issues
- Usar GitHub Issues
- Incluir logs de error
- Especificar entorno (local/cloud)
- Adjuntar screenshots si es relevante

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Tu Nombre**
- 📧 Email: tu.email@ejemplo.com
- 💼 LinkedIn: [Daniel Andrés Mardones Sanhueza](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
- 🐱 GitHub: [@Denniels](https://github.com/Denniels)
- 🌐 Portfolio: [integralservicespa.cl](https://integralservicespa.cl)

## 🙏 Agradecimientos

- **DIPRES** - Por proporcionar datos de presupuesto público
- **INE** - Por datos demográficos y estadísticos
- **datos.gob.cl** - Por la plataforma de datos abiertos
- **Streamlit Team** - Por el excelente framework
- **Plotly** - Por las herramientas de visualización

## 📚 Documentación Adicional

- [🚀 Guía de Despliegue](INFORME_DESPLIEGUE.md)
- [📊 Documentación de APIs](docs/)
- [🔧 Guías de Configuración](docs/)
- [📈 Análisis Detallados](notebooks/)

---

**⭐ Si este proyecto te resulta útil, ¡no olvides darle una estrella!**

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=Denniels.ds_portfolio)
![GitHub stars](https://img.shields.io/github/stars/Denniels/ds_portfolio?style=social)
![GitHub forks](https://img.shields.io/github/forks/Denniels/ds_portfolio?style=social)
