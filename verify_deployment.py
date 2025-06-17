"""
Script de verificación pre-despliegue para calidad del agua
Verifica que todos los archivos y dependencias estén correctos
"""

import json
import sys
from pathlib import Path

def verify_json_files():
    """Verifica la integridad de los archivos JSON"""
    print("🔍 Verificando archivos JSON...")
    
    cache_dir = Path("app/data/cache")
    required_files = [
        "calidad_agua_metadata.json",
        "calidad_agua_estaciones.json", 
        "calidad_agua_conclusiones.json"
    ]
    
    all_valid = True
    
    for filename in required_files:
        filepath = cache_dir / filename
        
        if not filepath.exists():
            print(f"❌ Archivo faltante: {filepath}")
            all_valid = False
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_size = filepath.stat().st_size
            print(f"✅ {filename}: {file_size:,} bytes, válido")
            
            # Verificaciones específicas por archivo
            if filename == "calidad_agua_metadata.json":
                required_keys = ['total_estaciones', 'estaciones_georreferenciadas', 'total_mediciones']
                for key in required_keys:
                    if key not in data:
                        print(f"⚠️  Clave faltante en metadata: {key}")
                        
            elif filename == "calidad_agua_estaciones.json":
                if not isinstance(data, list) or len(data) == 0:
                    print(f"❌ {filename} debe ser una lista no vacía")
                    all_valid = False
                else:
                    # Verificar estructura de primera estación
                    estacion = data[0]
                    required_keys = ['codigo', 'nombre', 'lat', 'lon', 'indice_contaminacion']
                    for key in required_keys:
                        if key not in estacion:
                            print(f"⚠️  Clave faltante en estación: {key}")
                            
        except json.JSONDecodeError as e:
            print(f"❌ Error JSON en {filename}: {e}")
            all_valid = False
        except Exception as e:
            print(f"❌ Error al verificar {filename}: {e}")
            all_valid = False
    
    return all_valid

def verify_streamlit_imports():
    """Verifica que las importaciones de Streamlit funcionen"""
    print("\n📦 Verificando importaciones...")
    
    try:
        import streamlit as st
        print("✅ Streamlit importado correctamente")
    except ImportError:
        print("❌ Error: Streamlit no está instalado")
        return False
    
    try:
        import folium
        print("✅ Folium importado correctamente")
    except ImportError:
        print("❌ Error: Folium no está instalado")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas importado correctamente")
    except ImportError:
        print("❌ Error: Pandas no está instalado")
        return False
    
    return True

def verify_page_structure():
    """Verifica que la página de Streamlit tenga la estructura correcta"""
    print("\n🏗️ Verificando estructura de la página...")
    
    page_file = Path("app/pages/02_calidad_agua.py")
    
    if not page_file.exists():
        print(f"❌ Archivo de página faltante: {page_file}")
        return False
    
    try:
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar elementos clave
        checks = [
            ("st.set_page_config", "Configuración de página"),
            ("load_agua_data", "Función de carga de datos"),
            ("folium.Map", "Mapa interactivo"),
            ("st.tabs", "Pestañas de navegación")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}: encontrado")
            else:
                print(f"⚠️  {description}: no encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar página: {e}")
        return False

def verify_data_consistency():
    """Verifica la consistencia entre los datos"""
    print("\n🔗 Verificando consistencia de datos...")
    
    try:
        # Cargar metadata
        with open("app/data/cache/calidad_agua_metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Cargar estaciones
        with open("app/data/cache/calidad_agua_estaciones.json", 'r', encoding='utf-8') as f:
            estaciones = json.load(f)
        
        # Verificar consistencia
        metadata_count = metadata.get('estaciones_georreferenciadas', 0)
        actual_count = len(estaciones)
        
        if metadata_count == actual_count:
            print(f"✅ Consistencia de conteo: {actual_count} estaciones")
        else:
            print(f"⚠️  Inconsistencia: metadata dice {metadata_count}, archivo tiene {actual_count}")
        
        # Verificar distribución de contaminación
        dist_metadata = metadata.get('distribucion_contaminacion', {})
        total_metadata = sum(dist_metadata.values())
        
        if total_metadata == actual_count:
            print(f"✅ Distribución consistente: {total_metadata} estaciones categorizadas")
        else:
            print(f"⚠️  Distribución inconsistente: suma {total_metadata}, esperado {actual_count}")
        
        # Verificar que hay variedad en los índices
        indices = [est['indice_contaminacion'] for est in estaciones]
        min_indice = min(indices)
        max_indice = max(indices)
        
        if max_indice > min_indice and max_indice > 0:
            print(f"✅ Variedad en índices: {min_indice:.1f} - {max_indice:.1f}")
        else:
            print(f"⚠️  Índices sin variedad o todos en cero")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar consistencia: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("="*60)
    print("🚀 VERIFICACIÓN PRE-DESPLIEGUE - CALIDAD DEL AGUA")
    print("="*60)
    
    checks = [
        ("Archivos JSON", verify_json_files),
        ("Importaciones", verify_streamlit_imports),
        ("Estructura de página", verify_page_structure),
        ("Consistencia de datos", verify_data_consistency)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        print(f"\n{'='*40}")
        print(f"🔍 {check_name}")
        print(f"{'='*40}")
        
        try:
            result = check_func()
            results.append(result)
            
            if result:
                print(f"✅ {check_name}: CORRECTO")
            else:
                print(f"❌ {check_name}: FALLÓ")
                
        except Exception as e:
            print(f"❌ Error en {check_name}: {e}")
            results.append(False)
    
    # Resumen final
    print(f"\n{'='*60}")
    print("📋 RESUMEN DE VERIFICACIÓN")
    print(f"{'='*60}")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("✅ El proyecto está listo para despliegue en Streamlit Cloud")
        print("\n🚀 Pasos siguientes:")
        print("   1. git commit -m 'Pipeline calidad agua completado'")
        print("   2. git push origin main")
        print("   3. Desplegar en Streamlit Cloud")
        return True
    else:
        print(f"⚠️  {passed}/{total} verificaciones pasaron")
        print("❌ Corrija los errores antes de desplegar")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
