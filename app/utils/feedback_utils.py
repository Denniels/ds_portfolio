"""
Utilidades para el manejo de feedback y comentarios de usuarios
"""
import json
from datetime import datetime
from pathlib import Path
import streamlit as st
from typing import List, Dict
import uuid

class FeedbackManager:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "data"
        self.feedback_file = self.data_dir / "feedback" / "comments.json"
        self._ensure_dirs()
        self.load_comments()

    def _ensure_dirs(self):
        """Asegura que existan los directorios necesarios"""
        self.feedback_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.feedback_file.exists():
            self.save_comments([])

    def load_comments(self) -> List[Dict]:
        """Carga los comentarios del archivo JSON"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_comments(self, comments: List[Dict]):
        """Guarda los comentarios en el archivo JSON"""
        with open(self.feedback_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=2)

    def add_comment(self, name: str, email: str, comment: str, parent_id: str = None) -> Dict:
        """Añade un nuevo comentario o respuesta"""
        comments = self.load_comments()
        
        new_comment = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "comment": comment,
            "date": datetime.now().isoformat(),
            "parent_id": parent_id,
            "status": "pending",  # pending, approved, rejected
            "replies": []
        }

        if parent_id:
            # Es una respuesta a un comentario existente
            for c in comments:
                if c["id"] == parent_id:
                    c["replies"].append(new_comment)
                    break
        else:
            # Es un nuevo comentario
            comments.append(new_comment)

        self.save_comments(comments)
        return new_comment

    def get_comment_thread(self, comment_id: str) -> Dict:
        """Obtiene un comentario y sus respuestas"""
        comments = self.load_comments()
        for comment in comments:
            if comment["id"] == comment_id:
                return comment
        return None

    def update_comment_status(self, comment_id: str, status: str):
        """Actualiza el estado de un comentario"""
        comments = self.load_comments()
        
        def update_status(comment_list):
            for comment in comment_list:
                if comment["id"] == comment_id:
                    comment["status"] = status
                    return True
                if comment["replies"]:
                    if update_status(comment["replies"]):
                        return True
            return False

        if update_status(comments):
            self.save_comments(comments)

    def get_recent_comments(self, limit: int = 5) -> List[Dict]:
        """Obtiene los comentarios más recientes"""
        comments = self.load_comments()
        
        # Aplanar comentarios y respuestas
        all_comments = []
        for comment in comments:
            all_comments.append(comment)
            for reply in comment["replies"]:
                reply["is_reply"] = True
                all_comments.append(reply)
        
        # Ordenar por fecha
        all_comments.sort(key=lambda x: x["date"], reverse=True)
        return all_comments[:limit]

    def render_comment(self, comment: Dict, allow_replies: bool = True):
        """Renderiza un comentario en Streamlit"""
        with st.container():
            col1, col2 = st.columns([4,1])
            
            with col1:
                st.markdown(f"**{comment['name']}**")
                st.markdown(comment["comment"])
                
            with col2:
                date = datetime.fromisoformat(comment["date"]).strftime("%d/%m/%Y")
                st.caption(f"📅 {date}")
            
            if allow_replies:
                if st.button("Responder", key=f"btn_reply_{comment['id']}"):
                    st.session_state["replying_to"] = comment["id"]
            
            # Mostrar respuestas
            if comment.get("replies"):
                with st.container():
                    for reply in comment["replies"]:
                        st.markdown("---")
                        self.render_comment(reply, allow_replies=False)

    def render_feedback_form(self):
        """Renderiza el formulario de feedback"""
        with st.form("feedback_form"):
            name = st.text_input("Nombre")
            email = st.text_input("Email")
            comment = st.text_area("Comentario")
            
            parent_id = st.session_state.get("replying_to")
            if parent_id:
                st.info("Respondiendo a un comentario existente")
            
            submitted = st.form_submit_button("Enviar")
            
            if submitted and name and email and comment:
                self.add_comment(name, email, comment, parent_id)
                st.success("¡Gracias por tu comentario!")
                if parent_id:
                    del st.session_state["replying_to"]
                return True
            
            return False

    def render_recent_comments(self, limit: int = 5):
        """Renderiza los comentarios más recientes"""
        comments = self.get_recent_comments(limit)
        
        if not comments:
            st.info("No hay comentarios aún. ¡Sé el primero en comentar!")
            return
        
        for comment in comments:
            if not comment.get("is_reply"):
                self.render_comment(comment)
                st.markdown("---")
