"""
Página de currículum vitae
"""
import streamlit as st

# Importar configuración global
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import apply_styles_only
from pathlib import Path
from utils.contact_components import add_page_footer, add_sidebar_contact

# Configuración de la página
st.set_page_config(
    page_title="Currículum | Daniel Mardones",
    page_icon="📄",
    layout="wide"
)

# Aplicar estilos compartidos después de configurar la página
apply_styles_only()

def load_cv_content():
    """Carga el contenido del CV desde el archivo markdown"""
    cv_path = Path(__file__).parent.parent.parent / "docs" / "curriculum.md"
    
    if cv_path.exists():
        return cv_path.read_text(encoding="utf-8")
    else:
        return """
# Daniel Andrés Mardones Sanhueza

## 📊 Data Science | 🔧 Mantenimiento Industrial

> Profesional con más de 10 años de experiencia en mantenimiento industrial,
> transitando hacia el análisis de datos y la ciencia de datos.

### 🎓 Formación

- **Data Science**, Academia Desafío Latam (2023-2024)
- **Ingeniero en Mantenimiento Industrial**, Universidad Técnica Federico Santa María (2008-2013)

### 💼 Experiencia Profesional

#### Ingeniero de Mantenimiento Senior | Integral Service
*2015 - Presente*
- Optimización de procesos industriales
- Análisis de datos para mantenimiento predictivo
- Gestión de equipos técnicos

#### Ingeniero de Planta | Nutraseed
*2013 - 2015*
- Implementación de programas de mantenimiento
- Mejora continua de procesos
- Supervisión de operaciones

### 🛠️ Habilidades Técnicas

#### Análisis de Datos
- Python, Pandas, NumPy
- SQL, BigQuery
- Visualización de datos (Plotly, Matplotlib)

#### Mantenimiento Industrial
- PLCs y automatización
- Análisis de vibraciones
- Mantenimiento predictivo

### 📫 Contacto

- [LinkedIn](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
- [GitHub](https://github.com/Denniels)
- [Web](https://integralservicespa.cl)
"""

def main():
    # Agregar enlaces de contacto al sidebar
    add_sidebar_contact()
    
    # Título
    st.title("📄 Currículum Vitae")
    
    # Cargar y mostrar el contenido del CV
    cv_content = load_cv_content()
    st.markdown(cv_content)
    
    # Botón para descargar CV en PDF (simulado)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 Descargar CV en PDF", type="primary"):
            st.info("Funcionalidad de descarga en desarrollo. Por ahora puedes guardar esta página como PDF desde tu navegador.")
    
    # Enlaces de contacto en el footer
    add_page_footer()

if __name__ == "__main__":
    main()
