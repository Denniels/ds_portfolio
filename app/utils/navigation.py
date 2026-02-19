"""
Utilidades de navegación para la aplicación
"""
import streamlit as st
from pathlib import Path
import os
from .theme_state import get_theme, toggle_theme

def navigate_to(page_name):
    """
    Función robusta para navegar a una página específica
    
    Args:
        page_name (str): Nombre de la página (sin extensión ni prefijo numérico)
        
    Returns:
        bool: True si la navegación fue exitosa, False en caso contrario
    """
    # Manejo especial para la página principal
    if page_name == "/" or page_name == "main" or page_name == "":
        try:
            st.switch_page("main.py")
            return True
        except Exception:
            st.markdown("""
            <meta http-equiv="refresh" content="0;URL=/" />
            """, unsafe_allow_html=True)
            st.info("Redirigiendo a la página principal...")
            st.stop()
            return True
    
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

def add_theme_selector():
    """Agrega el selector de tema al sidebar"""
    with st.sidebar:
        st.markdown('<div class="theme-selector">', unsafe_allow_html=True)
        # Obtener tema actual
        current_theme = get_theme()
        
        # Selector de tema
        theme = st.radio(
            "🎨 Tema",
            options=['Claro', 'Oscuro'],
            index=0 if current_theme == 'light' else 1,
            key='theme_selector',
            on_change=toggle_theme
        )
        
        st.markdown('</div>', unsafe_allow_html=True)

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

"""
Componente de navegación lateral para el portafolio
"""
import streamlit as st

def get_nav_items():
    """Retorna los items de navegación para el menú lateral"""
    return [
        {
            "name": "Inicio",
            "icon": "🏠",
            "page": "/"
        },
        {
            "name": "Estudios",
            "icon": "📊",
            "items": [
                {
                    "name": "Emisiones CO2",
                    "icon": "🌡️",
                    "page": "01_emisiones_co2"
                },
                {
                    "name": "Calidad del Agua",
                    "icon": "💧",
                    "page": "02_calidad_agua"
                },
                {
                    "name": "Demografía",
                    "icon": "👥",
                    "page": "03_demografia"
                },
                {
                    "name": "Presupuesto",
                    "icon": "💰",
                    "page": "04_presupuesto_publico"
                }
            ]
        },
        {
            "name": "Información",
            "icon": "ℹ️",
            "items": [
                {
                    "name": "Curriculum",
                    "icon": "📄",
                    "page": "05_curriculum"
                },
                {
                    "name": "Servicios",
                    "icon": "🛠️",
                    "page": "06_servicios"
                },
                {
                    "name": "Feedback",
                    "icon": "📝",
                    "page": "07_feedback"
                }
            ]
        },
        {
            "name": "Productos",
            "icon": "💡",
            "items": [
                {
                    "name": "Catálogo",
                    "icon": "🛍️",
                    "page": "08_productos"
                }
            ]
        }
    ]

def create_nav_menu():
    """Crea el menú de navegación lateral"""
    st.sidebar.markdown("### Navegación")
    
    for section in get_nav_items():
        if "items" in section:
            # Sección con submenú
            st.sidebar.markdown(f"#### {section['icon']} {section['name']}")
            
            for item in section["items"]:
                if st.sidebar.button(
                    f"{item['icon']} {item['name']}", 
                    key=f"nav_{section['name']}_{item['name']}",
                    use_container_width=True
                ):
                    navigate_to(item['page'])
            
            st.sidebar.markdown("---")
        else:
            # Sección sin submenú
            if st.sidebar.button(
                f"{section['icon']} {section['name']}", 
                key=f"nav_{section['name']}",
                use_container_width=True
            ):
                navigate_to(section['page'])
    
    # Selector de tema
    current_theme = get_theme()
    theme_icon = "🌙" if current_theme == "dark" else "☀️"
    theme_text = "Modo Oscuro" if current_theme == "dark" else "Modo Claro"
    
    st.sidebar.markdown("#### 🎨 Apariencia")
    if st.sidebar.button(
        f"{theme_icon} {theme_text}",
        key="theme_toggle",
        use_container_width=True
    ):
        toggle_theme()

def init_navigation():
    """Inicializa la navegación y mantiene el estado"""
    # Extraer la página actual de la URL
    try:
        current_path = st.query_params.get('page', [''])[0]
    except:
        current_path = ''
    
    # Actualizar el estado
    if current_path:
        st.session_state.current_page = current_path
    elif 'current_page' not in st.session_state:
        st.session_state.current_page = ''

def get_current_page():
    """Obtiene la página actual"""
    try:
        return st.query_params.get('page', [''])[0]
    except:
        return st.session_state.get('current_page', '')
