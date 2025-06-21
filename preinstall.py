"""
Script de pre-instalación para configurar el entorno Python
"""
import sys
import subprocess
import os

def main():
    # Verificar Python
    print(f"Python version: {sys.version}")
    
    # Instalar setuptools y wheel manualmente primero
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip==23.0.1"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools==65.5.1", "wheel==0.38.4"])
    
    # Asegurarse de que distutils está disponible
    try:
        import distutils.core
        print("distutils está disponible")
    except ImportError:
        print("WARNING: distutils no está disponible")
        
    # Configurar variables de entorno para usar binarios
    os.environ['PIP_ONLY_BINARY'] = ':all:'

if __name__ == "__main__":
    main()
