"""
Debug específico para verificar rutas en Streamlit Cloud
"""

import streamlit as st
import os
from pathlib import Path
import json

def debug_streamlit_cloud_paths():
    """Debug para verificar rutas en Streamlit Cloud"""
    
    st.title("🔍 Debug - Rutas de Archivos en Streamlit Cloud")
    
    # Información del entorno
    st.subheader("🌍 Información del Entorno")
    st.write(f"**IS_STREAMLIT_CLOUD**: {os.getenv('IS_STREAMLIT_CLOUD', 'no definida')}")
    st.write(f"**Directorio actual**: {os.getcwd()}")
    st.write(f"**__file__**: {__file__}")
    
    # Detectar entorno
    is_cloud = os.getenv('IS_STREAMLIT_CLOUD', 'false').lower() == 'true'
    
    # Probar diferentes rutas base
    st.subheader("📁 Explorando Rutas Posibles")
    
    base_options = [
        Path(__file__).parent.parent / 'data' / 'cache',  # Ruta desde debug
        Path.cwd() / 'app' / 'data' / 'cache',             # Desde raíz del proyecto
        Path('/mount/src/ds_portfolio/app/data/cache'),    # Ruta absoluta Streamlit Cloud
        Path('./app/data/cache'),                          # Ruta relativa
    ]
    
    for i, base_path in enumerate(base_options):
        st.write(f"**Opción {i+1}**: `{base_path}`")
        
        # Verificar si el directorio existe
        if base_path.exists():
            st.success(f"✅ Directorio existe")
            
            # Listar archivos
            files = list(base_path.glob('*.json'))
            if files:
                st.write("**Archivos encontrados:**")
                for file in files:
                    size = file.stat().st_size
                    st.write(f"  - {file.name}: {size} bytes")
                    
                    # Intentar cargar el contenido
                    try:
                        with open(file, 'r', encoding='utf-8') as f:
                            content = json.load(f)
                            st.write(f"    ✅ JSON válido: {len(str(content))} caracteres")
                    except Exception as e:
                        st.write(f"    ❌ Error cargando: {e}")
            else:
                st.warning("⚠️ No se encontraron archivos JSON")
        else:
            st.error(f"❌ Directorio no existe")
        
        st.write("---")
    
    # Probar estructura completa
    st.subheader("🗂️ Estructura de Directorios")
    
    try:
        # Desde la raíz del proyecto
        project_root = Path.cwd()
        st.write(f"**Raíz del proyecto**: `{project_root}`")
        
        # Verificar estructura esperada
        expected_structure = [
            'app',
            'app/data',
            'app/data/cache',
            'app/data/cache/emisiones_anuales.json',
            'app/data/cache/emisiones_regionales.json',
            'app/data/cache/cache_metadata.json'
        ]
        
        for path_str in expected_structure:
            full_path = project_root / path_str
            exists = full_path.exists()
            st.write(f"- `{path_str}`: {'✅' if exists else '❌'}")
            
            if exists and path_str.endswith('.json'):
                size = full_path.stat().st_size
                st.write(f"  ({size} bytes)")
                
    except Exception as e:
        st.error(f"Error explorando estructura: {e}")

if __name__ == "__main__":
    debug_streamlit_cloud_paths()
