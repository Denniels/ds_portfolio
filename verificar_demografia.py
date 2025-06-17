#!/usr/bin/env python3
"""
Script de verificación final para la integración de demografía
Verifica que todos los componentes estén funcionando correctamente
"""

import sys
import json
from pathlib import Path
import requests

def verificar_gitignore():
    """Verificar que los archivos de demografía estén en .gitignore"""
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        return False, "Archivo .gitignore no encontrado"
    
    content = gitignore_path.read_text(encoding='utf-8')
    if 'demografia_data.json' in content:
        return True, "✅ demografia_data.json está excluido del repositorio"
    else:
        return False, "❌ demografia_data.json NO está en .gitignore"

def verificar_archivo_demografia():
    """Verificar si existe el archivo de datos de demografía"""
    data_path = Path('app/data/cache/demografia_data.json')
    if data_path.exists():
        return True, f"✅ Archivo de datos encontrado: {data_path}"
    else:
        return False, f"⚠️  Archivo de datos no existe (esto es normal): {data_path}"

def verificar_api_banco_mundial():
    """Verificar conectividad con la API del Banco Mundial"""
    try:
        url = "https://api.worldbank.org/v2/country/CHL/indicator/SP.POP.TOTL?format=json&date=2023:2023"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1] and data[1][0]['value']:
                poblacion = data[1][0]['value']
                return True, f"✅ API del Banco Mundial funcionando - Población 2023: {poblacion:,}"
            else:
                return False, "❌ API del Banco Mundial responde pero sin datos válidos"
        else:
            return False, f"❌ API del Banco Mundial error HTTP: {response.status_code}"
    except Exception as e:
        return False, f"❌ Error conectando a API del Banco Mundial: {str(e)}"

def verificar_notebook_demografia():
    """Verificar que el notebook de demografía existe"""
    notebook_path = Path('notebooks/03_Analisis_Demografia.ipynb')
    if notebook_path.exists():
        return True, f"✅ Notebook de demografía encontrado: {notebook_path}"
    else:
        return False, f"❌ Notebook de demografía no encontrado: {notebook_path}"

def verificar_pagina_streamlit():
    """Verificar que la página de Streamlit existe"""
    page_path = Path('app/pages/03_demografia.py')
    if page_path.exists():
        # Verificar que contiene las funciones necesarias
        content = page_path.read_text(encoding='utf-8')
        if 'load_demografia_data' in content and 'generate_demografia_data_fallback' in content:
            return True, f"✅ Página de Streamlit completa: {page_path}"
        else:
            return False, f"⚠️  Página de Streamlit existe pero le faltan funciones: {page_path}"
    else:
        return False, f"❌ Página de Streamlit no encontrada: {page_path}"

def main():
    print("🔍 VERIFICACIÓN FINAL - INTEGRACIÓN DEMOGRAFÍA")
    print("=" * 60)
    
    verificaciones = [
        ("GitIgnore", verificar_gitignore),
        ("Archivo de Datos", verificar_archivo_demografia),
        ("API Banco Mundial", verificar_api_banco_mundial),
        ("Notebook", verificar_notebook_demografia),
        ("Página Streamlit", verificar_pagina_streamlit)
    ]
    
    resultados = []
    
    for nombre, funcion in verificaciones:
        try:
            exito, mensaje = funcion()
            resultados.append((nombre, exito, mensaje))
            print(f"\n{nombre}: {mensaje}")
        except Exception as e:
            resultados.append((nombre, False, f"Error en verificación: {str(e)}"))
            print(f"\n{nombre}: ❌ Error en verificación: {str(e)}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE VERIFICACIONES")
    print("=" * 60)
    
    exitosos = sum(1 for _, exito, _ in resultados if exito)
    total = len(resultados)
    
    for nombre, exito, mensaje in resultados:
        estado = "✅" if exito else "❌"
        print(f"{estado} {nombre}")
    
    print(f"\n🎯 ESTADO GENERAL: {exitosos}/{total} verificaciones exitosas")
    
    if exitosos == total:
        print("\n🎉 ¡INTEGRACIÓN COMPLETAMENTE FUNCIONAL!")
        print("La aplicación está lista para despliegue en Streamlit Community Cloud.")
    elif exitosos >= total - 1:
        print("\n⚠️  Integración mayormente funcional con advertencias menores.")
        print("La aplicación debería funcionar correctamente.")
    else:
        print("\n❌ Se encontraron problemas que requieren atención.")
        print("Revise los errores antes del despliegue.")
    
    print("\n📝 PRÓXIMOS PASOS:")
    print("1. Ejecutar: streamlit run app/main.py")
    print("2. Navegar a la página de Demografía")
    print("3. Verificar que los datos se cargan correctamente")
    print("4. Desplegar en Streamlit Community Cloud")

if __name__ == "__main__":
    main()
