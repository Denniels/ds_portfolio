#!/usr/bin/env python3
"""
Script de preparación para despliegue en Streamlit Cloud
"""

import os
import shutil
from pathlib import Path
import subprocess
import json
from PIL import Image
import gzip
import pandas as pd

def optimize_images(static_dir):
    """Optimiza imágenes para web"""
    print("🖼️ Optimizando imágenes...")
    img_dir = Path(static_dir) / 'images'
    if not img_dir.exists():
        return
    
    for img_path in img_dir.glob('*'):
        if img_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            try:
                img = Image.open(img_path)
                webp_path = img_path.with_suffix('.webp')
                img.save(webp_path, 'WEBP', quality=80)
                os.remove(img_path)
                print(f"✅ Convertida: {img_path.name} -> {webp_path.name}")
            except Exception as e:
                print(f"❌ Error optimizando {img_path.name}: {e}")

def compress_data_files(data_dir):
    """Comprime archivos de datos"""
    print("📦 Comprimiendo archivos de datos...")
    data_dir = Path(data_dir)
    if not data_dir.exists():
        return
    
    for file_path in data_dir.rglob('*'):
        if file_path.suffix in ['.csv', '.json']:
            try:
                # Para CSVs, convertir a parquet
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path)
                    parquet_path = file_path.with_suffix('.parquet.gz')
                    df.to_parquet(parquet_path, compression='gzip')
                    os.remove(file_path)
                    print(f"✅ Convertido: {file_path.name} -> {parquet_path.name}")
                
                # Para JSONs, comprimir con gzip
                elif file_path.suffix == '.json':
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    os.remove(file_path)
                    print(f"✅ Comprimido: {file_path.name} -> {file_path.name}.gz")
            except Exception as e:
                print(f"❌ Error comprimiendo {file_path.name}: {e}")

def minify_css(css_dir):
    """Minifica archivos CSS"""
    print("🎨 Minificando CSS...")
    css_dir = Path(css_dir)
    if not css_dir.exists():
        return
    
    try:
        subprocess.run(['npm', 'install', '-g', 'clean-css-cli'])
        for css_file in css_dir.glob('*.css'):
            if not css_file.name.endswith('.min.css'):
                output_file = css_file.with_name(f"{css_file.stem}.min.css")
                subprocess.run(['cleancss', '-o', str(output_file), str(css_file)])
                print(f"✅ Minificado: {css_file.name} -> {output_file.name}")
    except Exception as e:
        print(f"❌ Error minificando CSS: {e}")

def verify_requirements():
    """Verifica y limpia requirements.txt"""
    print("📝 Verificando requirements.txt...")
    try:
        # Obtener dependencias instaladas
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
        installed = result.stdout.splitlines()
        
        # Filtrar solo las necesarias
        essential = [
            'streamlit',
            'pandas',
            'numpy',
            'plotly',
            'folium',
            'streamlit-folium',
            'python-dotenv',
            'psutil'
        ]
        
        filtered = [pkg for pkg in installed if any(
            pkg.lower().startswith(dep.lower()) for dep in essential
        )]
        
        # Guardar requirements.txt limpio
        with open('requirements.txt', 'w') as f:
            f.write('\n'.join(filtered))
        print("✅ requirements.txt actualizado")
    except Exception as e:
        print(f"❌ Error actualizando requirements.txt: {e}")

def main():
    """Función principal"""
    print("🚀 Preparando proyecto para Streamlit Cloud...")
    
    # Directorios del proyecto
    project_dir = Path(__file__).parent
    app_dir = project_dir / 'app'
    static_dir = app_dir / 'static'
    data_dir = app_dir / 'data'
    css_dir = static_dir / 'css'
    
    # Ejecutar optimizaciones
    optimize_images(static_dir)
    compress_data_files(data_dir)
    minify_css(css_dir)
    verify_requirements()
    
    print("\n✨ ¡Proyecto listo para despliegue!")
    print("\nRecuerda:")
    print("1. Verificar los archivos optimizados")
    print("2. Probar localmente antes de subir")
    print("3. Actualizar la documentación si es necesario")

if __name__ == '__main__':
    main()
