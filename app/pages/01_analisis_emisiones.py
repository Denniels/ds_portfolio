"""
Página de análisis de emisiones de CO2
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import json
from datetime import datetime

def cargar_mapa_emisiones():
    """
    Carga el mapa de emisiones desde los archivos estáticos
    """
    static_dir = Path(__file__).parent.parent / "static" / "maps"
    timestamp = datetime.now().strftime("%Y%m")
    map_path = static_dir / f"emisiones_co2_{timestamp}.html"
    
    if map_path.exists():
        with open(map_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def main():
    st.title("📊 Análisis de Emisiones de CO2 en Chile")
    
    # Cargar datos
    data_dir = Path(__file__).parent.parent / "data" / "cache"
    
    with open(data_dir / "emisiones_anuales.json", 'r') as f:
        emisiones_anuales = json.load(f)
    
    with open(data_dir / "emisiones_regionales.json", 'r') as f:
        emisiones_regionales = json.load(f)
    
    # Convertir a DataFrame para visualización
    df_anual = pd.DataFrame(list(emisiones_anuales.items()), columns=['Año', 'Emisiones_CO2_Mt'])
    df_regional = pd.DataFrame(emisiones_regionales).T.reset_index()
    df_regional.columns = ['Region', 'lat', 'lon', 'emisiones']
    
    # Gráfico de tendencia temporal
    st.subheader("Tendencia Histórica de Emisiones")
    fig_tendencia = px.line(
        df_anual, 
        x='Año', 
        y='Emisiones_CO2_Mt',
        title='Emisiones de CO2 en Chile (2010-2024)',
        markers=True
    )
    fig_tendencia.update_layout(height=500)
    st.plotly_chart(fig_tendencia, use_container_width=True)
    
    # Mapa de emisiones
    st.subheader("Distribución Geográfica de Emisiones")
    
    col1, col2 = st.columns([2,1])
    
    with col1:
        # Cargar y mostrar mapa
        mapa_html = cargar_mapa_emisiones()
        if mapa_html:
            st.components.v1.html(mapa_html, height=500)
        else:
            st.error("No se pudo cargar el mapa de emisiones")
    
    with col2:
        # Tabla de emisiones por región
        st.markdown("### Emisiones por Región")
        tabla_regional = df_regional[['Region', 'emisiones']].sort_values('emisiones', ascending=False)
        tabla_regional.columns = ['Región', 'Emisiones (Mt)']
        st.dataframe(tabla_regional, height=400)
    
    # Análisis adicional
    with st.expander("📊 Análisis Detallado"):
        st.markdown("""
        ### Observaciones Clave
        
        1. **Tendencia General**
           - Las emisiones muestran una tendencia al alza
           - Se observan fluctuaciones anuales significativas
        
        2. **Distribución Regional**
           - La Región Metropolitana concentra la mayor cantidad de emisiones
           - Las regiones industriales muestran niveles elevados
           - Hay una clara correlación con la densidad poblacional
        
        3. **Factores Contribuyentes**
           - Actividad industrial
           - Transporte urbano
           - Generación de energía
           - Desarrollo urbano
        """)
    
    # Metadata y fuentes
    st.markdown("---")
    st.caption(f"Datos actualizados al: {datetime.now().strftime('%d/%m/%Y')}")
    st.caption("Fuente: Simulación basada en datos del Ministerio del Medio Ambiente")

if __name__ == "__main__":
    main()
