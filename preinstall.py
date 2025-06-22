"""
Script de pre-instalación para configurar el entorno Python y manejar dependencias
para Streamlit Community Cloud
"""
import sys
import subprocess
import os
import platform

def main():
    # Verificar Python
    print(f"Python version: {sys.version}")
    print(f"Plataforma: {platform.platform()}")
    
    # Instalar setuptools y wheel manualmente primero con versiones compatibles
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools>=65.5.1", "wheel>=0.38.4"])
    
    # Asegurarse de que distutils está disponible
    try:
        import distutils.core
        print("distutils está disponible")
    except ImportError:
        print("WARNING: distutils no está disponible")
    
    # Instalar dependencias críticas que podrían causar problemas con versiones específicas
    print("Instalando dependencias críticas...")
    dependencies = [
        "numpy>=1.22.4",
        "cython>=0.29.32",
    ]
    
    for dep in dependencies:
        try:
            print(f"Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado correctamente")
        except Exception as e:
            print(f"❌ Error instalando {dep}: {str(e)}")
    
    # Verificar instalación de numpy
    try:
        import numpy
        print(f"NumPy version: {numpy.__version__}")
    except ImportError:
        print("WARNING: NumPy no está disponible después de la instalación")
    
    print("Preinstalación completada")

if __name__ == "__main__":
    main()
