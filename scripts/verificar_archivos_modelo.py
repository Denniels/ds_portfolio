"""
Script para verificar la consistencia de archivos de modelo inmobiliario 
y generar directrices para el despliegue en Streamlit Cloud
"""
import os
import sys
import json
import shutil
from pathlib import Path
import datetime

# Definir rutas posibles para los archivos del modelo
MODEL_PATHS = [
    "app/data/inmobiliario/modelo_inmobiliario.pkl",
    "app/data/modelos/modelo_inmobiliario.pkl",
    "app/models/modelo_inmobiliario.pkl",
]

SCALER_PATHS = [
    "app/data/inmobiliario/scaler_inmobiliario.pkl",
    "app/data/modelos/scaler_inmobiliario.pkl",
    "app/models/scaler_inmobiliario.pkl",
]

INFO_PATHS = [
    "app/data/inmobiliario/model_info.json",
    "app/data/modelos/model_info.json",
    "app/models/model_info.json",
]

def check_file_exists(file_path):
    """Verificar si el archivo existe y retornar información sobre el mismo"""
    path = Path(file_path)
    if path.exists():
        stat = path.stat()
        return {
            "exists": True,
            "size": stat.st_size,
            "last_modified": datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "path": str(path.absolute())
        }
    else:
        return {
            "exists": False,
            "size": 0,
            "last_modified": "N/A",
            "path": str(path.absolute())
        }

def create_directories_if_not_exist(file_paths):
    """Crear directorios si no existen para las rutas de archivos dadas"""
    for file_path in file_paths:
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            print(f"Creando directorio: {directory}")
            os.makedirs(directory, exist_ok=True)

def copy_file_to_all_locations(source_path, target_paths):
    """Copiar archivo a todas las ubicaciones especificadas"""
    if not os.path.exists(source_path):
        print(f"Error: Archivo fuente no encontrado: {source_path}")
        return False
    
    # Crear directorios si no existen
    create_directories_if_not_exist(target_paths)
    
    # Copiar archivo a todas las ubicaciones
    for target_path in target_paths:
        try:
            shutil.copy2(source_path, target_path)
            print(f"Archivo copiado: {source_path} -> {target_path}")
        except Exception as e:
            print(f"Error al copiar a {target_path}: {str(e)}")
    
    return True

def main():
    print("Verificando consistencia de archivos de modelo inmobiliario...")
    
    # Verificar archivos de modelo
    print("\nArchivos de modelo:")
    model_files = [check_file_exists(path) for path in MODEL_PATHS]
    for i, file_info in enumerate(model_files):
        status = "✅" if file_info["exists"] else "❌"
        print(f"{status} {MODEL_PATHS[i]}")
        if file_info["exists"]:
            print(f"   - Tamaño: {file_info['size']} bytes")
            print(f"   - Modificado: {file_info['last_modified']}")
    
    # Verificar archivos de scaler
    print("\nArchivos de scaler:")
    scaler_files = [check_file_exists(path) for path in SCALER_PATHS]
    for i, file_info in enumerate(scaler_files):
        status = "✅" if file_info["exists"] else "❌"
        print(f"{status} {SCALER_PATHS[i]}")
        if file_info["exists"]:
            print(f"   - Tamaño: {file_info['size']} bytes")
            print(f"   - Modificado: {file_info['last_modified']}")
    
    # Verificar archivos de información
    print("\nArchivos de información:")
    info_files = [check_file_exists(path) for path in INFO_PATHS]
    for i, file_info in enumerate(info_files):
        status = "✅" if file_info["exists"] else "❌"
        print(f"{status} {INFO_PATHS[i]}")
        if file_info["exists"]:
            print(f"   - Tamaño: {file_info['size']} bytes")
            print(f"   - Modificado: {file_info['last_modified']}")
    
    # Determinar si hay archivos faltantes
    missing_model = not any(file_info["exists"] for file_info in model_files)
    missing_scaler = not any(file_info["exists"] for file_info in scaler_files)
    missing_info = not any(file_info["exists"] for file_info in info_files)
    
    # Encontrar archivos existentes para copiar
    existing_model_path = next((file_info["path"] for file_info in model_files if file_info["exists"]), None)
    existing_scaler_path = next((file_info["path"] for file_info in scaler_files if file_info["exists"]), None)
    existing_info_path = next((file_info["path"] for file_info in info_files if file_info["exists"]), None)
    
    # Determinar acciones a realizar
    print("\n===== DIAGNÓSTICO =====")
    if missing_model or missing_scaler or missing_info:
        print("❌ Se detectaron archivos faltantes.")
        
        if missing_model and existing_model_path:
            print(f"   - Modelo encontrado en: {existing_model_path}")
            print("     Se requiere copiar a las demás ubicaciones.")
        elif missing_model:
            print("   - No se encontró el archivo del modelo en ninguna ubicación.")
        
        if missing_scaler and existing_scaler_path:
            print(f"   - Scaler encontrado en: {existing_scaler_path}")
            print("     Se requiere copiar a las demás ubicaciones.")
        elif missing_scaler:
            print("   - No se encontró el archivo del scaler en ninguna ubicación.")
        
        if missing_info and existing_info_path:
            print(f"   - Información encontrada en: {existing_info_path}")
            print("     Se requiere copiar a las demás ubicaciones.")
        elif missing_info:
            print("   - No se encontró el archivo de información en ninguna ubicación.")
        
        # Preguntar si desea copiar archivos
        while True:
            response = input("\n¿Desea copiar los archivos existentes a todas las ubicaciones? (s/n): ").lower()
            if response in ['s', 'n']:
                break
        
        if response == 's':
            print("\nCopiando archivos...")
            
            if existing_model_path:
                print("\nCopiando modelo:")
                copy_file_to_all_locations(existing_model_path, MODEL_PATHS)
            
            if existing_scaler_path:
                print("\nCopiando scaler:")
                copy_file_to_all_locations(existing_scaler_path, SCALER_PATHS)
            
            if existing_info_path:
                print("\nCopiando información:")
                copy_file_to_all_locations(existing_info_path, INFO_PATHS)
            
            print("\nOperación completada.")
        else:
            print("\nOperación cancelada.")
    else:
        print("✅ Todos los archivos necesarios están presentes.")
    
    # Verificar contenido de model_info.json si existe
    print("\n===== VERIFICACIÓN DE COMPATIBILIDAD =====")
    info_content = None
    if existing_info_path:
        try:
            with open(existing_info_path, 'r', encoding='utf-8') as f:
                info_content = json.load(f)
                
            print(f"Información del modelo:")
            if 'version' in info_content:
                print(f"   - scikit-learn: {info_content['version'].get('scikit-learn', 'No especificado')}")
                print(f"   - numpy: {info_content['version'].get('numpy', 'No especificado')}")
                print(f"   - pandas: {info_content['version'].get('pandas', 'No especificado')}")
                print(f"   - joblib: {info_content['version'].get('joblib', 'No especificado')}")
            
            if 'feature_names' in info_content:
                print(f"   - Número de características: {len(info_content['feature_names'])}")
                print(f"   - Características: {', '.join(info_content['feature_names'][:5])}...")
            
            print(f"   - Fecha de creación: {info_content.get('created_at', 'No especificado')}")
        except Exception as e:
            print(f"Error al leer el archivo de información: {str(e)}")
    else:
        print("No se pudo verificar la compatibilidad porque no se encontró el archivo de información.")
    
    # Generar informe con recomendaciones
    print("\n===== RECOMENDACIONES PARA STREAMLIT CLOUD =====")
    print("1. Asegúrese de que todos los archivos del modelo estén rastreados por git y se suban al repositorio.")
    print("2. Verifique que las versiones de las bibliotecas en requirements.txt sean compatibles con las utilizadas para crear el modelo.")
    print("3. Añada logging adicional en la aplicación para verificar que los archivos se encuentran correctamente en producción.")
    print("4. En el predictor inmobiliario, utilice el modo de depuración añadiendo '?debug=true' a la URL.")
    print("5. Verifique que las características utilizadas para la predicción coincidan exactamente con las esperadas por el modelo.")
    print("6. Considere regenerar el modelo con las mismas versiones de bibliotecas que utiliza Streamlit Cloud.")
    
    print("\n===== RESUMEN =====")
    if missing_model or missing_scaler or missing_info:
        print("❌ El modelo inmobiliario NO está correctamente configurado. Siga las instrucciones anteriores.")
    else:
        print("✅ El modelo inmobiliario está correctamente configurado. Si hay problemas en Streamlit Cloud,")
        print("   utilice el modo de depuración para obtener más información.")
    
    print("\nFin del diagnóstico.")

if __name__ == "__main__":
    main()
