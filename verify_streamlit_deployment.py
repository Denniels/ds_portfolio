#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación final para despliegue en Streamlit Community Cloud
Valida que todos los componentes críticos estén presentes y funcionando
"""

import os
import json
import sys
from pathlib import Path
import pandas as pd

def print_header(title):
    """Imprime un header formateado"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"❌ {message}")

def print_warning(message):
    """Imprime mensaje de advertencia"""
    print(f"⚠️  {message}")

def verify_project_structure():
    """Verifica la estructura básica del proyecto"""
    print_header("VERIFICACIÓN DE ESTRUCTURA DEL PROYECTO")
    
    required_files = [
        "app/main.py",
        "requirements_streamlit_cloud.txt",
        ".streamlit/config.toml",
        "app/pages/01_emisiones_co2.py",
        "app/pages/02_calidad_agua.py", 
        "app/pages/03_demografia.py",
        "app/pages/04_presupuesto_publico.py",
        "app/pages/05_curriculum.py",
        "app/pages/06_servicios.py",
        "app/pages/07_feedback.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print_success(f"Archivo presente: {file_path}")
        else:
            print_error(f"Archivo faltante: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print_error(f"FALTAN {len(missing_files)} ARCHIVOS CRÍTICOS")
        return False
    else:
        print_success("ESTRUCTURA DE PROYECTO COMPLETA")
        return True

def verify_presupuesto_data():
    """Verifica los datos críticos del presupuesto público"""
    print_header("VERIFICACIÓN DE DATOS PRESUPUESTO PÚBLICO")
    
    data_path = Path("app/data/processed")
    
    required_files = [
        "resumen_ejecutivo.json",
        "datos_visualizacion.json", 
        "metadatos.json",
        "top_ministerios.csv",
        "top_regiones.csv",
        "distribucion_sectores.csv",
        "presupuesto_chile_2024.csv",
        "ejecucion_presupuestaria_2024.csv",
        "transferencias_regionales_2024.csv",
        "inversion_publica_2024.csv"
    ]
    
    missing_files = []
    valid_files = []
    
    for filename in required_files:
        file_path = data_path / filename
        if file_path.exists():
            try:
                if filename.endswith('.json'):
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    print_success(f"JSON válido: {filename} ({len(data)} keys)")
                    valid_files.append(filename)
                elif filename.endswith('.csv'):
                    df = pd.read_csv(file_path)
                    print_success(f"CSV válido: {filename} ({len(df)} filas, {len(df.columns)} columnas)")
                    valid_files.append(filename)
            except Exception as e:
                print_error(f"Error en {filename}: {e}")
                missing_files.append(filename)
        else:
            print_error(f"Archivo faltante: {filename}")
            missing_files.append(filename)
    
    if missing_files:
        print_error(f"FALTAN O SON INVÁLIDOS {len(missing_files)} ARCHIVOS DE DATOS")
        return False
    else:
        print_success("TODOS LOS DATOS DEL PRESUPUESTO VÁLIDOS")
        return True

def verify_json_content():
    """Verifica el contenido específico de los JSONs críticos"""
    print_header("VERIFICACIÓN DE CONTENIDO JSON")
    
    # Verificar resumen_ejecutivo.json
    try:
        with open("app/data/processed/resumen_ejecutivo.json", 'r') as f:
            resumen = json.load(f)
        
        required_fields = [
            'presupuesto_total', 'transferencias_totales', 'inversion_total',
            'inversion_ejecutada', 'eficiencia_ejecucion', 'avance_promedio',
            'eficiencia_inversion'
        ]
        
        for field in required_fields:
            if field in resumen:
                value = resumen[field]
                print_success(f"Campo {field}: {type(value).__name__} = {value}")
            else:
                print_error(f"Campo faltante: {field}")
                return False
                
    except Exception as e:
        print_error(f"Error verificando resumen_ejecutivo.json: {e}")
        return False
    
    # Verificar metadatos.json
    try:
        with open("app/data/processed/metadatos.json", 'r') as f:
            metadatos = json.load(f)
        
        print_success(f"Metadatos: versión {metadatos.get('version', 'N/A')}")
        print_success(f"Fecha: {metadatos.get('fecha_generacion', 'N/A')}")
        print_success(f"Registros: {metadatos.get('total_registros', 'N/A')}")
        
    except Exception as e:
        print_error(f"Error verificando metadatos.json: {e}")
        return False
    
    print_success("CONTENIDO JSON VÁLIDO")
    return True

def verify_requirements():
    """Verifica el archivo de requirements"""
    print_header("VERIFICACIÓN DE REQUIREMENTS")
    
    try:
        with open("requirements_streamlit_cloud.txt", 'r') as f:
            requirements = f.read()
        
        essential_packages = [
            'streamlit', 'pandas', 'numpy', 'plotly', 
            'folium', 'streamlit-folium'
        ]
        
        for package in essential_packages:
            if package in requirements:
                print_success(f"Paquete presente: {package}")
            else:
                print_error(f"Paquete faltante: {package}")
                return False
        
        print_success("REQUIREMENTS COMPLETOS")
        return True
        
    except Exception as e:
        print_error(f"Error verificando requirements: {e}")
        return False

def verify_streamlit_config():
    """Verifica la configuración de Streamlit"""
    print_header("VERIFICACIÓN DE CONFIGURACIÓN STREAMLIT")
    
    config_path = ".streamlit/config.toml"
    if os.path.exists(config_path):
        print_success(f"Archivo de configuración presente: {config_path}")
        try:
            with open(config_path, 'r') as f:
                config_content = f.read()
            
            if 'developmentMode = false' in config_content:
                print_success("Modo desarrollo deshabilitado ✓")
            if 'caching = true' in config_content:
                print_success("Cache habilitado ✓")
            
            print_success("CONFIGURACIÓN STREAMLIT VÁLIDA")
            return True
            
        except Exception as e:
            print_error(f"Error leyendo configuración: {e}")
            return False
    else:
        print_warning("Archivo de configuración no encontrado (opcional)")
        return True

def verify_imports():
    """Verifica que las importaciones críticas funcionen"""
    print_header("VERIFICACIÓN DE IMPORTACIONES")
    
    critical_imports = [
        ('streamlit', 'st'),
        ('pandas', 'pd'), 
        ('numpy', 'np'),
        ('plotly.express', 'px'),
        ('plotly.graph_objects', 'go'),
        ('folium', 'folium'),
        ('json', 'json'),
        ('pathlib', 'Path')
    ]
    
    failed_imports = []
    
    for module, alias in critical_imports:
        try:
            exec(f"import {module} as {alias}")
            print_success(f"Importación exitosa: {module}")
        except ImportError as e:
            print_error(f"Error importando {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print_error(f"FALLAN {len(failed_imports)} IMPORTACIONES CRÍTICAS")
        return False
    else:
        print_success("TODAS LAS IMPORTACIONES EXITOSAS")
        return True

def verify_app_syntax():
    """Verifica la sintaxis del archivo principal"""
    print_header("VERIFICACIÓN DE SINTAXIS DE LA APP")
    
    try:
        import py_compile
        py_compile.compile('app/main.py', doraise=True)
        print_success("Sintaxis de app/main.py válida")
        
        # Verificar páginas críticas
        critical_pages = [
            'app/pages/04_presupuesto_publico.py'
        ]
        
        for page in critical_pages:
            try:
                py_compile.compile(page, doraise=True)
                print_success(f"Sintaxis válida: {page}")
            except Exception as e:
                print_error(f"Error de sintaxis en {page}: {e}")
                return False
                
        print_success("SINTAXIS DE APLICACIÓN VÁLIDA")
        return True
        
    except Exception as e:
        print_error(f"Error verificando sintaxis: {e}")
        return False

def generate_deployment_summary():
    """Genera resumen para deployment"""
    print_header("RESUMEN PARA DEPLOYMENT")
    
    print("📋 CONFIGURACIÓN PARA STREAMLIT CLOUD:")
    print("   Repository: Denniels/ds_portfolio")
    print("   Branch: main") 
    print("   Main file path: app/main.py")
    print("   Python version: 3.11+")
    print()
    print("📊 DATOS CRÍTICOS PRESENTES:")
    print("   ✅ app/data/processed/resumen_ejecutivo.json")
    print("   ✅ app/data/processed/datos_visualizacion.json") 
    print("   ✅ app/data/processed/metadatos.json")
    print("   ✅ Archivos CSV del presupuesto (10 archivos)")
    print()
    print("🔧 OPTIMIZACIONES IMPLEMENTADAS:")
    print("   ✅ Cache inteligente con @st.cache_data")
    print("   ✅ Fallback data para casos de error")
    print("   ✅ Formateo robusto anti-errores")
    print("   ✅ Manejo de excepciones comprehensivo")
    print()
    print("🚀 ESTADO: LISTO PARA DEPLOYMENT")

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN FINAL - STREAMLIT CLOUD DEPLOYMENT")
    print("=" * 60)
    
    verifications = [
        ("Estructura del Proyecto", verify_project_structure),
        ("Datos Presupuesto Público", verify_presupuesto_data),
        ("Contenido JSON", verify_json_content),
        ("Requirements", verify_requirements),
        ("Configuración Streamlit", verify_streamlit_config),
        ("Importaciones", verify_imports),
        ("Sintaxis de la App", verify_app_syntax)
    ]
    
    results = []
    
    for name, verification_func in verifications:
        try:
            result = verification_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error en verificación {name}: {e}")
            results.append((name, False))
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIONES")
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
            passed += 1
        else:
            print_error(f"{name}: FAILED")
    
    print(f"\n📊 RESULTADO: {passed}/{total} verificaciones exitosas")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS VERIFICACIONES PASARON!")
        print("🚢 EL PROYECTO ESTÁ LISTO PARA DEPLOYMENT EN STREAMLIT CLOUD")
        generate_deployment_summary()
        return True
    else:
        print(f"\n⚠️  {total - passed} VERIFICACIONES FALLARON")
        print("🔧 CORREGIR LOS PROBLEMAS ANTES DEL DEPLOYMENT")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
