# Data Science Portfolio

## 📊 Proyectos Disponibles

### 1. Análisis de Emisiones CO2 en Chile
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/tu-usuario/ds_portfolio/main/app/Home.py)

Análisis comprehensivo de las emisiones de CO2 en Chile basado en datos del RETC.

- [Ver Dashboard Interactivo](https://share.streamlit.io/tu-usuario/ds_portfolio/main/app/Home.py)
- [Ver Análisis Detallado](../notebooks/01_Analisis_Emisiones_CO2_Chile.ipynb)
- [Documentación Técnica](./technical/co2_analysis.md)

#### Características Principales:
- Visualización geoespacial de emisiones
- Análisis por sector y región
- Identificación de principales emisores
- Dashboard interactivo con modo claro/oscuro

## 🚀 Ejecutar Localmente

### Usando Docker
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/ds_portfolio.git
cd ds_portfolio

# Construir y ejecutar con Docker Compose
docker-compose up
```

### Instalación Manual
```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/ds_portfolio.git
cd ds_portfolio

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app/Home.py
```

## 📚 Estructura del Proyecto

```
ds_portfolio/
├── app/                # Aplicaciones Streamlit
├── data/              # Datasets y recursos
├── notebooks/         # Análisis detallados
├── src/              # Código fuente
└── docs/             # Documentación
```

## 🔄 Actualizaciones Periódicas

Este portfolio se actualiza regularmente con nuevos análisis y visualizaciones. Próximos proyectos incluirán:
- Análisis de calidad del aire
- Estudios de impacto ambiental
- Predicción de tendencias climáticas

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](../LICENSE) para más detalles.
