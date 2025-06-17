"""
Utilidades de navegación para la aplicación
"""
import streamlit as st
from pathlib import Path
import os

def create_back_button(label="← Volver al Inicio", path=None):
    """
    Crea un botón para regresar a la página principal
    
    Args:
        label (str): Texto para el botón
        path (str, optional): Ruta alternativa. Por defecto regresa a main.py
    """
    if path is None:
        # Por defecto, volver al inicio
        path = "main.py"
    
    if st.button(label):
        st.switch_page(path)

def create_page_navigation(pages_dict, title="Navegación"):
    """
    Crea un menú de navegación entre páginas
    
    Args:
        pages_dict (dict): Diccionario con etiquetas como claves y rutas como valores
        title (str): Título del menú de navegación
    """
    st.sidebar.markdown(f"### {title}")
    
    for label, path in pages_dict.items():
        if st.sidebar.button(label):
            st.switch_page(path)
    
    st.sidebar.markdown("---")

def get_page_path(page_name):
    """
    Obtiene la ruta a una página por su nombre
    
    Args:
        page_name (str): Nombre de la página (sin extensión)
        
    Returns:
        str: Ruta a la página
    """
    pages_dir = Path(__file__).parent.parent / "pages"
    
    # Buscar archivo que comience con el nombre proporcionado
    for file_path in pages_dir.glob(f"{page_name}*.py"):
        return str(file_path.relative_to(Path(__file__).parent.parent))
    
    # Si no se encuentra, buscar en todas las páginas
    for file_path in pages_dir.glob("*.py"):
        if page_name.lower() in file_path.stem.lower():
            return str(file_path.relative_to(Path(__file__).parent.parent))
    
    # Si no se encuentra ninguna coincidencia, devolver None
    return None

def create_sidebar_nav_menu():
    """
    Crea un menú de navegación en la barra lateral con todas las páginas disponibles
    """
    st.sidebar.markdown("### 📑 Navegación")
    
    # Obtener todas las páginas
    pages_dir = Path(__file__).parent.parent / "pages"
    pages = []
    
    for file_path in pages_dir.glob("*.py"):
        # Ignorar archivos que comienzan con _ (módulos internos)
        if not file_path.stem.startswith("_"):
            # Intentar leer el título de la página desde el archivo
            title = _get_page_title(file_path)
            if not title:
                title = file_path.stem.replace("_", " ").title()
            
            pages.append({
                "title": title,
                "path": str(file_path.relative_to(Path(__file__).parent.parent)),
                "order": int(file_path.stem.split("_")[0]) if file_path.stem[0].isdigit() else 99
            })
    
    # Ordenar páginas por el número de orden
    pages.sort(key=lambda x: x["order"])
    
    # Crear botones para cada página
    for page in pages:
        if st.sidebar.button(page["title"]):
            st.switch_page(page["path"])
    
    # Botón para volver al inicio
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 Página Principal"):
        st.switch_page("main.py")

def _get_page_title(file_path):
    """
    Intenta extraer el título de una página desde el archivo
    
    Args:
        file_path (Path): Ruta al archivo de la página
        
    Returns:
        str: Título extraído o None
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Buscar título en st.title o st.header
            import re
            title_match = re.search(r'st\.title\(["\'](.+?)["\']\)', content)
            if title_match:
                return title_match.group(1)
            
            header_match = re.search(r'st\.header\(["\'](.+?)["\']\)', content)
            if header_match:
                return header_match.group(1)
            
        return None
    except:
        return None
