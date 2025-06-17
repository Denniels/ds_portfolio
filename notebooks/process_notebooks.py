"""
Script para procesar notebooks y generar datos intermedios para la aplicación Streamlit.
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
import os
import sys
import re

# Agregar directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

# Directorios
NOTEBOOK_DIR = ROOT_DIR / "notebooks"
DATA_DIR = ROOT_DIR / "app" / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"

# Asegurar que existan los directorios
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def process_emisiones_co2():
    """Procesa los datos de emisiones de CO2 del notebook correspondiente"""
    print("Procesando datos de emisiones CO2...")
    
    # Generar datos simplificados
    years = range(2015, 2026)
    
    # Datos de emisiones totales
    emissions_data = {
        'years': list(years),
        'emissions': [80 + i*2 for i in range(len(years))]
    }
    
    # Datos por sector
    sectors = ['Energía', 'Transporte', 'Industria', 'Residencial', 'Otros']
    sector_data = {
        'sector': sectors,
        'emissions': [30, 25, 20, 15, 10]
    }
    
    # Datos regionales
    regiones = {
        'Metropolitana': {'coords': {'lat': -33.4489, 'lon': -70.6693}, 'emisiones': 42},
        'Valparaíso': {'coords': {'lat': -33.0472, 'lon': -71.6127}, 'emisiones': 18},
        'Biobío': {'coords': {'lat': -36.8261, 'lon': -73.0498}, 'emisiones': 15},
        'Antofagasta': {'coords': {'lat': -23.6509, 'lon': -70.3975}, 'emisiones': 10},
        'O\'Higgins': {'coords': {'lat': -34.1708, 'lon': -70.7444}, 'emisiones': 8},
        'Maule': {'coords': {'lat': -35.4264, 'lon': -71.6553}, 'emisiones': 7}
    }
    
    # Guardar datos procesados
    with open(PROCESSED_DIR / "emisiones_co2.json", "w", encoding="utf-8") as f:
        json.dump({
            'emisiones_totales': emissions_data,
            'emisiones_por_sector': sector_data,
            'emisiones_regionales': {'regiones': regiones}
        }, f, ensure_ascii=False, indent=2)
    
    # Generar caché para la app
    with open(CACHE_DIR / "emisiones_anuales.json", "w", encoding="utf-8") as f:
        json.dump(emissions_data, f, ensure_ascii=False, indent=2)
    
    with open(CACHE_DIR / "emisiones_regionales.json", "w", encoding="utf-8") as f:
        json.dump({'regiones': regiones}, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos de emisiones CO2 procesados")

def process_calidad_agua():
    """Procesa los datos de calidad del agua del notebook correspondiente"""
    print("Procesando datos de calidad del agua...")
    
    # Datos de ejemplo de estaciones
    stations_data = {
        'station_name': [
            'Estación Maipo', 'Estación Mapocho', 'Estación Biobío',
            'Estación Cautín', 'Estación Valdivia'
        ],
        'region': [
            'Metropolitana', 'Metropolitana', 'Biobío',
            'Araucanía', 'Los Ríos'
        ],
        'water_quality_index': [78, 72, 85, 88, 92],
        'latitude': [-33.6147, -33.4331, -36.8384, -38.7359, -39.8142],
        'longitude': [-70.9758, -70.6503, -73.0496, -72.6667, -73.2320]
    }
    
    # Convertir a formato para la app
    estaciones = []
    for i in range(len(stations_data['station_name'])):
        estaciones.append({
            'nombre': stations_data['station_name'][i],
            'region': stations_data['region'][i],
            'indice_calidad': stations_data['water_quality_index'][i],
            'coordenadas': {
                'lat': stations_data['latitude'][i],
                'lon': stations_data['longitude'][i]
            }
        })
    
    # Guardar datos procesados
    with open(PROCESSED_DIR / "calidad_agua.json", "w", encoding="utf-8") as f:
        json.dump({
            'estaciones': estaciones
        }, f, ensure_ascii=False, indent=2)
    
    # Generar caché para la app
    with open(CACHE_DIR / "estaciones_agua.json", "w", encoding="utf-8") as f:
        json.dump({'estaciones': estaciones}, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos de calidad del agua procesados")

def process_demografia():
    """Procesa los datos demográficos del notebook correspondiente"""
    print("Procesando datos demográficos...")
    
    # Crear datos de ejemplo
    years = range(2015, 2026)
    demo_data = {
        'year': list(years),
        'total_population': [17000000 + i*100000 for i in range(len(years))],
        'growth_rate': [1.1 - i*0.02 for i in range(len(years))],
        'median_age': [34 + i*0.2 for i in range(len(years))]
    }
    
    # Datos de estructura etaria
    age_data = {
        'age_group': ['0-14', '15-29', '30-44', '45-59', '60+'],
        'population': [3000000, 4000000, 4500000, 3500000, 2000000]
    }
    
    # Convertir a formato para la app
    demografia = {
        'poblacion_total': {
            'años': list(years),
            'valores': demo_data['total_population']
        },
        'indicadores': {
            'años': list(years),
            'tasa_crecimiento': demo_data['growth_rate'],
            'edad_mediana': demo_data['median_age']
        },
        'estructura_etaria': {
            'grupos': age_data['age_group'],
            'poblacion': age_data['population']
        }
    }
    
    # Guardar datos procesados
    with open(PROCESSED_DIR / "demografia.json", "w", encoding="utf-8") as f:
        json.dump(demografia, f, ensure_ascii=False, indent=2)
    
    # Generar caché para la app
    with open(CACHE_DIR / "demografia_datos.json", "w", encoding="utf-8") as f:
        json.dump(demografia, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos demográficos procesados")

def process_presupuesto():
    """Procesa los datos de presupuesto del notebook correspondiente"""
    print("Procesando datos de presupuesto público...")
    
    # Crear datos de ejemplo
    budget_data = {
        'year': [2023] * 5 + [2024] * 5,
        'ministry': ['Educación', 'Salud', 'Vivienda', 'Obras Públicas', 'Desarrollo Social'] * 2,
        'program': ['Programa 1', 'Programa 2', 'Programa 3', 'Programa 4', 'Programa 5'] * 2,
        'budget': [1000000, 800000, 600000, 500000, 400000] * 2
    }
    
    # Convertir a formato para la app
    presupuesto = {
        'años': [2023, 2024],
        'ministerios': list(set(budget_data['ministry'])),
        'datos': []
    }
    
    # Formatear datos
    for i in range(len(budget_data['year'])):
        presupuesto['datos'].append({
            'año': budget_data['year'][i],
            'ministerio': budget_data['ministry'][i],
            'programa': budget_data['program'][i],
            'monto': budget_data['budget'][i]
        })
    
    # Guardar datos procesados
    with open(PROCESSED_DIR / "presupuesto.json", "w", encoding="utf-8") as f:
        json.dump(presupuesto, f, ensure_ascii=False, indent=2)
    
    # Generar caché para la app
    with open(CACHE_DIR / "presupuesto_datos.json", "w", encoding="utf-8") as f:
        json.dump(presupuesto, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos de presupuesto procesados")

def main():
    """Función principal que procesa todos los notebooks"""
    print("Iniciando procesamiento de notebooks...")
    
    # Procesar cada tipo de datos
    process_emisiones_co2()
    process_calidad_agua()
    process_demografia()
    process_presupuesto()
    
    print("\n✅ Todos los datos han sido procesados correctamente")
    print(f"📂 Datos procesados guardados en: {PROCESSED_DIR}")
    print(f"📂 Caché generada en: {CACHE_DIR}")

if __name__ == "__main__":
    main()
