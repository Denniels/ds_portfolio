import streamlit as st
import pandas as pd
import gdown
import os
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile

# Definir rutas relativas para que funcionen tanto en local como en Streamlit Cloud
ROOT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_DIR = ROOT_DIR / "data" / "raw"
CACHE_DIR = Path(tempfile.gettempdir()) / "ds_portfolio_cache"

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
        # Asegurarse de que el directorio de caché existe
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / "emisiones_aire.csv"
        
        # Si no existe el archivo en caché, intentar descargarlo
        if not cache_file.exists():
            st.info("🌐 Descargando datos desde Google Drive...")
            url = f"https://drive.google.com/uc?id={file_id}"
            try:
                gdown.download(url, str(cache_file), quiet=False)
                st.success("✅ Archivo descargado correctamente")
            except Exception as e:
                st.error(f"❌ Error descargando archivo: {str(e)}")
                return pd.DataFrame()
        
        # Intentar leer el CSV con diferentes configuraciones
        try:
            # Primer intento: lectura básica
            df = pd.read_csv(cache_file, encoding='utf-8')
            st.success("✅ Datos cargados exitosamente")
            return df
        except pd.errors.ParserError:
            st.warning("⚠️ Error en el formato del CSV, intentando con configuración alternativa...")
            try:
                # Segundo intento: manejo de errores más flexible
                df = pd.read_csv(
                    cache_file,
                    encoding='utf-8',
                    on_bad_lines='skip',  # Usar on_bad_lines en lugar de error_bad_lines
                    sep=None,  # Detectar separador automáticamente
                    engine='python'  # Usar el engine de Python que es más flexible
                )
                st.warning("⚠️ Algunos registros pueden haber sido omitidos debido a errores de formato")
                return df
            except Exception as e:
                st.error(f"❌ Error en la lectura del archivo: {str(e)}")
                return pd.DataFrame()
            
    except Exception as e:
        st.error(f"❌ Error en la carga de datos: {str(e)}")
        return pd.DataFrame()

class DataLoader:
    def __init__(self):
        self.FILE_ID = "1XbMaVUuL9GzklMNBpq0wsFUStfzlzczf"
        
    def get_emissions_summary(self) -> Optional[Dict[str, Any]]:
        """Obtener resumen de emisiones"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return None
            
            # Verificar y mostrar las columnas disponibles
            st.info(f"Columnas disponibles: {', '.join(df.columns)}")
            
            # Verificar columnas necesarias
            required_columns = ['cantidad', 'anno']  # Ajustar nombres según el CSV real
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                st.error(f"Faltan columnas requeridas: {', '.join(missing_columns)}")
                return None
            
            return {
                "total_emissions": float(df["cantidad"].sum()),
                "average_emissions": float(df["cantidad"].mean()),
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
            
            st.info(f"Columnas disponibles: {', '.join(df.columns)}")
            region_col = 'region' if 'region' in df.columns else 'Region'
            emissions_col = 'cantidad' if 'cantidad' in df.columns else 'Cantidad'
            
            return df.groupby(region_col)[emissions_col].sum().reset_index()
        except Exception as e:
            st.error(f"Error cargando datos regionales: {str(e)}")
            return pd.DataFrame()

    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener principales emisores"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
            
            # Ajustar nombres de columnas según el CSV real
            nombre_col = 'nombre_establecimiento' if 'nombre_establecimiento' in df.columns else 'Establecimiento'
            region_col = 'region' if 'region' in df.columns else 'Region'
            comuna_col = 'comuna' if 'comuna' in df.columns else 'Comuna'
            emissions_col = 'cantidad' if 'cantidad' in df.columns else 'Cantidad'
            
            return df.nlargest(limit, emissions_col)[[nombre_col, region_col, comuna_col, emissions_col]]
        except Exception as e:
            st.error(f"Error cargando principales emisores: {str(e)}")
            return pd.DataFrame()

    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos con coordenadas"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
            
            # Ajustar nombres de columnas según el CSV real
            st.info(f"Columnas disponibles: {', '.join(df.columns)}")
            geo_columns = ['nombre_establecimiento', 'region', 'comuna', 'latitud', 'longitud', 'cantidad']
            available_columns = [col for col in geo_columns if col in df.columns]
            
            return df[available_columns].dropna(subset=['latitud', 'longitud'])
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
