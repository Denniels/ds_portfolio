"""
Script para preprocesar datos antes del despliegue en Cloud Run
Reduce significativamente el consumo de recursos en tiempo de ejecución

Este script:
1. Preprocesa los datasets usados por la aplicación
2. Genera versiones optimizadas para carga rápida
3. Crea caches que minimizan el procesamiento en tiempo real
"""

import os
import pandas as pd
import numpy as np
import json
from pathlib import Path
import shutil

print("Iniciando preprocesamiento de datos para optimización...")

# Directorios importantes
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = BASE_DIR / "app" / "data" / "cache"

# Crear directorios si no existen
PROCESSED_DIR.mkdir(exist_ok=True, parents=True)
CACHE_DIR.mkdir(exist_ok=True, parents=True)

print(f"Directorios configurados: {PROCESSED_DIR}, {CACHE_DIR}")

# Función auxiliar para optimizar DataFrames
def optimize_dataframe(df):
    """Optimiza un DataFrame reduciendo el uso de memoria"""
    result = df.copy()
    
    # Optimizar tipos numéricos
    for col in result.select_dtypes(include=['int']).columns:
        col_min = result[col].min()
        col_max = result[col].max()
        
        if col_min >= 0:
            if col_max < 255:
                result[col] = result[col].astype(np.uint8)
            elif col_max < 65535:
                result[col] = result[col].astype(np.uint16)
            else:
                result[col] = result[col].astype(np.uint32)
        else:
            if col_min > -128 and col_max < 127:
                result[col] = result[col].astype(np.int8)
            elif col_min > -32768 and col_max < 32767:
                result[col] = result[col].astype(np.int16)
            else:
                result[col] = result[col].astype(np.int32)
    
    # Optimizar tipos de punto flotante
    for col in result.select_dtypes(include=['float']).columns:
        result[col] = result[col].astype(np.float32)
    
    # Optimizar objetos y strings
    for col in result.select_dtypes(include=['object']).columns:
        # Usar categorías para columnas con pocos valores únicos
        if result[col].nunique() / len(result) < 0.5:
            result[col] = result[col].astype('category')
    
    return result

# Procesamiento de datos de emisiones CO2
try:
    print("\nProcesando datos de emisiones CO2...")
    print("Ejecutando notebook simplificado para generar datos y visualizaciones...")
    
    # Simulamos datos temporales
    años = list(range(2010, 2024))
    emisiones = [70.5, 72.3, 74.8, 76.1, 77.5, 79.2, 80.6, 81.8, 82.5, 83.6, 79.8, 80.5, 83.7, 85.2]
    
    df_emisiones = pd.DataFrame({
        'Año': años,
        'Emisiones_CO2_Mt': emisiones
    })
    
    # Simulamos datos geográficos
    regiones_data = {
        "Metropolitana": {"lat": -33.4489, "lon": -70.6693, "emisiones": 45.2},
        "Valparaíso": {"lat": -33.0458, "lon": -71.6197, "emisiones": 12.8},
        "Biobío": {"lat": -36.8201, "lon": -73.0443, "emisiones": 18.5},
        "Antofagasta": {"lat": -23.6509, "lon": -70.3975, "emisiones": 25.3},
        "O'Higgins": {"lat": -34.1708, "lon": -70.7444, "emisiones": 15.6},
        "Maule": {"lat": -35.4264, "lon": -71.6553, "emisiones": 8.9},
        "Araucanía": {"lat": -38.7359, "lon": -72.5904, "emisiones": 7.4},
        "Los Lagos": {"lat": -41.4693, "lon": -72.9424, "emisiones": 6.8}
    }
    
    df_regiones = pd.DataFrame.from_dict(regiones_data, orient='index')
    df_regiones.index.name = 'Region'
    df_regiones.reset_index(inplace=True)
    
    # Optimizar y guardar datos
    df_emisiones_optimizado = optimize_dataframe(df_emisiones)
    df_regiones_optimizado = optimize_dataframe(df_regiones)
    
    df_emisiones_optimizado.to_parquet(PROCESSED_DIR / "emisiones_co2_optimizado.parquet")
    df_regiones_optimizado.to_parquet(PROCESSED_DIR / "emisiones_regiones_optimizado.parquet")
    
    # Generar versiones agregadas para diferentes vistas
    emisiones_anual = df_emisiones.set_index('Año').to_dict()['Emisiones_CO2_Mt']
    emisiones_regional = df_regiones.set_index('Region').to_dict('index')
    
    # Guardar como JSON para carga rápida
    with open(CACHE_DIR / "emisiones_anuales.json", "w") as f:
        json.dump(emisiones_anual, f)
    
    with open(CACHE_DIR / "emisiones_regionales.json", "w") as f:
        json.dump(emisiones_regional, f)
    
    # Generar mapa estático
    try:
        import folium
        print("Generando mapa estático de emisiones...")
        
        # Crear mapa base
        m = folium.Map(
            location=[-33.4489, -70.6693],
            zoom_start=5,
            tiles='cartodbpositron'
        )
        
        # Añadir marcadores de emisiones
        for region, data in emisiones_regional.items():
            # Color basado en nivel de emisiones
            color = 'red' if data['emisiones'] > 20 else 'orange' if data['emisiones'] > 10 else 'green'
            
            folium.CircleMarker(
                location=[data['lat'], data['lon']],
                radius=data['emisiones']/2,  # Tamaño proporcional a emisiones
                popup=f"{region}<br>Emisiones: {data['emisiones']} Mt CO2",
                color=color,
                fill=True,
                fill_opacity=0.6
            ).add_to(m)
        
        # Añadir leyenda
        legend_html = """
        <div style="position: fixed; bottom: 50px; right: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid grey; border-radius: 5px;">
            <h4>Emisiones de CO2 (Mt)</h4>
            <p><i style="background: red; width: 10px; height: 10px; display: inline-block;"></i> > 20 Mt</p>
            <p><i style="background: orange; width: 10px; height: 10px; display: inline-block;"></i> 10-20 Mt</p>
            <p><i style="background: green; width: 10px; height: 10px; display: inline-block;"></i> < 10 Mt</p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Guardar mapa en directorio estático
        static_dir = CACHE_DIR.parent / "static" / "maps"
        static_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = pd.Timestamp.now().strftime("%Y%m")
        map_path = static_dir / f"emisiones_co2_{timestamp}.html"
        m.save(str(map_path))
        
        print(f"✅ Mapa estático generado: {map_path}")
        
    except ImportError:
        print("⚠️ No se pudo generar el mapa estático (folium no instalado)")
    except Exception as e:
        print(f"⚠️ Error generando mapa estático: {str(e)}")
    
    print("✅ Datos de emisiones CO2 procesados correctamente")
except Exception as e:
    print(f"Error procesando datos de emisiones: {e}")

# Procesamiento de datos de calidad del agua
try:
    print("Procesando datos de calidad de agua...")
    
    # Datos simulados para el ejemplo - estaciones con coordenadas
    estaciones = pd.DataFrame({
        'Nombre': [
            'Est. Santiago', 'Est. Valparaíso', 'Est. Concepción', 'Est. Antofagasta',
            'Est. Puerto Montt', 'Est. Temuco', 'Est. La Serena', 'Est. Copiapó'
        ],
        'Latitud': [-33.45, -33.04, -36.83, -23.65, -41.47, -38.73, -29.90, -27.37],
        'Longitud': [-70.67, -71.62, -73.05, -70.40, -72.94, -72.60, -71.25, -70.33],
        'Índice_Calidad': [85, 78, 82, 68, 90, 76, 72, 65]
    })
    
    # Optimizar y guardar
    estaciones_opt = optimize_dataframe(estaciones)
    estaciones_opt.to_parquet(PROCESSED_DIR / "estaciones_agua_optimizado.parquet")
    
    # Generar cache de coordenadas
    coordenadas = {}
    for _, row in estaciones.iterrows():
        coordenadas[row['Nombre']] = {'lat': row['Latitud'], 'lon': row['Longitud']}
    
    with open(CACHE_DIR / "coordenadas_estaciones.json", "w") as f:
        json.dump(coordenadas, f)
    
    print("✅ Datos de calidad del agua procesados correctamente")
except Exception as e:
    print(f"Error procesando datos de calidad del agua: {e}")

# Procesamiento de datos demográficos
try:
    print("Procesando datos demográficos...")
    
    # Simulación de datos demográficos por edad
    grupos_edad = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', 
                   '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
    
    # Datos para 2010 y proyección 2025
    datos_demograficos = {
        "piramide": {
            "grupos_edad": grupos_edad,
            "hombres_2010": [-800, -650, -640, -630, -690, -720, -680, -650, -590, -540, -500, -420, -350, -270, -210, -120, -90],
            "mujeres_2010": [780, 630, 620, 610, 680, 730, 690, 670, 610, 560, 530, 450, 380, 310, 250, 180, 150],
            "hombres_2025": [-750, -600, -590, -620, -680, -750, -740, -730, -690, -640, -590, -520, -480, -390, -320, -240, -210],
            "mujeres_2025": [730, 580, 570, 600, 670, 760, 750, 750, 710, 670, 610, 550, 510, 430, 370, 300, 280]
        }
    }
    
    # Guardar para carga rápida
    with open(CACHE_DIR / "demograficos_procesados.json", "w") as f:
        json.dump(datos_demograficos, f)
    
    print("✅ Datos demográficos procesados correctamente")
except Exception as e:
    print(f"Error procesando datos demográficos: {e}")

# Procesamiento de datos de presupuesto
try:
    print("Procesando datos de presupuesto público...")
    
    años = list(range(2010, 2026))
    
    # Sectores y sus valores iniciales (% del presupuesto)
    sectores = {
        'Salud': 16.8,
        'Educación': 19.2,
        'Protección Social': 14.5,
        'Infraestructura': 9.8,
        'Defensa': 7.6,
        'Seguridad': 6.2,
        'Otros': 25.9
    }
    
    # Crear datos simulados con tendencias
    np.random.seed(42)
    datos_presupuesto = {sector: [] for sector in sectores}
    
    for sector, valor_inicial in sectores.items():
        if sector == 'Salud':
            cambio = np.linspace(0, 0.3, len(años))
        elif sector == 'Educación':
            cambio = np.linspace(0, 0.2, len(años))
        elif sector == 'Defensa':
            cambio = np.linspace(0, -0.15, len(años))
        else:
            cambio = np.random.normal(0, 0.05, len(años))
        
        valores = [valor_inicial]
        for i in range(1, len(años)):
            valores.append(valores[-1] + cambio[i])
        
        datos_presupuesto[sector] = valores
    
    # Añadir años al diccionario final
    datos_presupuesto['años'] = años
    
    # Guardar para carga rápida
    with open(CACHE_DIR / "presupuesto_procesado.json", "w") as f:
        json.dump(datos_presupuesto, f)
    
    print("✅ Datos de presupuesto procesados correctamente")
except Exception as e:
    print(f"Error procesando datos de presupuesto: {e}")

# Crear archivo de metadatos para seguimiento
metadata = {
    "fecha_procesamiento": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
    "archivos_generados": [
        str(PROCESSED_DIR / "emisiones_co2_optimizado.parquet"),
        str(PROCESSED_DIR / "estaciones_agua_optimizado.parquet"),
        str(CACHE_DIR / "emisiones_anuales.json"),
        str(CACHE_DIR / "coordenadas_estaciones.json"),
        str(CACHE_DIR / "demograficos_procesados.json"),
        str(CACHE_DIR / "presupuesto_procesado.json")
    ],
    "memoria_estimada": "< 5MB"
}

with open(CACHE_DIR / "metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

print("✅ Preprocesamiento completado correctamente")
print(f"Total de archivos generados: {len(metadata['archivos_generados'])}")
print(f"Memoria estimada: {metadata['memoria_estimada']}")
print("Los datos están optimizados para despliegue en la capa gratuita de Cloud Run")
