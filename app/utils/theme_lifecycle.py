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
        
        return migrated_theme    @staticmethod
    def initialize_theme_state() -> None:
        """Inicializa el estado del tema de forma robusta usando múltiples fuentes"""
        current_theme = None
          # Fuente 1: Comprobar query parameters en la URL
        try:
            # Usar la nueva API de query params (Streamlit v1.22+)
            query_params = st.query_params if hasattr(st, 'query_params') else {}
            
            if 'theme_mode' in query_params and 'theme_name' in query_params:
                mode = query_params['theme_mode']
                name = query_params['theme_name']
                
                # Manejar si query_params devuelve listas (versiones anteriores)
                if isinstance(mode, list):
                    mode = mode[0]
                if isinstance(name, list):
                    name = name[0]
                    
                if (mode in ['light', 'dark'] and 
                    name in ThemeLifecycleManager.get_available_themes()):
                    current_theme = {'mode': mode, 'name': name}
                    # Limpiar query params después de extraer el tema si es posible
                    try:
                        if hasattr(st, 'query_params'):
                            st.query_params.clear()
                    except:
                        pass
        except:
            pass
        
        # Fuente 2: theme_state (principal)
        if current_theme is None:
            if ('theme_state' in st.session_state and 
                isinstance(st.session_state.theme_state, dict) and 
                'current_theme' in st.session_state.theme_state):
                candidate = st.session_state.theme_state['current_theme']
                if (isinstance(candidate, dict) and 
                    'mode' in candidate and 
                    'name' in candidate and
                    candidate['name'] in ThemeLifecycleManager.get_available_themes()):
                    current_theme = candidate
        
        # Fuente 3: variables legadas
        if current_theme is None:
            if ('theme_mode' in st.session_state and 
                'theme_name' in st.session_state and
                st.session_state.theme_name in ThemeLifecycleManager.get_available_themes()):
                current_theme = {
                    'mode': st.session_state.theme_mode,
                    'name': st.session_state.theme_name
                }
        
        # Fuente 4: current_theme directo
        if current_theme is None:
            if ('current_theme' in st.session_state and 
                isinstance(st.session_state.current_theme, dict) and
                'mode' in st.session_state.current_theme and
                'name' in st.session_state.current_theme and
                st.session_state.current_theme['name'] in ThemeLifecycleManager.get_available_themes()):
                current_theme = st.session_state.current_theme
        
        # Si no hay tema válido, usar el por defecto
        if current_theme is None:
            current_theme = ThemeLifecycleManager.DEFAULT_THEME.copy()
        
        # Asegurar que el estado esté sincronizado en todas las variables
        st.session_state.theme_state = {
            'current_theme': current_theme.copy(),
            'needs_reload': False
        }
        
        # Sincronizar con variables legadas para compatibilidad
        st.session_state.current_theme = current_theme.copy()
        st.session_state.theme_mode = current_theme['mode']
        st.session_state.theme_name = current_theme['name']
        
        # Inyectar JavaScript para mantener sincronización con localStorage
        js_sync = f"""
        <script>
        // Sincronizar tema con localStorage
        const currentTheme = {{
            mode: '{current_theme['mode']}',
            name: '{current_theme['name']}'
        }};
        
        try {{
            localStorage.setItem('portfolio_theme', JSON.stringify(currentTheme));
            document.cookie = `portfolio_theme_mode=${{currentTheme.mode}}; path=/; max-age=31536000`;
            document.cookie = `portfolio_theme_name=${{currentTheme.name}}; path=/; max-age=31536000`;
        }} catch (e) {{
            console.log('Error saving theme:', e);
        }}
        </script>
        """
        st.markdown(js_sync, unsafe_allow_html=True)

    @staticmethod
    def get_available_themes() -> list:
        """Obtiene la lista de temas disponibles"""
        return [
            "Corporate Blue",            "Modern Mint",
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
        """Actualiza el tema actual y lo persiste en múltiples ubicaciones incluyendo localStorage"""
        ThemeLifecycleManager.initialize_theme_state()
        
        new_theme = {'mode': mode, 'name': name}
        
        # Actualizar en todas las ubicaciones para máxima persistencia
        st.session_state.theme_state = {
            'current_theme': new_theme.copy(),
            'needs_reload': True
        }
        
        # Sincronizar con variables legadas
        st.session_state.current_theme = new_theme.copy()
        st.session_state.theme_mode = mode
        st.session_state.theme_name = name
        
        # Guardar en localStorage usando JavaScript
        js_save_theme = f"""
        <script>
        try {{
            const theme = {{
                mode: '{mode}',
                name: '{name}'
            }};
            localStorage.setItem('portfolio_theme', JSON.stringify(theme));
            console.log('Theme saved to localStorage:', theme);
        }} catch (e) {{
            console.error('Error saving theme to localStorage:', e);
        }}
        </script>
        """
        
        st.markdown(js_save_theme, unsafe_allow_html=True)
        
        # Forzar aplicación inmediata
        ThemeLifecycleManager.apply_theme_styles()
    
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
    def force_theme_persistence() -> None:
        """
        Fuerza la persistencia del tema actual en todas las variables de estado
        """
        ThemeLifecycleManager.initialize_theme_state()
        current = ThemeLifecycleManager.get_current_theme()
        
        # Asegurar que el tema esté en todas las ubicaciones posibles
        st.session_state.theme_state = {
            'current_theme': current.copy(),
            'needs_reload': False
        }
        
        # Mantener compatibilidad con variables legadas
        st.session_state.current_theme = current.copy()
        st.session_state.theme_mode = current['mode']
        st.session_state.theme_name = current['name']
          # También agregar algunas variables adicionales para debugging
        st.session_state.theme_initialized = True
        st.session_state.last_theme_update = current.copy()
    
    @staticmethod
    def check_localstorage_theme() -> None:
        """
        Verifica si hay un tema en localStorage y lo aplica si es diferente al actual
        """
        # JavaScript para verificar localStorage y aplicar tema si es necesario
        js_check_theme = """
        <script>
        function checkAndApplyLocalStorageTheme() {
            try {
                const stored = localStorage.getItem('portfolio_theme');
                if (stored) {
                    const theme = JSON.parse(stored);
                    if (theme.mode && theme.name) {
                        // Verificar si el tema actual es diferente
                        const currentThemeElements = document.querySelectorAll('[data-testid="stSelectbox"] select');
                        let needsUpdate = false;
                        
                        // Verificar modo (radio buttons)
                        const modeRadios = document.querySelectorAll('input[type="radio"]');
                        for (let radio of modeRadios) {
                            if (radio.checked) {
                                const isLight = radio.value === 'light' || radio.nextElementSibling?.textContent?.includes('Claro');
                                const isCurrentLight = theme.mode === 'light';
                                if (isLight !== isCurrentLight) {
                                    needsUpdate = true;
                                    break;
                                }
                            }
                        }
                        
                        if (needsUpdate) {
                            console.log('Applying theme from localStorage:', theme);
                            // Simular click en el modo correcto
                            for (let radio of modeRadios) {
                                const isLight = radio.nextElementSibling?.textContent?.includes('Claro');
                                const shouldSelect = (theme.mode === 'light' && isLight) || (theme.mode === 'dark' && !isLight);
                                if (shouldSelect && !radio.checked) {
                                    radio.click();
                                    break;
                                }
                            }
                        }
                    }
                }
            } catch (e) {
                console.log('Error checking localStorage theme:', e);
            }
        }
        
        // Ejecutar después de que la página se carga
        setTimeout(checkAndApplyLocalStorageTheme, 500);
        setTimeout(checkAndApplyLocalStorageTheme, 1000);
        setTimeout(checkAndApplyLocalStorageTheme, 2000);
        </script>
        """
        
        st.markdown(js_check_theme, unsafe_allow_html=True)
    
    @staticmethod
    def get_theme_vars() -> Tuple[str, str]:
        """
        Obtiene las variables del tema actual
        Returns:
            Tuple[str, str]: (mode, name) del tema actual
        """
        current = ThemeLifecycleManager.get_current_theme()
        return current['mode'], current['name']

    @staticmethod
    def get_theme_colors(theme_name: str, mode: str) -> Dict[str, str]:
        """
        Obtiene los colores para el tema y modo especificados
        """
        theme_colors = {
            "Corporate Blue": {
                "light": {
                    "primary": "#0066cc",
                    "secondary": "#4d94ff",
                    "background": "#ffffff",
                    "text": "#333333",
                    "accent": "#0052a3"
                },
                "dark": {
                    "primary": "#66b3ff",
                    "secondary": "#0066cc",
                    "background": "#1a1a1a",
                    "text": "#ffffff",
                    "accent": "#99ccff"
                }
            },
            "Modern Mint": {
                "light": {
                    "primary": "#2ecc71",
                    "secondary": "#27ae60",
                    "background": "#ffffff",
                    "text": "#2c3e50",
                    "accent": "#16a085"
                },
                "dark": {
                    "primary": "#2ecc71",
                    "secondary": "#27ae60",
                    "background": "#1a1a1a",
                    "text": "#ecf0f1",
                    "accent": "#16a085"
                }
            },
            "Slate Pro": {
                "light": {
                    "primary": "#34495e",
                    "secondary": "#7f8c8d",
                    "background": "#ecf0f1",
                    "text": "#2c3e50",
                    "accent": "#95a5a6"
                },
                "dark": {
                    "primary": "#bdc3c7",
                    "secondary": "#95a5a6",
                    "background": "#2c3e50",
                    "text": "#ecf0f1",
                    "accent": "#7f8c8d"
                }
            },
            "Coral Elegance": {
                "light": {
                    "primary": "#ff6b6b",
                    "secondary": "#ff8787",
                    "background": "#ffffff",
                    "text": "#333333",
                    "accent": "#fa5252"
                },
                "dark": {
                    "primary": "#ff8787",
                    "secondary": "#ff6b6b",
                    "background": "#1a1a1a",
                    "text": "#ffffff",
                    "accent": "#ffa8a8"
                }
            },
            "Ocean Breeze": {
                "light": {
                    "primary": "#00b4d8",
                    "secondary": "#48cae4",
                    "background": "#ffffff",
                    "text": "#333333",
                    "accent": "#0096c7"
                },
                "dark": {
                    "primary": "#48cae4",
                    "secondary": "#00b4d8",
                    "background": "#1a1a1a",
                    "text": "#ffffff",
                    "accent": "#90e0ef"
                }
            }
        }
        
        return theme_colors.get(theme_name, theme_colors["Corporate Blue"])[mode]

    @staticmethod
    def _hex_to_rgb(hex_color):
        """
        Convierte un color hexadecimal a RGB
        
        Args:
            hex_color (str): Color en formato hexadecimal (#RRGGBB)
            
        Returns:
            str: Valores RGB separados por comas
        """
        # Eliminar el # si existe
        hex_color = hex_color.lstrip('#')
        
        # Convertir a RGB
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return f"{r}, {g}, {b}"

    @staticmethod
    def apply_theme_styles() -> None:
        """
        Aplica los estilos CSS del tema actual
        """
        mode, name = ThemeLifecycleManager.get_theme_vars()
        colors = ThemeLifecycleManager.get_theme_colors(name, mode)
        
        # Crear variables RGB para permitir transparencia
        rgb_vars = {k: ThemeLifecycleManager._hex_to_rgb(v) for k, v in colors.items()}
        
        # CSS base para modo claro/oscuro
        css = f"""
        /* Variables globales del tema */
        :root {{
            --primary-color: {colors['primary']};
            --primary-rgb: {rgb_vars['primary']};
            --secondary-color: {colors['secondary']};
            --secondary-rgb: {rgb_vars['secondary']};
            --background-color: {colors['background']};
            --background-rgb: {rgb_vars['background']};
            --text-color: {colors['text']};
            --text-rgb: {rgb_vars['text']};
            --accent-color: {colors['accent']};
            --accent-rgb: {rgb_vars['accent']};
            --text-secondary: {'rgba(0, 0, 0, 0.6)' if mode == 'light' else 'rgba(255, 255, 255, 0.7)'};
            --border-color: {'rgba(0, 0, 0, 0.1)' if mode == 'light' else 'rgba(255, 255, 255, 0.1)'};
        }}
        
        /* Estilos generales */
        .main {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        
        /* Estilos para la barra lateral */
        .css-1d391kg {{  /* Selector para sidebar */
            background-color: var(--background-color);
        }}
        
        .css-1d391kg .css-17z41qg {{  /* Texto del sidebar */
            color: var(--text-color) !important;
        }}
        
        /* Botones y controles */
        .stButton>button {{
            background-color: var(--primary-color);
            color: {'#ffffff' if mode == 'light' else '#1a1a1a'};
            border: none;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            background-color: var(--accent-color);
            transform: translateY(-1px);
        }}
        
        /* Enlaces */
        a {{
            color: var(--primary-color);
            text-decoration: none;
            transition: color 0.2s ease;
        }}
        
        a:hover {{
            color: var(--accent-color);
            text-decoration: underline;
        }}
        
        /* Métricas y KPIs */
        .css-1xarl3l {{  /* Métricas */
            background-color: var(--secondary-color);
            color: {'#1a1a1a' if mode == 'light' else '#ffffff'};
            padding: 1rem;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Tarjetas y contenedores */
        .css-1r6slb0 {{  /* Contenedores */
            background-color: {'#f8f9fa' if mode == 'light' else '#2d3436'};
            border: 1px solid {'#dee2e6' if mode == 'light' else '#4d4d4d'};
            border-radius: 4px;
            padding: 1rem;
            margin: 0.5rem 0;
        }}
        
        /* Estilos específicos para el sidebar en modo oscuro */
        [data-testid="stSidebar"] [data-testid="stMarkdown"] {{
            color: var(--text-color) !important;
        }}
        
        /* Forzar visibilidad de texto en sidebar */
        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] li {{
            color: var(--text-color) !important;
            text-shadow: none !important;
        }}        """
        
        st.markdown(
            f'<style>{css}</style>',
            unsafe_allow_html=True
        )

    @staticmethod
    def ensure_theme_consistency() -> None:
        """
        Asegura la consistencia del tema en la página actual sin forzar reinicios innecesarios
        """
        # Inicializar estado si es necesario (preservando configuración existente)
        ThemeLifecycleManager.initialize_theme_state()
        
        # Forzar persistencia del tema
        ThemeLifecycleManager.force_theme_persistence()
        
        # Aplicar estilos del tema actual
        ThemeLifecycleManager.apply_theme_styles()
          # Solo reiniciar si realmente se necesita (cambio de tema)
        if ThemeLifecycleManager.check_and_handle_reload():
            st.rerun()
    
    @staticmethod
    def debug_theme_state() -> None:
        """
        Función de depuración para mostrar el estado actual del tema
        Solo para desarrollo/debugging
        """
        if st.session_state.get('STREAMLIT_DEBUG_THEME', False):
            with st.sidebar.expander("🔧 Debug Tema", expanded=False):
                st.write("**Estado theme_state:**")
                st.json(st.session_state.get('theme_state', 'No existe'))
                
                st.write("**Variables legadas:**")
                st.write(f"current_theme: {st.session_state.get('current_theme', 'No existe')}")
                st.write(f"theme_mode: {st.session_state.get('theme_mode', 'No existe')}")
                st.write(f"theme_name: {st.session_state.get('theme_name', 'No existe')}")
                st.write("**Tema detectado por get_current_theme:**")
                current = ThemeLifecycleManager.get_current_theme()
                st.json(current)
    
    @staticmethod
    def force_theme_from_url() -> None:
        """
        Intenta forzar el tema usando query parameters en la URL
        """
        try:
            # Intentar obtener tema de query params
            query_params = st.query_params
            
            if 'theme_mode' in query_params and 'theme_name' in query_params:
                mode = query_params['theme_mode']
                name = query_params['theme_name']
                
                if (mode in ['light', 'dark'] and 
                    name in ThemeLifecycleManager.get_available_themes()):
                    
                    # Aplicar tema
                    ThemeLifecycleManager.update_theme(mode, name)
                    
                    # Limpiar query params para evitar loops
                    st.query_params.clear()
                    
        except Exception as e:
            pass  # Fallar silenciosamente
