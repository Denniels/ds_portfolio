"""
Utilidades para el manejo del menú de navegación
"""
import streamlit as st
import json
from pathlib import Path

def load_menu_config():
    """Carga la configuración del menú desde el archivo JSON"""
    config_path = Path(__file__).parent.parent / "config" / "menu_config.json"
    
    if not config_path.exists():
        return {}
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_sidebar_menu():
    """Renderiza el menú lateral"""
    with st.sidebar:
        st.title("🔍 Navegación")
        
        config = load_menu_config()
        menu_items = config.get('menu_items', [])
        
        # Filtrar solo elementos activos
        active_items = [item for item in menu_items if item['status'] == 'active']
        
        # Crear opciones de menú
        options = {item['id']: f"{item['icon']} {item['name']}" for item in active_items}
        
        selected = st.radio(
            "Selecciona una sección:",
            options=list(options.keys()),
            format_func=lambda x: options[x]
        )
        
        return selected

def update_menu_item(item_id, status):
    """Actualiza el estado de un elemento del menú"""
    config_path = Path(__file__).parent.parent / "config" / "menu_config.json"
    
    if not config_path.exists():
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Actualizar estado del elemento
    for item in config['menu_items']:
        if item['id'] == item_id:
            item['status'] = status
            break
    
    # Guardar cambios
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
