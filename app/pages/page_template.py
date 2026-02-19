"""
Plantilla para páginas del portafolio
"""
import streamlit as st
from pathlib import Path
import sys
from utils.page_setup import setup_page, add_page_title, add_page_footer, create_card

# Configuración de rutas
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Configuración de directorios de datos
DATA_CACHE_DIR = parent_dir / "data" / "cache"
DATA_DIR = parent_dir / "data"

# Configurar la página
st = setup_page(
    title="Título de la Página",  # Cambia esto
    icon="📊"  # Cambia esto
)

# Título de la página
add_page_title(
    "Título Principal",  # Cambia esto
    "Descripción detallada de la página",  # Cambia esto
    "🔍"  # Cambia esto
)

# Ejemplo de estructura de contenido
col1, col2 = st.columns(2)

with col1:
    create_card(
        title="Sección Importante",
        content="Contenido relevante que quieras destacar.",
        icon="💡",
        is_featured=True
    )

with col2:
    create_card(
        title="Otra Sección",
        content="Más contenido interesante.",
        icon="📈"
    )

# Contenido principal
st.header("Contenido Principal")
st.write("Aquí va el contenido específico de tu página.")

# Métricas de ejemplo
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="Métrica 1",
        value="123",
        delta="10%"
    )

with metric_col2:
    st.metric(
        label="Métrica 2",
        value="456",
        delta="-5%"
    )

with metric_col3:
    st.metric(
        label="Métrica 3",
        value="789",
        delta="15%"
    )

# Agregar el footer
add_page_footer()
