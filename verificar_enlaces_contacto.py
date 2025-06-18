#!/usr/bin/env python3
"""
Script para verificar que todos los enlaces de contacto están actualizados correctamente
"""

import os
import re
import json
from pathlib import Path

def verificar_enlaces_contacto():
    """
    Verifica que todos los enlaces de contacto estén actualizados en el proyecto
    """
    
    # Enlaces correctos esperados
    enlaces_correctos = {
        "linkedin": "https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777",
        "github": "https://github.com/Denniels",
        "website": "https://integralservicespa.cl",
        "repo": "Denniels/ds_portfolio"
    }
    
    # Archivos a verificar
    archivos_importantes = [
        "README.md",
        "app/components/contact_links.py",
        "app/utils/contact_components.py",
        "app/pages/05_curriculum.py",
        "app/pages/06_servicios.py",
        "app/config/contact_config.json",
        ".streamlit/secrets.toml"
    ]
    
    print("🔍 Verificando enlaces de contacto...")
    print("=" * 50)
    
    errores = []
    archivos_verificados = 0
    
    for archivo in archivos_importantes:
        ruta_archivo = Path(archivo)
        if ruta_archivo.exists():
            print(f"✅ Verificando: {archivo}")
            
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                contenido = f.read()
                
            # Buscar enlaces incorrectos
            patrones_incorrectos = [
                r'tu-usuario',
                r'tu-perfil',
                r'data-scientist-chile',
                r'ds-portfolio-chile',
                r'linkedin\.com/in/(?!daniel-andres-mardones-sanhueza)',
                r'github\.com/(?!Denniels)'
            ]
            
            for patron in patrones_incorrectos:
                matches = re.findall(patron, contenido, re.IGNORECASE)
                if matches:
                    errores.append(f"❌ {archivo}: Encontrado patrón incorrecto '{patron}'")
            
            archivos_verificados += 1
        else:
            print(f"⚠️  Archivo no encontrado: {archivo}")
    
    print(f"\n📊 Resumen de verificación:")
    print(f"   • Archivos verificados: {archivos_verificados}")
    print(f"   • Errores encontrados: {len(errores)}")
    
    if errores:
        print(f"\n❌ Errores encontrados:")
        for error in errores:
            print(f"   {error}")
        return False
    else:
        print(f"\n✅ ¡Todos los enlaces están correctamente actualizados!")
        print(f"\n📝 Enlaces configurados:")
        print(f"   • LinkedIn: {enlaces_correctos['linkedin']}")
        print(f"   • GitHub: {enlaces_correctos['github']}")
        print(f"   • Website: {enlaces_correctos['website']}")
        print(f"   • Repository: {enlaces_correctos['repo']}")
        return True

def verificar_config_contacto():
    """
    Verifica que el archivo de configuración de contacto esté correcto
    """
    config_path = Path("app/config/contact_config.json")
    
    if not config_path.exists():
        print("❌ Archivo de configuración de contacto no encontrado")
        return False
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        enlaces_esperados = {
            "linkedin": "https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777",
            "github": "https://github.com/Denniels",
            "website": "https://integralservicespa.cl"
        }
        
        contact_info = config.get("contact_info", {})
        
        for key, valor_esperado in enlaces_esperados.items():
            if contact_info.get(key) != valor_esperado:
                print(f"❌ Configuración incorrecta para {key}")
                return False
        
        print("✅ Configuración de contacto correcta")
        return True
        
    except Exception as e:
        print(f"❌ Error al leer configuración: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VERIFICACIÓN DE ENLACES DE CONTACTO")
    print("=" * 60)
    
    resultado1 = verificar_enlaces_contacto()
    print("\n" + "-" * 60)
    resultado2 = verificar_config_contacto()
    
    if resultado1 and resultado2:
        print(f"\n🎉 ¡VERIFICACIÓN EXITOSA!")
        print(f"   Todos los enlaces de contacto están correctamente configurados.")
        print(f"   El proyecto está listo para despliegue en Streamlit Community Cloud.")
    else:
        print(f"\n⚠️  Se encontraron problemas que necesitan corrección.")
