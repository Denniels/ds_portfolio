"""
Gestión de temas mejorada para la aplicación
"""
import streamlit as st
import time
from pathlib import Path

# Definición de temas disponibles ampliada
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
            "border_color": "#667eea",
            "animated_bg": "radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.05) 0%, transparent 50%), radial-gradient(circle at 80% 20%, rgba(118, 75, 162, 0.05) 0%, transparent 50%)"
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
            "border_color": "#38b2ac",
            "animated_bg": "radial-gradient(circle at 30% 40%, rgba(56, 178, 172, 0.08) 0%, transparent 50%), radial-gradient(circle at 70% 80%, rgba(44, 122, 123, 0.08) 0%, transparent 50%)"
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
            "border_color": "#ed8936",
            "animated_bg": "radial-gradient(circle at 60% 30%, rgba(237, 137, 54, 0.06) 0%, transparent 50%), radial-gradient(circle at 40% 70%, rgba(192, 86, 33, 0.06) 0%, transparent 50%)"
        },
        "Rosa Sutil": {
            "primary_color": "#e53e3e",
            "background_color": "#fff5f5",
            "text_color": "#4a5568",
            "secondary_color": "#c53030",
            "accent_color": "#9b2c2c",
            "card_bg": "#ffffff",
            "gradient": "linear-gradient(135deg, #e53e3e 0%, #9b2c2c 100%)",
            "shadow": "0 2px 4px rgba(0,0,0,0.06)",
            "border_color": "#e53e3e",
            "animated_bg": "radial-gradient(circle at 25% 60%, rgba(229, 62, 62, 0.06) 0%, transparent 50%), radial-gradient(circle at 75% 20%, rgba(155, 44, 44, 0.06) 0%, transparent 50%)"
        },
        "Púrpura Elegante": {
            "primary_color": "#805ad5",
            "background_color": "#faf5ff",
            "text_color": "#4a5568",
            "secondary_color": "#6b46c1",
            "accent_color": "#553c9a",
            "card_bg": "#ffffff",
            "gradient": "linear-gradient(135deg, #805ad5 0%, #553c9a 100%)",
            "shadow": "0 2px 4px rgba(0,0,0,0.07)",
            "border_color": "#805ad5",
            "animated_bg": "radial-gradient(circle at 45% 30%, rgba(128, 90, 213, 0.07) 0%, transparent 50%), radial-gradient(circle at 80% 60%, rgba(85, 60, 154, 0.07) 0%, transparent 50%)"
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
            "border_color": "#6b8afd",
            "animated_bg": "radial-gradient(circle at 20% 30%, rgba(107, 138, 253, 0.15) 0%, transparent 50%), radial-gradient(circle at 80% 70%, rgba(76, 110, 245, 0.15) 0%, transparent 50%)"
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
            "border_color": "#f6ad55",
            "animated_bg": "radial-gradient(circle at 40% 20%, rgba(246, 173, 85, 0.12) 0%, transparent 50%), radial-gradient(circle at 70% 80%, rgba(221, 107, 32, 0.12) 0%, transparent 50%)"
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
            "border_color": "#4fd1c5",
            "animated_bg": "radial-gradient(circle at 60% 40%, rgba(79, 209, 197, 0.12) 0%, transparent 50%), radial-gradient(circle at 30% 80%, rgba(49, 151, 149, 0.12) 0%, transparent 50%)"
        },
        "Magenta Cyber": {
            "primary_color": "#f093fb",
            "background_color": "#0f172a",
            "text_color": "#e2e8f0",
            "secondary_color": "#c084fc",
            "accent_color": "#a855f7",
            "card_bg": "#1e293b",
            "gradient": "linear-gradient(135deg, #f093fb 0%, #a855f7 100%)",
            "shadow": "0 4px 6px rgba(0,0,0,0.4)",
            "border_color": "#f093fb",
            "animated_bg": "radial-gradient(circle at 35% 25%, rgba(240, 147, 251, 0.15) 0%, transparent 50%), radial-gradient(circle at 75% 65%, rgba(168, 85, 247, 0.15) 0%, transparent 50%)"
        },
        "Verde Matrix": {
            "primary_color": "#22c55e",
            "background_color": "#0c1d0f",
            "text_color": "#dcfce7",
            "secondary_color": "#16a34a",
            "accent_color": "#15803d",
            "card_bg": "#1f2937",
            "gradient": "linear-gradient(135deg, #22c55e 0%, #15803d 100%)",
            "shadow": "0 4px 6px rgba(0,0,0,0.4)",
            "border_color": "#22c55e",
            "animated_bg": "radial-gradient(circle at 50% 30%, rgba(34, 197, 94, 0.1) 0%, transparent 50%), radial-gradient(circle at 80% 70%, rgba(21, 128, 61, 0.1) 0%, transparent 50%)"
        },
        "Rojo Profundo": {
            "primary_color": "#ef4444",
            "background_color": "#1a0c0c",
            "text_color": "#fecaca",
            "secondary_color": "#dc2626",
            "accent_color": "#b91c1c",
            "card_bg": "#2d1b1b",
            "gradient": "linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)",
            "shadow": "0 4px 6px rgba(0,0,0,0.4)",
            "border_color": "#ef4444",
            "animated_bg": "radial-gradient(circle at 40% 50%, rgba(239, 68, 68, 0.12) 0%, transparent 50%), radial-gradient(circle at 80% 30%, rgba(185, 28, 28, 0.12) 0%, transparent 50%)"
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

def apply_animated_background(theme, mode):
    """Aplica fondos animados dinámicos"""
    
    # CSS básico para animaciones
    animation_css = f"""
    <style>
        /* Fondo animado dinámico */
        .main .block-container {{
            position: relative;
            background: {theme['background_color']};
        }}
        
        .main .block-container::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: {theme['animated_bg']};
            z-index: -1;
            animation: backgroundMove 20s ease-in-out infinite;
            pointer-events: none;
        }}
        
        @keyframes backgroundMove {{
            0%, 100% {{
                transform: translate(0, 0) scale(1);
            }}
            25% {{
                transform: translate(-10px, -10px) scale(1.02);
            }}
            50% {{
                transform: translate(10px, -5px) scale(0.98);
            }}
            75% {{
                transform: translate(-5px, 10px) scale(1.01);
            }}
        }}
        
        /* Efecto de particulas flotantes */
        .floating-particles {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }}
        
        .particle {{
            position: absolute;
            width: 4px;
            height: 4px;
            background: {theme['primary_color']}88;
            border-radius: 50%;
            animation: float 15s infinite linear;
        }}
        
        @keyframes float {{
            from {{
                transform: translateY(100vh) translateX(0px);
                opacity: 0;
            }}
            10% {{
                opacity: 1;
            }}
            90% {{
                opacity: 1;
            }}
            to {{
                transform: translateY(-100px) translateX(100px);
                opacity: 0;
            }}
        }}
    </style>
    """
    
    # CSS adicional para temas oscuros
    if mode == "dark":
        wave_css = f"""
        <style>
        .wave-background {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(45deg, {theme['background_color']} 0%, {theme['card_bg']} 50%, {theme['background_color']} 100%);
            background-size: 400% 400%;
            animation: waveMove 8s ease-in-out infinite;
            pointer-events: none;
        }}
        
        @keyframes waveMove {{
            0%, 100% {{ background-position: 0% 0%; }}
            25% {{ background-position: 100% 0%; }}
            50% {{ background-position: 100% 100%; }}
            75% {{ background-position: 0% 100%; }}
        }}
        </style>
        """
        animation_css += wave_css
    
    st.markdown(animation_css, unsafe_allow_html=True)

def apply_theme_styles(mode, theme_name):
    """
    Aplica el tema seleccionado usando variables CSS
    """
    # Guardar el tema seleccionado en session_state
    st.session_state.theme_mode = mode
    st.session_state.theme_name = theme_name
    
    # Obtener configuración del tema
    theme_config = THEMES[mode][theme_name]
    
    # Aplicar el tema usando CSS personalizado
    st.markdown(f"""
        <style>
        /* Configuración del tema {theme_name} */
        :root {{
            --background-color: {theme_config['background_color']};
            --text-color: {theme_config['text_color']};
            --primary-color: {theme_config['primary_color']};
            --secondary-color: {theme_config['secondary_color']};
            --accent-color: {theme_config['accent_color']};
            --link-color: {theme_config['primary_color']};
            --link-hover-color: {theme_config['secondary_color']};
            --card-bg: {theme_config['card_bg']};
            --gradient: {theme_config['gradient']};
        }}
        </style>
    """, unsafe_allow_html=True)
    
    return True

def apply_basic_theme_styles(mode, theme_name):
    """Aplica estilos básicos sin animaciones para mejor rendimiento"""
    theme = get_theme_config(mode, theme_name)
    
    css = f"""
    <style>
        /* Estilos básicos de tema: {theme_name} ({mode}) */
        .main .block-container {{
            background-color: {theme['background_color']};
        }}
        
        h1, h2, h3, h4, h5 {{
            color: {theme["primary_color"] if mode == "dark" else theme["text_color"]};
        }}
        
        p, li, span {{
            color: {theme["text_color"]};
        }}
        
        .stButton > button {{
            background-color: {theme["primary_color"]};
            color: white;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {theme["primary_color"]} !important;
            color: white !important;
        }}
        
        section[data-testid="stSidebar"] {{
            background-color: {"#f8f9fa" if mode == "light" else "#1a202c"};
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def create_theme_selector():
    """
    Crea el selector de temas
    """
    # Contenedor para selector de tema
    with st.container():
        st.markdown("### 🎨 Selector de temas")
        
        # Radio buttons para modo claro/oscuro
        mode = st.radio("🌓 Modo:", 
                       options=["claro", "oscuro"],
                       horizontal=True,
                       key="theme_mode_selector")
        
        # Mapear nombres en español a inglés
        mode_map = {"claro": "light", "oscuro": "dark"}
        selected_mode = mode_map[mode]
        
        # Selector de tema específico
        theme_options = list(THEMES[selected_mode].keys())
        selected_theme = st.selectbox("Selecciona un tema:",
                                    options=theme_options,
                                    key="theme_name_selector")
        
        # Aplicar tema seleccionado
        if selected_theme:
            apply_theme_styles(selected_mode, selected_theme)
