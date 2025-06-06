import streamlit as st
from utils.data_loader import DataLoader
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Emisiones RETC Chile",
    page_icon="🌍",
    layout="wide"
)

# Inicialización del DataLoader
data_loader = DataLoader()

# Título principal
st.title("🌍 Análisis de Emisiones RETC Chile")
st.markdown("""
Esta aplicación presenta un análisis detallado de las emisiones atmosféricas en Chile,
basado en los datos del Registro de Emisiones y Transferencias de Contaminantes (RETC).
""")

# Resumen de emisiones
with st.container():
    st.subheader("📊 Resumen General")
    summary = data_loader.get_emissions_summary()
    
    if summary:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Emisiones (ton)", f"{summary['total_emissions']:,.2f}")
        with col2:
            st.metric("Promedio por Instalación (ton)", f"{summary['average_emissions']:,.2f}")
        with col3:
            st.metric("Número de Instalaciones", f"{summary['num_facilities']:,}")

# Emisiones por región
with st.container():
    st.subheader("🗺️ Emisiones por Región")
    emissions_by_region = data_loader.get_emissions_by_region()
    
    if not emissions_by_region.empty:
        fig = px.bar(
            emissions_by_region,
            x='region',
            y='emision',
            title='Emisiones Totales por Región',
            labels={'region': 'Región', 'emision': 'Emisiones (ton)'}
        )
        st.plotly_chart(fig, use_container_width=True)

# Top emisores
with st.container():
    st.subheader("🏭 Principales Emisores")
    top_emitters = data_loader.get_top_emitters(limit=10)
    
    if not top_emitters.empty:
        st.dataframe(
            top_emitters[['nombre_establecimiento', 'region', 'comuna', 'emision']],
            column_config={
                'nombre_establecimiento': 'Establecimiento',
                'region': 'Región',
                'comuna': 'Comuna',
                'emision': st.column_config.NumberColumn(
                    'Emisiones (ton)',
                    format="%.2f"
                )
            }
        )

# Mapa geográfico
with st.container():
    st.subheader("📍 Distribución Geográfica de Emisiones")
    geo_data = data_loader.get_geographical_data()
    
    if not geo_data.empty:
        # Crear mapa base centrado en Chile
        m = folium.Map(location=[-33.4489, -70.6693], zoom_start=4)
        
        # Agregar marcadores para cada instalación
        for _, row in geo_data.iterrows():
            folium.CircleMarker(
                location=[row['latitud'], row['longitud']],
                radius=5,
                popup=f"{row['nombre_establecimiento']}<br>Emisiones: {row['emision']:,.2f} ton",
                color='red',
                fill=True
            ).add_to(m)
        
        # Mostrar el mapa
        st_folium(m, width=800, height=600)

# Pie de página
st.markdown("""
---
Datos obtenidos del [Registro de Emisiones y Transferencias de Contaminantes (RETC)](https://retc.mma.gob.cl/)
""")