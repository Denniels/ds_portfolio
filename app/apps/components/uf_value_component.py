"""
Componente para mostrar el valor actualizado de la UF
=====================================================
Muestra el valor actual de la UF consultando Firestore.
Diseñado para ser usado en cualquier parte de la aplicación.
"""

import streamlit as st
from google.cloud import firestore
from datetime import datetime, timedelta
import pytz
import locale

# Configuración de formateo para números chilenos
try:
    locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')  # Alternativa
    except:
        pass  # Si falla, usaremos el formato predeterminado

# Colección de Firestore donde se almacena el valor de la UF
FIRESTORE_COLLECTION = "indicadores_economicos"
UF_DOCUMENT_ID = "valor_uf"

class UFValueComponent:
    """Componente para mostrar el valor de la UF actualizado"""
    
    def __init__(self):
        """Inicializa el componente"""
        self._initialize_firestore()
    
    def _initialize_firestore(self):
        """Inicializa la conexión a Firestore"""
        try:
            self.db = firestore.Client()
            self.collection = self.db.collection(FIRESTORE_COLLECTION)
            self.is_firestore_available = True
        except Exception as e:
            st.warning("No se pudo conectar a Firestore para obtener el valor de la UF. Usando valor por defecto.")
            self.is_firestore_available = False
    
    def get_uf_value(self):
        """Obtiene el valor actual de la UF desde Firestore"""
        if not self.is_firestore_available:
            return {"valor": 39000, "fecha": datetime.now().strftime("%Y-%m-%d"), "actualizado": False}
        
        try:
            doc = self.collection.document(UF_DOCUMENT_ID).get()
            if doc.exists:
                data = doc.to_dict()
                # Verificar si el valor está actualizado (no más de 3 días)
                fecha = datetime.strptime(data["fecha"], "%Y-%m-%d").date()
                today = datetime.now(pytz.timezone('America/Santiago')).date()
                
                is_current = (today - fecha).days <= 3
                
                return {
                    "valor": data["valor"],
                    "fecha": data["fecha"],
                    "actualizado": is_current,
                    "fuente": data.get("fuente", "Desconocida")
                }
            else:
                return {"valor": 39000, "fecha": datetime.now().strftime("%Y-%m-%d"), "actualizado": False}
        except Exception as e:
            return {"valor": 39000, "fecha": datetime.now().strftime("%Y-%m-%d"), "actualizado": False}
    
    def render_compact(self):
        """Muestra una versión compacta del valor de la UF"""
        uf_data = self.get_uf_value()
        
        html = f"""
        <div style="font-size:0.9em; color:#666; text-align:right; padding:4px 8px; border-radius:4px; 
                    background-color: {'#f0f8ff' if uf_data['actualizado'] else '#fff8e6'};">
            UF: ${uf_data['valor']:,.2f} <small>({uf_data['fecha']})</small>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Muestra el valor de la UF en la barra lateral"""
        uf_data = self.get_uf_value()
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 💱 Valor de la UF")
        
        valor_formateado = f"${uf_data['valor']:,.0f}" if uf_data['valor'] > 100 else f"${uf_data['valor']:,.2f}"
        
        col1, col2 = st.sidebar.columns([3, 2])
        col1.metric("Valor actual", valor_formateado)
        col2.markdown(f"<div style='margin-top:15px; font-size:0.85em; color:#666;'>Fecha: {uf_data['fecha']}</div>", unsafe_allow_html=True)
        
        if not uf_data['actualizado']:
            st.sidebar.caption("⚠️ Este valor podría no estar actualizado")
    
    def render_full(self):
        """Muestra información completa sobre el valor de la UF"""
        uf_data = self.get_uf_value()
        
        st.markdown("## 💱 Valor de la Unidad de Fomento (UF)")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            valor_formateado = f"${uf_data['valor']:,.0f}" if uf_data['valor'] > 100 else f"${uf_data['valor']:,.2f}"
            st.markdown(f"### {valor_formateado} CLP")
            
            if not uf_data['actualizado']:
                st.warning("⚠️ Este valor podría no estar actualizado")
            else:
                st.success("✅ Valor actualizado")
        
        with col2:
            st.markdown(f"**Fecha:** {uf_data['fecha']}")
            if 'fuente' in uf_data:
                st.markdown(f"**Fuente:** {uf_data['fuente']}")
            
            # Convertir valores comunes a UF
            st.markdown("### Equivalencias")
            
            valores = [1000000, 5000000, 10000000, 50000000]
            for valor in valores:
                uf_equiv = valor / uf_data['valor']
                st.text(f"${valor:,.0f} = {uf_equiv:.2f} UF")
        
        st.markdown("---")
        st.caption("Los contratos a plazo fijo se cotizan en UF para protección ante la inflación.")


# Función para obtener una instancia del componente
def get_uf_component():
    """Devuelve una instancia reutilizable del componente UF"""
    if 'uf_component' not in st.session_state:
        st.session_state['uf_component'] = UFValueComponent()
    return st.session_state['uf_component']


# Para probar el componente de forma independiente
if __name__ == "__main__":
    st.set_page_config(page_title="Componente UF", page_icon="💱", layout="wide")
    st.title("Demo - Componente de Valor UF")
    
    uf_comp = get_uf_component()
    
    st.subheader("1. Versión compacta:")
    uf_comp.render_compact()
    
    st.subheader("2. Versión completa:")
    uf_comp.render_full()
    
    st.subheader("3. Versión barra lateral:")
    st.write("(Revisa el sidebar)")
    uf_comp.render_sidebar()
