"""
Utilidad para validar predicciones del modelo inmobiliario
"""
import numpy as np
import pandas as pd
import streamlit as st
from typing import Dict, Any, Optional, Tuple

def validate_input_data(input_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Valida los datos de entrada para asegurar que sean razonables"""
    try:
        # Validar metros totales
        if not (30 <= input_data['metros_totales'] <= 1000):
            return False, "Los metros totales deben estar entre 30 y 1000"
            
        # Validar metros construidos
        if not (25 <= input_data['metros_construidos'] <= input_data['metros_totales']):
            return False, "Los metros construidos deben ser menores a los metros totales y mayores a 25"
            
        # Validar dormitorios
        if not (1 <= input_data['dormitorios'] <= 10):
            return False, "El número de dormitorios debe estar entre 1 y 10"
            
        # Validar baños
        if not (1 <= input_data['banos'] <= 8):
            return False, "El número de baños debe estar entre 1 y 8"
            
        # Validar estacionamientos
        if not (0 <= input_data['estacionamientos'] <= 10):
            return False, "El número de estacionamientos debe estar entre 0 y 10"
            
        # Validar antigüedad
        if not (0 <= input_data['antiguedad_anos'] <= 100):
            return False, "La antigüedad debe estar entre 0 y 100 años"
            
        return True, None
        
    except KeyError as e:
        return False, f"Falta el campo requerido: {str(e)}"
    except Exception as e:
        return False, f"Error de validación: {str(e)}"

def validate_prediction(precio_uf: float, input_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Valida que la predicción esté dentro de rangos razonables"""
    
    # Rangos de precios por comuna (en UF)
    rangos_comuna = {
        'Las Condes': (2000, 25000),
        'Providencia': (1800, 20000),
        'Vitacura': (2500, 30000),
        'Lo Barnechea': (2000, 35000),
        'Ñuñoa': (1500, 15000),
        'La Reina': (1800, 20000),
        'Santiago': (1000, 12000),
        'La Florida': (800, 8000)
    }
    
    # Validar contra rangos por comuna
    comuna = input_data.get('comuna')
    if comuna in rangos_comuna:
        min_uf, max_uf = rangos_comuna[comuna]
        if not (min_uf <= precio_uf <= max_uf):
            return False, f"Precio fuera del rango esperado para {comuna} ({min_uf:,.0f} UF - {max_uf:,.0f} UF)"
    
    # Validar precio por metro cuadrado
    precio_por_m2 = precio_uf / input_data['metros_construidos']
    if not (20 <= precio_por_m2 <= 200):
        return False, f"Precio por m² ({precio_por_m2:.1f} UF) fuera del rango esperado (20-200 UF/m²)"
    
    return True, None

def log_prediction(input_data: Dict[str, Any], precio_uf: float, is_demo: bool = False) -> None:
    """Registra la predicción para análisis posterior"""
    try:
        log_file = "predicciones_inmobiliarias.csv"
        
        # Preparar datos para el log
        log_data = {
            'timestamp': pd.Timestamp.now(),
            'precio_uf': precio_uf,
            'is_demo': is_demo,
            **input_data
        }
        
        # Convertir a DataFrame
        df_log = pd.DataFrame([log_data])
        
        # Agregar al archivo de log
        df_log.to_csv(log_file, mode='a', header=not pd.io.common.file_exists(log_file), index=False)
        
    except Exception as e:
        st.warning(f"No se pudo registrar la predicción: {str(e)}")

def convertir_precio(precio_clp: float) -> Tuple[float, float, float]:
    """Convierte el precio en CLP a diferentes formatos"""
    
    # Valor UF actual (aproximado)
    valor_uf = 36000
    
    # Convertir a UF
    precio_uf = precio_clp / valor_uf
    
    # Convertir a millones
    precio_millones = precio_clp / 1_000_000
    
    return precio_clp, precio_millones, precio_uf
