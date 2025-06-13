"""
Sistema de Feedback para el Portafolio (Versión Firestore)
=====================================================
Permite a los usuarios dejar comentarios y sugerencias,
almacenándolos en Firestore para optimizar el uso de la capa gratuita de GCP.

Esta versión está optimizada específicamente para usar Google Cloud Firestore
en la capa gratuita de GCP, permitiendo un almacenamiento eficiente de comentarios
sin costos adicionales.
"""

import streamlit as st
import json
from datetime import datetime
from google.cloud import firestore
import uuid
from pathlib import Path
import os
import sys

# Sistema de almacenamiento de feedback con Firestore
class FirestoreFeedbackSystem:    
    def __init__(self):
        """Inicializa el sistema de feedback con Firestore"""
        try:
            # Intentar inicializar Firestore
            self.db = firestore.Client()
            self.collection = self.db.collection('portfolio_feedback')
            self.is_firestore_available = True
            print("✅ Conexión exitosa a Firestore")
        except Exception as e:
            error_message = str(e)
            print(f"❌ Error al conectar con Firestore: {error_message}")
            
            # Verificar si es un error de API no habilitada (error 403)
            if "403" in error_message and "SERVICE_DISABLED" in error_message:
                print("🛑 La API de Firestore no está habilitada en este proyecto.")
                print("ℹ️  Para habilitar Firestore, ejecuta el script en /scripts/enable_firestore.bat")
                # Mensaje especial para StreamLit
                if "streamlit" in sys.modules:
                    st.warning("""
                    ### ⚠️ Firestore no está habilitado
                    
                    La API de Cloud Firestore no está habilitada en tu proyecto. Para habilitar Firestore:
                    
                    1. Ve a la [Consola de Google Cloud](https://console.cloud.google.com/firestore/databases?project=retc-emissions-analysis)
                    2. Selecciona tu proyecto "retc-emissions-analysis"
                    3. Haz clic en "Crear base de datos"
                    4. Selecciona "modo Nativo" y la región "us-central1"
                    
                    Alternativamente, ejecuta el script `scripts/enable_firestore.bat` desde una terminal.
                    
                    **Mientras tanto, los comentarios se guardarán localmente.**
                    """)
            
            self.is_firestore_available = False
            # Crear directorio local para almacenamiento de respaldo
            local_dir = Path(__file__).parent.parent.parent / "feedback_data"
            local_dir.mkdir(exist_ok=True)
            print(f"📁 Usando almacenamiento local en: {local_dir}")
            self.local_dir = local_dir

    def save_feedback(self, feedback_data):
        """Guarda el feedback en Firestore o localmente como respaldo"""
        # Genera ID único para el feedback
        feedback_id = str(uuid.uuid4())
        
        # Estructura del feedback
        feedback_entry = {
            'id': feedback_id,
            'timestamp': datetime.now(),  # Firestore maneja objetos datetime directamente
            'user_id': feedback_data.get('name', 'anónimo'),
            'email': feedback_data.get('email', 'anónimo'),
            'message': feedback_data['message'],
            'category': feedback_data.get('category', 'general'),
            'processed': False,  # Campo para seguimiento de estado
            'tags': []  # Para categorización futura
        }
        
        try:
            if self.is_firestore_available:
                # Guardar en Firestore - usa el ID del documento como feedback_id
                self.collection.document(feedback_id).set(feedback_entry)
                print(f"Feedback guardado en Firestore con ID: {feedback_id}")
            else:
                # Guardar localmente como respaldo si Firestore no está disponible
                local_path = self.local_dir / f"{feedback_id}.json"
                # Convertir datetime a string para serializar a JSON
                serializable_entry = feedback_entry.copy()
                serializable_entry['timestamp'] = serializable_entry['timestamp'].isoformat()
                
                with open(local_path, 'w', encoding='utf-8') as f:
                    json.dump(serializable_entry, f, ensure_ascii=False, indent=2)
                print(f"Feedback guardado localmente con ID: {feedback_id}")
                    
        except Exception as e:
            error_msg = f"Error al guardar feedback: {str(e)}"
            print(error_msg)
            # Guardar localmente como último recurso
            try:
                local_path = Path(__file__).parent.parent.parent / "feedback_data" / f"error_{feedback_id}.json"
                # Convertir datetime a string para serializar a JSON
                serializable_entry = feedback_entry.copy()
                serializable_entry['timestamp'] = serializable_entry['timestamp'].isoformat()
                serializable_entry['error'] = str(e)
                
                with open(local_path, 'w', encoding='utf-8') as f:
                    json.dump(serializable_entry, f, ensure_ascii=False, indent=2)
                print(f"Feedback guardado en modo de emergencia como: {local_path}")
            except:
                pass
            return None, error_msg
        
        return feedback_id, None

    def get_recent_feedback(self, limit=5):
        """Obtiene los comentarios más recientes (solo para administradores)"""
        try:
            if self.is_firestore_available:
                # Consulta Firestore ordenando por timestamp descendiente
                query = self.collection.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
                results = query.stream()
                
                feedback_list = []
                for doc in results:
                    feedback = doc.to_dict()
                    # Convertir timestamp a string para mostrar
                    if isinstance(feedback.get('timestamp'), datetime):
                        feedback['timestamp'] = feedback['timestamp'].strftime('%d-%m-%Y %H:%M')
                    feedback_list.append(feedback)
                    
                return feedback_list
            else:
                # Modo local como respaldo
                feedback_list = []
                try:
                    files = list(self.local_dir.glob('*.json'))
                    # Ordenar por fecha de modificación (más reciente primero)
                    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                    
                    for i, file_path in enumerate(files[:limit]):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            feedback = json.load(f)
                            feedback_list.append(feedback)
                            
                    return feedback_list
                except Exception as e:
                    print(f"Error al leer feedback local: {str(e)}")
                    return []
        except Exception as e:
            print(f"Error al obtener feedback reciente: {str(e)}")
            return []

# CSS personalizado
def load_feedback_css():
    """Carga el CSS personalizado para la aplicación de feedback"""
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
        
        /* Mejoras estéticas para el formulario */
        .stTextInput input {
            border-radius: 8px; 
        }
        
        .stTextArea textarea {
            border-radius: 8px;
        }
        
        /* Mejoras para la versión móvil */
        @media (max-width: 768px) {
            .feedback-header {
                padding: 1rem;
            }
            
            .feedback-box {
                padding: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

class FirestoreFeedbackApp:
    """Aplicación principal de feedback usando Firestore"""
    
    def __init__(self):
        """Inicializa la aplicación"""
        # Cargar CSS
        load_feedback_css()
        # Crear el sistema de feedback
        self.feedback_system = FirestoreFeedbackSystem()
        
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
        
        # Crear un formulario amigable para el usuario
        with st.form("feedback_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nombre (opcional)", "")
            
            with col2:
                email = st.text_input("Email (opcional)", "")
                
            category = st.selectbox(
                "Categoría",
                ["General", "Sugerencia", "Error/Bug", "Nueva Funcionalidad", "Pregunta"]
            )
            
            message = st.text_area(
                "Tu mensaje",
                height=150,
                placeholder="Escribe aquí tu comentario o sugerencia..."
            )
            
            # Botón de envío con un color que destaque
            submit = st.form_submit_button("Enviar Feedback")
            
            if submit and message:  # Asegurarse de que hay un mensaje
                try:
                    feedback_id, error = self.feedback_system.save_feedback({
                        'name': name,
                        'email': email,
                        'category': category,
                        'message': message
                    })
                    
                    if feedback_id:
                        st.markdown(f"""
                        <div class="success-message">
                            <strong>¡Gracias por tu feedback!</strong><br>
                            Tu mensaje ha sido registrado con el ID: {feedback_id}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="error-message">
                            <strong>No se pudo guardar el feedback:</strong><br>
                            {error}
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
            - ❓ **Preguntas**: Dudas sobre los análisis o metodologías utilizadas
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
        
        # Sección de administración (oculta por defecto)
        # Esto podría activarse mediante una variable de entorno o autenticación
        show_admin = os.environ.get('SHOW_FEEDBACK_ADMIN', 'false').lower() == 'true'
        
        if show_admin and st.sidebar.checkbox("Panel de Administración", False):
            st.sidebar.warning("Panel de administración (solo visible para administradores)")
            if st.sidebar.button("Ver comentarios recientes"):
                st.subheader("Comentarios recientes")
                recent_feedback = self.feedback_system.get_recent_feedback(10)
                
                if recent_feedback:
                    for fb in recent_feedback:
                        with st.expander(f"{fb.get('category')} - {fb.get('timestamp', 'Sin fecha')}"):
                            st.write(f"**Usuario:** {fb.get('user_id', 'Anónimo')}")
                            if fb.get('email') and fb['email'] != 'anónimo':
                                st.write(f"**Email:** {fb['email']}")
                            st.write(f"**Mensaje:** {fb.get('message', 'Sin mensaje')}")
                else:
                    st.info("No hay comentarios recientes para mostrar")
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #64748b; padding: 1rem;'>
            📝 <strong>Sistema de Feedback con Firestore</strong><br>
            Desarrollado como parte del DS Portfolio | Junio 2025
        </div>
        """, unsafe_allow_html=True)
    
    def __call__(self):
        """Hace que la clase sea llamable"""
        self.run()
        
# Crear instancia global de la aplicación
app = FirestoreFeedbackApp()

# Para ser usada como una aplicación independiente
if __name__ == "__main__":
    app.run()
