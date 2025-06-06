import streamlit as st

def set_theme():
    # Inicializar el tema si no existe
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    with st.sidebar:
        st.markdown("## ⚙️ Configuración")
        if st.button("🌓 Cambiar Tema"):
            # Cambiar al tema opuesto
            st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
            st.rerun()

def apply_theme():
    # Obtener el tema actual
    current_theme = st.session_state.get("theme", "light")
    
    # Definir colores según el tema
    if current_theme == "dark":
        background_color = "#0E1117"
        text_color = "#FFFFFF"
        secondary_background = "#262730"
        plot_background = "#1E1E1E"
        plot_text = "#FFFFFF"
    else:
        background_color = "#FFFFFF"
        text_color = "#000000"
        secondary_background = "#F0F2F6"
        plot_background = "#FFFFFF"
        plot_text = "#000000"

    # Aplicar estilos globales
    st.markdown(f"""
        <style>
            /* Estilos generales */
            .stApp {{
                background-color: {background_color};
                color: {text_color};
            }}
            
            /* Barra lateral */
            [data-testid="stSidebar"] {{
                background-color: {secondary_background};
                color: {text_color};
            }}
            
            /* Tarjetas y contenedores */
            .css-1r6slb0, .css-12w0qpk {{
                background-color: {secondary_background};
                color: {text_color};
            }}
            
            /* Métricas */
            [data-testid="stMetricValue"] {{
                color: {text_color};
            }}
            
            /* Texto y encabezados */
            h1, h2, h3, h4, h5, h6, p {{
                color: {text_color} !important;
            }}
            
            /* Selectbox y otros inputs */
            .stSelectbox label {{
                color: {text_color} !important;
            }}
            
            /* Gráficos de Plotly */
            .js-plotly-plot {{
                background-color: {secondary_background};
            }}
            
            /* Botones */
            .stButton button {{
                color: {text_color};
                background-color: {secondary_background};
                border: 1px solid {text_color};
            }}
            
            /* Hover effect para botones */
            .stButton button:hover {{
                background-color: {text_color};
                color: {background_color};
            }}
        </style>
    """, unsafe_allow_html=True)
