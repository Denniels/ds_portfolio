"""
Script para generar una imagen de perfil profesional para el portafolio
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_data_science_profile_image(save_path, size=(400, 400)):
    """
    Crea una imagen de perfil profesional relacionada con ciencia de datos
    
    Args:
        save_path: Ruta donde guardar la imagen
        size: Tamaño de la imagen (ancho, alto)
    """
    # Crear una imagen base
    img = Image.new('RGBA', size, color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Colores para el diseño
    background_color = (39, 55, 77, 255)  # Azul oscuro profesional
    accent_color = (82, 134, 180, 255)    # Azul claro
    highlight_color = (221, 159, 58, 255) # Naranja como acento
    
    # Dibujar fondo
    draw.rectangle([0, 0, size[0], size[1]], fill=background_color)
    
    # Dibujar elementos de visualización de datos estilizados
    
    # 1. Gráfico de barras estilizado
    bar_width = 20
    bar_spacing = 10
    num_bars = 5
    bar_heights = [120, 80, 150, 60, 100]
    
    start_x = (size[0] - (num_bars * bar_width + (num_bars-1) * bar_spacing)) // 2
    base_y = size[1] - 70
    
    for i in range(num_bars):
        x = start_x + i * (bar_width + bar_spacing)
        height = bar_heights[i]
        # Degradado en las barras
        for h in range(height):
            alpha = 255 - int(h * 0.8)
            current_color = accent_color[:3] + (alpha,)
            draw.rectangle([x, base_y - h, x + bar_width, base_y], fill=current_color)
    
    # 2. Elementos de código Python
    code_elements = [
        "import pandas as pd",
        "import numpy as np",
        "df.plot()",
        "model.fit(X, y)"
    ]
    
    font_size = 16
    try:
        # Intentar cargar una fuente monoespaciada si está disponible
        font = ImageFont.truetype("Courier New", font_size)
    except IOError:
        # Usar fuente por defecto si no está disponible
        font = ImageFont.load_default()
    
    for i, code in enumerate(code_elements):
        y_pos = 50 + i * 20
        draw.text((40, y_pos), code, fill=(255, 255, 255, 200), font=font)
    
    # 3. Círculo de datos en la esquina
    draw.ellipse([size[0] - 120, size[1] - 120, size[0] - 20, size[1] - 20], 
                fill=highlight_color)
    
    # 4. Título "Data Science"
    title = "Data Science"
    title_font_size = 28
    try:
        title_font = ImageFont.truetype("Arial Bold", title_font_size)
    except IOError:
        title_font = ImageFont.load_default()
    
    title_width = draw.textlength(title, font=title_font)
    draw.text(((size[0] - title_width) // 2, 15), title, 
                fill=(255, 255, 255, 230), font=title_font)
    
    # Guardar la imagen
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    img.save(save_path, format="PNG")
    print(f"Imagen guardada en: {save_path}")

if __name__ == "__main__":
    # Directorio de la aplicación
    app_dir = Path(__file__).parent.parent
    
    # Crear la imagen y guardarla
    img_path = app_dir / "static" / "images" / "data_science_profile.png"
    create_data_science_profile_image(img_path)
    
    # Crear una versión más pequeña para el perfil
    img_path_small = app_dir / "static" / "images" / "data_science_profile_small.png"
    create_data_science_profile_image(img_path_small, size=(150, 150))
