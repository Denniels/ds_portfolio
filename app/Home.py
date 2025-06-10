import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# Configuración de la página y memoria
st.set_page_config(
    page_title="Análisis de Emisiones RETC Chile",
    page_icon="🌍",
    layout="wide"
)

# Función para cargar datos optimizada
@st.cache_data(ttl=3600)
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
    
    try:
        # Leer el archivo CSV sin conversión de tipos inicialmente
        delimiter = detect_delimiter(RAW_DATA_PATH)
        df = pd.read_csv(
            RAW_DATA_PATH, 
            encoding='utf-8', 
            delimiter=delimiter,
            dtype=str  # Leer todo como strings primero
        )
        
        # Función mejorada para convertir valores numéricos
        def convert_numeric(x):
            if pd.isna(x):
                return np.nan
            if isinstance(x, str):
                # Primero limpiar el string
                x = x.strip()
                try:
                    # Intentar convertir directamente
                    return float(x)
                except ValueError:
                    try:
                        # Reemplazar coma por punto y convertir
                        return float(x.replace(',', '.'))
                    except:
                        return np.nan
            return x

        # Convertir columnas numéricas usando vectorización
        numeric_cols = ['cantidad_toneladas', 'latitud', 'longitud']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].apply(convert_numeric), errors='coerce')
        
        # Renombrar columnas
        column_mapping = {
            'cantidad_toneladas': 'emision',
            'nom_comuna': 'comuna',
            'nom_region': 'region'
        }
        df = df.rename(columns=column_mapping)
        
        # Filtrar filas con valores no válidos
        df = df.dropna(subset=['emision', 'latitud', 'longitud'])
        
        # Validar rango de coordenadas para Chile
        mask_lat = (df['latitud'] >= -56.0) & (df['latitud'] <= -17.0)
        mask_lon = (df['longitud'] >= -76.0) & (df['longitud'] <= -66.0)
        df = df[mask_lat & mask_lon]
        
        return df
    except Exception as e:
        st.error(f"Error al cargar los datos: {str(e)}")
        return pd.DataFrame()

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
        # Control de rendimiento
        st.sidebar.header("⚙️ Configuración")
        total_records = len(df)
        num_records = st.sidebar.slider(
            "Número de registros a procesar",
            min_value=100000,
            max_value=total_records,
            value=min(200000, total_records),
            step=10000,
            help="Ajusta el número de registros para equilibrar rendimiento y precisión"
        )
        
        # Guardar el número de registros en el estado de la sesión
        st.session_state['num_records'] = num_records
        
        if total_records > num_records:
            df = df.sample(n=num_records, random_state=42)
            st.sidebar.info(f"📊 Mostrando {num_records:,} de {total_records:,} registros totales")

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

        # Emisiones por región con gráfico optimizado
        with st.container():
            st.subheader("🗺️ Emisiones por Región")
            emissions_by_region = df.groupby('region')['emision'].sum().reset_index()
            
            fig = px.bar(
                emissions_by_region,
                x='region',
                y='emision',
                title='Emisiones Totales por Región',
                labels={'region': 'Región', 'emision': 'Emisiones (ton)'},
                color='emision',
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                showlegend=False,
                xaxis_tickangle=-45,
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

        # Top emisores con formato mejorado
        with st.container():
            st.subheader("🏭 Principales Emisores")
            top_emitters = df.nlargest(10, 'emision')
            
            st.dataframe(
                top_emitters[['razon_social', 'region', 'comuna', 'emision']].style.format({
                    'emision': '{:,.2f}'
                }),
                column_config={
                    'razon_social': 'Establecimiento',
                    'region': 'Región',
                    'comuna': 'Comuna',
                    'emision': st.column_config.NumberColumn(
                        'Emisiones (ton)',
                        format="%.2f"
                    )
                },
                height=400
            )

        # Mapa geográfico optimizado usando Plotly
        with st.container():
            st.subheader("📍 Distribución Geográfica de Emisiones")
            
            # Filtrar y preparar datos para el mapa
            geo_data = df.dropna(subset=['latitud', 'longitud']).copy()
            
            if not geo_data.empty:
                # Aplicar transformación logarítmica para mejor visualización
                geo_data['color_weight'] = np.log1p(geo_data['emision'])
                
                # Crear mapa base con plotly
                fig_map = go.Figure()
                
                # Agregar capa de mapa de calor
                fig_map.add_densitymapbox(
                    lat=geo_data['latitud'],
                    lon=geo_data['longitud'],
                    z=geo_data['color_weight'],
                    radius=20,
                    colorscale=[
                        [0, 'rgba(247,251,255,0)'],
                        [0.2, 'rgba(222,235,247,0.5)'],
                        [0.4, 'rgba(198,219,239,0.6)'],
                        [0.6, 'rgba(158,202,225,0.7)'],
                        [0.8, 'rgba(107,174,214,0.8)'],
                        [1, 'rgba(8,81,156,0.9)']
                    ],
                    showscale=True,
                    name='Emisiones',
                    hovertemplate='<b>Emisiones:</b> %{customdata[0]:.2f} ton<br>' +
                                '<b>Región:</b> %{customdata[1]}<extra></extra>',
                    colorbar=dict(
                        title='Emisiones (log)',
                        thickness=15,
                        len=0.7,
                        bgcolor='rgba(255,255,255,0.8)'
                    ),
                    customdata=np.column_stack((
                        geo_data['emision'],
                        geo_data['region']
                    ))
                )
                
                # Configurar diseño del mapa
                fig_map.update_layout(
                    mapbox=dict(
                        style='carto-positron',
                        center=dict(lat=-33.4489, lon=-70.6693),
                        zoom=4
                    ),
                    margin=dict(l=0, r=0, t=0, b=0),
                    height=600,
                    showlegend=False
                )
                
                st.plotly_chart(fig_map, use_container_width=True)

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