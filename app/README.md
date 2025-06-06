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

## 🔧 Estructura de la Aplicación
```
app/
├── Home.py                # Página principal
├── components/           # Componentes reutilizables
│   └── theme.py         # Gestión de temas
└── pages/               # Páginas del dashboard
    └── co2_analysis.py  # Análisis de CO2
```

## 💻 Tecnologías Utilizadas
- **Streamlit**: Framework principal
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Procesamiento de datos
- **NumPy**: Cálculos numéricos

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

## 🔄 Actualizaciones Planificadas
- Nuevos módulos de análisis ambiental
- Más opciones de personalización
- Integración con APIs en tiempo real
- Funcionalidades de exportación mejoradas

## 📈 Datos
Los datos utilizados provienen del Registro de Emisiones y Transferencias de Contaminantes (RETC) de Chile.

## 👥 Contribuciones
Las contribuciones son bienvenidas. Por favor, revisa las guías de contribución en el repositorio principal.
