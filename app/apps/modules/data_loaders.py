"""
Utilidades para carga y procesamiento de datos
=============================================
"""

import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
from io import BytesIO, StringIO
import requests
from pathlib import Path

def load_water_quality_data():
    """Carga datos de calidad del agua desde fuente oficial o demo"""
    from .config import DATA_SOURCES
    from .water_quality import create_demo_water_data
    
    try:
        # Intentar cargar datos oficiales
        st.info("🔄 Cargando datos oficiales de la DGA...")
        url = DATA_SOURCES['water_quality']
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        try:
            # Intentar como Excel primero
            df = pd.read_excel(
                BytesIO(response.content),
                sheet_name=0,
                header=0,
                na_values=['', 'N/A', 'NA', 'null', 'NULL']
            )
            st.success(f"✅ Datos oficiales cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
            
        except Exception:
            # Intentar diferentes configuraciones de CSV
            content = response.content.decode('utf-8', errors='ignore')
            for separator in [',', ';', '\t']:
                try:
                    df = pd.read_csv(
                        StringIO(content),
                        sep=separator,
                        encoding='utf-8',
                        on_bad_lines='skip',
                        low_memory=False,
                        dtype=str,
                        quoting=1,
                        skipinitialspace=True
                    )
                    if len(df.columns) >= 5:
                        st.info(f"📊 Datos cargados como CSV con separador '{separator}'")
                        break
                except Exception:
                    continue
        
        # Procesamiento básico
        df = process_water_data(df)
        return df, True
        
    except Exception as e:
        st.warning(f"⚠️ Error al cargar datos oficiales: {str(e)}")
        st.info("🔄 Cargando datos de demostración...")
        
        df = create_demo_water_data()
        return df, False

def process_water_data(df):
    """Procesa y limpia los datos de calidad del agua"""
    
    if df is None or len(df) == 0:
        return df
    
    st.info(f"📋 Procesando datos: {len(df)} filas, {len(df.columns)} columnas")
    
    # Limpiar nombres de columnas
    df.columns = df.columns.astype(str).str.strip()
    
    # Convertir fechas - buscar columnas de fecha comunes
    date_columns = [
        'FEC_MEDICION', 'FECHA', 'Fecha', 'fecha_medicion', 'Date',
        'Fecha Medición', 'FECHA_MEDICION', 'fecha_muestra'
    ]
    
    date_col = None
    for col in date_columns:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                df['FEC_MEDICION'] = df[col]  # Normalizar nombre
                date_col = col
                break
            except Exception:
                continue
    
    if date_col:
        df['año'] = df['FEC_MEDICION'].dt.year
        df['mes'] = df['FEC_MEDICION'].dt.month
        df['mes_nombre'] = df['FEC_MEDICION'].dt.month_name()
        st.info(f"✅ Fechas procesadas desde columna: {date_col}")
    else:
        st.warning("⚠️ No se encontraron columnas de fecha válidas")
    
    return df

def load_emissions_data(csv_path):
    """Carga datos de emisiones CO2 desde CSV del RETC"""
    
    try:
        if not Path(csv_path).exists():
            raise FileNotFoundError(f"Archivo no encontrado: {csv_path}")
        
        # Leer CSV con parámetros específicos para el formato RETC
        raw_data = pd.read_csv(
            csv_path,
            sep=';',  # Separador punto y coma
            encoding='utf-8',  # Encoding UTF-8
            low_memory=False,  # Para archivos grandes
            on_bad_lines='skip'  # Saltar líneas mal formateadas
        )
        
        st.success(f"✅ Datos RETC cargados: {len(raw_data):,} registros")
        return raw_data
        
    except Exception as e:
        st.error(f"❌ Error al cargar datos RETC: {str(e)}")
        return None

def diagnose_excel_structure(file_path):
    """Diagnostica la estructura de un archivo Excel"""
    
    try:
        excel_file = pd.ExcelFile(file_path)
        diagnosis = {
            'filename': Path(file_path).name,
            'total_sheets': len(excel_file.sheet_names),
            'sheet_names': excel_file.sheet_names,
            'sheets_info': {}
        }
        
        for sheet_name in excel_file.sheet_names[:3]:  # Solo las primeras 3 hojas
            try:
                df_sample = pd.read_excel(file_path, sheet_name=sheet_name, nrows=5)
                diagnosis['sheets_info'][sheet_name] = {
                    'columns': list(df_sample.columns),
                    'sample_data': df_sample.head(2).to_dict(),
                    'shape_estimate': f"~{len(df_sample.columns)} columnas"
                }
            except Exception as e:
                diagnosis['sheets_info'][sheet_name] = {'error': str(e)}
        
        return diagnosis
        
    except Exception as e:
        return {'error': f"Error al analizar archivo: {str(e)}"}

def convert_numeric_columns(df, columns):
    """Convierte columnas a numéricas manejando formato chileno (comas decimales)"""
    
    for col in columns:
        if col in df.columns:
            try:
                # Convertir a string y reemplazar comas por puntos
                df[col] = pd.to_numeric(
                    df[col].astype(str).str.replace(',', '.', regex=False),
                    errors='coerce'
                ).fillna(0)
                st.info(f"✅ Columna '{col}' convertida a numérica")
            except Exception as e:
                st.warning(f"⚠️ Error convirtiendo '{col}': {str(e)}")
    
    return df
