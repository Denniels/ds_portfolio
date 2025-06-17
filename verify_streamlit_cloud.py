#!/usr/bin/env python3
"""
Script de verificación para despliegue en Streamlit Community Cloud
Verifica que todos los componentes estén optimizados para la capa gratuita
"""

import os
import json
import sys
from pathlib import Path

def check_streamlit_cloud_readiness():
    """Verifica que la aplicación esté lista para Streamlit Cloud"""
    
    print("🔍 Verificando preparación para Streamlit Community Cloud...")
    print("=" * 60)
    
    issues = []
    successes = []
    
    # 1. Verificar estructura de archivos
    print("\n📁 Verificando estructura de archivos:")
    
    required_files = [
        'requirements_streamlit_cloud.txt',
        'app/main.py',
        '.streamlit/config.toml',
        'app/utils/streamlit_cloud_data.py'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            successes.append(f"✅ {file_path}")
            print(f"✅ {file_path}")
        else:
            issues.append(f"❌ Archivo faltante: {file_path}")
            print(f"❌ {file_path}")
    
    # 2. Verificar datos críticos
    print("\n📊 Verificando datos de CO2:")
    
    data_files = [
        'app/data/cache/emisiones_anuales.json',
        'app/data/cache/emisiones_regionales.json', 
        'app/data/cache/cache_metadata.json'
    ]
    
    for file_path in data_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            if size > 20:  # Archivo debe tener contenido meaningful
                successes.append(f"✅ {file_path} ({size} bytes)")
                print(f"✅ {file_path} ({size} bytes)")
            else:
                issues.append(f"⚠️ {file_path} muy pequeño ({size} bytes)")
                print(f"⚠️ {file_path} muy pequeño ({size} bytes)")
        else:
            issues.append(f"❌ Archivo de datos faltante: {file_path}")
            print(f"❌ {file_path}")
    
    # 3. Verificar requirements.txt
    print("\n📦 Verificando dependencias:")
    
    req_file = Path('requirements_streamlit_cloud.txt')
    if req_file.exists():
        with open(req_file, 'r') as f:
            requirements = f.read()
            
        required_packages = ['streamlit', 'pandas', 'plotly', 'folium']
        missing_packages = []
        
        for package in required_packages:
            if package in requirements:
                print(f"✅ {package}")
            else:
                missing_packages.append(package)
                print(f"❌ {package}")
        
        if missing_packages:
            issues.append(f"Paquetes faltantes en requirements: {missing_packages}")
    else:
        issues.append("❌ requirements_streamlit_cloud.txt no encontrado")
      # 4. Verificar .gitignore y archivos en Git
    print("\n🔧 Verificando Git:")
    
    if Path('.gitignore').exists():
        with open('.gitignore', 'r', encoding='utf-8') as f:
            gitignore = f.read()
        
        # Verificar que los datos JSON no estén excluidos globalmente
        if '!app/data/cache/emisiones_anuales.json' in gitignore:
            successes.append("✅ Datos CO2 incluidos en Git")
            print("✅ Datos CO2 incluidos en Git")
        else:
            issues.append("⚠️ Verificar que datos JSON estén incluidos en Git")
            print("⚠️ Verificar que datos JSON estén incluidos en Git")
    
    # 5. Verificar configuración Streamlit
    print("\n⚙️ Verificando configuración Streamlit:")
    
    config_file = Path('.streamlit/config.toml')
    if config_file.exists():
        successes.append("✅ config.toml presente")
        print("✅ config.toml presente")
        
        with open(config_file, 'r') as f:
            config = f.read()
            
        if 'headless = true' in config:
            print("✅ Configurado para headless")
        else:
            issues.append("⚠️ Falta configuración headless")
    else:
        issues.append("❌ config.toml faltante")
    
    # 6. Verificar que el gestor de datos funcione
    print("\n🧪 Verificando gestor de datos:")
    
    try:
        sys.path.append(str(Path('app').absolute()))
        from utils.streamlit_cloud_data import StreamlitCloudDataManager
        
        manager = StreamlitCloudDataManager()
        data = manager.load_co2_data()
        
        if data and data.get('emisiones_regionales'):
            regions_count = len(data['emisiones_regionales'])
            successes.append(f"✅ Gestor de datos funcional ({regions_count} regiones)")
            print(f"✅ Gestor de datos funcional ({regions_count} regiones)")
        else:
            issues.append("⚠️ Gestor de datos retorna datos vacíos")
            print("⚠️ Gestor de datos retorna datos vacíos")
            
    except Exception as e:
        issues.append(f"❌ Error en gestor de datos: {str(e)}")
        print(f"❌ Error en gestor de datos: {str(e)}")
    
    # 7. Resumen final
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    print(f"\n✅ ÉXITOS ({len(successes)}):")
    for success in successes:
        print(f"  {success}")
    
    print(f"\n⚠️ PROBLEMAS ({len(issues)}):")
    for issue in issues:
        print(f"  {issue}")
    
    # Veredicto final
    print("\n🎯 VEREDICTO:")
    if len(issues) == 0:
        print("🎉 ¡LISTO PARA STREAMLIT CLOUD!")
        print("   La aplicación está optimizada para despliegue.")
        return True
    elif len(issues) <= 2:
        print("⚠️  CASI LISTO - Revisar problemas menores")
        print("   La aplicación funcionará pero con limitaciones.")
        return True
    else:
        print("❌ NECESITA CORRECCIONES")
        print("   Resolver problemas antes del despliegue.")
        return False

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    success = check_streamlit_cloud_readiness()
    sys.exit(0 if success else 1)
