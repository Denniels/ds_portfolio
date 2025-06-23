"""
Gestión de temas para la aplicación
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
    """Aplica los estilos CSS del tema seleccionado"""
    theme = get_theme_config(mode, theme_name)
    
    # Definir background para final-message según el modo
    if mode == "light":
        final_message_bg = f"linear-gradient(to right, #f6f9fc, {theme['card_bg']})"
        page_bg = "#ffffff"
    else:
        final_message_bg = f"linear-gradient(to right, #2a3441, {theme['card_bg']})"
        page_bg = "#1a202c"
    
    # Crear CSS personalizado basado en el tema
    css = f"""
    <style>
        /* Estilos de tema: {theme_name} ({mode}) */
        
        /* Color de fondo para toda la página */
        .main .block-container {{
            background-color: {page_bg};
        }}
        
        /* Color de texto para toda la página */
        body {{
            color: {theme["text_color"]};
        }}
        
        .main-title {{
            color: {theme["secondary_color"]};
        }}
        .hero-section {{
            background: {theme["gradient"]};
        }}
        .project-card {{
            background: {theme["card_bg"]};
            box-shadow: {theme["shadow"]};
            border-left: 4px solid {theme["primary_color"]};
        }}
        .project-card h3 {{
            color: {theme["text_color"]};
        }}
        .project-card p em {{
            color: {theme["primary_color"]};
        }}
        .stButton > button {{
            background-color: {theme["primary_color"]};
            color: {"#ffffff" if mode == "light" else "#1a202c"};
        }}
        .stButton > button:hover {{
            background-color: {theme["secondary_color"]};
        }}
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {"#f1f3f9" if mode == "light" else "#2d3748"};
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: {"#e9ecef" if mode == "light" else "#1e2533"};
            color: {theme["text_color"]};
        }}
        .stTabs [aria-selected="true"] {{
            background-color: {theme["primary_color"]} !important;
            color: {"#ffffff" if mode == "light" else "#1a202c"} !important;
        }}
        .final-message {{
            background: {final_message_bg};
            border-left: 4px solid {theme["primary_color"]};
        }}
        .final-message h3 {{
            color: {theme["text_color"]};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {"#f8f9fa" if mode == "light" else "#1a202c"};
        }}
        section[data-testid="stSidebar"] a:hover {{
            color: {theme["primary_color"]};
            background-color: rgba(102, 126, 234, 0.1);
            border-left: 3px solid {theme["primary_color"]};
        }}
        section[data-testid="stSidebar"] a.active {{
            color: {theme["primary_color"]};
            background-color: rgba(102, 126, 234, 0.15);
            border-left: 3px solid {theme["primary_color"]};
        }}
    </style>
    """
    
    # Aplicar CSS
    st.markdown(css, unsafe_allow_html=True)

def create_theme_selector():
    """Crea un selector de temas en la barra lateral"""
    st.sidebar.markdown("### 🎨 Temas")
    
    # Selector de modo (claro/oscuro)
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = "light"
    
    # Obtener tema anterior
    previous_mode = st.session_state.theme_mode
    previous_theme = st.session_state.get('theme_name', '')
    
    theme_mode = st.sidebar.radio(
        "Modo:", 
        ["Claro", "Oscuro"], 
        index=0 if st.session_state.theme_mode == "light" else 1,
        horizontal=True,
        key="theme_mode_selector"
    )
    
    # Actualizar el modo del tema en session_state
    current_mode = "light" if theme_mode == "Claro" else "dark"
    st.session_state.theme_mode = current_mode
    
    # Obtener nombres de temas para el modo seleccionado
    theme_names = get_theme_names()
    available_themes = theme_names[current_mode]
    
    # Si no hay un tema guardado o cambiamos de modo, usar el primero de la lista
    if 'theme_name' not in st.session_state or previous_mode != current_mode:
        st.session_state.theme_name = available_themes[0]
    
    # Selector de tema específico
    selected_theme = st.sidebar.selectbox(
        "Selecciona un tema:",
        available_themes,
        index=available_themes.index(st.session_state.theme_name),
        key="theme_name_selector"
    )
    
    # Actualizar el tema en session_state
    st.session_state.theme_name = selected_theme
    
    # Verificar si hubo cambios
    theme_changed = previous_theme != selected_theme or previous_mode != current_mode
    
    # Aplicar el tema seleccionado
    apply_theme_styles(current_mode, selected_theme)
    
    # Si hubo cambios, forzar recargar con un rerun
    if theme_changed and previous_theme != '':
        st.experimental_rerun()
    
    st.sidebar.markdown("---")
    
    return {
        "mode": current_mode,
        "theme": selected_theme
    }
