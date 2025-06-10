import streamlit as st
import pandas as pd
import gdown
import os
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile

@st.cache_data(ttl=3600)
def load_data_from_gdrive(file_id: str) -> pd.DataFrame:
    """
    Carga datos desde Google Drive con caché de Streamlit
    
    Args:
        file_id: ID del archivo en Google Drive
        
    Returns:
        DataFrame con los datos cargados
    """
    try:
        cache_dir = Path(tempfile.gettempdir()) / "ds_portfolio_cache"
        cache_dir.mkdir(exist_ok=True)
        cache_file = cache_dir / "emisiones_aire.csv"
        
        if not cache_file.exists():
            url = f"https://drive.google.com/uc?id={file_id}"
            gdown.download(url, str(cache_file), quiet=False)
        
        return pd.read_csv(cache_file)
    except Exception as e:
        st.error(f"Error cargando datos: {str(e)}")
        return pd.DataFrame()

class DataLoader:
    def __init__(self):
        self.FILE_ID = "1XbMaVUuL9GzklMNBpq0wsFUStfzlzczf"  # retc_emisiones_aire_2023.csv
        
    def get_emissions_summary(self) -> Optional[Dict[str, Any]]:
        """Obtener resumen de emisiones"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return None
            
            return {
                "total_emissions": float(df["emision"].sum()),
                "average_emissions": float(df["emision"].mean()),
                "num_facilities": len(df),
                "last_updated": df["anno"].max() if "anno" in df.columns else None
            }
        except Exception as e:
            st.error(f"Error procesando datos: {str(e)}")
            return None

    def get_emissions_by_region(self) -> pd.DataFrame:
        """Obtener emisiones por región"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
            
            return df.groupby('region')['emision'].sum().reset_index()
        except Exception as e:
            st.error(f"Error cargando datos regionales: {str(e)}")
            return pd.DataFrame()

    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener principales emisores"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
            
            return df.nlargest(limit, "emision")[['nombre_establecimiento', 'region', 'comuna', 'emision']]
        except Exception as e:
            st.error(f"Error cargando principales emisores: {str(e)}")
            return pd.DataFrame()

    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos con coordenadas"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
            
            geo_columns = ['nombre_establecimiento', 'region', 'comuna', 'latitud', 'longitud', 'emision']
            return df[geo_columns].dropna(subset=['latitud', 'longitud'])
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
