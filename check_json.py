import json
from pathlib import Path

# Ruta del archivo
path = Path('./app/data/cache/emisiones_regionales.json')

print(f'Archivo existe: {path.exists()}')
if path.exists():
    # Cargar datos
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        print(f'Número de regiones: {len(data)}')
        
        # Mostrar la primera región
        if data:
            primera_region = list(data.keys())[0]
            print(f'Primera región: {primera_region}')
            print(f'Datos de la primera región: {data[primera_region]}')
        else:
            print('Archivo de datos vacío')
    except Exception as e:
        print(f'Error al cargar el archivo: {str(e)}')
