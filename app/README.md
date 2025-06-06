# Dashboard de Análisis de Datos Ambientales

## 📊 Descripción
Este dashboard interactivo desarrollado con Streamlit proporciona visualizaciones y análisis detallados de datos ambientales en Chile. Actualmente incluye un análisis comprehensivo de emisiones de CO2, con planes de expansión para incluir otros indicadores ambientales.

## 🌟 Características

### Análisis de Emisiones CO2
- Visualización geográfica de emisiones
- Análisis por región y sector
- Identificación de principales emisores
- Distribución por tipo de fuente
- Comparativas interactivas

### Características Técnicas
- Modo claro/oscuro
- Diseño responsivo
- Gráficos interactivos
- Filtros dinámicos
- Exportación de datos
- Optimizaciones para rendimiento en cloud

## 🔧 Estructura de la Aplicación
```
app/
├── Home.py                # Página principal
├── components/           # Componentes reutilizables
│   └── theme.py         # Gestión de temas
├── utils/               # Utilidades y funciones comunes
│   └── data_loader.py   # Carga y procesamiento de datos
└── pages/               # Páginas del dashboard
    └── co2_analysis.py  # Análisis de CO2
```

## 💻 Tecnologías Utilizadas
- **Streamlit**: Framework principal
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Procesamiento de datos
- **NumPy**: Cálculos numéricos
- **Folium**: Mapas interactivos

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de Instalación
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
streamlit run app/Home.py
```

## 📱 Uso de la Aplicación

### Navegación
- Usar la barra lateral para acceder a diferentes análisis
- Botón de tema para cambiar entre modo claro/oscuro
- Controles interactivos en cada sección

### Visualizaciones
- Hacer zoom en el mapa
- Interactuar con gráficos
- Filtrar datos por región
- Exportar visualizaciones

## 📊 Optimizaciones de Rendimiento

Para mejorar el rendimiento en entornos cloud con recursos limitados (como Streamlit Cloud), la aplicación implementa las siguientes optimizaciones:

### Manejo de Datos
- **Muestreo estratificado**: Reducción a 100,000 registros (50% del dataset original)
- **Detección de health checks**: Retorno de datos mínimos durante verificaciones del sistema
- **Conversión de tipos de datos**: Optimización de memoria con tipos apropiados
- **Almacenamiento en caché**: Uso de `st.cache_data` con persistencia en disco

### Visualizaciones
- **Mapas optimizados**: Límite de 5,000 puntos en mapas de calor
- **Gráficos de torta independientes**: Evita errores de DOM con gráficos separados
- **Simplificación de categorías**: Agrupación de categorías menores en "Otros"
- **Manejo robusto de errores**: Captura de excepciones y mensajes informativos

Estas optimizaciones permiten que la aplicación funcione eficientemente en Streamlit Cloud mientras mantiene la integridad del análisis y una experiencia de usuario fluida.

## 🔄 Actualizaciones Planificadas
- Nuevos módulos de análisis ambiental
- Más opciones de personalización
- Integración con APIs en tiempo real
- Funcionalidades de exportación mejoradas

## 📈 Datos
Los datos utilizados provienen del Registro de Emisiones y Transferencias de Contaminantes (RETC) de Chile.

## 👥 Contribuciones
Las contribuciones son bienvenidas. Por favor, revisa las guías de contribución en el repositorio principal.
