#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificación final de archivos críticos para Streamlit Cloud
Confirma que todos los archivos necesarios están incluidos en git
"""

import subprocess
import sys
from pathlib import Path

def run_git_command(command):
    """Ejecuta comando git y retorna la salida"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip().split('\n') if result.stdout.strip() else []
    except Exception as e:
        print(f"Error ejecutando comando git: {e}")
        return []

def verify_critical_files():
    """Verifica que todos los archivos críticos estén en git"""
    print("🔍 VERIFICACIÓN FINAL - ARCHIVOS CRÍTICOS EN GIT")
    print("=" * 60)
    
    # Archivos críticos que DEBEN estar en el repositorio
    critical_files = [
        "app/main.py",
        "requirements_streamlit_cloud.txt",
        ".streamlit/config.toml",
        "app/data/processed/resumen_ejecutivo.json",
        "app/data/processed/datos_visualizacion.json", 
        "app/data/processed/metadatos.json",
        "app/data/processed/top_ministerios.csv",
        "app/data/processed/top_regiones.csv",
        "app/data/processed/distribucion_sectores.csv",
        "app/data/processed/presupuesto_chile_2024.csv",
        "app/data/processed/ejecucion_presupuestaria_2024.csv",
        "app/data/processed/transferencias_regionales_2024.csv",
        "app/data/processed/inversion_publica_2024.csv"
    ]
    
    # Obtener lista de archivos trackeados por git
    tracked_files = run_git_command("git ls-files")
    
    print("\n📋 VERIFICACIÓN DE ARCHIVOS CRÍTICOS:")
    
    missing_files = []
    present_files = []
    
    for file_path in critical_files:
        if file_path in tracked_files:
            print(f"✅ {file_path}")
            present_files.append(file_path)
        else:
            print(f"❌ {file_path} - NO ENCONTRADO EN GIT")
            missing_files.append(file_path)
    
    print(f"\n📊 RESUMEN:")
    print(f"✅ Archivos presentes: {len(present_files)}/{len(critical_files)}")
    print(f"❌ Archivos faltantes: {len(missing_files)}")
    
    if missing_files:
        print(f"\n🚨 ARCHIVOS FALTANTES CRÍTICOS:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print(f"\n⚠️  ESTOS ARCHIVOS SON NECESARIOS PARA STREAMLIT CLOUD")
        return False
    else:
        print(f"\n🎉 TODOS LOS ARCHIVOS CRÍTICOS ESTÁN PRESENTES")
        return True

def verify_gitignore():
    """Verifica que el .gitignore incluya las excepciones correctas"""
    print("\n" + "=" * 60)
    print("🔍 VERIFICACIÓN DEL .GITIGNORE")
    print("=" * 60)
    
    try:
        with open('.gitignore', 'r') as f:
            gitignore_content = f.read()
        
        required_exceptions = [
            '!app/data/processed/resumen_ejecutivo.json',
            '!app/data/processed/datos_visualizacion.json',
            '!app/data/processed/metadatos.json'
        ]
        
        print("\n📋 VERIFICACIÓN DE EXCEPCIONES JSON:")
        
        all_present = True
        for exception in required_exceptions:
            if exception in gitignore_content:
                print(f"✅ {exception}")
            else:
                print(f"❌ {exception} - NO ENCONTRADO")
                all_present = False
        
        if all_present:
            print(f"\n✅ TODAS LAS EXCEPCIONES JSON ESTÁN CONFIGURADAS")
            return True
        else:
            print(f"\n❌ FALTAN EXCEPCIONES EN .GITIGNORE")
            return False
            
    except Exception as e:
        print(f"❌ Error leyendo .gitignore: {e}")
        return False

def verify_file_sizes():
    """Verifica que los archivos no sean demasiado grandes para git"""
    print("\n" + "=" * 60)
    print("🔍 VERIFICACIÓN DE TAMAÑOS DE ARCHIVO")
    print("=" * 60)
    
    max_size_mb = 100  # Límite de 100MB para GitHub
    large_files = []
    
    critical_files = [
        "app/data/processed/resumen_ejecutivo.json",
        "app/data/processed/datos_visualizacion.json", 
        "app/data/processed/metadatos.json",
        "app/data/processed/presupuesto_chile_2024.csv",
        "app/data/processed/ejecucion_presupuestaria_2024.csv",
        "app/data/processed/transferencias_regionales_2024.csv",
        "app/data/processed/inversion_publica_2024.csv"
    ]
    
    print("\n📏 TAMAÑOS DE ARCHIVOS CRÍTICOS:")
    
    for file_path in critical_files:
        if Path(file_path).exists():
            size_bytes = Path(file_path).stat().st_size
            size_mb = size_bytes / (1024 * 1024)
            
            if size_mb > max_size_mb:
                print(f"⚠️  {file_path}: {size_mb:.2f} MB (DEMASIADO GRANDE)")
                large_files.append(file_path)
            else:
                print(f"✅ {file_path}: {size_mb:.2f} MB")
        else:
            print(f"❌ {file_path}: NO EXISTE")
    
    if large_files:
        print(f"\n⚠️  ARCHIVOS DEMASIADO GRANDES PARA GITHUB:")
        for file_path in large_files:
            print(f"   - {file_path}")
        return False
    else:
        print(f"\n✅ TODOS LOS ARCHIVOS TIENEN TAMAÑO APROPIADO")
        return True

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN FINAL PARA STREAMLIT CLOUD DEPLOYMENT")
    print("Confirmando que todos los archivos críticos estén incluidos en git")
    
    results = []
    
    # Verificaciones
    results.append(("Archivos Críticos", verify_critical_files()))
    results.append(("Configuración .gitignore", verify_gitignore()))
    results.append(("Tamaños de Archivo", verify_file_sizes()))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for name, result in results:
        if result:
            print(f"✅ {name}: PASSED")
            passed += 1
        else:
            print(f"❌ {name}: FAILED")
    
    print(f"\n📈 RESULTADO: {passed}/{total} verificaciones exitosas")
    
    if passed == total:
        print("\n🎉 ¡REPOSITORIO LISTO PARA STREAMLIT CLOUD!")
        print("🚢 Todos los archivos críticos están incluidos en git")
        print("📁 Los datos del presupuesto público estarán disponibles en deployment")
        return True
    else:
        print(f"\n⚠️  {total - passed} VERIFICACIONES FALLARON")
        print("🔧 CORREGIR ANTES DEL DEPLOYMENT")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
