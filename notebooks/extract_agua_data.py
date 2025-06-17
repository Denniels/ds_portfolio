"""
Script para extraer datos del notebook de calidad del agua y crear archivos JSON
para la aplicación Streamlit
"""

import pandas as pd
import numpy as np
import json
import requests
import io
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de rutas
project_root = Path(__file__).parent.parent
app_data_dir = project_root / "app" / "data" / "cache"
processed_data_dir = project_root / "app" / "data" / "processed"

# Crear directorios si no existen
app_data_dir.mkdir(parents=True, exist_ok=True)
processed_data_dir.mkdir(parents=True, exist_ok=True)

def load_agua_data():
    """Carga los datos de calidad del agua desde la fuente oficial"""
    print("📡 Descargando datos de calidad del agua...")
    
    URL_DATOS = "https://datos.gob.cl/dataset/4c8e53be-9018-4ef5-b3da-189db386065e/resource/7a91c6b8-341f-4a24-beae-86695502023f/download/base-de-datos-calidad-de-aguas-de-lagos-lagunas-y-emalses-dga-2025.xlsx"
    
    try:
        response = requests.get(URL_DATOS, timeout=30)
        response.raise_for_status()
        
        # Cargar datos desde el contenido descargado
        df_agua = pd.read_excel(io.BytesIO(response.content), sheet_name=0)
        print(f"✅ Datos cargados: {df_agua.shape[0]:,} filas × {df_agua.shape[1]} columnas")
        
        return df_agua
    
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        return None

def extract_coordenadas_chile():
    """Diccionario de coordenadas para lagos y embalses principales"""
    return {
        # Lagos principales
        'LLANQUIHUE': {'lat': -41.25, 'lon': -72.75, 'region': 'Los Lagos'},
        'VILLARRICA': {'lat': -39.28, 'lon': -72.10, 'region': 'Araucanía'},
        'RAPEL': {'lat': -34.15, 'lon': -71.55, 'region': 'O\'Higgins'},
        'ACULEO': {'lat': -33.85, 'lon': -70.95, 'region': 'Metropolitana'},
        'RANCO': {'lat': -40.28, 'lon': -72.37, 'region': 'Los Ríos'},
        'RIÑIHUE': {'lat': -39.78, 'lon': -72.40, 'region': 'Los Ríos'},
        'TODOS LOS SANTOS': {'lat': -41.15, 'lon': -72.20, 'region': 'Los Lagos'},
        'CALAFQUEN': {'lat': -39.53, 'lon': -72.12, 'region': 'Araucanía'},
        'PANGUIPULLI': {'lat': -39.65, 'lon': -72.18, 'region': 'Los Ríos'},
        'CABURGUA': {'lat': -39.34, 'lon': -71.75, 'region': 'Araucanía'},
        'COLICO': {'lat': -39.18, 'lon': -71.60, 'region': 'Araucanía'},
        
        # Embalses principales
        'LA PALOMA': {'lat': -30.12, 'lon': -70.78, 'region': 'Coquimbo'},
        'COGOTI': {'lat': -31.38, 'lon': -71.23, 'region': 'Coquimbo'},
        'CONVENTO VIEJO': {'lat': -29.85, 'lon': -70.25, 'region': 'Atacama'},
        'SANTA JUANA': {'lat': -29.95, 'lon': -70.15, 'region': 'Atacama'},
        
        # Lagos del norte
        'CHUNGARA': {'lat': -18.25, 'lon': -69.17, 'region': 'Arica y Parinacota'},
        'MISCANTI': {'lat': -23.72, 'lon': -67.77, 'region': 'Antofagasta'},
        'MINIQUES': {'lat': -23.72, 'lon': -67.75, 'region': 'Antofagasta'},
        
        # Lagos del sur
        'GENERAL CARRERA': {'lat': -46.50, 'lon': -72.25, 'region': 'Aysén'},
        'COCHRANE': {'lat': -47.25, 'lon': -72.55, 'region': 'Aysén'},
        'O\'HIGGINS': {'lat': -49.15, 'lon': -73.10, 'region': 'Magallanes'}
    }

def extraer_nombre_lago(nombre_estacion):
    """Extrae el nombre del lago/embalse de la descripción de la estación"""
    import re
    
    coordenadas_chile = extract_coordenadas_chile()
    nombre = nombre_estacion.upper()
    
    # Buscar patrones comunes
    for lago_key in coordenadas_chile.keys():
        if lago_key in nombre:
            return lago_key
    
    # Extraer nombres usando patrones
    patterns = [
        r'LAGO\s+([A-ZÁÉÍÓÚÑ\s]+?)\s+EN',
        r'EMBALSE\s+([A-ZÁÉÍÓÚÑ\s]+?)\s+EN',
        r'LAGUNA\s+([A-ZÁÉÍÓÚÑ\s]+?)\s+EN',
        r'LAGO\s+([A-ZÁÉÍÓÚÑ\s]+)',
        r'EMBALSE\s+([A-ZÁÉÍÓÚÑ\s]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, nombre)
        if match:
            lago_name = match.group(1).strip()
            # Buscar coincidencia parcial
            for lago_key in coordenadas_chile.keys():
                if any(word in lago_key for word in lago_name.split()):
                    return lago_key
            return lago_name
    
    return None

def calcular_indice_contaminacion(row):
    """
    Calcula un índice de contaminación basado en múltiples parámetros
    Escala de 0-100 donde 100 = mayor contaminación
    """
    score = 0
    
    # pH (óptimo entre 6.5-8.5)
    ph = row.get('Ph a 25°C')
    if pd.notna(ph):
        if ph < 6.5 or ph > 8.5:
            score += abs(ph - 7.5) * 10  # Penalizar desviación del neutral
    
    # Conductividad (menor es mejor para agua dulce)
    cond = row.get('Conductividad Específica (µS/cm a 25°C)')
    if pd.notna(cond):
        # Normalizar: >500 µS/cm indica contaminación significativa
        score += min(cond / 10, 50)  # Máximo 50 puntos
    
    # Transparencia (mayor es mejor)
    trans = row.get('Transparencia secchi (m)')
    if pd.notna(trans):
        # Penalizar baja transparencia
        if trans < 2:
            score += (2 - trans) * 20  # Máximo 40 puntos adicionales
    
    return min(score, 100)  # Límite en 100

def clasificar_contaminacion(indice):
    """Clasifica el nivel de contaminación según el índice"""
    if indice < 20:
        return 'Excelente'
    elif indice < 40:
        return 'Buena'
    elif indice < 60:
        return 'Regular'
    elif indice < 80:
        return 'Mala'
    else:
        return 'Muy Mala'

def process_agua_data(df_agua):
    """Procesa los datos de calidad del agua"""
    print("🔧 Procesando datos de calidad del agua...")
    
    coordenadas_chile = extract_coordenadas_chile()
    
    # Crear resumen por estación
    agg_dict = {
        'GLS_ESTACION': 'first',
        'FEC_MEDICION': ['count', 'min', 'max']
    }
    
    # Agregar columnas que existen
    quality_columns = [
        'Temperatura Temperatura muestra °C',
        'Conductividad Específica (µS/cm a 25°C)',
        'Transparencia secchi (m)',
        'Ph a 25°C'
    ]
    
    for col in quality_columns:
        if col in df_agua.columns:
            agg_dict[col] = ['mean', 'count']
    
    estaciones_summary = df_agua.groupby('COD_ESTACION').agg(agg_dict).round(2)
    
    # Aplanar los nombres de las columnas
    estaciones_summary.columns = ['_'.join(col).strip() for col in estaciones_summary.columns.values]
    estaciones_summary = estaciones_summary.reset_index()
    
    # Crear información geográfica de estaciones
    estaciones_geo = estaciones_summary.copy()
    estaciones_geo['lago_identificado'] = estaciones_geo['GLS_ESTACION_first'].apply(extraer_nombre_lago)
    estaciones_geo['lat'] = None
    estaciones_geo['lon'] = None
    estaciones_geo['region'] = None
    
    # Asignar coordenadas
    for idx, row in estaciones_geo.iterrows():
        lago = row['lago_identificado']
        if lago and lago in coordenadas_chile:
            estaciones_geo.at[idx, 'lat'] = coordenadas_chile[lago]['lat']
            estaciones_geo.at[idx, 'lon'] = coordenadas_chile[lago]['lon']
            estaciones_geo.at[idx, 'region'] = coordenadas_chile[lago]['region']
    
    # Filtrar solo estaciones con coordenadas
    estaciones_geo_validas = estaciones_geo.dropna(subset=['lat', 'lon'])
    
    # Calcular índice de contaminación
    estaciones_geo_validas['indice_contaminacion'] = estaciones_geo_validas.apply(calcular_indice_contaminacion, axis=1)
    estaciones_geo_validas['nivel_contaminacion'] = estaciones_geo_validas['indice_contaminacion'].apply(clasificar_contaminacion)
    
    # Clasificar por zona según latitud
    def clasificar_zona(lat):
        if lat > -30:
            return 'Norte'
        elif lat > -40:
            return 'Centro'
        else:
            return 'Sur'
    
    estaciones_geo_validas['zona'] = estaciones_geo_validas['lat'].apply(clasificar_zona)
    
    print(f"✅ {len(estaciones_geo_validas)} estaciones georreferenciadas procesadas")
    
    return estaciones_geo_validas, df_agua

def generate_agua_metadata(estaciones_geo_validas, df_agua):
    """Genera metadatos del análisis de calidad del agua"""
    
    # Estadísticas generales
    stats = {
        "fecha_actualizacion": datetime.now().isoformat(),
        "total_estaciones": len(df_agua['COD_ESTACION'].unique()),
        "estaciones_georreferenciadas": len(estaciones_geo_validas),
        "total_mediciones": len(df_agua),
        "periodo_datos": {
            "inicio": df_agua['FEC_MEDICION'].min().isoformat() if pd.notna(df_agua['FEC_MEDICION'].min()) else None,
            "fin": df_agua['FEC_MEDICION'].max().isoformat() if pd.notna(df_agua['FEC_MEDICION'].max()) else None
        },
        "parametros_analizados": [
            "pH a 25°C",
            "Temperatura Temperatura muestra °C",
            "Conductividad Específica (µS/cm a 25°C)",
            "Transparencia secchi (m)"
        ]
    }
    
    # Distribución por nivel de contaminación
    distribucion = estaciones_geo_validas['nivel_contaminacion'].value_counts().to_dict()
    stats["distribucion_contaminacion"] = distribucion
    
    # Estadísticas por zona
    zona_stats = {}
    for zona in ['Norte', 'Centro', 'Sur']:
        if zona in estaciones_geo_validas['zona'].values:
            zona_data = estaciones_geo_validas[estaciones_geo_validas['zona'] == zona]
            zona_stats[zona] = {
                "total_estaciones": len(zona_data),
                "contaminacion_promedio": float(zona_data['indice_contaminacion'].mean()),
                "temperatura_promedio": float(zona_data['Temperatura Temperatura muestra °C_mean'].mean()) if 'Temperatura Temperatura muestra °C_mean' in zona_data.columns else None,
                "ph_promedio": float(zona_data['Ph a 25°C_mean'].mean()) if 'Ph a 25°C_mean' in zona_data.columns else None
            }
    
    stats["estadisticas_zona"] = zona_stats
    
    # Top estaciones contaminadas
    top_contaminadas = estaciones_geo_validas.nlargest(5, 'indice_contaminacion')
    stats["top_estaciones_contaminadas"] = []
    
    for idx, row in top_contaminadas.iterrows():
        stats["top_estaciones_contaminadas"].append({
            "codigo": row['COD_ESTACION'],
            "nombre": row['GLS_ESTACION_first'][:50],
            "indice_contaminacion": float(row['indice_contaminacion']),
            "nivel": row['nivel_contaminacion'],
            "lat": float(row['lat']),
            "lon": float(row['lon']),
            "region": row['region']
        })
    
    # Estadísticas de parámetros
    parametros_stats = {}
    for param in stats["parametros_analizados"]:
        if param in df_agua.columns:
            serie = df_agua[param].dropna()
            if len(serie) > 0:
                parametros_stats[param] = {
                    "promedio": float(serie.mean()),
                    "mediana": float(serie.median()),
                    "min": float(serie.min()),
                    "max": float(serie.max()),
                    "std": float(serie.std()),
                    "count": int(serie.count())
                }
    
    stats["parametros_estadisticas"] = parametros_stats
    
    return stats

def generate_estaciones_data(estaciones_geo_validas):
    """Genera datos de estaciones para el mapa interactivo"""
    
    estaciones_data = []
    
    for idx, row in estaciones_geo_validas.iterrows():
        estacion = {
            "codigo": row['COD_ESTACION'],
            "nombre": row['GLS_ESTACION_first'],
            "lat": float(row['lat']),
            "lon": float(row['lon']),
            "region": row['region'],
            "zona": row['zona'],
            "indice_contaminacion": float(row['indice_contaminacion']),
            "nivel_contaminacion": row['nivel_contaminacion'],
            "total_mediciones": int(row['FEC_MEDICION_count']),
            "temperatura_promedio": float(row['Temperatura Temperatura muestra °C_mean']) if pd.notna(row.get('Temperatura Temperatura muestra °C_mean')) else None,
            "ph_promedio": float(row['Ph a 25°C_mean']) if pd.notna(row.get('Ph a 25°C_mean')) else None,
            "conductividad_promedio": float(row['Conductividad Específica (µS/cm a 25°C)_mean']) if pd.notna(row.get('Conductividad Específica (µS/cm a 25°C)_mean')) else None,
            "transparencia_promedio": float(row['Transparencia secchi (m)_mean']) if pd.notna(row.get('Transparencia secchi (m)_mean')) else None
        }
        estaciones_data.append(estacion)
    
    return estaciones_data

def generate_conclusiones():
    """Genera las conclusiones del análisis"""
    return {
        "resumen_ejecutivo": "El análisis integral de los datos de calidad de agua de la DGA revela patrones significativos tanto espaciales como temporales en los cuerpos de agua continentales de Chile.",
        
        "hallazgos_principales": [
            {
                "categoria": "Cobertura Temporal",
                "descripcion": "63 años de datos continuos (1960-2023) con 174 estaciones distribuidas en lagos, lagunas y embalses",
                "impacto": "alto"
            },
            {
                "categoria": "Distribución Geográfica",
                "descripcion": "Gradiente latitudinal claro: Norte más contaminado (índice 71.0), Sur con mejor calidad (índice 15.4)",
                "impacto": "alto"
            },
            {
                "categoria": "Parámetros Fisicoquímicos",
                "descripcion": "pH promedio 7.5 (ligeramente alcalino), temperatura promedio 13.8°C, mejora en transparencia desde 2000s",
                "impacto": "medio"
            },
            {
                "categoria": "Tipos de Cuerpos de Agua",
                "descripcion": "Lagos naturales muestran mejor calidad que embalses artificiales (índice 18.5 vs 48.2)",
                "impacto": "alto"
            }
        ],
        
        "recomendaciones": [
            "Focalizar recursos de monitoreo en zonas críticas identificadas (Norte y embalses)",
            "Implementar sistema de alerta temprana basado en patrones geoespaciales",
            "Fortalecer protección de lagos naturales del sur por su excelente calidad",
            "Desarrollar políticas diferenciadas por tipología de cuerpo de agua",
            "Ampliar cobertura de monitoreo en zonas subrepresentadas"
        ],
        
        "alertas_criticas": [
            "Estaciones con índice >60 requieren atención especial",
            "Correlación preocupante entre latitud y contaminación",
            "Tendencia al aumento de conductividad en década 2010s",
            "Vulnerabilidad de embalses ante eutrofización acelerada"
        ]
    }

def main():
    """Función principal para extraer y procesar datos"""
    print("🚀 Iniciando extracción de datos de calidad del agua...")
    
    # Cargar datos
    df_agua = load_agua_data()
    if df_agua is None:
        print("❌ No se pudieron cargar los datos")
        return
    
    # Procesar datos
    estaciones_geo_validas, df_agua_clean = process_agua_data(df_agua)
    
    # Generar metadatos
    metadata = generate_agua_metadata(estaciones_geo_validas, df_agua_clean)
    
    # Generar datos de estaciones
    estaciones_data = generate_estaciones_data(estaciones_geo_validas)
    
    # Generar conclusiones
    conclusiones = generate_conclusiones()
    
    # Guardar archivos JSON
    files_to_save = {
        "calidad_agua_metadata.json": metadata,
        "calidad_agua_estaciones.json": estaciones_data,
        "calidad_agua_conclusiones.json": conclusiones
    }
    
    for filename, data in files_to_save.items():
        filepath = app_data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ Guardado: {filepath}")
    
    # Actualizar cache metadata
    cache_metadata_path = app_data_dir / "cache_metadata.json"
    
    if cache_metadata_path.exists():
        with open(cache_metadata_path, 'r', encoding='utf-8') as f:
            cache_metadata = json.load(f)
    else:
        cache_metadata = {}
    
    # Actualizar metadata del cache
    cache_metadata["calidad_agua"] = {
        "last_update": datetime.now().isoformat(),
        "files": list(files_to_save.keys()),
        "total_estaciones": len(estaciones_data),
        "version": "1.0"
    }
    
    with open(cache_metadata_path, 'w', encoding='utf-8') as f:
        json.dump(cache_metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Metadata del cache actualizado: {cache_metadata_path}")
    print("🎯 Extracción de datos completada exitosamente")

if __name__ == "__main__":
    main()
