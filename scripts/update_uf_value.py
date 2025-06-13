"""
Actualizador automático del valor de la UF
==========================================
Consulta y almacena el valor actualizado de la UF (Unidad de Fomento)
utilizando la API gratuita del Banco Central de Chile y almacenando
los resultados en Firestore.

Este script está diseñado para ser ejecutado como una función Cloud Run
programada para ejecutarse una vez al día, aprovechando la capa gratuita.
"""

import requests
import json
from datetime import datetime, timedelta
import pytz
from google.cloud import firestore
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# URLs y configuraciones
SBIF_API_BASE_URL = "https://api.sbif.cl/api-sbifv3/recursos_api"
MINDICADOR_API_URL = "https://mindicador.cl/api"
BANCO_CENTRAL_SCRAPER_URL = "https://si3.bcentral.cl/indicadoressiete/secure/IndicadoresDiarios.aspx"

# Colección de Firestore para almacenar valores
FIRESTORE_COLLECTION = "indicadores_economicos"
UF_DOCUMENT_ID = "valor_uf"

class UFUpdater:
    def __init__(self):
        """Inicializa el actualizador de UF"""
        # Inicializar Firestore
        try:
            self.db = firestore.Client()
            self.collection = self.db.collection(FIRESTORE_COLLECTION)
            logger.info("Conexión exitosa a Firestore")
        except Exception as e:
            logger.error(f"Error al conectar con Firestore: {str(e)}")
            raise

    def get_uf_value(self):
        """Intenta obtener el valor de UF desde varias fuentes"""
        # Estrategia 1: mindicador.cl (API pública y gratuita)
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
            logger.warning(f"Error al obtener UF de mindicador.cl: {str(e)}")

        # Estrategia 2: cmfchile.cl (intento sin API key)
        try:
            # Este endpoint puede requerir API key en producción
            url = "https://api.cmfchile.cl/api-sbifv3/recursos_api/uf?formato=json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if "UFs" in data and len(data["UFs"]) > 0:
                    latest_value = data["UFs"][0]
                    return {
                        "valor": float(latest_value["Valor"].replace(".", "").replace(",", ".")),
                        "fecha": latest_value["Fecha"],
                        "fuente": "cmfchile.cl",
                        "timestamp": datetime.now(pytz.timezone('America/Santiago')).isoformat()
                    }
        except Exception as e:
            logger.warning(f"Error al obtener UF de cmfchile.cl: {str(e)}")
        
        # Si llegamos aquí, ambas estrategias fallaron
        logger.error("No se pudo obtener el valor de la UF de ninguna fuente")
        return None

    def store_uf_value(self, uf_data):
        """Almacena el valor de la UF en Firestore"""
        if not uf_data:
            logger.error("No hay datos de UF para almacenar")
            return False
        
        try:
            # Actualizar el documento existente o crear uno nuevo
            self.collection.document(UF_DOCUMENT_ID).set(uf_data, merge=True)
            
            # También almacenar en histórico
            history_doc_id = f"uf_history_{uf_data['fecha'].replace('-', '')}"
            self.collection.document(history_doc_id).set(uf_data)
            
            logger.info(f"Valor de UF almacenado correctamente: {uf_data['valor']} ({uf_data['fecha']})")
            return True
        except Exception as e:
            logger.error(f"Error al guardar valor de UF en Firestore: {str(e)}")
            return False
    
    def get_stored_uf_value(self):
        """Obtiene el último valor de UF almacenado en Firestore"""
        try:
            doc = self.collection.document(UF_DOCUMENT_ID).get()
            if doc.exists:
                return doc.to_dict()
            else:
                logger.warning("No hay valor de UF almacenado")
                return None
        except Exception as e:
            logger.error(f"Error al leer valor de UF desde Firestore: {str(e)}")
            return None
    
    def update(self):
        """Función principal que actualiza el valor de la UF"""
        # Verificar si ya se actualizó hoy
        current_value = self.get_stored_uf_value()
        today = datetime.now(pytz.timezone('America/Santiago')).strftime("%Y-%m-%d")
        
        if current_value and "fecha" in current_value and current_value["fecha"] == today:
            logger.info(f"El valor de UF ya está actualizado para hoy: {current_value['valor']}")
            return current_value
        
        # Obtener nuevo valor
        new_value = self.get_uf_value()
        if new_value:
            self.store_uf_value(new_value)
            return new_value
        
        return None

# Función para ser llamada por Cloud Run
def update_uf_value(request):
    """Endpoint para Cloud Run Functions"""
    updater = UFUpdater()
    result = updater.update()
    
    if result:
        return json.dumps({
            "success": True,
            "value": result["valor"],
            "date": result["fecha"]
        }), 200, {'Content-Type': 'application/json'}
    else:
        return json.dumps({
            "success": False,
            "error": "No se pudo actualizar el valor de la UF"
        }), 500, {'Content-Type': 'application/json'}

# Para pruebas locales o ejecución directa
if __name__ == "__main__":
    updater = UFUpdater()
    result = updater.update()
    if result:
        print(f"UF actualizada: ${result['valor']:,.2f} ({result['fecha']})")
    else:
        print("No se pudo actualizar el valor de la UF")
