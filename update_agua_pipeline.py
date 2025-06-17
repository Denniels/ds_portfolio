"""
Script para actualizar datos del notebook a la aplicación Streamlit
Ejecuta el script de extracción y verifica la integridad de los datos
"""

import subprocess
import sys
from pathlib import Path
import json
from datetime import datetime

# Configuración de rutas
project_root = Path(__file__).parent
notebooks_dir = project_root / "notebooks"
app_data_dir = project_root / "app" / "data" / "cache"

def run_extraction_script():
    """Ejecuta el script de extracción de datos de calidad del agua"""
    print("🚀 Ejecutando script de extracción de datos...")
    
    script_path = notebooks_dir / "extract_agua_data.py"
    
    if not script_path.exists():
        print(f"❌ Script no encontrado: {script_path}")
        return False
    
    try:
        # Ejecutar el script de extracción
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(notebooks_dir),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos máximo
        )
        
        if result.returncode == 0:
            print("✅ Script de extracción ejecutado exitosamente")
            print(result.stdout)
            return True
        else:
            print("❌ Error en la ejecución del script:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: El script tardó más de 5 minutos en ejecutarse")
        return False
    except Exception as e:
        print(f"❌ Error al ejecutar script: {e}")
        return False

def verify_data_integrity():
    """Verifica la integridad de los datos generados"""
    print("🔍 Verificando integridad de los datos...")
    
    required_files = [
        "calidad_agua_metadata.json",
        "calidad_agua_estaciones.json", 
        "calidad_agua_conclusiones.json"
    ]
    
    missing_files = []
    corrupted_files = []
    
    for filename in required_files:
        filepath = app_data_dir / filename
        
        if not filepath.exists():
            missing_files.append(filename)
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Verificaciones específicas por archivo
            if filename == "calidad_agua_metadata.json":
                required_keys = ['fecha_actualizacion', 'total_estaciones', 'estaciones_georreferenciadas']
                for key in required_keys:
                    if key not in data:
                        corrupted_files.append(f"{filename} - missing key: {key}")
                        
            elif filename == "calidad_agua_estaciones.json":
                if not isinstance(data, list) or len(data) == 0:
                    corrupted_files.append(f"{filename} - invalid format or empty")
                    
            elif filename == "calidad_agua_conclusiones.json":
                required_keys = ['resumen_ejecutivo', 'hallazgos_principales', 'recomendaciones']
                for key in required_keys:
                    if key not in data:
                        corrupted_files.append(f"{filename} - missing key: {key}")
                        
        except json.JSONDecodeError:
            corrupted_files.append(f"{filename} - invalid JSON")
        except Exception as e:
            corrupted_files.append(f"{filename} - error: {e}")
    
    # Reportar resultados
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
    
    if corrupted_files:
        print("❌ Archivos corruptos o inválidos:")
        for file in corrupted_files:
            print(f"   - {file}")
    
    if not missing_files and not corrupted_files:
        print("✅ Todos los archivos están presentes y válidos")
        return True
    else:
        return False

def update_cache_metadata():
    """Actualiza los metadatos del cache"""
    print("📝 Actualizando metadatos del cache...")
    
    cache_metadata_path = app_data_dir / "cache_metadata.json"
    
    try:
        if cache_metadata_path.exists():
            with open(cache_metadata_path, 'r', encoding='utf-8') as f:
                cache_metadata = json.load(f)
        else:
            cache_metadata = {}
        
        # Actualizar metadata específico de calidad del agua
        cache_metadata["calidad_agua"] = {
            "last_update": datetime.now().isoformat(),
            "pipeline_version": "1.1",
            "status": "active",
            "files": [
                "calidad_agua_metadata.json",
                "calidad_agua_estaciones.json", 
                "calidad_agua_conclusiones.json"
            ]
        }
        
        # Guardar metadatos actualizados
        with open(cache_metadata_path, 'w', encoding='utf-8') as f:
            json.dump(cache_metadata, f, ensure_ascii=False, indent=2)
        
        print("✅ Metadatos del cache actualizados")
        return True
        
    except Exception as e:
        print(f"❌ Error al actualizar metadatos: {e}")
        return False

def show_data_summary():
    """Muestra un resumen de los datos procesados"""
    print("\n📊 Resumen de los datos procesados:")
    
    try:
        # Cargar metadata
        metadata_path = app_data_dir / "calidad_agua_metadata.json"
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Cargar datos de estaciones
        estaciones_path = app_data_dir / "calidad_agua_estaciones.json"
        with open(estaciones_path, 'r', encoding='utf-8') as f:
            estaciones = json.load(f)
        
        print(f"   📍 Total de estaciones: {metadata['total_estaciones']}")
        print(f"   🗺️ Estaciones georreferenciadas: {metadata['estaciones_georreferenciadas']}")
        print(f"   📊 Total de mediciones: {metadata['total_mediciones']:,}")
        print(f"   📅 Período: {metadata['periodo_datos']['inicio'][:4]} - {metadata['periodo_datos']['fin'][:4]}")
        print(f"   📋 Archivo de estaciones: {len(estaciones)} registros")
        
        # Distribución por región
        regiones = {}
        for estacion in estaciones:
            region = estacion.get('region', 'Sin definir')
            regiones[region] = regiones.get(region, 0) + 1
        
        print(f"   🌍 Distribución por región:")
        for region, count in sorted(regiones.items()):
            print(f"      - {region}: {count} estaciones")
            
    except Exception as e:
        print(f"❌ Error al mostrar resumen: {e}")

def main():
    """Función principal del pipeline"""
    print("="*60)
    print("🚀 PIPELINE DE ACTUALIZACIÓN DE DATOS - CALIDAD DEL AGUA")
    print("="*60)
    
    success = True
    
    # Paso 1: Ejecutar extracción
    if not run_extraction_script():
        print("❌ Fallo en la extracción de datos")
        success = False
    
    # Paso 2: Verificar integridad
    if success and not verify_data_integrity():
        print("❌ Fallo en la verificación de integridad")
        success = False
    
    # Paso 3: Actualizar metadatos
    if success and not update_cache_metadata():
        print("❌ Fallo en la actualización de metadatos")
        success = False
    
    # Paso 4: Mostrar resumen
    if success:
        show_data_summary()
        print("\n✅ Pipeline completado exitosamente")
        print("🎯 Los datos están listos para usar en Streamlit")
        print("📱 Ejecute la aplicación con: streamlit run app/main.py")
    else:
        print("\n❌ Pipeline completado con errores")
        print("🔧 Revise los logs anteriores para identificar problemas")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
