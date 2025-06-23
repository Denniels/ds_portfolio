"""
Utilidades para mejorar la visualización de gráficos en Streamlit
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Optional, Dict, List, Union, Any

def apply_standard_layout(fig, title: str, height: int = 500, width: int = 800,
                         xaxis_title: Optional[str] = None, 
                         yaxis_title: Optional[str] = None) -> go.Figure:
    """
    Aplica un layout estándar para mejorar la visualización de cualquier gráfico de Plotly
    
    Args:
        fig: Figura de Plotly (px o go)
        title: Título del gráfico
        height: Altura del gráfico en píxeles (default: 500)
        width: Ancho del gráfico en píxeles (default: 800)
        xaxis_title: Título del eje X (opcional)
        yaxis_title: Título del eje Y (opcional)
        
    Returns:
        go.Figure: La figura con el layout mejorado
    """
    # Verificar que la figura tiene datos
    if not fig.data or len(fig.data) == 0:
        # Si no hay datos, agregar un mensaje de texto en el gráfico
        fig.add_annotation(
            text="No hay datos disponibles para mostrar",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color="red")
        )
    
    # Configuración base
    fig.update_layout(
        title={
            'text': title,
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 20, 'color': '#2F4F4F'}
        },
        height=height,
        width=width,
        template='plotly_white',
        margin=dict(l=60, r=40, t=100, b=60),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Títulos de ejes si se proporcionan
    if xaxis_title:
        fig.update_xaxes(title=xaxis_title)
        
    if yaxis_title:
        fig.update_yaxes(title=yaxis_title)
    
    # Mejoras de cuadrícula y asegurar rangos adecuados
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='lightgray',
        autorange=True
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='lightgray',
        zeroline=False,
        autorange=True
    )
    
    return fig

def enhanced_plotly_chart(fig, title: Optional[str] = None, 
                         filename: Optional[str] = None, 
                         **kwargs) -> None:
    """
    Muestra un gráfico de Plotly con configuraciones mejoradas y optimizadas para Streamlit
    
    Args:
        fig: Figura de Plotly (px o go)
        title: Título para actualizar (opcional)
        filename: Nombre de archivo para exportar (opcional)
        **kwargs: Argumentos adicionales para st.plotly_chart
    """
    # Asegurarse de que el gráfico tenga datos para mostrar
    if not fig.data or len(fig.data) == 0:
        st.warning(f"⚠️ No hay datos disponibles para el gráfico: {title or 'Sin título'}")
        return
    
    # Actualizar título si se proporciona uno nuevo
    if title:
        fig.update_layout(
            title={
                'text': title,
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 20, 'color': '#2F4F4F'}
            }
        )
    
    # Establecer nombre de archivo para exportación
    if not filename:
        # Usar el título del gráfico o un nombre genérico
        if fig.layout.title.text:
            filename = fig.layout.title.text.replace(" ", "_").lower()[:30]
        else:
            filename = "grafico_plotly"
    
    # Asegurar rangos de ejes adecuados para evitar gráficos vacíos
    if hasattr(fig, 'update_xaxes'):
        fig.update_xaxes(autorange=True)
    if hasattr(fig, 'update_yaxes'):
        fig.update_yaxes(autorange=True)
    
    # Configuración avanzada para la visualización
    st.plotly_chart(
        fig, 
        use_container_width=True,
        config={
            'displayModeBar': True,
            'responsive': True,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': filename,
                'height': fig.layout.height if hasattr(fig.layout, 'height') else 600,
                'width': fig.layout.width if hasattr(fig.layout, 'width') else 1000,
                'scale': 2  # Mayor resolución
            }
        },
        **kwargs
    )

def create_histogram(df, column, title=None, color='#3366CC', bins=None, height=500, width=800):
    """
    Crea un histograma optimizado para visualización en Streamlit
    
    Args:
        df: DataFrame de pandas
        column: Nombre de la columna para el histograma
        title: Título (opcional, por defecto usa el nombre de la columna)
        color: Color del histograma
        bins: Número de bins (opcional)
        height: Altura del gráfico
        width: Ancho del gráfico
        
    Returns:
        go.Figure: Histograma optimizado
    """
    if not title:
        title = f"Distribución de {column}"
    
    # Crear histograma
    fig = px.histogram(
        df, 
        x=column, 
        title=title,
        height=height,
        width=width,
        template='plotly_white',
        color_discrete_sequence=[color]
    )
    
    # Aplicar layout estándar
    return apply_standard_layout(
        fig, 
        title=title, 
        height=height, 
        width=width,
        xaxis_title=column,
        yaxis_title="Frecuencia"
    )

def create_bar_chart(x_values, y_values, title=None, orientation='v', color='#4CAF50',
                    x_title=None, y_title=None, height=500, width=800):
    """
    Crea un gráfico de barras optimizado para visualización en Streamlit
    
    Args:
        x_values: Valores para el eje X
        y_values: Valores para el eje Y
        title: Título del gráfico
        orientation: Orientación ('v' para vertical, 'h' para horizontal)
        color: Color para las barras
        x_title: Título del eje X
        y_title: Título del eje Y
        height: Altura del gráfico
        width: Ancho del gráfico
        
    Returns:
        go.Figure: Gráfico de barras optimizado
    """
    if orientation == 'h':
        # En horizontal, x e y se invierten
        fig = px.bar(x=x_values, y=y_values, orientation='h')
        default_x = "Valor"
        default_y = "Categoría"
    else:
        fig = px.bar(x=y_values, y=x_values)  # Invertidos por la orientación
        default_x = "Categoría"
        default_y = "Valor"
    
    # Aplicar layout estándar
    return apply_standard_layout(
        fig, 
        title=title or "Gráfico de Barras", 
        height=height, 
        width=width,
        xaxis_title=x_title or default_x,
        yaxis_title=y_title or default_y
    )

# Colores predeterminados para gráficos
CHART_COLORS = {
    'blue': '#3366CC',
    'green': '#4CAF50',
    'red': '#FF6B6B',
    'orange': '#FFA726',
    'purple': '#9C27B0',
    'cyan': '#4ECDC4',
    'yellow': '#FFF176',
}
