import streamlit as st
import pandas as pd
import gdown
import os
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import time
import sys

# Definir rutas para el caché
CACHE_DIR = Path(tempfile.gettempdir()) / "ds_portfolio_cache"

def is_health_check() -> bool:
    """Verifica si la aplicación está siendo ejecutada en modo health check"""
    return any('health-check' in arg for arg in sys.argv) if len(sys.argv) > 1 else False

@st.cache_data(ttl=24*3600, show_spinner="Cargando datos...", persist="disk")
def load_data_from_gdrive(file_id: str) -> pd.DataFrame:
    """
    Carga datos desde Google Drive con caché de Streamlit
    
    Args:
        file_id: ID del archivo en Google Drive
        
    Returns:
        DataFrame con los datos cargados
    """
    try:
        # Si es un health check, devolver un DataFrame mínimo inmediatamente
        if is_health_check():
            return pd.DataFrame({'mensaje': ['Modo health check activo']})
        
        # Asegurarse de que el directorio de caché existe
        CACHE_DIR.mkdir(exist_ok=True)
        cache_file = CACHE_DIR / "emisiones_aire.csv"
        
        # Si no existe el archivo en caché, intentar descargarlo
        if not cache_file.exists():
            # No usamos st.info durante la inicialización para evitar errores en health check
            url = f"https://drive.google.com/uc?id={file_id}"
            try:
                # Descargar con un timeout para evitar bloqueos
                gdown.download(url, str(cache_file), quiet=True, fuzzy=True)
            except Exception as e:
                print(f"Error downloading file: {str(e)}")
                return pd.DataFrame()
        
        # Leer el CSV con pandas de manera más eficiente
        try:            # Usar usecols para seleccionar solo las columnas necesarias y reducir memoria
            columns_to_use = [
                'nombre_establecimiento', 'region', 'comuna', 'cantidad_toneladas',
                'año', 'latitud', 'longitud', 'contaminante', 'razon_social', 'tipo_fuente',
                'fuente_emisora_general'
            ]
            
            # Primero leer solo la cabecera para verificar qué columnas están disponibles
            header = pd.read_csv(cache_file, encoding='utf-8', sep=';', nrows=0)
            available_cols = [col for col in columns_to_use if col in header.columns]
            
            # Leer solo las columnas que necesitamos
            df = pd.read_csv(
                cache_file,
                encoding='utf-8',
                sep=';',  # Usar punto y coma como separador
                usecols=available_cols,  # Solo leer las columnas necesarias
                dtype='str',  # Leer todo como string inicialmente
                low_memory=True,  # Para manejar archivos grandes
                on_bad_lines='skip'  # Ignorar líneas con problemas
            )
            
            # Convertir columnas numéricas usando método más eficiente
            numeric_columns = {
                'cantidad_toneladas': float,
                'año': int,
                'latitud': float,
                'longitud': float
            }
            
            for col, dtype in numeric_columns.items():
                if col in df.columns:
                    # Limpiar datos numéricos más eficientemente
                    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')
                    if dtype == int:
                        df[col] = df[col].fillna(0).astype(int)
                    else:
                        df[col] = df[col].fillna(0.0)
            
            # Limpiar filas con valores críticos faltantes
            critical_columns = ['cantidad_toneladas', 'nombre_establecimiento', 'region']
            df = df.dropna(subset=[col for col in critical_columns if col in df.columns])
            
            return df
            
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV: {str(e)}")
            # Intentar leer con configuración más permisiva
            try:
                df = pd.read_csv(cache_file, encoding='utf-8', sep=None, engine='python')
                return df
            except Exception as e2:
                print(f"Alternative reading failed: {str(e2)}")
                return pd.DataFrame()

    except Exception as e:
        print(f"General error loading data: {str(e)}")
        return pd.DataFrame()

class DataLoader:
    def __init__(self):
        self.FILE_ID = "1XbMaVUuL9GzklMNBpq0wsFUStfzlzczf"
        
    def load_data_from_gdrive(self, file_id: str) -> pd.DataFrame:
        """Wrapper para la función global load_data_from_gdrive"""
        return load_data_from_gdrive(file_id)
    
    def get_emissions_summary(self) -> Optional[Dict[str, Any]]:
        """Obtener resumen de emisiones"""
        try:
            # Verificar si es un health check
            if is_health_check():
                return {"total_emissions": 0, "average_emissions": 0, "num_facilities": 0, "last_updated": "2023"}
            
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty or 'mensaje' in df.columns:
                return None
            
            # Verificar columnas necesarias
            emissions_col = 'cantidad_toneladas'
            year_col = 'año'
            
            if emissions_col not in df.columns or year_col not in df.columns:
                return None
            
            return {
                "total_emissions": float(df[emissions_col].sum()),
                "average_emissions": float(df[emissions_col].mean()),
                "num_facilities": len(df),
                "last_updated": df[year_col].max()
            }
        except Exception as e:
            print(f"Error processing data: {str(e)}")
            return None
    
    def get_emissions_by_region(self) -> pd.DataFrame:
        """Obtener emisiones por región"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty or 'mensaje' in df.columns:
                return pd.DataFrame()
            
            # Asegurarse de que cantidad_toneladas sea numérico
            emissions_col = 'cantidad_toneladas'
            if emissions_col in df.columns and 'region' in df.columns:
                # Agrupar por región y sumar emisiones
                regional_emissions = df.groupby('region', as_index=False).agg({
                    emissions_col: 'sum'
                }).rename(columns={emissions_col: 'emision'})
                
                return regional_emissions.sort_values('emision', ascending=False)
            
            return pd.DataFrame()
        except Exception as e:
            print(f"Error in regional data: {str(e)}")
            return pd.DataFrame()
    
    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener los principales emisores"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty or 'mensaje' in df.columns:
                return pd.DataFrame()
            
            # Verificar columnas necesarias
            columns = ['nombre_establecimiento', 'region', 'comuna', 'cantidad_toneladas']
            available_columns = [col for col in columns if col in df.columns]
            
            if 'cantidad_toneladas' in available_columns:
                top_emitters = df[available_columns].copy()
                top_emitters = top_emitters.sort_values('cantidad_toneladas', ascending=False).head(limit)
                return top_emitters.rename(columns={'cantidad_toneladas': 'emision'})
            
            return pd.DataFrame()
        except Exception as e:
            print(f"Error in top emitters: {str(e)}")
            return pd.DataFrame()
    
    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos de las instalaciones"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty or 'mensaje' in df.columns:
                return pd.DataFrame()
            
            # Verificar columnas necesarias
            geo_columns = ['nombre_establecimiento', 'latitud', 'longitud', 'cantidad_toneladas']
            available_columns = [col for col in geo_columns if col in df.columns]
            
            if all(col in available_columns for col in ['latitud', 'longitud']):
                geo_data = df[available_columns].copy()
                
                # Convertir coordenadas a valores numéricos
                for coord_col in ['latitud', 'longitud']:
                    if coord_col in geo_data.columns:
                        geo_data[coord_col] = pd.to_numeric(geo_data[coord_col], errors='coerce')
                
                geo_data = geo_data.dropna(subset=['latitud', 'longitud'])
                
                # Renombrar la columna de emisiones si existe
                if 'cantidad_toneladas' in geo_data.columns:
                    geo_data = geo_data.rename(columns={'cantidad_toneladas': 'emision'})
                
                return geo_data
            
            return pd.DataFrame()
        except Exception as e:
            print(f"Error in geographical data: {str(e)}")
            return pd.DataFrame()
