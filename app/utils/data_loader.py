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
            # Primero leer solo las primeras filas para diagnóstico
            df_sample = pd.read_csv(cache_file, nrows=5)
            st.write("Muestra de las primeras filas:")
            st.write(df_sample)
            st.write("Tipos de datos detectados:")
            st.write(df_sample.dtypes)

            # Leer el archivo completo con configuración específica
            df = pd.read_csv(
                cache_file,
                dtype={
                    'cantidad_toneladas': str,
                    'año': str,
                    'latitud': str,
                    'longitud': str,
                    'region': str,
                    'comuna': str,
                    'nombre_establecimiento': str
                }
            )

            # Convertir y limpiar datos numéricos
            def clean_numeric_column(series):
                # Remover cualquier carácter que no sea número, punto o coma
                cleaned = series.str.replace(r'[^\d,.-]', '', regex=True)
                # Reemplazar coma por punto para decimales
                cleaned = cleaned.str.replace(',', '.')
                # Convertir a numérico
                return pd.to_numeric(cleaned, errors='coerce')

            # Limpiar columnas numéricas
            if 'cantidad_toneladas' in df.columns:
                st.write("Limpiando cantidad_toneladas...")
                df['cantidad_toneladas'] = clean_numeric_column(df['cantidad_toneladas'])
                st.write("Estadísticas de cantidad_toneladas:")
                st.write(df['cantidad_toneladas'].describe())

            if 'año' in df.columns:
                st.write("Limpiando año...")
                df['año'] = pd.to_numeric(df['año'].astype(str).replace(r'\D', '', regex=True), errors='coerce')
                df['año'] = df['año'].fillna(0).astype(int)

            for col in ['latitud', 'longitud']:
                if col in df.columns:
                    st.write(f"Limpiando {col}...")
                    df[col] = clean_numeric_column(df[col])

            # Limpiar filas con valores nulos en columnas críticas
            before_len = len(df)
            df = df.dropna(subset=['cantidad_toneladas', 'nombre_establecimiento', 'region'])
            after_len = len(df)
            st.write(f"Filas eliminadas por valores nulos: {before_len - after_len}")

            # Validar tipos de datos finales
            st.success("✅ Datos procesados exitosamente")
            st.write("Tipos de datos finales:")
            st.write(df.dtypes)
            st.write("Resumen de datos:")
            st.write(df.describe())

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
            
            # Asegurarse de que cantidad_toneladas sea numérico
            if not pd.api.types.is_numeric_dtype(df['cantidad_toneladas']):
                df['cantidad_toneladas'] = pd.to_numeric(df['cantidad_toneladas'].astype(str).str.replace(',', '.'), errors='coerce')
                df['cantidad_toneladas'] = df['cantidad_toneladas'].fillna(0)
            
            # Seleccionar y ordenar los principales emisores
            top_emitters = df[['nombre_establecimiento', 'region', 'comuna', 'cantidad_toneladas']]
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
            geo_data = df[['nombre_establecimiento', 'latitud', 'longitud', 'cantidad_toneladas']]
            geo_data = geo_data.dropna(subset=['latitud', 'longitud'])
            return geo_data.rename(columns={'cantidad_toneladas': 'emision'})
        except Exception as e:
            st.error(f"Error cargando datos geográficos: {str(e)}")
            return pd.DataFrame()
