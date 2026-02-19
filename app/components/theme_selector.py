"""
Componente selector de tema personalizado
"""
import streamlit as st

def add_theme_selector():
    """
    Agrega un selector de tema personalizado al sidebar
    """
    with st.sidebar:
        st.markdown("""
        <style>
        .theme-selector {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 1rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
        }
        
        .theme-selector label {
            color: #E2E8F0;
            font-size: 0.9rem;
        }
        
        .stRadio > label {
            color: #E2E8F0 !important;
        }
        
        /* Estilo para los botones de radio */
        .stRadio [role="radiogroup"] {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.5rem;
            border-radius: 5px;
        }
        
        /* Animación suave al cambiar */
        .stApp {
            transition: background-color 0.3s ease;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="theme-selector">', unsafe_allow_html=True)
        
        # Si no existe el tema en session_state, inicializarlo
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
        
        # Selector de tema
        theme = st.radio(
            "🎨 Tema",
            options=['Claro', 'Oscuro'],
            index=0 if st.session_state.theme == 'light' else 1,
            key='theme_selector'
        )
        
        # Aplicar tema cuando cambie
        if theme == 'Oscuro' and st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
            st.markdown("""
                <script>
                    document.body.classList.add('dark-theme');
                    localStorage.setItem('theme', 'dark');
                </script>
                """, unsafe_allow_html=True)
        elif theme == 'Claro' and st.session_state.theme == 'dark':
            st.session_state.theme = 'light'
            st.markdown("""
                <script>
                    document.body.classList.remove('dark-theme');
                    localStorage.setItem('theme', 'light');
                </script>
                """, unsafe_allow_html=True)
        
        # Restaurar tema al cargar la página
        st.markdown(f"""
            <script>
                var savedTheme = localStorage.getItem('theme') || 'light';
                if (savedTheme === 'dark') {{
                    document.body.classList.add('dark-theme');
                }} else {{
                    document.body.classList.remove('dark-theme');
                }}
            </script>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
