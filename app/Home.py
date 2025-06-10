import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Emisiones RETC Chile",
    page_icon="🌍",
    layout="wide"
)

# Función para cargar datos
@st.cache_data
def load_data():
    DATA_DIR = Path(__file__).parent.parent / 'data'
    RAW_DATA_PATH = DATA_DIR / 'raw' / 'retc_emisiones_aire_2023.csv'
    
    def detect_delimiter(file_path):
        delimiters = [',', ';', '\t']
        with open(file_path, 'r', encoding='utf-8') as f:
            header = f.readline().strip()
            for delimiter in delimiters:
                if header.count(delimiter) > 0:
                    return delimiter
        return ','
    
    delimiter = detect_delimiter(RAW_DATA_PATH)
    df = pd.read_csv(RAW_DATA_PATH, encoding='utf-8', delimiter=delimiter)
    
    # Convertir columnas numéricas
    def convert_numeric(x):
        if isinstance(x, str):
            return float(x.replace(',', '.'))
        return x

    df['cantidad_toneladas'] = df['cantidad_toneladas'].apply(convert_numeric)
    df['latitud'] = df['latitud'].apply(convert_numeric)
    df['longitud'] = df['longitud'].apply(convert_numeric)
    
    # Renombrar columnas
    column_mapping = {
        'cantidad_toneladas': 'emision',
        'nom_comuna': 'comuna',
        'nom_region': 'region'
    }
    df = df.rename(columns=column_mapping)
    
    return df

# Título principal
st.title("🌍 Análisis de Emisiones RETC Chile")
st.markdown("""
Esta aplicación presenta un análisis detallado de las emisiones atmosféricas en Chile,
basado en los datos del Registro de Emisiones y Transferencias de Contaminantes (RETC).
""")

try:
    # Cargar datos
    df = load_data()
    
    if not df.empty:
        # Resumen de emisiones
        with st.container():
            st.subheader("📊 Resumen General")
            col1, col2, col3 = st.columns(3)
            with col1:
                total_emissions = df['emision'].sum()
                st.metric("Total Emisiones (ton)", f"{total_emissions:,.2f}")
            with col2:
                avg_emissions = df['emision'].mean()
                st.metric("Promedio por Instalación (ton)", f"{avg_emissions:,.2f}")
            with col3:
                num_facilities = len(df)
                st.metric("Número de Instalaciones", f"{num_facilities:,}")

        # Emisiones por región
        with st.container():
            st.subheader("🗺️ Emisiones por Región")
            emissions_by_region = df.groupby('region')['emision'].sum().reset_index()
            
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
            top_emitters = df.nlargest(10, 'emision')
            
            st.dataframe(
                top_emitters[['razon_social', 'region', 'comuna', 'emision']],
                column_config={
                    'razon_social': 'Establecimiento',
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
            
            # Filtrar datos con coordenadas válidas
            geo_data = df.dropna(subset=['latitud', 'longitud']).copy()
            
            if not geo_data.empty:
                # Crear mapa base centrado en Chile
                m = folium.Map(location=[-33.4489, -70.6693], zoom_start=4)
                
                # Agregar marcadores para cada instalación
                for _, row in geo_data.iterrows():
                    folium.CircleMarker(
                        location=[row['latitud'], row['longitud']],
                        radius=5,
                        popup=f"{row['razon_social']}<br>Emisiones: {row['emision']:,.2f} ton",
                        color='red',
                        fill=True
                    ).add_to(m)
                
                # Mostrar el mapa
                st_folium(m, width=800, height=600)

except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    st.markdown("""
    Por favor, asegúrese de que:
    1. El archivo de datos existe en la ruta correcta
    2. El formato del archivo es correcto
    3. Tienes todas las dependencias instaladas
    """)

# Pie de página
st.markdown("""
---
Datos obtenidos del [Registro de Emisiones y Transferencias de Contaminantes (RETC)](https://retc.mma.gob.cl/)
""")