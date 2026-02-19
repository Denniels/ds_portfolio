"""
Gestor centralizado del ciclo de vida de temas para Streamlit
"""
import streamlit as st
from typing import Dict, Optional, Tuple

class ThemeLifecycleManager:
    """
    Gestiona el ciclo de vida completo de los temas en la aplicación.
    Centraliza la lógica de temas y maneja el estado de forma eficiente.
    """
    
    DEFAULT_THEME = {
        'mode': 'light',
        'name': 'Corporate Blue'
    }
    
    @staticmethod
    def _migrate_legacy_theme(old_theme: dict) -> dict:
        """Migra temas antiguos a los nuevos temas disponibles"""
        legacy_theme_mapping = {
            'Azul Clásico': 'Corporate Blue',
            'Verde Naturaleza': 'Modern Mint',
            'Púrpura Real': 'Slate Pro'
        }
        
        migrated_theme = old_theme.copy()
        if old_theme['name'] in legacy_theme_mapping:
            migrated_theme['name'] = legacy_theme_mapping[old_theme['name']]
        else:
            migrated_theme['name'] = ThemeLifecycleManager.DEFAULT_THEME['name']
        
        return migrated_theme

    @staticmethod
    def initialize_theme_state() -> None:
        """Inicializa el estado del tema si no existe"""
        if 'theme_state' not in st.session_state:
            st.session_state.theme_state = {
                'current_theme': ThemeLifecycleManager.DEFAULT_THEME.copy(),
                'needs_reload': False
            }
        else:
            current_theme = st.session_state.theme_state['current_theme']
            if current_theme['name'] not in ThemeLifecycleManager.get_available_themes():
                st.session_state.theme_state['current_theme'] = ThemeLifecycleManager._migrate_legacy_theme(current_theme)
                st.session_state.theme_state['needs_reload'] = True

    @staticmethod
    def get_available_themes() -> list:
        """Obtiene la lista de temas disponibles"""
        return [
            "Corporate Blue",
            "Modern Mint",
            "Slate Pro",
            "Coral Elegance",
            "Ocean Breeze"
        ]

    @staticmethod
    def get_current_theme() -> Dict[str, str]:
        """Obtiene el tema actual"""
        ThemeLifecycleManager.initialize_theme_state()
        return st.session_state.theme_state['current_theme']
    
    @staticmethod
    def update_theme(mode: str, name: str) -> None:
        """Actualiza el tema actual y marca para recarga si es necesario"""
        ThemeLifecycleManager.initialize_theme_state()
        current = st.session_state.theme_state['current_theme']
        
        if current['mode'] != mode or current['name'] != name:
            st.session_state.theme_state['current_theme'] = {
                'mode': mode,
                'name': name
            }
            st.session_state.theme_state['needs_reload'] = True
    
    @staticmethod
    def check_and_handle_reload() -> bool:
        """
        Verifica si se necesita recargar y maneja el estado
        Returns:
            bool: True si se necesita recargar, False en caso contrario
        """
        ThemeLifecycleManager.initialize_theme_state()
        if st.session_state.theme_state.get('needs_reload', False):
            st.session_state.theme_state['needs_reload'] = False
            return True
        return False
    
    @staticmethod
    def get_theme_vars() -> Tuple[str, str]:
        """
        Obtiene las variables del tema actual
        Returns:
            Tuple[str, str]: (mode, name) del tema actual
        """
        current = ThemeLifecycleManager.get_current_theme()
        return current['mode'], current['name']

def create_theme_selector() -> None:
    """Crea un selector de tema mejorado con opciones profesionales"""
    theme_manager = ThemeLifecycleManager()
    current_theme = theme_manager.get_current_theme()
    
    with st.sidebar.expander("🎨 Tema y Apariencia", expanded=False):
        st.markdown("""
        <div class="theme-description">
        Personaliza la apariencia de la aplicación eligiendo entre temas profesionales diseñados para una óptima legibilidad y elegancia.
        </div>
        """, unsafe_allow_html=True)
        
        # Selector de modo (claro/oscuro)
        mode = st.radio(
            "Modo de visualización",
            options=["light", "dark"],
            format_func=lambda x: "☀️ Claro" if x == "light" else "🌙 Oscuro",
            index=0 if current_theme['mode'] == 'light' else 1,
            key="theme_mode_selector",
            horizontal=True
        )
        
        # Selector de tema con descripciones
        theme_descriptions = {
            "Corporate Blue": "Diseño profesional y confiable",
            "Modern Mint": "Fresco y contemporáneo",
            "Slate Pro": "Elegante y sofisticado",
            "Coral Elegance": "Cálido y acogedor",
            "Ocean Breeze": "Sereno y enfocado"
        }
        
        st.markdown("### Estilo del tema")
        available_themes = ThemeLifecycleManager.get_available_themes()
        theme_name = st.selectbox(
            "Selecciona un tema",
            options=available_themes,
            index=available_themes.index(current_theme['name']) if current_theme['name'] in available_themes else 0,
            key="theme_name_selector",
            help="Elige el estilo visual que mejor represente tu contenido"
        )
        
        # Mostrar descripción del tema seleccionado
        st.markdown(f"""
        <div class="theme-description">
        {theme_descriptions[theme_name]}
        </div>
        """, unsafe_allow_html=True)
        
        # Actualizar tema si hay cambios
        if (mode != current_theme['mode'] or 
            theme_name != current_theme['name']):
            theme_manager.update_theme(mode, theme_name)
            st.rerun()

def apply_theme_styles(mode: Optional[str] = None, theme_name: Optional[str] = None) -> None:
    """Aplica los estilos del tema actual o los especificados"""
    if mode is None or theme_name is None:
        mode, theme_name = ThemeLifecycleManager.get_theme_vars()

    # Variables CSS base - Temas profesionales y elegantes
    theme_vars = {
        'light': {
            'Corporate Blue': {
                '--accent-color': '#2c5282',
                '--bg-color': '#ffffff',
                '--text-color': '#2d3748',
                '--text-secondary': '#4a5568',
                '--sidebar-bg': '#f7fafc',
                '--card-bg': '#fff',
                '--border-color': '#e2e8f0'
            },
            'Modern Mint': {
                '--accent-color': '#276749',
                '--bg-color': '#f0fff4',
                '--text-color': '#1a202c',
                '--text-secondary': '#4a5568',
                '--sidebar-bg': '#f0fff4',
                '--card-bg': '#ffffff',
                '--border-color': '#c6f6d5'
            },
            'Slate Pro': {
                '--accent-color': '#434190',
                '--bg-color': '#f7fafc',
                '--text-color': '#2d3748',
                '--text-secondary': '#4a5568',
                '--sidebar-bg': '#edf2f7',
                '--card-bg': '#ffffff',
                '--border-color': '#e2e8f0'
            },
            'Coral Elegance': {
                '--accent-color': '#c05621',
                '--bg-color': '#fffaf0',
                '--text-color': '#2d3748',
                '--text-secondary': '#4a5568',
                '--sidebar-bg': '#fffaf0',
                '--card-bg': '#ffffff',
                '--border-color': '#feebc8'
            },
            'Ocean Breeze': {
                '--accent-color': '#2c5282',
                '--bg-color': '#ebf8ff',
                '--text-color': '#2d3748',
                '--text-secondary': '#4a5568',
                '--sidebar-bg': '#ebf8ff',
                '--card-bg': '#ffffff',
                '--border-color': '#bee3f8'
            }
        },
        'dark': {
            'Corporate Blue': {
                '--accent-color': '#63b3ed',
                '--bg-color': '#1a202c',
                '--text-color': '#f7fafc',
                '--text-secondary': '#e2e8f0',
                '--sidebar-bg': '#2d3748',
                '--card-bg': '#2d3748',
                '--border-color': '#4a5568'
            },
            'Modern Mint': {
                '--accent-color': '#9ae6b4',
                '--bg-color': '#1a202c',
                '--text-color': '#f7fafc',
                '--text-secondary': '#e2e8f0',
                '--sidebar-bg': '#2d3748',
                '--card-bg': '#2d3748',
                '--border-color': '#2f855a'
            },
            'Slate Pro': {
                '--accent-color': '#7f9cf5',
                '--bg-color': '#1a202c',
                '--text-color': '#f7fafc',
                '--text-secondary': '#e2e8f0',
                '--sidebar-bg': '#2d3748',
                '--card-bg': '#2d3748',
                '--border-color': '#4a5568'
            },
            'Coral Elegance': {
                '--accent-color': '#ed8936',
                '--bg-color': '#1a202c',
                '--text-color': '#f7fafc',
                '--text-secondary': '#e2e8f0',
                '--sidebar-bg': '#2d3748',
                '--card-bg': '#2d3748',
                '--border-color': '#dd6b20'
            },
            'Ocean Breeze': {
                '--accent-color': '#4299e1',
                '--bg-color': '#1a202c',
                '--text-color': '#f7fafc',
                '--text-secondary': '#e2e8f0',
                '--sidebar-bg': '#2d3748',
                '--card-bg': '#2d3748',
                '--border-color': '#2b6cb0'
            }
        }
    }
    
    # Obtener variables del tema actual
    current_vars = theme_vars[mode][theme_name]
    
    # Aplicar estilos mediante CSS
    styles = f"""
    <style>
        :root {{
            --accent-color: {current_vars['--accent-color']};
            --bg-color: {current_vars['--bg-color']};
            --text-color: {current_vars['--text-color']};
            --text-secondary: {current_vars['--text-secondary']};
            --sidebar-bg: {current_vars['--sidebar-bg']};
            --card-bg: {current_vars['--card-bg']};
            --border-color: {current_vars['--border-color']};
        }}
        
        /* Estilos base */
        .stApp {{
            background-color: var(--bg-color);
            color: var(--text-color);
        }}
        
        /* Sidebar y sus componentes */
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] [data-testid="stMarkdown"] {{
            background-color: var(--sidebar-bg);
            color: var(--text-color) !important;
        }}

        /* Ajustes específicos para el sidebar */
        [data-testid="stSidebar"] .stRadio label,
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] p {{
            color: var(--text-color) !important;
        }}

        /* Estilos para secciones del sidebar */
        .sidebar-section {{
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }}

        /* Información de perfil */
        .profile-info h1 {{
            color: var(--accent-color) !important;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}

        .profile-role {{
            color: var(--text-secondary) !important;
            font-size: 1rem;
            margin-bottom: 1rem;
        }}

        /* Enlaces y navegación */
        .sidebar-section a {{
            color: var(--text-color) !important;
            text-decoration: none;
            display: block;
            padding: 0.5rem;
            border-radius: 4px;
            margin-bottom: 0.25rem;
            transition: all 0.2s ease-in-out;
        }}

        .sidebar-section a:hover {{
            background-color: var(--accent-color);
            color: white !important;
            padding-left: 1rem;
        }}

        /* Headers de secciones */
        .sidebar-section h3 {{
            color: var(--accent-color) !important;
            font-size: 1.1rem;
            margin: 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
        }}

        /* Selector de temas */
        [data-testid="stSidebar"] .streamlit-expanderHeader {{
            color: var(--accent-color) !important;
            background-color: transparent;
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
        }}

        .theme-description {{
            color: var(--text-secondary) !important;
            font-size: 0.85rem;
            margin: 0.5rem 0;
            padding: 0.5rem;
            border-radius: 0.25rem;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
        }}

        /* Componentes generales */
        .stButton button {{
            background-color: var(--accent-color);
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            transition: opacity 0.2s;
        }}
        
        .stButton button:hover {{
            opacity: 0.9;
        }}
        
        /* Cards y contenedores */
        .element-container, .stMarkdown {{
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid var(--border-color);
            margin-bottom: 1rem;
        }}
        
        /* Títulos y textos */
        h1, h2, h3 {{
            color: var(--accent-color);
            font-weight: 600;
        }}
        
        .text-secondary {{
            color: var(--text-secondary);
        }}
        
        /* Formularios */
        .stSelectbox [data-baseweb="select"] {{
            background-color: var(--card-bg);
            border-color: var(--border-color);
            color: var(--text-color);
        }}
        
        .stTextInput input {{
            background-color: var(--card-bg);
            border-color: var(--border-color);
            color: var(--text-color);
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: var(--sidebar-bg);
            border-radius: 0.5rem;
            padding: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: var(--text-color);
        }}
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {{
            color: var(--accent-color);
            font-weight: 600;
        }}
        
        /* Scrollbars */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--bg-color);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--accent-color);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            opacity: 0.8;
        }}
    </style>
    """
    
    st.markdown(styles, unsafe_allow_html=True)
