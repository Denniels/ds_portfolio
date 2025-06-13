import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Inicializar Firebase Admin (si no está inicializado)
if not firebase_admin._apps:
    # Inicializar con credenciales por defecto
    try:
        firebase_admin.initialize_app()
        print("Inicializado Firebase con credenciales predeterminadas")
    except Exception as e:
        print(f"Error al inicializar Firebase: {e}")
        # Intentar usar las credenciales de la cuenta de servicio si están presentes
        try:
            cred_path = os.path.join('credentials', 'analicis-demografico-0fa332bfc9a7.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print(f"Inicializado Firebase con credenciales desde {cred_path}")
            else:
                print(f"No se encontró el archivo de credenciales en {cred_path}")
                exit(1)
        except Exception as e2:
            print(f"Error al inicializar Firebase con credenciales personalizadas: {e2}")
            exit(1)

# Obtener una referencia a Firestore
db = firestore.client()

# Leer variables de entorno para la configuración
collection_name = os.environ.get("FIRESTORE_COLLECTION", "portfolio_feedback")

# Obtener todos los documentos de la colección
try:
    docs = db.collection(collection_name).stream()
    
    print(f"\n--- Mensajes en la colección '{collection_name}' ---\n")
    
    count = 0
    for doc in docs:
        count += 1
        doc_data = doc.to_dict()
        print(f"ID del documento: {doc.id}")
        print(f"Fecha: {doc_data.get('timestamp', 'No disponible')}")
        print(f"App: {doc_data.get('app_name', 'No especificada')}")
        print(f"Mensaje: {doc_data.get('message', '')}")
        print(f"Puntuación: {doc_data.get('rating', 'No especificada')}")
        print("-" * 50)
    
    if count == 0:
        print("No se encontraron mensajes en la colección.")
    else:
        print(f"Total de mensajes: {count}")
    
except Exception as e:
    print(f"Error al acceder a Firestore: {e}")
