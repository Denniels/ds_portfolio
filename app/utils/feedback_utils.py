"""
Utilidades para gestionar feedback y comentarios
"""
import os
import json
import uuid
from datetime import datetime
from pathlib import Path
import streamlit as st

class FeedbackManager:
    """
    Clase para gestionar comentarios y feedback de los usuarios
    """
    def __init__(self):
        # Detectar entorno
        self.is_streamlit_cloud = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
        self.is_cloud_run = os.getenv('CLOUD_RUN_SERVICE', 'false').lower() == 'true'
        
        # Definir ruta del archivo de comentarios según entorno
        if self.is_streamlit_cloud:
            self.comments_dir = Path('/app/data/feedback')
        elif self.is_cloud_run:
            self.comments_dir = Path('/app/data/feedback')
        else:
            # En desarrollo local, usar rutas relativas
            self.comments_dir = Path(__file__).parent.parent / 'data' / 'feedback'
            
        # Asegurar que existe el directorio
        os.makedirs(self.comments_dir, exist_ok=True)
        
        # Ruta al archivo de comentarios
        self.comments_file = self.comments_dir / 'comments.json'
        
        # Crear archivo si no existe
        if not self.comments_file.exists():
            self._create_empty_comments_file()
            
        # Inicializar estado para formulario
        if 'feedback_name' not in st.session_state:
            st.session_state.feedback_name = ""
        if 'feedback_email' not in st.session_state:
            st.session_state.feedback_email = ""
        if 'feedback_comment' not in st.session_state:
            st.session_state.feedback_comment = ""
        if 'feedback_parent_id' not in st.session_state:
            st.session_state.feedback_parent_id = None
        if 'feedback_submitted' not in st.session_state:
            st.session_state.feedback_submitted = False
            
    def _create_empty_comments_file(self):
        """Crea un archivo de comentarios vacío"""
        empty_data = {
            "comments": [],
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "count": 0
            }
        }
        with open(self.comments_file, 'w') as f:
            json.dump(empty_data, f, indent=2)
    
    def load_comments(self):
        """
        Carga los comentarios desde el archivo
        
        Returns:
            list: Lista de comentarios
        """
        try:
            with open(self.comments_file, 'r') as f:
                data = json.load(f)
                return data.get("comments", [])
        except Exception as e:
            st.error(f"Error al cargar comentarios: {e}")
            return []
    
    def save_comment(self, name, email, comment, parent_id=None):
        """
        Guarda un nuevo comentario
        
        Args:
            name (str): Nombre del usuario
            email (str): Email del usuario
            comment (str): Texto del comentario
            parent_id (str, optional): ID del comentario padre si es una respuesta
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            # Cargar comentarios existentes
            with open(self.comments_file, 'r') as f:
                data = json.load(f)
            
            # Generar ID único
            comment_id = str(uuid.uuid4())
            
            # Crear nuevo comentario
            new_comment = {
                "id": comment_id,
                "name": name,
                "email": email,
                "comment": comment,
                "parent_id": parent_id,
                "created_at": datetime.now().isoformat(),
                "status": "pending",  # pending, approved, rejected
                "likes": 0,
                "dislikes": 0
            }
            
            # Añadir a la lista
            data["comments"].append(new_comment)
            
            # Actualizar metadatos
            data["metadata"]["count"] += 1
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Guardar archivo
            with open(self.comments_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            st.error(f"Error al guardar comentario: {e}")
            return False
    
    def update_comment_status(self, comment_id, status):
        """
        Actualiza el estado de un comentario
        
        Args:
            comment_id (str): ID del comentario
            status (str): Nuevo estado ('pending', 'approved', 'rejected')
            
        Returns:
            bool: True si se actualizó correctamente
        """
        try:
            # Cargar comentarios
            with open(self.comments_file, 'r') as f:
                data = json.load(f)
            
            # Buscar comentario
            for comment in data["comments"]:
                if comment["id"] == comment_id:
                    comment["status"] = status
                    comment["updated_at"] = datetime.now().isoformat()
                    break
            
            # Actualizar metadatos
            data["metadata"]["last_updated"] = datetime.now().isoformat()
            
            # Guardar archivo
            with open(self.comments_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            return True
        except Exception as e:
            st.error(f"Error al actualizar comentario: {e}")
            return False
    
    def render_feedback_form(self):
        """Renderiza el formulario de feedback"""
        with st.form("feedback_form"):
            st.text_input("Nombre", key="feedback_name")
            st.text_input("Email", key="feedback_email")
            st.text_area("Comentario", key="feedback_comment", height=150)
            
            # Mostrar si está respondiendo a otro comentario
            if st.session_state.feedback_parent_id:
                st.info("Estás respondiendo a un comentario. Haz clic en 'Cancelar' para crear un nuevo comentario.")
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Enviar Respuesta"):
                        self._submit_comment()
                with col2:
                    if st.form_submit_button("Cancelar"):
                        st.session_state.feedback_parent_id = None
                        st.session_state.feedback_comment = ""
                        st.rerun()
            else:
                if st.form_submit_button("Enviar Comentario"):
                    self._submit_comment()
    
    def _submit_comment(self):
        """Procesa el envío de un comentario"""
        # Validar campos
        if not st.session_state.feedback_name:
            st.error("Por favor, ingresa tu nombre")
            return
            
        if not st.session_state.feedback_email:
            st.error("Por favor, ingresa tu email")
            return
            
        if not st.session_state.feedback_comment:
            st.error("Por favor, ingresa un comentario")
            return
            
        # Guardar comentario
        success = self.save_comment(
            name=st.session_state.feedback_name,
            email=st.session_state.feedback_email,
            comment=st.session_state.feedback_comment,
            parent_id=st.session_state.feedback_parent_id
        )
        
        if success:
            st.session_state.feedback_submitted = True
            st.session_state.feedback_comment = ""
            st.session_state.feedback_parent_id = None
            st.success("¡Gracias por tu comentario! Será revisado y publicado pronto.")
        else:
            st.error("Hubo un problema al guardar tu comentario. Por favor, intenta nuevamente.")
    
    def render_recent_comments(self):
        """Renderiza los comentarios recientes"""
        comments = self.load_comments()
        
        # Filtrar solo comentarios aprobados
        approved_comments = [c for c in comments if c["status"] == "approved"]
        
        if not approved_comments:
            st.info("No hay comentarios todavía. ¡Sé el primero en dejar tu opinión!")
            return
            
        # Separar comentarios principales y respuestas
        main_comments = [c for c in approved_comments if not c["parent_id"]]
        replies = [c for c in approved_comments if c["parent_id"]]
        
        # Ordenar por fecha, más recientes primero
        main_comments.sort(key=lambda x: x["created_at"], reverse=True)
        
        # Mostrar comentarios principales
        for comment in main_comments[:5]:  # Mostrar solo los 5 más recientes
            self._render_comment(comment, replies)
            
        # Mostrar mensaje si hay más comentarios
        if len(main_comments) > 5:
            with st.expander("Ver más comentarios"):
                for comment in main_comments[5:]:
                    self._render_comment(comment, replies)
    
    def _render_comment(self, comment, all_replies):
        """
        Renderiza un comentario individual
        
        Args:
            comment (dict): Datos del comentario
            all_replies (list): Lista de todas las respuestas
        """
        # Crear un contenedor para el comentario
        with st.container():
            # Información del comentario
            st.markdown(f"""
            <div style="border-left: 3px solid #4A86E8; padding-left: 10px; margin-bottom: 15px;">
                <p><strong>{comment["name"]}</strong> • {self._format_date(comment["created_at"])}</p>
                <p>{comment["comment"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Encontrar respuestas a este comentario
            comment_replies = [r for r in all_replies if r["parent_id"] == comment["id"]]
            
            # Mostrar respuestas si hay
            if comment_replies:
                with st.expander(f"Ver {len(comment_replies)} respuestas"):
                    for reply in comment_replies:
                        st.markdown(f"""
                        <div style="border-left: 2px solid #9FC5E8; margin-left: 20px; padding-left: 10px; margin-bottom: 10px;">
                            <p><strong>{reply["name"]}</strong> • {self._format_date(reply["created_at"])}</p>
                            <p>{reply["comment"]}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Botón para responder
            if st.button("Responder", key=f"reply_{comment['id']}"):
                st.session_state.feedback_parent_id = comment["id"]
                st.rerun()
    
    def _format_date(self, date_str):
        """
        Formatea una fecha ISO a un formato legible
        
        Args:
            date_str (str): Fecha en formato ISO
            
        Returns:
            str: Fecha formateada
        """
        try:
            date = datetime.fromisoformat(date_str)
            return date.strftime("%d/%m/%Y %H:%M")
        except:
            return date_str
