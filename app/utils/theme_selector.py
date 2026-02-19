"""
Componente de selección de temas para Streamlit con soporte para temas personalizados
"""
import streamlit as st

# Definir paletas de colores para tema claro
LIGHT_THEMES = {
    'Ocean Breeze': {
        'primary': '#3182CE',
        'secondary': '#4FD1C5',
        'background': '#F8FAFC',
        'text': '#2D3748',
        'accent': '#63B3ED'
    },
    'Spring Garden': {
        'primary': '#48BB78',
        'secondary': '#4299E1',
        'background': '#F0FFF4',
        'text': '#2D3748',
        'accent': '#9AE6B4'
    },
    'Sunset Warm': {
        'primary': '#ED8936',
        'secondary': '#D53F8C',
        'background': '#FFFFF0',
        'text': '#2D3748',
        'accent': '#FBD38D'
    },
    'Purple Rain': {
        'primary': '#805AD5',
        'secondary': '#D53F8C',
        'background': '#FAF5FF',
        'text': '#2D3748',
        'accent': '#B794F4'
    },
    'Coffee & Cream': {
        'primary': '#8B4513',
        'secondary': '#D69E2E',
        'background': '#FFFAF0',
        'text': '#2D3748',
        'accent': '#DEB887'
    }
}

# Definir paletas de colores para tema oscuro
DARK_THEMES = {
    'Night Ocean': {
        'primary': '#4FD1C5',
        'secondary': '#3182CE',
        'background': '#1A202C',
        'text': '#E2E8F0',
        'accent': '#2C5282'
    },
    'Dark Forest': {
        'primary': '#68D391',
        'secondary': '#38B2AC',
        'background': '#1A2F1F',
        'text': '#E2E8F0',
        'accent': '#276749'
    },
    'Midnight Purple': {
        'primary': '#B794F4',
        'secondary': '#F687B3',
        'background': '#1A1A2E',
        'text': '#E2E8F0',
        'accent': '#553C9A'
    },
    'Dark Rust': {
        'primary': '#F6AD55',
        'secondary': '#FC8181',
        'background': '#1A1A1A',
        'text': '#E2E8F0',
        'accent': '#C05621'
    },
    'Deep Space': {
        'primary': '#81E6D9',
        'secondary': '#B794F4',
        'background': '#0F1629',
        'text': '#E2E8F0',
        'accent': '#2B6CB0'
    }
}

def get_default_theme(is_dark=False):
    """Obtiene el tema por defecto según el modo"""
    return 'Night Ocean' if is_dark else 'Ocean Breeze'

def get_theme_data(theme_name, is_dark=False):
    """
    Obtiene los datos del tema especificado
    
    Args:
        theme_name (str): Nombre del tema
        is_dark (bool): Si es modo oscuro
        
    Returns:
        dict: Datos del tema
    """
    themes = DARK_THEMES if is_dark else LIGHT_THEMES
    default_theme = get_default_theme(is_dark)
    
    # Asegurarse de que theme_name sea str o usar el default
    if not isinstance(theme_name, str):
        theme_name = default_theme
    
    # Si el tema no está en la lista, usar el default
    if theme_name not in themes.keys():
        theme_name = default_theme
    
    return themes[theme_name]

def get_theme_css(theme_name, is_dark=False):
    """
    Genera el CSS para un tema específico
    
    Args:
        theme_name (str): Nombre del tema
        is_dark (bool): Si es modo oscuro
        
    Returns:
        str: CSS del tema
    """
    theme = get_theme_data(theme_name, is_dark)
    
    # Extraer colores RGB para efectos de transparencia
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    primary_rgb = hex_to_rgb(theme['primary'])
    secondary_rgb = hex_to_rgb(theme['secondary'])
    
    return f"""
    <style>
    /* Variables de tema */
    :root {{
        --primary-color: {theme['primary']};
        --secondary-color: {theme['secondary']};
        --background-color: {theme['background']};
        --text-color: {theme['text']};
        --accent-color: {theme['accent']};
        --primary-color-rgb: {primary_rgb[0]}, {primary_rgb[1]}, {primary_rgb[2]};
        --secondary-color-rgb: {secondary_rgb[0]}, {secondary_rgb[1]}, {secondary_rgb[2]};
    }}
    
    /* Estilos base */
    .stApp {{
        background-color: var(--background-color);
        color: var(--text-color);
    }}
    
    /* Enlaces */
    a {{
        color: var(--primary-color);
    }}
    
    /* Botones */
    .stButton>button {{
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }}
    
    .stButton>button:hover {{
        opacity: 0.9;
        transform: translateY(-1px);
    }}
    
    /* Selectores */
    .stSelectbox {{
        border-color: var(--primary-color);
    }}
    
    /* Widgets */
    .stProgress {{
        background-color: var(--accent-color);
    }}
    
    /* Sidebar */
    .css-1d391kg {{
        background: linear-gradient(
            to bottom,
            rgba(var(--primary-color-rgb), 0.05),
            rgba(var(--secondary-color-rgb), 0.05)
        );
        backdrop-filter: blur(10px);
    }}
    
    /* Cards y contenedores */
    .css-12w0qpk {{
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1rem;
    }}
    
    /* Separadores */
    hr {{
        border-color: rgba(var(--text-color), 0.1);
    }}
    </style>
    """

def initialize_theme():
    """Inicializa el tema en el estado de la sesión"""
    # Inicializar modo oscuro primero
    if 'is_dark_mode' not in st.session_state:
        st.session_state.is_dark_mode = False
    
    # Obtener el tema por defecto según el modo
    default_theme = get_default_theme(st.session_state.get('is_dark_mode', False))
    
    # Inicializar o validar el tema actual
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = default_theme
    elif not isinstance(st.session_state.current_theme, str):
        st.session_state.current_theme = default_theme
    elif st.session_state.current_theme not in (DARK_THEMES if st.session_state.is_dark_mode else LIGHT_THEMES):
        st.session_state.current_theme = default_theme

def get_theme():
    """Obtiene el tema actual"""
    return st.session_state.get('current_theme', get_default_theme(False))

def toggle_theme():
    """Alterna entre modo claro y oscuro"""
    st.session_state.is_dark_mode = not st.session_state.get('is_dark_mode', False)
    current_theme = st.session_state.get('current_theme', get_default_theme(False))
    
    # Si cambiamos de modo, usamos el tema por defecto del nuevo modo
    st.session_state.current_theme = get_default_theme(st.session_state.is_dark_mode)

def apply_theme(theme_name=None, is_dark=None):
    """
    Aplica un tema específico
    
    Args:
        theme_name (str): Nombre del tema a aplicar
        is_dark (bool): Si se debe usar modo oscuro
    """
    try:
        # Determinar modo oscuro
        is_dark = is_dark if is_dark is not None else st.session_state.get('is_dark_mode', False)
        
        # Obtener nombre del tema
        if theme_name is None or not isinstance(theme_name, str):
            theme_name = get_default_theme(is_dark)
        
        # Validar que el tema exista
        themes = DARK_THEMES if is_dark else LIGHT_THEMES
        if theme_name not in themes:
            theme_name = get_default_theme(is_dark)
        
        # Generar y aplicar CSS
        css = get_theme_css(theme_name, is_dark)
        st.markdown(css, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"Error aplicando tema. Usando tema por defecto: {str(e)}")
        # Aplicar tema por defecto en caso de error
        default_theme = get_default_theme(False)
        css = get_theme_css(default_theme, False)
        st.markdown(css, unsafe_allow_html=True)
