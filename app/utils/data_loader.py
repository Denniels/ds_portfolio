import streamlit as st
import pandas as pd
import gdown
import os
from typing import Dict, Any
from pathlib import Path
import tempfile

@st.cache_data(ttl=3600)
def _get_cached_dataframe(file_id: str, cache_file: Path) -> pd.DataFrame:
    """Obtiene el DataFrame con caché"""
    try:
        if not cache_file.exists():
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, str(cache_file), quiet=False)
        return pd.read_csv(cache_file)
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return pd.DataFrame()

class DataLoader:
    def __init__(self):
        self.CACHE_DIR = Path(tempfile.gettempdir()) / "ds_portfolio_cache"
        self.CACHE_DIR.mkdir(exist_ok=True)
        # ID del archivo CSV en Google Drive
        self.FILE_ID = "1XbMaVUuL9GzklMNBpq0wsFUStfzlzczf"  # retc_emisiones_aire_2023.csv
        self.CACHE_FILE = self.CACHE_DIR / "emisiones_aire.csv"

    def get_emissions_summary(self) -> Dict[str, Any]:
        """Obtener resumen de emisiones"""
        try:
            df = _get_cached_dataframe(self.FILE_ID, self.CACHE_FILE)
            if df.empty:
                return None
            
            summary = {
                "total_emissions": float(df["emision"].sum()),
                "average_emissions": float(df["emision"].mean()),
                "num_facilities": len(df),
                "last_updated": df["anno"].max() if "anno" in df.columns else None
            }
            return summary
        except Exception as e:
            st.error(f"Error procesando datos: {str(e)}")
            return None

    def get_emissions_by_region(self) -> pd.DataFrame:
        """Obtener emisiones por región"""
        try:
            df = _get_cached_dataframe(self.FILE_ID, self.CACHE_FILE)
            if df.empty:
                return pd.DataFrame()
            
            return df.groupby('region')['emision'].sum().reset_index()
        except Exception as e:
            st.error(f"Error cargando datos regionales: {str(e)}")
            return pd.DataFrame()

    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener principales emisores"""
        try:
            df = _get_cached_dataframe(self.FILE_ID, self.CACHE_FILE)
            if df.empty:
                return pd.DataFrame()
            
            return df.nlargest(limit, "emision")
        except Exception as e:
            st.error(f"Error cargando principales emisores: {str(e)}")
            return pd.DataFrame()

    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos con coordenadas"""
        try:
            df = _get_cached_dataframe(self.FILE_ID, self.CACHE_FILE)
            if df.empty:
                return pd.DataFrame()
            
            # Seleccionar solo las columnas relevantes para datos geográficos
            geo_columns = ['nombre_establecimiento', 'region', 'comuna', 'latitud', 'longitud', 'emision']
            return df[geo_columns].dropna(subset=['latitud', 'longitud'])
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
