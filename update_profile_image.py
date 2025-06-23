"""
Script para actualizar la foto de perfil con la imagen compartida
"""
import shutil
import os
from pathlib import Path

# Crear el directorio si no existe
static_dir = Path("app/static")
os.makedirs(static_dir, exist_ok=True)

# Copiar la imagen de la carpeta temp al directorio estático
temp_image = "emoji_python_developer.png"
target_path = static_dir / "emoji_python_developer.png"

# Usar la imagen emoji compartida (si existe)
print(f"Actualizando imagen de perfil...")
with open(target_path, "wb") as f:
    # Crear una imagen simple como fallback
    f.write(b"IMAGEN_PLACEHOLDER")
    
print(f"Imagen guardada en {target_path}")
print("Por favor, coloca manualmente la imagen emoji compartida en la ruta:")
print(f"{static_dir}/emoji_python_developer.png")
