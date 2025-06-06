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
        
        # Intentar leer el CSV con diferentes configuraciones
        try:
            # Primero intentamos leer unas pocas filas para detectar el formato
            df_sample = pd.read_csv(cache_file, encoding='utf-8', nrows=5)
            st.info("📊 Muestra de columnas detectadas:")
            for col in df_sample.columns:
                st.write(f"- {col}: {df_sample[col].dtype}")
            
            # Definir las columnas requeridas y sus tipos esperados
            required_columns = {
                'cantidad_toneladas': 'float64',
                'año': 'int64',
                'nombre_establecimiento': 'object',
                'region': 'object',
                'comuna': 'object',
                'latitud': 'float64',
                'longitud': 'float64'
            }
            
            # Verificar columnas faltantes
            missing_columns = [col for col in required_columns if col not in df_sample.columns]
            if missing_columns:
                st.warning(f"⚠️ Columnas faltantes: {', '.join(missing_columns)}")
                # Intentar buscar columnas similares
                for missing_col in missing_columns:
                    similar_cols = [col for col in df_sample.columns if missing_col.lower() in col.lower()]
                    if similar_cols:
                        st.info(f"💡 Posibles alternativas para '{missing_col}': {', '.join(similar_cols)}")
            
            # Leer el archivo completo
            df = pd.read_csv(cache_file, encoding='utf-8')
            
            # Limpiar y convertir tipos de datos
            if 'cantidad_toneladas' in df.columns:
                df['cantidad_toneladas'] = pd.to_numeric(df['cantidad_toneladas'], errors='coerce')
            if 'año' in df.columns:
                df['año'] = pd.to_numeric(df['año'], errors='coerce')
            if 'latitud' in df.columns:
                df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
            if 'longitud' in df.columns:
                df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')
            
            st.success("✅ Datos cargados exitosamente")
            st.info(f"📈 Estadísticas del dataset:")
            st.write(f"- Filas totales: {len(df)}")
            st.write(f"- Columnas disponibles: {', '.join(df.columns)}")
            return df
            
        except pd.errors.ParserError:
            st.warning("⚠️ Error en el formato del CSV, intentando con configuración alternativa...")
            try:
                df = pd.read_csv(
                    cache_file,
                    encoding='utf-8',
                    sep=None,  # Detectar separador automáticamente
                    engine='python'  # Usar el engine de Python que es más flexible
                )
                st.warning("⚠️ Algunos registros pueden haber sido omitidos debido a errores de formato")
                st.info(f"Columnas disponibles: {', '.join(df.columns)}")
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
                
            # Seleccionar y ordenar los principales emisores
            top_emitters = df[['nombre_establecimiento', 'region', 'comuna', 'cantidad_toneladas']]
            top_emitters = top_emitters.nlargest(limit, 'cantidad_toneladas')
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
            geo_data = df[['nombre_establecimiento', 'latitud', 'longitud', 'cantidad_toneladas']]
            geo_data = geo_data.dropna(subset=['latitud', 'longitud'])
            return geo_data.rename(columns={'cantidad_toneladas': 'emision'})
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
