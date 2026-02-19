"""
Componente de selector de tema para el sidebar
"""
import streamlit as st
from utils.theme_selector import (
    initialize_theme,
    apply_theme,
    LIGHT_THEMES,
    DARK_THEMES
)

def get_theme_name_from_state():
    """Obtiene el nombre del tema actual del session_state"""
    current_theme = st.session_state.get('current_theme', 'Ocean Breeze')
    return str(current_theme) if current_theme else 'Ocean Breeze'

def render_theme_switcher():
    """Renderiza el selector de tema en el sidebar"""
    # Inicializar tema si es necesario
    initialize_theme()
    
    # Contenedor para el selector de tema
    with st.sidebar:
        st.markdown("""
            <style>
            /* Contenedor del selector de tema */
            .theme-container {
                background: linear-gradient(135deg,
                    rgba(var(--primary-color-rgb), 0.1),
                    rgba(var(--secondary-color-rgb), 0.1)
                );
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1rem 0;
                transition: all 0.3s ease;
            }
            
            .theme-container:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.15);
            }
            
            /* Cabecera del selector */
            .theme-header {
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--primary-color);
                background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            /* Toggle y selector personalizados */
            [data-testid="stCheckbox"], 
            [data-testid="stSelectbox"] {
                background: rgba(255, 255, 255, 0.05) !important;
                border-radius: 12px !important;
                padding: 0.5rem !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                transition: all 0.3s ease !important;
            }
            
            [data-testid="stCheckbox"]:hover,
            [data-testid="stSelectbox"]:hover {
                background: rgba(255, 255, 255, 0.1) !important;
                border-color: var(--primary-color) !important;
            }
            
            /* Tema seleccionado */
            .theme-selected {
                margin-top: 1rem;
                padding: 1rem;
                border-radius: 12px;
                background: linear-gradient(135deg,
                    var(--primary-color)15,
                    var(--secondary-color)15
                );
                border: 1px solid var(--primary-color)25;
            }
            
            /* Previsualización del tema */
            .theme-preview {
                height: 80px;
                border-radius: 12px;
                background: linear-gradient(135deg,
                    var(--primary-color),
                    var(--secondary-color)
                );
                margin-top: 1rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
            }
            
            .theme-preview:hover {
                transform: scale(1.02);
                box-shadow: 0 6px 16px rgba(0,0,0,0.15);
            }
            </style>
            <div class="theme-container">
                <div class="theme-header">
                    <span>🎨</span>
                    <span>Personalización</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Modo claro/oscuro con mejor estilo
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("🌙")
        with col2:
            dark_mode = st.toggle("Modo Oscuro", st.session_state.get('is_dark_mode', False))
        
        # Temas disponibles según modo
        available_themes = DARK_THEMES if dark_mode else LIGHT_THEMES
        current_theme_name = get_theme_name_from_state()
        
        # Si cambiamos de modo, usar el primer tema del nuevo modo
        if dark_mode != st.session_state.get('is_dark_mode', False):
            current_theme_name = list(available_themes.keys())[0]
        
        # Selector de tema con íconos mejorados
        theme_options = {
            'Ocean Breeze': '🌊 Ocean Breeze',
            'Spring Garden': '🌿 Spring Garden',
            'Sunset Warm': '🌅 Sunset Warm',
            'Purple Rain': '💜 Purple Rain',
            'Coffee & Cream': '☕ Coffee & Cream',
            'Night Ocean': '🌌 Night Ocean',
            'Dark Forest': '🌲 Dark Forest',
            'Midnight Purple': '🌃 Midnight Purple',
            'Dark Rust': '🌆 Dark Rust',
            'Deep Space': '🚀 Deep Space'
        }
        
        # Encontrar el índice del tema actual
        try:
            theme_index = list(available_themes.keys()).index(current_theme_name)
        except ValueError:
            theme_index = 0
            current_theme_name = list(available_themes.keys())[0]
        
        st.markdown("<div class='theme-selected'>", unsafe_allow_html=True)
        selected_theme = st.selectbox(
            "Selecciona un tema",
            options=list(available_themes.keys()),
            format_func=lambda x: theme_options.get(x, x),
            index=theme_index
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Aplicar tema si hay cambios y persistir en session_state
        if selected_theme != current_theme_name or dark_mode != st.session_state.get('is_dark_mode', False):
            st.session_state.is_dark_mode = dark_mode
            st.session_state.current_theme = selected_theme
            apply_theme(theme_name=selected_theme, is_dark=dark_mode)
            st.rerun()
        
        # Previsualización del tema con animación
        st.markdown("""
            <div class="theme-preview"></div>
            <div style="text-align: center; margin-top: 0.5rem; opacity: 0.7; font-size: 0.8rem;">
                Vista previa del tema
            </div>
        """, unsafe_allow_html=True)
