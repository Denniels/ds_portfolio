import sys
sys.path.append('./app')
from utils.streamlit_cloud_data import StreamlitCloudDataManager
from pathlib import Path

def process_regional_data_for_visualization(emisiones_regionales):
    """Procesar datos regionales para visualización"""
    import pandas as pd
    if not emisiones_regionales:
        return pd.DataFrame()
    
    # Convertir a DataFrame para facilitar el manejo
    data_list = []
    for region, data in emisiones_regionales.items():
        data_list.append({
            'Region': region,
            'lat': data['lat'],
            'lon': data['lon'],
            'emisiones': data['emisiones'],
            'emisiones_mt': round(data['emisiones'] / 1000000, 2)  # Convertir a mega toneladas
        })
    
    return pd.DataFrame(data_list)

# Crear gestor
manager = StreamlitCloudDataManager()

# Cargar datos
print("Cargando datos...")
data = manager.load_co2_data()

# Verificar datos regionales
print(f"Datos regionales vacíos: {not bool(data['emisiones_regionales'])}")
print(f"Número de regiones: {len(data['emisiones_regionales'])}")

# Convertir a DataFrame
df_regiones = process_regional_data_for_visualization(data['emisiones_regionales'])
print(f"DataFrame vacío: {df_regiones.empty}")
print(f"Número de filas en DataFrame: {len(df_regiones)}")

# Mostrar algunas filas
if not df_regiones.empty:
    print("\nPrimeras 3 filas del DataFrame:")
    print(df_regiones.head(3))
else:
    print("\nDataFrame está vacío. Verificando estructura de emisiones_regionales:")
    print(data['emisiones_regionales'])
