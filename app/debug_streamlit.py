"""
Script de debugging para verificar estado en Streamlit Cloud
"""
import streamlit as st
import os
import sys
from pathlib import Path
import importlib.util

def main():
    st.title("🔍 Debug - Estado de la Aplicación")
    
    # Información del entorno
    st.header("🌍 Información del Entorno")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Variables de Entorno")
        env_vars = [
            "IS_STREAMLIT_CLOUD",
            "ENVIRONMENT", 
            "PWD",
            "HOME",
            "PYTHONPATH"
        ]
        
        for var in env_vars:
            value = os.getenv(var, "No definida")
            st.write(f"**{var}**: `{value}`")
    
    with col2:
        st.subheader("Sistema")
        st.write(f"**Python**: {sys.version}")
        st.write(f"**Platform**: {sys.platform}")
        st.write(f"**Streamlit Cloud**: {os.getenv('IS_STREAMLIT_CLOUD', 'false')}")
    
    # Verificar archivos críticos
    st.header("📁 Archivos Críticos")
    
    base_path = Path(__file__).parent
    
    critical_files = [
        "static/css/style.css",
        "static/css/style.min.css", 
        "static/css/main.css",
        "static/css/co2_analysis.css",
        "static/css/components.css",
        "data/cache/emisiones_anuales.json",
        "data/cache/emisiones_regionales.json",
        "data/cache/cache_metadata.json"
    ]
    
    for file_path in critical_files:
        full_path = base_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            st.success(f"✅ {file_path} - {size} bytes")
        else:
            st.error(f"❌ {file_path} - NO ENCONTRADO")
    
    # Verificar módulos
    st.header("📦 Módulos Críticos")
    
    modules = [
        "plotly",
        "folium", 
        "pandas",
        "numpy",
        "streamlit",
        "branca"
    ]
    
    for module in modules:
        try:
            spec = importlib.util.find_spec(module)
            if spec is not None:
                mod = importlib.import_module(module)
                version = getattr(mod, '__version__', 'Desconocida')
                st.success(f"✅ {module} - v{version}")
            else:
                st.error(f"❌ {module} - NO ENCONTRADO")
        except Exception as e:
            st.error(f"❌ {module} - ERROR: {str(e)}")
    
    # Verificar rutas de CSS
    st.header("🎨 Estado de CSS")
    
    css_path = 'static/css/style.min.css' if os.getenv('IS_STREAMLIT_CLOUD') == 'true' else 'static/css/style.css'
    st.write(f"**Ruta CSS utilizada**: `{css_path}`")
    
    try:
        with open(css_path) as f:
            css_content = f.read()
            st.success(f"✅ CSS cargado - {len(css_content)} caracteres")
            st.code(css_content[:500] + "..." if len(css_content) > 500 else css_content, language="css")
    except FileNotFoundError:
        st.error(f"❌ Archivo CSS no encontrado: {css_path}")
    except Exception as e:
        st.error(f"❌ Error cargando CSS: {str(e)}")
    
    # Test de datos
    st.header("📊 Test de Datos CO2")
    
    try:
        import json
        data_dir = Path(__file__).parent / "data" / "cache"
        
        if (data_dir / "emisiones_anuales.json").exists():
            with open(data_dir / "emisiones_anuales.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                st.success(f"✅ Datos anuales cargados - {len(data)} registros")
        
        if (data_dir / "emisiones_regionales.json").exists():
            with open(data_dir / "emisiones_regionales.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                st.success(f"✅ Datos regionales cargados - {len(data)} regiones")
                
    except Exception as e:
        st.error(f"❌ Error cargando datos: {str(e)}")

if __name__ == "__main__":
    main()
