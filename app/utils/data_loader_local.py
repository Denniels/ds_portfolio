import streamlit as st
import pandas as pd
from pathlib import Path
import numpy as np

@st.cache_data(ttl=3600)
def _get_cached_dataframe(file_path: Path) -> pd.DataFrame:
    """Obtiene el DataFrame con caché"""
    try:
        if not file_path.exists():
            st.error(f"No se encontró el archivo: {file_path}")
            return pd.DataFrame()
            
        # Intentar diferentes codificaciones
        encodings = ['utf-8', 'latin1', 'cp1252']
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                
                # Procesar columnas numéricas
                if 'cantidad_toneladas' in df.columns:
                    df['cantidad_toneladas'] = pd.to_numeric(
                        df['cantidad_toneladas'].astype(str).str.replace(',', '.'), 
                        errors='coerce'
                    )
                    
                # Renombrar columnas si es necesario
                column_mapping = {
                    'cantidad_toneladas': 'emision',
                    'nom_comuna': 'comuna',
                    'nom_region': 'region'
                }
                df = df.rename(columns=column_mapping)
                
                return df
                
            except Exception:
                continue
                
        st.error(f"No se pudo leer el archivo con ninguna codificación")
        return pd.DataFrame()
        
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return pd.DataFrame()

class LocalDataLoader:
    def __init__(self):
        self.DATA_DIR = Path(__file__).parent.parent.parent / 'data'
        self.RAW_DATA_PATH = self.DATA_DIR / 'raw' / 'retc_emisiones_aire_2023.csv'

    def get_emissions_summary(self) -> dict:
        """Obtener resumen de emisiones"""
        try:
            df = _get_cached_dataframe(self.RAW_DATA_PATH)
            if df.empty:
                return {
                    "total_emissions": 0.0,
                    "average_emissions": 0.0,
                    "num_facilities": 0
                }

            return {
                "total_emissions": float(df["emision"].sum()),
                "average_emissions": float(df["emision"].mean()),
                "num_facilities": len(df)
            }
        except Exception as e:
            st.error(f"Error procesando datos: {str(e)}")
            return None

    def get_emissions_by_region(self) -> pd.DataFrame:
        """Obtener emisiones por región"""
        try:
            df = _get_cached_dataframe(self.RAW_DATA_PATH)
            if df.empty:
                return pd.DataFrame()

            return df.groupby('region')['emision'].sum().reset_index()
        except Exception as e:
            st.error(f"Error cargando datos regionales: {str(e)}")
            return pd.DataFrame()

    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener principales emisores"""
        try:
            df = _get_cached_dataframe(self.RAW_DATA_PATH)
            if df.empty:
                return pd.DataFrame()

            return df.nlargest(limit, "emision")
        except Exception as e:
            st.error(f"Error cargando principales emisores: {str(e)}")
            return pd.DataFrame()

    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos con coordenadas"""
        try:
            df = _get_cached_dataframe(self.RAW_DATA_PATH)
            if df.empty:
                return pd.DataFrame()

            # Limpiar y validar coordenadas
            geo_data = df.copy()
            geo_data = geo_data.dropna(subset=['latitud', 'longitud'])
            
            # Filtrar coordenadas inválidas
            valid_lat = (geo_data['latitud'] >= -56.0) & (geo_data['latitud'] <= -17.0)
            valid_lon = (geo_data['longitud'] >= -76.0) & (geo_data['longitud'] <= -66.0)
            geo_data = geo_data[valid_lat & valid_lon]

            if len(geo_data) < len(df):
                st.warning(f"Se eliminaron {len(df) - len(geo_data)} registros con coordenadas inválidas")

            return geo_data
            
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
