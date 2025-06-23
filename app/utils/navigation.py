"""
Utilidades de navegación para la aplicación
"""
import streamlit as st
from pathlib import Path
import os

def navigate_to(page_name):
    """
    Función robusta para navegar a una página específica
    
    Args:
        page_name (str): Nombre de la página (sin extensión ni prefijo numérico)
        
    Returns:
        bool: True si la navegación fue exitosa, False en caso contrario
    """
    # Directorio de páginas
    pages_dir = Path(__file__).parent.parent / "pages"
    
    # Verificar si el nombre ya incluye la extensión .py
    if page_name.endswith('.py'):
        page_name = page_name[:-3]
    
    # Verificar si el nombre ya incluye el prefijo del directorio pages/
    if page_name.startswith('pages/'):
        page_name = page_name[6:]
        
    # Primero, buscar coincidencia exacta
    for file_path in pages_dir.glob("*.py"):
        if file_path.stem == page_name:
            try:
                st.switch_page(f"pages/{file_path.name}")
                return True
            except Exception:
                # Fallback para versiones antiguas de Streamlit
                st.markdown(f"""
                <meta http-equiv="refresh" content="0;URL={file_path.stem}" />
                """, unsafe_allow_html=True)
                st.info(f"Redirigiendo a {file_path.stem}...")
                st.stop()
                return True
    
    # Segundo, buscar por número de prefijo + nombre
    for file_path in pages_dir.glob("[0-9]*_*.py"):
        # Extrae el nombre sin el prefijo numérico
        name_without_prefix = '_'.join(file_path.stem.split('_')[1:])
        if name_without_prefix.lower() == page_name.lower() or file_path.stem.lower() == page_name.lower():
            try:
                st.switch_page(f"pages/{file_path.name}")
                return True
            except Exception:
                # Fallback para versiones antiguas de Streamlit
                st.markdown(f"""
                <meta http-equiv="refresh" content="0;URL={file_path.stem}" />
                """, unsafe_allow_html=True)
                st.info(f"Redirigiendo a {file_path.stem}...")
                st.stop()
                return True
    
    # Si no se encuentra, intentar con una búsqueda más flexible
    for file_path in pages_dir.glob("*.py"):
        if page_name.lower() in file_path.stem.lower():
            try:
                st.switch_page(f"pages/{file_path.name}")
                return True
            except Exception:
                # Fallback para versiones antiguas de Streamlit
                st.markdown(f"""
                <meta http-equiv="refresh" content="0;URL={file_path.stem}" />
                """, unsafe_allow_html=True)
                st.info(f"Redirigiendo a {file_path.stem}...")
                st.stop()
                return True
    
    return False

def nav_button(label, page_name, key=None):
    """
    Crea un botón que navega a una página específica
    
    Args:
        label (str): Texto para el botón
        page_name (str): Nombre de la página de destino
        key (str, optional): Clave única para el botón
    """
    if st.button(label, key=key):
        navigate_to(page_name)

def large_nav_button(label, page_name, key=None):
    """
    Crea un botón grande de navegación que abarca todo el ancho
    
    Args:
        label (str): Texto para el botón
        page_name (str): Nombre de la página de destino
        key (str, optional): Clave única para el botón
    """
    if st.button(label, key=key, use_container_width=True):
        navigate_to(page_name)

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

def create_robust_sidebar_nav():
    """
    Crea un menú de navegación en la barra lateral usando los métodos de redirección robustos
    """
    import sys
    from pathlib import Path
    
    # Asegurarse que utils está en el path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    if str(parent_dir) not in sys.path:
        sys.path.append(str(parent_dir))
          # Función de navegación robusta para botones
    def create_redirect_button(label, target_page, key=None, **kwargs):
        if st.sidebar.button(label, key=key):
            try:
                if target_page.endswith('.py'):
                    st.switch_page(target_page)
                else:
                    st.switch_page(f"{target_page}.py")
            except:
                # Fallback silencioso con meta refresh
                html_refresh = f"""
                    <meta http-equiv="refresh" content="0;URL='/{target_page}'" />
                """
                st.markdown(html_refresh, unsafe_allow_html=True)
                st.stop()
    
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
    for i, page in enumerate(pages):
        button_text = page["title"].split(" - ")[0] if " - " in page["title"] else page["title"]
        if st.sidebar.button(button_text, key=f"side_btn_{i}"):
            try:
                st.switch_page(page["path"])
            except:
                # Fallback con redirección HTML
                html = f"""
                    <meta http-equiv="refresh" content="0;URL='/{page["path"]}'" />
                    <p>Redirigiendo a {page["title"]}...</p>
                """
                st.markdown(html, unsafe_allow_html=True)
                st.stop()
    
    # Ya no agregamos el botón duplicado para volver al inicio
    # La navegación ya tiene los enlaces necesarios en la parte superior

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
