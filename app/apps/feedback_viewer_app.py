import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime
import pytz

# Definir función para inicializar Firebase si aún no está inicializado
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Intenta inicializar con credenciales por defecto
            firebase_admin.initialize_app()
            st.sidebar.success("Conectado a Firebase con credenciales predeterminadas")
        except Exception as e:
            # Si falla, intenta usar credenciales locales
            cred_path = os.path.join('credentials', 'analicis-demografico-0fa332bfc9a7.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                st.sidebar.success("Conectado a Firebase con credenciales locales")
            else:
                st.sidebar.error(f"No se pudo conectar a Firebase: {e}")
                st.sidebar.error(f"No se encontró archivo de credenciales en {cred_path}")
                return False
    return True

# Función para obtener todos los mensajes de feedback
def get_feedback():
    collection_name = os.environ.get("FIRESTORE_COLLECTION", "portfolio_feedback")
    db = firestore.client()
    
    try:
        # Obtener todos los comentarios, ordenados por fecha descendente
        feedback_ref = db.collection(collection_name).order_by('timestamp', direction=firestore.Query.DESCENDING)
        docs = feedback_ref.stream()
        
        feedback_list = []
        for doc in docs:
            data = doc.to_dict()
            feedback_list.append({
                "id": doc.id,
                "message": data.get("message", ""),
                "app_name": data.get("app_name", "No especificada"),
                "timestamp": data.get("timestamp", None),
                "rating": data.get("rating", None)
            })
        
        return feedback_list
    except Exception as e:
        st.error(f"Error al obtener mensajes: {e}")
        return []

# Función principal
def main():
    st.title("📝 Mensajes de Feedback")
    st.write("Aquí puedes ver todos los comentarios enviados por los usuarios.")
    
    # Inicializar Firebase
    if not initialize_firebase():
        st.error("No se pudo inicializar Firebase. Verifica las credenciales.")
        return
    
    # Obtener comentarios
    with st.spinner("Cargando mensajes..."):
        feedback_list = get_feedback()
    
    # Mostrar información de resumen
    st.subheader(f"Total de mensajes: {len(feedback_list)}")
    
    # Filtros
    with st.expander("Filtros", expanded=False):
        col1, col2 = st.columns(2)
        
        # Si hay aplicaciones disponibles, mostrar filtro
        all_apps = list(set([fb.get("app_name", "No especificada") for fb in feedback_list]))
        selected_app = col1.selectbox("Filtrar por aplicación", ["Todas"] + all_apps)
        
        # Filtro por fecha
        date_options = ["Todas", "Hoy", "Esta semana", "Este mes"]
        selected_date = col2.selectbox("Filtrar por fecha", date_options)
    
    # Aplicar filtros
    filtered_list = feedback_list
    
    if selected_app != "Todas":
        filtered_list = [fb for fb in filtered_list if fb.get("app_name") == selected_app]
    
    if selected_date != "Todas":
        now = datetime.now(pytz.UTC)
        if selected_date == "Hoy":
            filtered_list = [fb for fb in filtered_list if fb.get("timestamp") and 
                             fb.get("timestamp").date() == now.date()]
        elif selected_date == "Esta semana":
            filtered_list = [fb for fb in filtered_list if fb.get("timestamp") and 
                             (now - fb.get("timestamp")).days < 7]
        elif selected_date == "Este mes":
            filtered_list = [fb for fb in filtered_list if fb.get("timestamp") and 
                             fb.get("timestamp").month == now.month and 
                             fb.get("timestamp").year == now.year]
    
    # Mostrar resultados
    if not filtered_list:
        st.info("No se encontraron mensajes que coincidan con los filtros seleccionados.")
    else:
        st.subheader(f"Mostrando {len(filtered_list)} mensaje(s)")
        
        for fb in filtered_list:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                # Columna 1: Mensaje
                col1.markdown(f"**Mensaje:** {fb.get('message', 'No hay mensaje')}")
                
                # Columna 2: Metadatos
                col2.caption(f"ID: {fb.get('id', 'No disponible')[:8]}...")
                col2.caption(f"App: {fb.get('app_name', 'No especificada')}")
                if fb.get('timestamp'):
                    col2.caption(f"Fecha: {fb.get('timestamp').strftime('%d/%m/%Y %H:%M')}")
                if fb.get('rating'):
                    col2.caption(f"Puntuación: {fb.get('rating')}/5")
                
                st.divider()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()
