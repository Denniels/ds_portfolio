"""
Componentes reutilizables para la página de productos
"""
import streamlit as st
from .product_styles import get_product_card_styles, product_card_template


def show_product_card(
    title: str,
    description: str,
    icon: str,
    status: str,
    features: list = None,
    tech_stack: list = None,
    demo_path: str = None
) -> None:
    """
    Muestra una tarjeta de producto con estilo consistente
    
    Args:
        title: Título del producto
        description: Descripción del producto
        icon: Emoji o ícono del producto
        status: Estado del producto ('demo', 'dev', o 'concept')
        features: Lista de características del producto
        tech_stack: Lista de tecnologías usadas
        demo_path: Ruta al demo (solo para productos con status='demo')
    """
    # Cargar estilos solo una vez por sesión
    if 'product_styles_loaded' not in st.session_state:
        st.markdown(get_product_card_styles(), unsafe_allow_html=True)
        st.session_state.product_styles_loaded = True
    
    # Formatear y renderizar el HTML
    card_html = product_card_template(
        title=title,
        description=description.strip(),
        icon=icon,
        status=status,
        features=features or [],
        tech_stack=tech_stack or []
    )
    
    # Renderizar la tarjeta usando markdown con HTML habilitado
    st.markdown(
        f'{card_html}', 
        unsafe_allow_html=True
    )
    
    # Agregar botón de demo si corresponde
    if demo_path and status == "demo":
        if st.button(
            "🚀 Explorar Demo",
            key=f"demo_{title}",
            type="primary",
            use_container_width=True
        ):
            demo_path = f"pages/{demo_path}" if not demo_path.startswith('pages/') else demo_path
            st.switch_page(demo_path)
