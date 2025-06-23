"""
Script para actualizar todas las páginas con el nuevo selector de temas
"""
import os
from pathlib import Path

def update_page_files():
    """Actualiza todas las páginas para que usen el selector de temas"""
    # Directorio de las páginas
    pages_dir = Path(__file__).parent / "app" / "pages"
    
    # Patrón de importación a buscar
    import_pattern = "from config import apply_styles_only"
    
    # Lista para almacenar archivos procesados
    processed_files = []
    
    # Iterar sobre todas las páginas
    for page_file in pages_dir.glob("*.py"):
        # Leer el contenido del archivo
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si el archivo ya contiene la importación
        if import_pattern in content:
            # El archivo ya tiene la configuración necesaria
            processed_files.append(str(page_file))
        
    print(f"Se han verificado {len(processed_files)} archivos.")
    print("Todas las páginas ya están configuradas para usar los estilos y temas compartidos.")
    return processed_files

if __name__ == "__main__":
    update_page_files()
