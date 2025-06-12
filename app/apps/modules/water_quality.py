"""
Utilidades específicas para análisis de calidad del agua
=======================================================
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
from .config import DEMO_STATIONS
from .water_quality_config import WATER_QUALITY_PARAMETERS, QUALITY_CLASSIFICATION

def create_demo_water_data():
    """Crea datos de demostración realistas para calidad del agua"""
    
    np.random.seed(42)
    n_records = 5000
    
    # Crear fechas realistas
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start_date, end_date, periods=n_records)
    
    # Estaciones de demostración
    stations = list(DEMO_STATIONS.keys())
    
    # Generar datos realistas con patrones estacionales
    data = []
    
    for i, date in enumerate(dates):
        station = np.random.choice(stations)
        
        # Efectos estacionales (Chile hemisferio sur)
        month = date.month
        seasonal_factor = np.sin(2 * np.pi * (month - 1) / 12)
        
        # Temperatura con estacionalidad
        base_temp = 15
        temp = base_temp + 8 * seasonal_factor + np.random.normal(0, 3)
        temp = np.clip(temp, 5, 35)
        
        # pH relativamente estable
        ph = np.random.normal(7.2, 0.6)
        ph = np.clip(ph, 6.0, 9.0)
        
        # Conductividad con variabilidad
        conductivity = np.random.lognormal(5.5, 0.7)
        conductivity = np.clip(conductivity, 50, 2000)
        
        # Oxígeno disuelto (inversamente relacionado con temperatura)
        oxygen_base = 95 - (temp - 15) * 2
        oxygen = oxygen_base + np.random.normal(0, 10)
        oxygen = np.clip(oxygen, 30, 120)
        
        # Turbiedad con eventos ocasionales altos
        if np.random.random() < 0.05:  # 5% de eventos de alta turbiedad
            turbidity = np.random.lognormal(3, 1)
        else:
            turbidity = np.random.lognormal(0.5, 0.8)
        turbidity = np.clip(turbidity, 0.1, 100)
        
        # Sólidos suspendidos correlacionados con turbiedad
        solids = turbidity * np.random.uniform(0.8, 2.0) + np.random.normal(5, 2)
        solids = np.clip(solids, 1, 200)
        
        record = {
            'COD_ESTACION': np.random.randint(1000000, 9999999),
            'GLS_ESTACION': station,
            'FEC_MEDICION': date,
            'año': date.year,
            'mes': date.month,
            'mes_nombre': date.strftime('%B'),
            'Temperatura Temperatura muestra °C': round(temp, 1),
            'Ph a 25°C': round(ph, 2),
            'Conductividad Específica (µS/cm a 25°C)': round(conductivity, 0),
            'Oxigeno Disuelto (% Saturacion)': round(oxygen, 1),
            'Turbiedad (NTU)': round(turbidity, 2),
            'Solidos Suspendidos Totales ': round(solids, 1)
        }
        
        data.append(record)
    
    df = pd.DataFrame(data)
    return df

def calculate_water_quality_index(df, parameters):
    """Calcula un índice simplificado de calidad del agua"""
    
    if df.empty or not parameters:
        return df
    
    scores = []
    
    for param in parameters:
        if param in df.columns and param in WATER_QUALITY_PARAMETERS:
            values = df[param].copy()
            optimal_min, optimal_max = WATER_QUALITY_PARAMETERS[param]['optimal_range']
            
            # Calcular score (0-100) basado en proximidad al rango óptimo
            score = np.where(
                (values >= optimal_min) & (values <= optimal_max),
                100,  # Óptimo
                np.where(
                    values < optimal_min,
                    100 * (values / optimal_min),  # Por debajo del óptimo
                    100 * (optimal_max / values)   # Por encima del óptimo
                )
            )
            
            score = np.clip(score, 0, 100)
            scores.append(score)
    
    if scores:
        df['indice_calidad'] = np.nanmean(scores, axis=0)
        df['categoria_calidad'] = pd.cut(
            df['indice_calidad'],
            bins=[0, 25, 50, 75, 100],
            labels=['Deficiente', 'Regular', 'Buena', 'Excelente'],
            include_lowest=True
        )
    
    return df

def get_water_quality_summary_statistics(df, parameters):
    """Calcula estadísticas resumidas para parámetros de calidad del agua"""
    
    stats = {}
    
    for param in parameters:
        if param in df.columns:
            param_data = df[param].dropna()
            
            if len(param_data) > 0:
                param_info = WATER_QUALITY_PARAMETERS.get(param, {})
                optimal_range = param_info.get('optimal_range', (0, 100))
                  # Estadísticas básicas
                stats[param] = {
                    'count': len(param_data),
                    'mean': param_data.mean(),
                    'std': param_data.std(),
                    'median': param_data.median(),
                    'min': param_data.min(),
                    'max': param_data.max(),
                    'unit': param_info.get('unit', ''),
                    'name': param_info.get('name', param),
                    'min': param_data.min(),
                    'max': param_data.max(),
                    'median': param_data.median(),
                    'q25': param_data.quantile(0.25),
                    'q75': param_data.quantile(0.75)
                }
                
                # Porcentaje en rango óptimo
                in_optimal = param_data[(param_data >= optimal_range[0]) & 
                                      (param_data <= optimal_range[1])]
                stats[param]['percent_optimal'] = (len(in_optimal) / len(param_data)) * 100
                
                # Clasificación por calidad
                if param in QUALITY_CLASSIFICATION:
                    classification = QUALITY_CLASSIFICATION[param]
                    for quality_level, (min_val, max_val) in classification.items():
                        in_range = param_data[(param_data >= min_val) & (param_data <= max_val)]
                        stats[param][f'percent_{quality_level.lower()}'] = (len(in_range) / len(param_data)) * 100
    
    return stats

def filter_water_data(df, filters):
    """Filtra datos de calidad del agua basado en criterios"""
    
    if df is None or df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Filtro por años
    if 'year_range' in filters and 'año' in filtered_df.columns:
        min_year, max_year = filters['year_range']
        filtered_df = filtered_df[
            (filtered_df['año'] >= min_year) & 
            (filtered_df['año'] <= max_year)
        ]
    
    # Filtro por estaciones
    if 'stations' in filters and filters['stations'] and 'GLS_ESTACION' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['GLS_ESTACION'].isin(filters['stations'])]
    
    # Filtro por rango de valores para parámetros específicos
    if 'parameter_ranges' in filters:
        for param, (min_val, max_val) in filters['parameter_ranges'].items():
            if param in filtered_df.columns:
                filtered_df = filtered_df[
                    (filtered_df[param] >= min_val) & 
                    (filtered_df[param] <= max_val)
                ]
    
    return filtered_df
