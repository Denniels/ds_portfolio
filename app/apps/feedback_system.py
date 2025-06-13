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
import sys

# CSS personalizado
st.markdown("""
<style>
    .feedback-header {
        background: linear-gradient(90deg, #4f46e5, #6366f1);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .feedback-box {
        background: #f1f5f9;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .success-message {
        background: #dcfce7;
        color: #166534;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #16a34a;
    }
    
    .error-message {
        background: #fee2e2;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ef4444;
    }
</style>
""", unsafe_allow_html=True)

class FeedbackApp:
    """Aplicación principal de feedback"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        self.bucket_name = "ds-portfolio-feedback"
        
    def render_header(self):
        """Renderiza el encabezado principal"""
        st.markdown("""
        <div class="feedback-header">
            <h1>📝 Comentarios y Sugerencias</h1>
            <p>¡Tu opinión es importante! Ayúdanos a mejorar este portafolio</p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_feedback_form(self):
        """Renderiza el formulario de feedback"""
        st.markdown("""
        <div class="feedback-box">
            <h2>💭 Deja tu comentario</h2>
            <p>Nos encantaría conocer tu opinión sobre el portafolio, sugerencias de mejora o ideas para nuevos análisis.</p>
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
                    st.markdown(f"""
                    <div class="success-message">
                        <strong>¡Gracias por tu feedback!</strong><br>
                        Tu mensaje ha sido registrado con el ID: {feedback_id}
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        <strong>No se pudo guardar el feedback:</strong><br>
                        {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            elif submit:
                st.warning("Por favor, escribe un mensaje antes de enviar.")
                
    def render_information(self):
        """Renderiza información adicional"""
        st.markdown("## ℹ️ Información")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ¿Qué tipo de feedback puedes dejar?
            
            - 💡 **Sugerencias de mejora**: Nuevas funcionalidades, cambios en la interfaz, etc.
            - 🐞 **Reporte de errores**: Si encuentras algún problema o error en las aplicaciones
            - 📊 **Ideas para nuevos análisis**: Temas que te gustaría que incluyéramos
            - 👍 **Comentarios generales**: Tu opinión general sobre el portafolio
            """)
        
        with col2:
            st.markdown("""
            ### ¿Qué hacemos con tu feedback?
            
            - 📝 **Revisamos todos los comentarios** cuidadosamente
            - 🚀 **Implementamos mejoras** basadas en las sugerencias
            - 🔄 **Actualizamos periódicamente** el portafolio
            - 💪 **Mejoramos constantemente** las aplicaciones
            
            _Nota: Tu información de contacto es opcional y solo se utiliza para responder a tu feedback si es necesario._
            """)
                
    def run(self):
        """Ejecuta la aplicación principal"""
        # Renderizar componentes
        self.render_header()
        self.render_feedback_form()
        self.render_information()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #64748b; padding: 1rem;'>
            📝 <strong>Sistema de Feedback</strong><br>
            Desarrollado como parte del DS Portfolio | Junio 2025
        </div>
        """, unsafe_allow_html=True)
    
    def __call__(self):
        """Hace que la clase sea llamable"""
        self.run()
        
# Crear instancia global de la aplicación
app = FeedbackApp()

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
            try:
                self.bucket = self.client.create_bucket(
                    self.bucket_name,
                    location="us-central1"
                )
            except Exception as e:
                st.error(f"No se pudo acceder o crear el bucket: {str(e)}")
                # Crear un directorio local para almacenar el feedback si falla el bucket
                local_dir = Path(__file__).parent.parent.parent / "feedback_data"
                local_dir.mkdir(exist_ok=True)
                self.bucket = None

    def save_feedback(self, feedback_data):
        """Guarda el feedback en Cloud Storage o localmente"""
        # Genera ID único si no se proporciona nombre
        user_id = feedback_data.get('name', str(uuid.uuid4())[:8])
        feedback_id = str(uuid.uuid4())
        
        # Estructura del feedback
        feedback_entry = {
            'id': feedback_id,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'email': feedback_data.get('email', 'anónimo'),
            'message': feedback_data['message'],
            'category': feedback_data.get('category', 'general')
        }
        
        # Guarda en Cloud Storage o localmente
        try:
            if self.bucket:
                blob = self.bucket.blob(f"feedback/{feedback_entry['id']}.json")
                blob.upload_from_string(
                    json.dumps(feedback_entry),
                    content_type='application/json'
                )
            else:
                # Guardar localmente si no hay bucket
                local_path = Path(__file__).parent.parent.parent / "feedback_data" / f"{feedback_entry['id']}.json"
                with open(local_path, 'w', encoding='utf-8') as f:
                    json.dump(feedback_entry, f, ensure_ascii=False, indent=2)
                    
            # Guardar una copia en la base de datos
            self._save_to_database(feedback_entry)
                
        except Exception as e:
            st.error(f"Error al guardar feedback: {str(e)}")
        
        return feedback_id
        
    def _save_to_database(self, feedback_entry):
        """Guarda una copia en la base de datos (simulado)"""
        # Esta función es un placeholder para futura implementación de base de datos
        # Por ahora solo imprime un mensaje de log
        print(f"Feedback guardado con ID: {feedback_entry['id']}")

# Función eliminada ya que ahora está integrada en la clase FeedbackApp

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
