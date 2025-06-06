from google.cloud import storage
import pandas as pd
from pathlib import Path
import os

def upload_to_gcs():
    """Subir datos a Google Cloud Storage"""
    
    # Configurar cliente
    storage_client = storage.Client()
    
    # Nombre del bucket
    bucket_name = "emisiones-co2-data"
    
    # Crear bucket si no existe
    bucket = storage_client.bucket(bucket_name)
    if not bucket.exists():
        bucket = storage_client.create_bucket(bucket_name)
    
    # Ruta del archivo local
    data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "retc_emisiones_aire_2023.csv"
    
    # Cargar y procesar datos
    df = pd.read_csv(data_path)
    
    # Crear diferentes vistas de los datos
    data_views = {
        "summary": df.describe().to_json(),
        "by_region": df.groupby('region')['cantidad_toneladas'].agg(['sum', 'mean', 'count']).to_json(),
        "top_emitters": df.nlargest(50, 'cantidad_toneladas')[
            ['razon_social', 'region', 'cantidad_toneladas']
        ].to_json(),
        "geographical": df[['latitud', 'longitud', 'cantidad_toneladas', 'razon_social', 'region']].to_json()
    }
    
    # Subir cada vista a GCS
    for view_name, data in data_views.items():
        blob = bucket.blob(f"processed/{view_name}.json")
        blob.upload_from_string(data)
        
    print("✅ Datos subidos exitosamente a GCS")
