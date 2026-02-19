"""
Gestión del estado del tema entre páginas
"""
import streamlit as st

def get_theme():
    """Obtiene el tema actual desde session_state"""
    if 'current_theme' not in st.session_state:
        st.session_state.current_theme = 'light'
    return st.session_state.current_theme

def set_theme(theme):
    """Establece el tema en session_state y localStorage"""
    st.session_state.current_theme = theme
    # Script para sincronizar con localStorage
    st.markdown(f"""
    <script>
        localStorage.setItem('streamlit_theme', '{theme}');
        const isDark = '{theme}' === 'dark';
        if (isDark) {{
            document.body.classList.add('dark-theme');
        }} else {{
            document.body.classList.remove('dark-theme');
        }}
    </script>
    """, unsafe_allow_html=True)

def init_theme():
    """Inicializa el tema desde localStorage"""
    st.markdown("""
    <script>
        const storedTheme = localStorage.getItem('streamlit_theme') || 'light';
        if (window.parent) {
            window.parent.postMessage({
                type: 'streamlit:setSessionState',
                data: {current_theme: storedTheme}
            }, '*');
        }
        if (storedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
    </script>
    """, unsafe_allow_html=True)

def toggle_theme():
    """Alterna entre tema claro y oscuro"""
    current = get_theme()
    new_theme = 'dark' if current == 'light' else 'light'
    set_theme(new_theme)
