"""
Utilidades para gestión de contenido y recursos
"""
import streamlit as st
import json
from pathlib import Path
import pandas as pd
from datetime import datetime

class ContentManager:
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.texts_path = self.base_path / "data" / "texts" / "content.json"
        self.cache_path = self.base_path / "data" / "cache"
        self.static_path = self.base_path / "static"
        self._ensure_dirs()
        self.load_content()

    def _ensure_dirs(self):
        """Asegura que existan los directorios necesarios"""
        self.texts_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.static_path.mkdir(parents=True, exist_ok=True)

    @st.cache_data
    def load_content(self):
        """Carga el contenido desde JSON con caché"""
        if not self.texts_path.exists():
            return {}
        with open(self.texts_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_section_content(self, section_key, subsection_key=None):
        """Obtiene el contenido de una sección específica"""
        content = self.load_content()
        if section_key not in content:
            return None
        
        if subsection_key:
            return content[section_key].get(subsection_key)
        return content[section_key]

    def get_navigation_items(self):
        """Obtiene los ítems de navegación"""
        content = self.load_content()
        sections = content.get('principal', {}).get('sections', {})
        
        nav_items = {
            "principal": "📊 Principal"
        }
        
        for key, section in sections.items():
            icon = section.get('title', '').split()[0]
            name = ' '.join(section.get('title', '').split()[1:])
            nav_items[key] = f"{icon} {name}"
        
        return nav_items

    @st.cache_data
    def get_cached_data(self, cache_key):
        """Obtiene datos del caché"""
        cache_file = self.cache_path / f"{cache_key}.json"
        if not cache_file.exists():
            return None
        
        with open(cache_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_to_cache(self, cache_key, data):
        """Guarda datos en caché"""
        cache_file = self.cache_path / f"{cache_key}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_static_resource(self, resource_type, resource_name):
        """Obtiene un recurso estático"""
        resource_path = self.static_path / resource_type / resource_name
        if not resource_path.exists():
            return None
        
        if resource_path.suffix == '.html':
            with open(resource_path, 'r', encoding='utf-8') as f:
                return f.read()
        return str(resource_path)

class NavigationManager:
    def __init__(self, content_manager):
        self.content_manager = content_manager

    def render_sidebar(self):
        """Renderiza la barra lateral de navegación"""
        with st.sidebar:
            st.title("🔍 Navegación")
            
            nav_items = self.content_manager.get_navigation_items()
            selected = st.radio(
                "Selecciona una sección:",
                options=list(nav_items.keys()),
                format_func=lambda x: nav_items[x]
            )
            
            return selected

    def render_breadcrumbs(self, current_section):
        """Renderiza breadcrumbs de navegación"""
        nav_items = self.content_manager.get_navigation_items()
        if current_section in nav_items:
            st.markdown(f"### {nav_items[current_section]}")
            st.markdown("---")
