import streamlit as st
import pandas as pd
import gdown
import os
from typing import Dict, Any
from pathlib import Path
import tempfile

class DataLoader:
    def __init__(self):
        self.CACHE_DIR = Path(tempfile.gettempdir()) / "ds_portfolio_cache"
        self.CACHE_DIR.mkdir(exist_ok=True)
        # ID del archivo CSV en Google Drive
        self.FILE_ID = "1XbMaVUuL9GzklMNBpq0wsFUStfzlzczf"  # retc_emisiones_aire_2023.csv
        self.CACHE_FILE = self.CACHE_DIR / "emisiones_aire.csv"

    def _download_from_gdrive(self) -> bool:
        """Descarga un archivo desde Google Drive"""
        try:
            url = f"https://drive.google.com/uc?id={self.FILE_ID}"
            gdown.download(url, str(self.CACHE_FILE), quiet=False)
            return True
        except Exception as e:
            st.error(f"Error descargando archivo de Google Drive: {str(e)}")
            return False

    def _get_dataframe(self) -> pd.DataFrame:
        """Obtiene el DataFrame base, descargándolo si es necesario"""
        if not self.CACHE_FILE.exists():
            if not self._download_from_gdrive():
                return pd.DataFrame()
        return pd.read_csv(self.CACHE_FILE)

    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def get_emissions_summary(self) -> Dict[str, Any]:
        """Obtener resumen de emisiones"""
        try:
            df = self._get_dataframe()
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

    @st.cache_data(ttl=3600)
    def get_emissions_by_region(self) -> pd.DataFrame:
        """Obtener emisiones por región"""
        try:
            df = self._get_dataframe()
            if df.empty:
                return pd.DataFrame()
            
            return df.groupby('region')['emision'].sum().reset_index()
        except Exception as e:
            st.error(f"Error cargando datos regionales: {str(e)}")
            return pd.DataFrame()

    @st.cache_data(ttl=3600)
    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener principales emisores"""
        try:
            df = self._get_dataframe()
            if df.empty:
                return pd.DataFrame()
            
            return df.nlargest(limit, "emision")
        except Exception as e:
            st.error(f"Error cargando principales emisores: {str(e)}")
            return pd.DataFrame()

    @st.cache_data(ttl=3600)
    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos con coordenadas"""
        try:
            df = self._get_dataframe()
            if df.empty:
                return pd.DataFrame()
            
            # Seleccionar solo las columnas relevantes para datos geográficos
            geo_columns = ['nombre_establecimiento', 'region', 'comuna', 'latitud', 'longitud', 'emision']
            return df[geo_columns].dropna(subset=['latitud', 'longitud'])
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
