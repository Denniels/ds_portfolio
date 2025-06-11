# Análisis de Datos Ambientales en Chile

Este repositorio contiene análisis comprehensivos de datos ambientales en Chile, incluyendo:
- Emisiones de CO2 (basado en datos del RETC)
- Calidad del agua en lagos y embalses (basado en datos de la DGA)

## 🚀 Características Principales
- Análisis exploratorio detallado de datos ambientales
- Visualizaciones interactivas y mapas dinámicos
- Procesamiento y limpieza avanzada de datos
- Documentación detallada de metodologías analíticas
- Conclusiones y recomendaciones basadas en datos
- Optimizaciones para rendimiento en entornos cloud
- Análisis multivariado de parámetros ambientales
- Detección y evaluación de valores críticos

## 📦 Estructura del Proyecto
```
ds_portfolio/
├── notebooks/          # Guías y análisis interactivos
├── src/               # Código fuente principal
├── data/              # Datasets
├── app/               # Aplicación Streamlit
├── tests/             # Tests unitarios
├── docs/              # Documentación
├── models/            # Modelos entrenados
└── config/            # Configuración
```

## 🛠️ Tecnologías Utilizadas
- Python 3.10+
- Pandas y NumPy para análisis de datos
- Matplotlib, Seaborn y Plotly para visualización
- Jupyter Notebooks para análisis interactivo
- Streamlit para aplicación web interactiva

## 📋 Requisitos
- Python 3.10 o superior
- Dependencias listadas en `requirements.txt`

## 🔧 Instalación
1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

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
