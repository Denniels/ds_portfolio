"""
Helper module for managing visualizations in notebooks with GitHub compatibility.
Versión optimizada para rendimiento.
"""
import os
from pathlib import Path
from IPython.display import display, HTML
import plotly.io as pio

def save_plot_with_fallback(fig, filename, directory='figures', width=800, height=600):
    """
    Guarda una figura de Plotly como HTML y genera una versión estática para GitHub.
    Esta versión prioriza velocidad y confiabilidad.
    
    Args:
        fig: Figura de Plotly
        filename: Nombre base del archivo sin extensión
        directory: Directorio donde guardar los archivos
        width: Ancho de la imagen
        height: Alto de la imagen
    """
    try:
        # Crear directorio si no existe
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        # Path para el HTML
        html_path = directory / f'{filename}.html'
        
        print(f"Guardando visualización '{filename}'...")
        
        # 1. Guardar HTML (versión interactiva)
        print("- Guardando versión interactiva...", end=" ", flush=True)
        
        # Configurar para mejor rendimiento
        fig.update_layout(
            width=width,
            height=height,
            showlegend=True,
        )
        
        # Guardar HTML con CDN
        fig.write_html(
            str(html_path),
            include_plotlyjs='cdn',
            full_html=False,
            auto_play=False,
            include_mathjax=False
        )
        
        if html_path.exists():
            print(f"✓ ({html_path.stat().st_size / 1024:.1f} KB)")
            
        # 2. Crear versión estática para GitHub
        print("- Creando enlace estático para GitHub...")
        static_html = f'''
        <div>
            <a href="{html_path}" target="_blank">
                <img src="https://plotly.com/~plotly/0.png" alt="Click para ver gráfico interactivo" style="max-width:100%;height:auto;">
            </a>
            <br>
            <small><i>Click en la imagen para ver versión interactiva</i></small>
        </div>
        '''
        
        # Guardar referencia para GitHub
        github_path = directory / f'{filename}_github.html'
        with open(github_path, 'w', encoding='utf-8') as f:
            f.write(static_html)
        
        print(f"✓ Visualización guardada exitosamente:")
        print(f"- HTML interactivo: {html_path}")
        print(f"- Referencia GitHub: {github_path}")
        
        # Mostrar versión interactiva en el notebook
        display(fig)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise
