"""
Sistema de Feedback para el Portafolio
=====================================
Permite a los usuarios dejar comentarios y sugerencias,
almacenándolos en Google Cloud Storage.
"""

import streamlit as st
import json
from datetime import datetime
from google.cloud import storage
import uuid
from pathlib import Path
import os

class FeedbackSystem:
    def __init__(self):
        """Inicializa el sistema de feedback"""
        self.bucket_name = "ds-portfolio-feedback"
        self.client = storage.Client()
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Asegura que el bucket existe, si no, lo crea"""
        try:
            self.bucket = self.client.get_bucket(self.bucket_name)
        except Exception:
            self.bucket = self.client.create_bucket(
                self.bucket_name,
                location="us-central1"
            )

    def save_feedback(self, feedback_data):
        """Guarda el feedback en Cloud Storage"""
        # Genera ID único si no se proporciona nombre
        user_id = feedback_data.get('name', str(uuid.uuid4())[:8])
        
        # Estructura del feedback
        feedback_entry = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'email': feedback_data.get('email', 'anónimo'),
            'message': feedback_data['message'],
            'category': feedback_data.get('category', 'general')
        }
        
        # Guarda en Cloud Storage
        blob = self.bucket.blob(f"feedback/{feedback_entry['id']}.json")
        blob.upload_from_string(
            json.dumps(feedback_entry),
            content_type='application/json'
        )
        
        return feedback_entry['id']

def render_feedback_form():
    """Renderiza el formulario de feedback"""
    st.markdown("""
    <div style='background: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;'>
        <h2 style='color: #1e3c72;'>📝 Sugerencias y Comentarios</h2>
        <p style='color: #4a4a4a;'>
            ¡Tu opinión es importante! Ayúdame a mejorar este portafolio dejando tus comentarios o sugerencias.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("feedback_form"):
        name = st.text_input("Nombre (opcional)", "")
        email = st.text_input("Email (opcional)", "")
        category = st.selectbox(
            "Categoría",
            ["General", "Sugerencia", "Error/Bug", "Nueva Funcionalidad"]
        )
        message = st.text_area(
            "Tu mensaje",
            height=150,
            placeholder="Escribe aquí tu comentario o sugerencia..."
        )
        
        submit = st.form_submit_button("Enviar Feedback")
        
        if submit and message:  # Asegurarse de que hay un mensaje
            try:
                feedback_system = FeedbackSystem()
                feedback_id = feedback_system.save_feedback({
                    'name': name,
                    'email': email,
                    'category': category,
                    'message': message
                })
                st.success(f"¡Gracias por tu feedback! ID: {feedback_id}")
            except Exception as e:
                st.error(f"No se pudo guardar el feedback: {str(e)}")
        elif submit:
            st.warning("Por favor, escribe un mensaje antes de enviar.")
