"""
Script para corregir los errores de set_page_config en las páginas
"""
import os
import re
from pathlib import Path

def fix_page_configs():
    """Corrige las páginas para evitar llamadas duplicadas a set_page_config"""
    
    # Directorio de páginas
    pages_dir = Path(__file__).parent / "app" / "pages"
    
    # Recorrer todas las páginas
    for page_file in pages_dir.glob("*.py"):
        if page_file.name.startswith("_"):
            continue  # Ignorar archivos privados
            
        try:
            # Leer contenido actual
            with open(page_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Reemplazar la importación anterior por la nueva
            updated_content = content.replace(
                "from config import load_css\nload_css()",
                "from config import apply_styles_only"
            )
            
            # Buscar dónde termina la configuración de página
            set_page_config_pattern = r"st\.set_page_config\([^)]*\)"
            match = re.search(set_page_config_pattern, updated_content)
            
            if match:
                # Posición después de set_page_config
                end_pos = match.end()
                
                # Insertar la llamada a apply_styles_only después de set_page_config
                updated_content = updated_content[:end_pos] + "\n\n# Aplicar estilos compartidos después de configurar la página\napply_styles_only()" + updated_content[end_pos:]
                
                # Eliminar cualquier llamada duplicada a apply_shared_styles
                updated_content = updated_content.replace("from utils.shared_styles import apply_shared_styles\napply_shared_styles()", "")
                
                # Guardar el archivo actualizado
                with open(page_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                    
                print(f"✅ Corregido: {page_file.name}")
            else:
                print(f"❌ No se encontró st.set_page_config en {page_file.name}")
                
        except Exception as e:
            print(f"❌ Error al procesar {page_file.name}: {e}")
            
    print("Proceso completado.")

if __name__ == "__main__":
    fix_page_configs()
