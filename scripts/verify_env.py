"""
Script para verificar y ajustar el entorno antes de crear el modelo
"""
import subprocess
import sys
import pkg_resources

def check_and_install_dependencies():
    """Verifica y ajusta las dependencias necesarias"""
    required_versions = {
        'scikit-learn': '1.2.2',
        'numpy': '1.24.3',
        'scipy': '1.10.1',
        'joblib': '1.2.0',
        'threadpoolctl': '3.1.0'
    }
    
    print("🔍 Verificando versiones de dependencias...")
    
    for package, version in required_versions.items():
        try:
            installed = pkg_resources.get_distribution(package).version
            if installed != version:
                print(f"⚠️  {package}: instalado {installed}, necesario {version}")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install",
                    f"{package}=={version}", "--force-reinstall"
                ])
            else:
                print(f"✓ {package} {version} ya instalado correctamente")
        except pkg_resources.DistributionNotFound:
            print(f"⚠️  Instalando {package}=={version}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", f"{package}=={version}"
            ])

if __name__ == "__main__":
    print("\n🚀 Iniciando verificación del entorno...\n")
    check_and_install_dependencies()
    print("\n✨ Entorno verificado y ajustado correctamente!")
    
    # Ahora que tenemos las versiones correctas, importamos y ejecutamos
    # el script de creación del modelo
    print("\n🔄 Ejecutando creación del modelo...")
    subprocess.check_call([
        sys.executable, "scripts/create_compatible_model_v2.py"
    ])
