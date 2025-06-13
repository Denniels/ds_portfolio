"""
Componente para inicializar el valor de la UF en Firestore
=========================================================
Este script inicializa el valor de la UF en Firestore para el sistema de servicios.
"""

import streamlit as st
from google.cloud import firestore
from datetime import datetime
import pytz
import requests
import json

# Constantes
FIRESTORE_COLLECTION = "indicadores_economicos"
UF_DOCUMENT_ID = "valor_uf"
MINDICADOR_API_URL = "https://mindicador.cl/api"

def get_uf_value():
    """Intenta obtener el valor de UF actual"""
    try:
        response = requests.get(f"{MINDICADOR_API_URL}/uf")
        if response.status_code == 200:
            data = response.json()
            if "serie" in data and len(data["serie"]) > 0:
                latest_value = data["serie"][0]
                return {
                    "valor": float(latest_value["valor"]),
                    "fecha": latest_value["fecha"],
                    "fuente": "mindicador.cl",
                    "timestamp": datetime.now(pytz.timezone('America/Santiago')).isoformat()
                }
    except Exception as e:
        st.error(f"Error al obtener UF de mindicador.cl: {str(e)}")
    
    # Valor por defecto
    return {
        "valor": 39000.0,
        "fecha": datetime.now(pytz.timezone('America/Santiago')).strftime("%Y-%m-%d"),
        "fuente": "valor_predeterminado",
        "timestamp": datetime.now(pytz.timezone('America/Santiago')).isoformat()
    }

def main():
    st.title("💱 Inicialización de Valor UF")
    
    st.markdown("""
    Este script inicializa el valor de la UF en Firestore para usarlo en el catálogo de servicios.
    
    El sistema consultará mindicador.cl para obtener el valor actualizado.
    """)
    
    # Obtener el valor de la UF
    uf_data = get_uf_value()
    
    st.markdown(f"""
    **Valor UF obtenido:** ${uf_data['valor']:,.2f}  
    **Fecha:** {uf_data['fecha']}  
    **Fuente:** {uf_data['fuente']}
    """)
    
    # Inicializar Firestore
    try:
        db = firestore.Client()
        collection = db.collection(FIRESTORE_COLLECTION)
        
        # Comprobar si ya existe
        doc = collection.document(UF_DOCUMENT_ID).get()
        if doc.exists:
            st.info(f"El documento UF ya existe en Firestore. Valor actual: ${doc.to_dict().get('valor', 'N/A')}")
            
            if st.button("Actualizar valor existente"):
                collection.document(UF_DOCUMENT_ID).set(uf_data)
                st.success(f"Valor de UF actualizado en Firestore: ${uf_data['valor']:,.2f}")
        else:
            if st.button("Inicializar valor UF en Firestore"):
                collection.document(UF_DOCUMENT_ID).set(uf_data)
                st.success(f"Valor de UF inicializado en Firestore: ${uf_data['valor']:,.2f}")
    
    except Exception as e:
        st.error(f"Error al conectar con Firestore: {str(e)}")
        st.info("Asegúrate de que la API de Firestore está habilitada en tu proyecto de GCP.")
        
        if st.button("Mostrar instrucciones para habilitar Firestore"):
            st.markdown("""
            ### Pasos para habilitar Firestore:
            
            1. Ve a la [Consola de Google Cloud](https://console.cloud.google.com/)
            2. Selecciona tu proyecto
            3. En el menú lateral, ve a "Firestore"
            4. Haz clic en "Seleccionar modo nativo"
            5. Selecciona una región (us-central1 recomendada para optimizar costos)
            6. Haz clic en "Crear base de datos"
            7. Vuelve a ejecutar este script
            """)

if __name__ == "__main__":
    main()
