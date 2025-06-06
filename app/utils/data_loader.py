import streamlit as st
import pandas as pd
import gdown
import os
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile

# Definir rutas para el caché
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

        try:
            # Primero intentar leer el CSV con pandas
            df = pd.read_csv(
                cache_file,
                encoding='utf-8',
                sep=';',  # Usar punto y coma como separador
                dtype='str'  # Leer todo como string inicialmente
            )
            
            st.info("📊 Columnas detectadas en el archivo:")
            st.write(df.columns.tolist())
            
            # Convertir columnas numéricas
            numeric_columns = {
                'cantidad_toneladas': float,
                'año': int,
                'latitud': float,
                'longitud': float
            }
            
            for col, dtype in numeric_columns.items():
                if col in df.columns:
                    # Limpiar datos numéricos
                    df[col] = df[col].astype(str).str.replace(',', '.').str.replace(r'[^\d\.\-]', '', regex=True)
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    if dtype == int:
                        df[col] = df[col].fillna(0).astype(int)
                    else:
                        df[col] = df[col].fillna(0.0)
            
            # Limpiar filas con valores críticos faltantes
            critical_columns = ['cantidad_toneladas', 'nombre_establecimiento', 'region']
            df = df.dropna(subset=[col for col in critical_columns if col in df.columns])
            
            st.success("✅ Datos procesados exitosamente")
            st.write(f"Total de registros: {len(df)}")
            
            return df

        except pd.errors.ParserError as e:
            st.error(f"❌ Error en el formato del CSV: {str(e)}")
            # Intentar leer con configuración más permisiva
            try:
                df = pd.read_csv(cache_file, encoding='utf-8', sep=None, engine='python')
                st.warning("⚠️ Archivo leído con configuración alternativa")
                return df
            except Exception as e2:
                st.error(f"❌ Error en la lectura alternativa: {str(e2)}")
                return pd.DataFrame()

    except Exception as e:
        st.error(f"❌ Error general en la carga de datos: {str(e)}")
        st.exception(e)
        return pd.DataFrame()

class DataLoader:
    def __init__(self):
        self.FILE_ID = "1XbMaVUuL9GzklMNBpq0wsFUStfzlzczf"
        
    # Método para exponer la función load_data_from_gdrive como método de clase
    def load_data_from_gdrive(self, file_id: str) -> pd.DataFrame:
        """Wrapper para la función global load_data_from_gdrive"""
        return load_data_from_gdrive(file_id)
        
    def get_emissions_summary(self) -> Optional[Dict[str, Any]]:
        """Obtener resumen de emisiones"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return None
            
            # Verificar columnas necesarias
            emissions_col = 'cantidad_toneladas'
            year_col = 'año'
            
            if emissions_col not in df.columns or year_col not in df.columns:
                st.error(f"Faltan columnas requeridas: {emissions_col} y/o {year_col}")
                st.write("Columnas disponibles:", df.columns.tolist())
                return None
            
            return {
                "total_emissions": float(df[emissions_col].sum()),
                "average_emissions": float(df[emissions_col].mean()),
                "num_facilities": len(df),
                "last_updated": df[year_col].max()
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
            
            # Asegurarse de que cantidad_toneladas sea numérico
            emissions_col = 'cantidad_toneladas'
            if emissions_col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[emissions_col]):
                    df[emissions_col] = df[emissions_col].astype(str).str.replace(',', '.').str.replace(r'[^\d\.\-]', '', regex=True)
                    df[emissions_col] = pd.to_numeric(df[emissions_col], errors='coerce')
                    df[emissions_col] = df[emissions_col].fillna(0.0)
            else:
                st.error(f"❌ Columna '{emissions_col}' no encontrada")
                return pd.DataFrame()
                
            # Agrupar por región y sumar emisiones
            regional_emissions = df.groupby('region', as_index=False).agg({
                'cantidad_toneladas': 'sum'
            }).rename(columns={'cantidad_toneladas': 'emision'})
            
            return regional_emissions.sort_values('emision', ascending=False)
        except Exception as e:
            st.error(f"Error cargando datos regionales: {str(e)}")
            return pd.DataFrame()

    def get_top_emitters(self, limit: int = 10) -> pd.DataFrame:
        """Obtener los principales emisores"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
            
            # Asegurarse de que cantidad_toneladas sea numérico
            emissions_col = 'cantidad_toneladas'
            if emissions_col in df.columns:
                # Convertir a numérico si aún no lo es
                if not pd.api.types.is_numeric_dtype(df[emissions_col]):
                    df[emissions_col] = df[emissions_col].astype(str).str.replace(',', '.').str.replace(r'[^\d\.\-]', '', regex=True)
                    df[emissions_col] = pd.to_numeric(df[emissions_col], errors='coerce')
                    df[emissions_col] = df[emissions_col].fillna(0.0)
            else:
                st.error(f"❌ Columna '{emissions_col}' no encontrada")
                return pd.DataFrame()
            
            # Seleccionar y ordenar los principales emisores
            columns = ['nombre_establecimiento', 'region', 'comuna', 'cantidad_toneladas']
            available_columns = [col for col in columns if col in df.columns]
            
            top_emitters = df[available_columns].copy()
            top_emitters = top_emitters.sort_values('cantidad_toneladas', ascending=False).head(limit)
            return top_emitters.rename(columns={'cantidad_toneladas': 'emision'})
        except Exception as e:
            st.error(f"Error cargando principales emisores: {str(e)}")
            return pd.DataFrame()

    def get_geographical_data(self) -> pd.DataFrame:
        """Obtener datos geográficos de las instalaciones"""
        try:
            df = load_data_from_gdrive(self.FILE_ID)
            if df.empty:
                return pd.DataFrame()
                
            # Seleccionar columnas relevantes y filtrar registros con coordenadas válidas
            geo_columns = ['nombre_establecimiento', 'latitud', 'longitud', 'cantidad_toneladas']
            available_columns = [col for col in geo_columns if col in df.columns]
            
            if 'cantidad_toneladas' in available_columns:
                # Convertir a numérico si aún no lo es
                if not pd.api.types.is_numeric_dtype(df['cantidad_toneladas']):
                    df['cantidad_toneladas'] = df['cantidad_toneladas'].astype(str).str.replace(',', '.').str.replace(r'[^\d\.\-]', '', regex=True)
                    df['cantidad_toneladas'] = pd.to_numeric(df['cantidad_toneladas'], errors='coerce')
                    df['cantidad_toneladas'] = df['cantidad_toneladas'].fillna(0.0)
            
            geo_data = df[available_columns].copy()
            # Convertir coordenadas a valores numéricos
            for coord_col in ['latitud', 'longitud']:
                if coord_col in geo_data.columns:
                    geo_data[coord_col] = pd.to_numeric(geo_data[coord_col], errors='coerce')
            
            geo_data = geo_data.dropna(subset=[col for col in ['latitud', 'longitud'] if col in geo_data.columns])
            
            # Renombrar la columna de emisiones si existe
            if 'cantidad_toneladas' in geo_data.columns:
                geo_data = geo_data.rename(columns={'cantidad_toneladas': 'emision'})
                
            return geo_data
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
