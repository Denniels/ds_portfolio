#!/usr/bin/env python3
"""
Script de utilidades para el desarrollo del portafolio
====================================================

Este script contiene funciones útiles para el desarrollo y mantenimiento
del portafolio de Data Science.
"""

import os
import sys
import subprocess
from pathlib import Path

def start_portfolio():
    """Inicia la aplicación principal del portafolio"""
    app_dir = Path(__file__).parent / "app"
    os.chdir(app_dir)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])

def install_requirements():
    """Instala las dependencias del proyecto"""
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_tests():
    """Ejecuta las pruebas del proyecto"""
    subprocess.run([sys.executable, "-m", "pytest", "tests/"])

def create_new_app_template(app_name):
    """Crea una plantilla para una nueva aplicación"""
    apps_dir = Path(__file__).parent / "app" / "apps"
    app_file = apps_dir / f"{app_name}_app.py"
    
    template = f'''"""
{app_name.title()} App
========================

Aplicación {app_name} para el portafolio de Data Science.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

class {app_name.title().replace('_', '')}App:
    """Clase principal para la aplicación {app_name}"""
    
    def __init__(self):
        self.title = "{app_name.title().replace('_', ' ')}"
    
    def run(self):
        """Método principal para ejecutar la aplicación"""
        st.title(f"{{self.title}}")
        st.markdown("---")
        
        # Implementar funcionalidad aquí
        st.info("Esta aplicación está en desarrollo.")
        
        # Ejemplo de contenido
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sección 1")
            st.write("Contenido de la primera sección")
        
        with col2:
            st.subheader("Sección 2")
            st.write("Contenido de la segunda sección")

def main():
    """Función principal para ejecutar desde línea de comandos"""
    app = {app_name.title().replace('_', '')}App()
    app.run()

if __name__ == "__main__":
    main()
'''
    
    with open(app_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"Plantilla creada: {app_file}")
    print(f"Recuerda agregar la aplicación a main.py en available_apps")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Utilidades del portafolio DS")
    parser.add_argument("action", choices=["start", "install", "test", "new-app"],
                       help="Acción a realizar")
    parser.add_argument("--name", help="Nombre de la nueva aplicación (solo para new-app)")
    
    args = parser.parse_args()
    
    if args.action == "start":
        start_portfolio()
    elif args.action == "install":
        install_requirements()
    elif args.action == "test":
        run_tests()
    elif args.action == "new-app":
        if not args.name:
            print("Error: --name es requerido para crear una nueva aplicación")
            sys.exit(1)
        create_new_app_template(args.name)
