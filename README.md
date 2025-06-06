# Análisis de Emisiones de CO2 en Chile

Este repositorio contiene un análisis comprehensivo de las emisiones de CO2 en Chile, utilizando datos del Registro de Emisiones y Transferencias de Contaminantes (RETC).

## 🚀 Características Principales
- Análisis exploratorio detallado de datos de emisiones
- Visualizaciones interactivas y mapas
- Procesamiento y limpieza avanzada de datos
- Documentación detallada del proceso analítico
- Conclusiones y recomendaciones basadas en datos
- Optimizaciones para rendimiento en entornos cloud

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
