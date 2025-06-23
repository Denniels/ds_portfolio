"""
Script para actualizar todas las páginas con los estilos compartidos
"""
import os
from pathlib import Path

def update_page_imports():
    """Actualiza todas las páginas para importar los estilos compartidos"""
    
    # Directorio de páginas
    pages_dir = Path(__file__).parent / "app" / "pages"
    
    # Texto a insertar al inicio de cada archivo
    import_text = """
# Importar configuración global
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import load_css
load_css()
"""
    
    # Recorrer todas las páginas
    for page_file in pages_dir.glob("*.py"):
        if page_file.name.startswith("_"):
            continue  # Ignorar archivos privados
            
        try:
            # Leer contenido actual
            with open(page_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Verificar si ya tiene la importación
            if "from config import load_css" not in content:
                # Encontrar la posición después de las importaciones iniciales
                import_position = content.find("import streamlit as st")
                if import_position != -1:
                    # Encontrar el final de la línea
                    end_of_line = content.find("\n", import_position)
                    if end_of_line != -1:
                        # Insertar después de la importación de streamlit
                        new_content = content[:end_of_line+1] + import_text + content[end_of_line+1:]
                        
                        # Guardar el archivo actualizado
                        with open(page_file, "w", encoding="utf-8") as f:
                            f.write(new_content)
                            
                        print(f"✅ Actualizado: {page_file.name}")
                    else:
                        print(f"❌ No se pudo encontrar el final de línea en {page_file.name}")
                else:
                    print(f"❓ No se encontró 'import streamlit as st' en {page_file.name}")
            else:
                print(f"✓ Ya actualizado: {page_file.name}")
                
        except Exception as e:
            print(f"❌ Error al procesar {page_file.name}: {e}")
            
    print("Proceso completado.")

if __name__ == "__main__":
    update_page_imports()
