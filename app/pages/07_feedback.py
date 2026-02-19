"""
Página de feedback y comentarios
"""
import streamlit as st
import sys
from pathlib import Path

# Importar configuración de página
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Configurar directorios de datos
DATA_CACHE_DIR = parent_dir / "data" / "cache"
DATA_DIR = parent_dir / "data"

from utils.page_setup import setup_page, add_page_title, create_card

# Configurar página
st = setup_page(
    title="Feedback",
    icon="📬"
)

# Título y descripción de la página
add_page_title(
    "Feedback y Comentarios",
    "Comparte tu opinión y sugerencias sobre el portafolio para ayudarnos a mejorar.",
    "📬"
)

# Importar utilidades de feedback
from utils.feedback_utils import FeedbackManager

# Importar componente de contacto
try:
    from utils.contact_components import add_page_footer, add_sidebar_contact
except ImportError:
    # Fallback por si no encuentra el módulo
    def add_page_footer():
        st.markdown("---")
        st.markdown("© 2025 DS Portfolio")
    def add_sidebar_contact():
        st.sidebar.markdown("---")

# Añadir estilos específicos para la sección de comentarios que respetan el tema actual
st.markdown("""
<style>
    .feedback-header {
        text-align: center;
        padding: 2rem 0;
        color: var(--text-color);
    }
    .feedback-form {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background-color: var(--background-color);
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    .comment-section {
        max-width: 900px;
        margin: 2rem auto;
    }
    .comment-card {
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid var(--primary-color);
        background-color: rgba(var(--primary-rgb), 0.05);
        border-radius: 4px;
    }
    .comment-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
        color: var(--text-secondary);
    }
    .comment-body {
        color: var(--text-color);
    }
    .comment-rating {
        color: #FFD700;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="feedback-header">', unsafe_allow_html=True)
    st.title("💭 Feedback y Comentarios")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Agregar enlaces de contacto en la barra lateral
    #add_sidebar_contact()
    
    # Inicializar manager
    feedback_manager = FeedbackManager()
    
    # Layout principal
    col1, col2 = st.columns([2,3])
    
    with col1:
        st.markdown("### ✍️ Deja tu comentario")
        with st.container():
            feedback_manager.render_feedback_form()
    
    with col2:
        st.markdown("### 📝 Comentarios Recientes")
        with st.container():
            feedback_manager.render_recent_comments()
    
    # Información adicional
    with st.expander("ℹ️ Acerca de los comentarios"):
        st.markdown("""
        - Los comentarios son moderados antes de ser publicados
        - Puedes responder a comentarios existentes
        - Se notificará por email cuando alguien responda a tu comentario
        - Los comentarios inapropiados serán removidos
        """)
    
    # Estado de la moderación
    if st.session_state.get("show_moderation", False):
        with st.expander("🛡️ Panel de Moderación", expanded=True):
            comments = feedback_manager.load_comments()
            for comment in comments:
                if comment["status"] == "pending":
                    st.markdown(f"**{comment['name']}** - {comment['email']}")
                    st.text(comment["comment"])
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Aprobar", key=f"approve_{comment['id']}"):
                            feedback_manager.update_comment_status(comment["id"], "approved")
                            st.rerun()
                    with col2:
                        if st.button("Rechazar", key=f"reject_{comment['id']}"):
                            feedback_manager.update_comment_status(comment["id"], "rejected")
                            st.rerun()

    # Agregar footer al final de la página

    add_page_footer()
    add_sidebar_contact()

if __name__ == "__main__":
    main()
