"""
Script para actualizar las importaciones en todas las páginas de la aplicación
"""
import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """
    Corrige las importaciones en un archivo
    
    Args:
        file_path (str): Ruta al archivo
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Buscar y corregir importaciones
    if "from utils.navigation import create_back_button" in content:
        # Asegurarse de que el path está configurado antes de la importación
        if not re.search(r"parent_dir = Path\(__file__\).parent.parent.*?sys\.path\.append\(str\(parent_dir\)\).*?from utils\.navigation", content, re.DOTALL):
            content = re.sub(
                r"(from utils\.navigation import create_back_button)",
                r"# Agregar el directorio raíz al path\nparent_dir = Path(__file__).parent.parent\nif str(parent_dir) not in sys.path:\n    sys.path.append(str(parent_dir))\n\n\1",
                content
            )
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Actualizado: {file_path}")

def main():
    """Función principal"""
    # Directorio de la aplicación
    app_dir = Path(__file__).parent
    
    # Procesar todos los archivos Python en pages/
    pages_dir = app_dir / "pages"
    for file_path in pages_dir.glob("*.py"):
        # Omitir archivos que comienzan con _ (módulos internos)
        if not file_path.name.startswith("_"):
            fix_imports_in_file(file_path)
    
    print("Importaciones actualizadas en todos los archivos.")

if __name__ == "__main__":
    main()
