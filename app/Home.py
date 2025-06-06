import streamlit as st
from components.theme import set_theme, apply_theme

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Datos Ambientales",
    page_icon="🌍",
    layout="wide"
)

# Aplicar tema
set_theme()
apply_theme()

# Contenido de la página principal
st.title("🌎 Análisis de Emisiones en Chile")

st.markdown("""
## Bienvenido al Dashboard de Análisis de Emisiones

Este proyecto presenta un análisis detallado de las emisiones de CO2 y otros contaminantes en Chile, 
basado en datos del Registro de Emisiones y Transferencias de Contaminantes (RETC).

### 🎯 Objetivos del Análisis

1. **Visualización Geoespacial** de emisiones en todo Chile
2. **Análisis Sectorial** de principales emisores
3. **Tendencias Regionales** y patrones de emisión
4. **Identificación** de áreas de oportunidad para reducción

### 📊 Características Principales

- Mapas interactivos de emisiones
- Análisis detallado por región y sector
- Visualizaciones dinámicas
- Datos actualizados del RETC

### 🔍 Cómo Usar

1. Utiliza el menú lateral para navegar entre diferentes análisis
2. Interactúa con los gráficos haciendo hover o zoom
3. Filtra y explora los datos según tu interés

### 📝 Metodología

Los datos provienen del RETC y han sido procesados para garantizar:
- Limpieza y validación
- Normalización de unidades
- Georreferenciación precisa
- Análisis estadístico robusto

### 🤝 Contribuciones

Este es un proyecto de código abierto. Puedes encontrar el código fuente en GitHub y contribuir al análisis.

---
""")

# Mostrar información de contacto y enlaces
col1, col2, col3 = st.columns(3)

with col1:
    st.info("📊 **Explora el Análisis**\n\nUtiliza el menú lateral para navegar por las diferentes secciones del análisis.")

with col2:
    st.warning("📱 **Conéctate**\n\nSigue el proyecto y comparte tus insights en [LinkedIn](https://linkedin.com)")

with col3:
    st.success("💡 **Contribuye**\n\nVisita el [Repositorio en GitHub](https://github.com) para contribuir al proyecto.")
