"""
Script de pre-instalación para configurar el entorno Python y manejar dependencias
para Streamlit Community Cloud
"""
import sys
import subprocess
import os
import platform
import time

def run_command(cmd, desc=None, check=True, max_retries=3):
    """Ejecuta un comando con reintentos y mejor manejo de errores"""
    if desc:
        print(f"⏳ {desc}...")
    
    for attempt in range(max_retries):
        try:
            if check:
                return subprocess.check_call(cmd)
            else:
                return subprocess.call(cmd)
        except subprocess.CalledProcessError as e:
            if attempt < max_retries - 1:
                print(f"❌ Intento {attempt+1} falló con error: {str(e)}. Reintentando en 5 segundos...")
                time.sleep(5)
            else:
                print(f"❌ Todos los intentos fallaron: {str(e)}")
                if not check:
                    return 1
                raise

def main():
    # Verificar Python
    print(f"Python version: {sys.version}")
    print(f"Plataforma: {platform.platform()}")
    
    # Actualizar pip y setuptools primero
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        desc="Actualizando pip"
    )
    
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "setuptools>=65.5.1", "wheel>=0.38.4"],
        desc="Instalando setuptools y wheel"
    )
    
    # Asegurarse de que distutils está disponible
    try:
        import distutils.core
        print("✅ distutils está disponible")
    except ImportError:
        print("⚠️ WARNING: distutils no está disponible, intentando instalar")
        run_command(
            [sys.executable, "-m", "pip", "install", "setuptools"],
            desc="Instalando setuptools para obtener distutils",
            check=False
        )
    
    # Instalar dependencias críticas una por una con verificación
    critical_deps = [
        ("numpy>=1.22.4,<1.25.0", "numpy"),
        ("cython>=0.29.32", "cython"),
        ("scipy>=1.10.0,<1.11.0", "scipy"),
        ("scikit-learn>=1.2.0,<1.4.0", "sklearn")
    ]
    
    for dep_spec, module_name in critical_deps:
        print(f"🔄 Instalando {dep_spec}...")
        success = False
        
        try:
            run_command(
                [sys.executable, "-m", "pip", "install", "--no-cache-dir", dep_spec],
                desc=f"Instalando {dep_spec}",
                check=False
            )
            
            # Verificar instalación importando el módulo
            try:
                module = __import__(module_name)
                if hasattr(module, "__version__"):
                    print(f"✅ {module_name} instalado correctamente - version: {module.__version__}")
                else:
                    print(f"✅ {module_name} instalado correctamente")
                success = True
            except ImportError as e:
                print(f"❌ No se pudo importar {module_name} después de la instalación: {str(e)}")
        
        except Exception as e:
            print(f"❌ Error instalando {dep_spec}: {str(e)}")
        
        # Si falló, intentar una versión alternativa para numpy
        if not success and module_name == "numpy":
            print("⚠️ Intentando versión alternativa de numpy...")
            try:
                run_command(
                    [sys.executable, "-m", "pip", "install", "--no-cache-dir", "numpy==1.22.4"],
                    desc="Instalando numpy versión específica",
                    check=False
                )
            except Exception as e:
                print(f"❌ Error instalando numpy alternativo: {str(e)}")
    
    # Verificar que se hayan instalado correctamente las dependencias críticas
    missing_deps = []
    for _, module_name in critical_deps:
        try:
            __import__(module_name)
        except ImportError:
            missing_deps.append(module_name)
    
    if missing_deps:
        print(f"⚠️ ADVERTENCIA: Las siguientes dependencias críticas no están disponibles: {', '.join(missing_deps)}")
    else:
        print("✅ Todas las dependencias críticas están disponibles")
    
    print("✅ Preinstalación completada")

if __name__ == "__main__":
    main()
