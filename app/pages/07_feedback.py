"""
Página de feedback y comentarios
"""
import streamlit as st
from utils.feedback_utils import FeedbackManager

st.set_page_config(
    page_title="Feedback - Portafolio Data Science",
    page_icon="💭",
    layout="wide"
)

# Configurar estilo
st.markdown("""
<style>
    .feedback-header {
        text-align: center;
        padding: 2rem 0;
    }
    .feedback-form {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
    }
    .comment-section {
        max-width: 900px;
        margin: 2rem auto;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="feedback-header">', unsafe_allow_html=True)
    st.title("💭 Feedback y Comentarios")
    st.markdown("</div>", unsafe_allow_html=True)
    
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

if __name__ == "__main__":
    main()
