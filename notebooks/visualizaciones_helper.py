"""
Helper module for managing visualizations in notebooks with GitHub compatibility.
"""
import os
from IPython.display import HTML, Image

def save_plot_with_fallback(fig, filename, directory='figures', width=1200, height=800):
    """Saves a plotly figure both as HTML and PNG for maximum compatibility.
    
    Args:
        fig: Plotly figure object
        filename: Base filename without extension
        directory: Directory to save files in (relative to notebook location)
        width: Width of the static image in pixels
        height: Height of the static image in pixels
    """
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Save interactive HTML version
    html_path = os.path.join(directory, f'{filename}.html')
    fig.write_html(html_path)
    
    # Save static PNG version with high resolution
    png_path = os.path.join(directory, f'{filename}.png')
    fig.write_image(png_path, width=width, height=height, scale=2)
    
    # Show figure in notebook
    fig.show()
    
    # Use relative paths for markdown
    rel_html_path = os.path.join('./figures', f'{filename}.html')
    rel_png_path = os.path.join('./figures', f'{filename}.png')
    
    print("\n### Para incluir en el notebook:")
    print("\nVersión interactiva (visible en VS Code):")
    print(f'<iframe src="{rel_html_path}" width="100%" height="600px" frameborder="0"></iframe>')
    
    print("\nVersión estática (visible en GitHub):")
    print(f'![{filename}]({rel_png_path})')
