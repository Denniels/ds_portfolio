"""
Gestión de temas para la aplicación (versión original)
"""
import streamlit as st
from pathlib import Path

# Definición de temas disponibles
THEMES = {
    # Temas claros
    "light": {
        "Azul Clásico": {
            "primary_color": "#667eea",
            "background_color": "#ffffff",
            "text_color": "#4a4a4a",
            "secondary_color": "#2E86AB",
            "accent_color": "#764ba2",
            "card_bg": "#ffffff",
            "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "border_color": "#667eea"
        },
        "Verde Esmeralda": {
            "primary_color": "#38b2ac",
            "background_color": "#f7fafc",
            "text_color": "#2d3748",
            "secondary_color": "#319795",
            "accent_color": "#2c7a7b",
            "card_bg": "#ffffff",
            "gradient": "linear-gradient(135deg, #38b2ac 0%, #2c7a7b 100%)",
            "shadow": "0 2px 4px rgba(0,0,0,0.08)",
            "border_color": "#38b2ac"
        },
        "Ambar Cálido": {
            "primary_color": "#ed8936",
            "background_color": "#fffaf0",
            "text_color": "#4a5568",
            "secondary_color": "#dd6b20",
            "accent_color": "#c05621",
            "card_bg": "#ffffff",
            "gradient": "linear-gradient(135deg, #ed8936 0%, #c05621 100%)",
            "shadow": "0 2px 4px rgba(0,0,0,0.05)",
            "border_color": "#ed8936"
        }
    },
    # Temas oscuros
    "dark": {
        "Noche Azul": {
            "primary_color": "#6b8afd",
            "background_color": "#1a202c",
            "text_color": "#e2e8f0",
            "secondary_color": "#4c6ef5",
            "accent_color": "#7f9cf5",
            "card_bg": "#2d3748",
            "gradient": "linear-gradient(135deg, #6b8afd 0%, #4c6ef5 100%)",
            "shadow": "0 4px 6px rgba(0,0,0,0.3)",
            "border_color": "#6b8afd"
        },
        "Ámbar Oscuro": {
            "primary_color": "#f6ad55",
            "background_color": "#1a202c",
            "text_color": "#e2e8f0",
            "secondary_color": "#ed8936",
            "accent_color": "#dd6b20",
            "card_bg": "#2d3748",
            "gradient": "linear-gradient(135deg, #f6ad55 0%, #dd6b20 100%)",
            "shadow": "0 4px 6px rgba(0,0,0,0.3)",
            "border_color": "#f6ad55"
        },
        "Esmeralda Nocturna": {
            "primary_color": "#4fd1c5",
            "background_color": "#1a202c",
            "text_color": "#e2e8f0",
            "secondary_color": "#38b2ac",
            "accent_color": "#319795",
            "card_bg": "#2d3748",
            "gradient": "linear-gradient(135deg, #4fd1c5 0%, #319795 100%)",
            "shadow": "0 4px 6px rgba(0,0,0,0.3)",
            "border_color": "#4fd1c5"
        }
    }
}

def get_theme_names():
    """Devuelve una lista de temas disponibles organizados por modo"""
    themes = {"light": [], "dark": []}
    for mode in THEMES:
        for theme_name in THEMES[mode]:
            themes[mode].append(theme_name)
    return themes

def get_theme_config(mode, theme_name):
    """Obtiene la configuración de un tema específico"""
    try:
        return THEMES[mode][theme_name]
    except KeyError:
        # Si no se encuentra, devuelve el primer tema del modo solicitado
        default_theme = list(THEMES[mode].keys())[0]
        return THEMES[mode][default_theme]

def apply_theme_styles(mode, theme_name):
    """
    Aplica el tema seleccionado usando el sistema de variables CSS dinámicamente.
    """
    from config import get_theme_css
    
    if not hasattr(st.session_state, 'current_theme'):
        st.session_state.current_theme = {'mode': mode, 'name': theme_name}
    
    # Solo actualizar si el tema ha cambiado
    if (st.session_state.current_theme['mode'] != mode or 
        st.session_state.current_theme['name'] != theme_name):
        
        # Actualizar el tema en session_state
        st.session_state.current_theme = {'mode': mode, 'name': theme_name}
        
        # Obtener y aplicar el CSS del tema
        theme_css = get_theme_css(mode, theme_name)
        st.markdown(f'<style>{theme_css}</style>', unsafe_allow_html=True)
        
        # Marcar que necesitamos recargar
        st.session_state.theme_needs_reload = True
    
    return True

def create_theme_selector():
    """Crea un selector de temas en la barra lateral"""
    st.sidebar.markdown("### 🎨 Temas")
    
    # Obtener tema actual
    current_mode = st.session_state.current_theme['mode']
    current_theme = st.session_state.current_theme['name']
    
    # Selector de modo (claro/oscuro)
    mode = st.sidebar.radio(
        "Modo:",
        options=["Claro", "Oscuro"],
        index=0 if current_mode == "light" else 1,
        horizontal=True,
        key="theme_mode_selector",
        label_visibility="collapsed"
    )
    
    # Convertir selección a modo interno
    selected_mode = "light" if mode == "Claro" else "dark"
    
    # Obtener temas disponibles para el modo seleccionado
    theme_names = get_theme_names()
    available_themes = theme_names[selected_mode]
    
    # Selector de tema específico
    selected_theme = st.sidebar.selectbox(
        "Estilo:",
        available_themes,
        index=available_themes.index(current_theme) if current_theme in available_themes else 0,
        key="theme_style_selector"
    )
    
    # Aplicar cambios si es necesario
    if selected_mode != current_mode or selected_theme != current_theme:
        apply_theme_styles(selected_mode, selected_theme)
        
    return {
        'mode': selected_mode,
        'name': selected_theme
    }

"""
Utilidad para manejar el tema de la aplicación
"""
import streamlit as st
from streamlit.components.v1 import html

def init_theme_manager():
    """Inicializa el administrador de temas"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
        
def add_theme_persistance():
    """Agrega el script de persistencia del tema a la página"""
    st.markdown("""
    <script>
    // Función para obtener el tema guardado
    function getStoredTheme() {
        return localStorage.getItem('streamlit_theme') || 'light';
    }

    // Función para guardar el tema actual
    function setStoredTheme(theme) {
        localStorage.setItem('streamlit_theme', theme);
    }

    // Función para aplicar el tema
    function applyTheme(theme) {
        if (theme === 'dark') {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
    }

    // Inicializar tema desde localStorage
    document.addEventListener('DOMContentLoaded', (event) => {
        const storedTheme = getStoredTheme();
        applyTheme(storedTheme);
    });

    // Observar cambios en el tema
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.attributeName === 'class') {
                const isDark = document.body.classList.contains('dark-theme');
                setStoredTheme(isDark ? 'dark' : 'light');
            }
        });
    });

    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ['class']
    });
    </script>
    """, unsafe_allow_html=True)

def get_current_theme():
    """Obtiene el tema actual"""
    return st.session_state.get('theme', 'light')

def toggle_theme():
    """Cambia entre tema claro y oscuro"""
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    # El cambio se refleja automáticamente debido al script de persistencia
