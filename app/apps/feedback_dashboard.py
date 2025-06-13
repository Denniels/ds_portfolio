"""
Utilidad para administrar y visualizar feedback
============================================
"""

import streamlit as st
from google.cloud import storage
import json
from datetime import datetime
import pandas as pd

def load_feedback_data():
    """Carga todos los feedbacks del bucket"""
    client = storage.Client()
    bucket = client.bucket("ds-portfolio-feedback")
    
    feedback_data = []
    for blob in bucket.list_blobs(prefix="feedback/"):
        try:
            content = json.loads(blob.download_as_string())
            feedback_data.append(content)
        except Exception as e:
            st.error(f"Error al cargar feedback: {str(e)}")
    
    return pd.DataFrame(feedback_data)

def show_feedback_dashboard():
    """Muestra un dashboard con los feedbacks recibidos"""
    st.title("📊 Dashboard de Feedback")
    
    try:
        df = load_feedback_data()
        if df.empty:
            st.info("Aún no hay feedback registrado.")
            return
            
        # Métricas generales
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Feedback", len(df))
        with col2:
            st.metric("Usuarios Únicos", df['user_id'].nunique())
        with col3:
            st.metric("Categorías", df['category'].nunique())
            
        # Filtros
        st.subheader("🔍 Filtros")
        col1, col2 = st.columns(2)
        with col1:
            selected_category = st.multiselect(
                "Categoría",
                options=sorted(df['category'].unique()),
                default=[]
            )
        with col2:
            date_range = st.date_input(
                "Rango de fechas",
                value=(df['timestamp'].min(), df['timestamp'].max())
            )
            
        # Aplicar filtros
        if selected_category:
            df = df[df['category'].isin(selected_category)]
            
        # Mostrar feedbacks
        st.subheader("💬 Feedbacks Recibidos")
        for _, row in df.iterrows():
            with st.expander(f"{row['timestamp'][:10]} - {row['category']} - {row['user_id']}"):
                st.write(f"**Mensaje:** {row['message']}")
                if row['email'] != 'anónimo':
                    st.write(f"**Contact:** {row['email']}")
                    
    except Exception as e:
        st.error(f"Error al cargar el dashboard: {str(e)}")

if __name__ == "__main__":
    show_feedback_dashboard()
