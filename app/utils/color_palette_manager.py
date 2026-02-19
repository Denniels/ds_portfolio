"""
Gestor de paletas de colores para visualizaciones
"""
import streamlit as st
import plotly.express as px

# Paletas de colores disponibles
COLOR_PALETTES = {
    "Plotly": {
        "Plotly Default": px.colors.qualitative.Plotly,
        "Pastel": px.colors.qualitative.Pastel,
        "Vivid": px.colors.qualitative.Vivid,
        "Set1": px.colors.qualitative.Set1,
        "Set2": px.colors.qualitative.Set2,
        "Set3": px.colors.qualitative.Set3,
    },
    "Secuenciales": {
        "Blues": px.colors.sequential.Blues,
        "Viridis": px.colors.sequential.Viridis,
        "Plasma": px.colors.sequential.Plasma,
        "Inferno": px.colors.sequential.Inferno,
        "Magma": px.colors.sequential.Magma,
        "Cividis": px.colors.sequential.Cividis,
    },
    "Divergentes": {
        "RdBu": px.colors.diverging.RdBu,
        "RdYlBu": px.colors.diverging.RdYlBu,
        "Spectral": px.colors.diverging.Spectral,
        "Tealrose": px.colors.diverging.Tealrose,
        "Temps": px.colors.diverging.Temps,
    },
    "Personalizadas": {
        "Data Science": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"],
        "Oceano": ["#0077be", "#00a8cc", "#00b4d8", "#90e0ef", "#caf0f8", "#48cae4", "#023e8a", "#03045e"],
        "Atardecer": ["#ff6b6b", "#feca57", "#ff9ff3", "#54a0ff", "#5f27cd", "#00d2d3", "#ff9f43", "#10ac84"],
        "Naturaleza": ["#27ae60", "#2ecc71", "#3498db", "#9b59b6", "#34495e", "#16a085", "#f39c12", "#e74c3c"],
        "Corporativo": ["#2c3e50", "#34495e", "#7f8c8d", "#95a5a6", "#bdc3c7", "#ecf0f1", "#3498db", "#2980b9"],
        "Minimalista": ["#2d3436", "#636e72", "#74b9ff", "#0984e3", "#fd79a8", "#e84393", "#00cec9", "#00b894"],
    }
}

def create_color_palette_selector():
    """
    Crea un selector de paleta de colores en el sidebar
    """
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Paleta de Colores")
    
    # Inicializar session state
    if 'color_palette_category' not in st.session_state:
        st.session_state.color_palette_category = "Plotly"
    if 'color_palette_name' not in st.session_state:
        st.session_state.color_palette_name = "Plotly Default"
      # Selector de categoría
    palette_category = st.sidebar.selectbox(
        "📂 Categoría:",
        list(COLOR_PALETTES.keys()),
        index=list(COLOR_PALETTES.keys()).index(st.session_state.color_palette_category),
        key="palette_category_selector"
    )
    
    # Selector de paleta específica
    available_palettes = list(COLOR_PALETTES[palette_category].keys())
    default_palette = available_palettes[0] if st.session_state.color_palette_name not in available_palettes else st.session_state.color_palette_name
    
    palette_name = st.sidebar.selectbox(
        "🎯 Paleta:",
        available_palettes,
        index=available_palettes.index(default_palette) if default_palette in available_palettes else 0,
        key="palette_name_selector"
    )
    
    # Actualizar session state
    st.session_state.color_palette_category = palette_category
    st.session_state.color_palette_name = palette_name
    
    # Obtener colores seleccionados
    selected_colors = COLOR_PALETTES[palette_category][palette_name]
    
    # Mostrar preview de la paleta
    if len(selected_colors) > 0:
        st.sidebar.markdown("**Vista previa:**")
        
        # Crear HTML para mostrar los colores
        color_preview = '<div style="display: flex; flex-wrap: wrap; gap: 2px; margin: 5px 0;">'
        for i, color in enumerate(selected_colors[:8]):  # Mostrar máximo 8 colores
            color_preview += f'''
            <div style="
                width: 20px; 
                height: 20px; 
                background-color: {color}; 
                border-radius: 3px; 
                border: 1px solid rgba(255,255,255,0.3);
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            " title="{color}"></div>
            '''
        color_preview += '</div>'
        
        st.sidebar.markdown(color_preview, unsafe_allow_html=True)
    
    return {
        "category": palette_category,
        "name": palette_name,
        "colors": selected_colors
    }

def get_current_color_palette():
    """
    Obtiene la paleta de colores actualmente seleccionada
    """
    if 'color_palette_category' not in st.session_state:
        return COLOR_PALETTES["Plotly"]["Plotly Default"]
    
    category = st.session_state.color_palette_category
    name = st.session_state.color_palette_name
    
    return COLOR_PALETTES.get(category, {}).get(name, COLOR_PALETTES["Plotly"]["Plotly Default"])

def apply_color_palette_to_fig(fig, palette=None):
    """
    Aplica la paleta de colores seleccionada a una figura de Plotly
    
    Args:
        fig: Figura de Plotly
        palette: Lista de colores (opcional, usa la paleta seleccionada si no se especifica)
    
    Returns:
        fig: Figura modificada con la nueva paleta
    """
    if palette is None:
        palette = get_current_color_palette()
    
    # Aplicar paleta dependiendo del tipo de gráfico
    if hasattr(fig, 'data') and len(fig.data) > 0:
        for i, trace in enumerate(fig.data):
            if hasattr(trace, 'marker'):
                if hasattr(trace.marker, 'color'):
                    # Para gráficos de barras, scatter, etc.
                    if isinstance(trace.marker.color, (list, tuple)):
                        # Si es una lista de colores, mapear con la paleta
                        new_colors = [palette[j % len(palette)] for j in range(len(trace.marker.color))]
                        trace.marker.color = new_colors
                    else:
                        # Si es un color único, usar el color de la paleta según el índice
                        trace.marker.color = palette[i % len(palette)]
            
            # Para líneas
            if hasattr(trace, 'line') and hasattr(trace.line, 'color'):
                trace.line.color = palette[i % len(palette)]
            
            # Para gráficos de área
            if hasattr(trace, 'fillcolor'):
                trace.fillcolor = palette[i % len(palette)]
    
    return fig

def get_color_palette_info():
    """
    Retorna información sobre la paleta actual para mostrar en la UI
    """
    if 'color_palette_category' not in st.session_state:
        return "Paleta: Plotly Default"
    
    return f"🎨 Paleta: {st.session_state.color_palette_name} ({st.session_state.color_palette_category})"
