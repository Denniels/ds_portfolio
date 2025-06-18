#!/usr/bin/env python3
"""
Script para verificar que todos los botones sociales usan el nuevo diseño
"""

import os
import re
from pathlib import Path

def verificar_botones_sociales():
    """
    Verifica que todos los componentes usen el nuevo diseño de botones
    """
    print("🔘 VERIFICACIÓN DE BOTONES SOCIALES ACTUALIZADOS")
    print("=" * 60)
    
    # Archivos que deberían tener botones sociales
    archivos_con_botones = [
        "app/components/contact_links.py",
        "app/utils/contact_components.py", 
        "app/pages/01_emisiones_co2.py"
    ]
    
    # Patrones del nuevo diseño
    patrones_nuevos = [
        r'class="social-button linkedin"',
        r'class="social-button github"',
        r'LINKEDIN',
        r'GITHUB',
        r'💼.*LINKEDIN',
        r'⚡.*GITHUB'
    ]
    
    # Patrones del diseño antiguo que NO deben estar
    patrones_antiguos = [
        r'🔗.*LinkedIn',
        r'💻.*GitHub',
        r'padding: 8px 12px',
        r'border-radius: 5px'
    ]
    
    archivos_actualizados = 0
    total_archivos = len(archivos_con_botones)
    
    for archivo in archivos_con_botones:
        ruta = Path(archivo)
        if ruta.exists():
            print(f"\n📁 Verificando {archivo}:")
            
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Verificar nuevos patrones
            nuevos_encontrados = 0
            for patron in patrones_nuevos:
                if re.search(patron, contenido):
                    nuevos_encontrados += 1
            
            # Verificar patrones antiguos (no deben estar)
            antiguos_encontrados = 0
            for patron in patrones_antiguos:
                if re.search(patron, contenido):
                    antiguos_encontrados += 1
                    print(f"   ⚠️  Encontrado patrón antiguo: {patron}")
            
            if nuevos_encontrados >= 2 and antiguos_encontrados == 0:
                print(f"   ✅ Botones actualizados correctamente")
                archivos_actualizados += 1
            elif nuevos_encontrados >= 2:
                print(f"   🔄 Mayormente actualizado (algunos patrones antiguos restantes)")
            else:
                print(f"   ❌ Necesita actualización")
        else:
            print(f"❌ {archivo} no encontrado")
    
    print(f"\n📊 Resumen:")
    print(f"   • Archivos actualizados: {archivos_actualizados}/{total_archivos}")
    
    return archivos_actualizados == total_archivos

def verificar_estilos_css():
    """
    Verifica que los archivos CSS tengan los nuevos estilos
    """
    print(f"\n🎨 VERIFICACIÓN DE ESTILOS CSS")
    print("=" * 60)
    
    archivos_css = [
        "app/static/css/streamlit_cloud.css",
        "app/static/css/style.css"
    ]
    
    # Estilos que deben estar presentes
    estilos_requeridos = [
        "text-transform: uppercase",
        "letter-spacing: 0.5px",
        "min-width: 120px",
        "padding: 12px 20px",
        "border-radius: 4px",
        "font-weight: 600"
    ]
    
    archivos_correctos = 0
    
    for archivo in archivos_css:
        ruta = Path(archivo)
        if ruta.exists():
            print(f"\n📄 Verificando {archivo}:")
            
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            estilos_encontrados = 0
            for estilo in estilos_requeridos:
                if estilo in contenido:
                    print(f"   ✅ {estilo}")
                    estilos_encontrados += 1
                else:
                    print(f"   ❌ {estilo}")
            
            if estilos_encontrados == len(estilos_requeridos):
                print(f"   🎯 CSS completo")
                archivos_correctos += 1
            else:
                print(f"   ⚠️  Faltan {len(estilos_requeridos) - estilos_encontrados} estilos")
        else:
            print(f"❌ {archivo} no encontrado")
    
    print(f"\n📊 Archivos CSS correctos: {archivos_correctos}/{len(archivos_css)}")
    return archivos_correctos == len(archivos_css)

def verificar_fallback_main():
    """
    Verifica que main.py tenga el fallback CSS actualizado
    """
    print(f"\n🚀 VERIFICACIÓN DE FALLBACK EN MAIN.PY")
    print("=" * 60)
    
    main_py = Path("app/main.py")
    if not main_py.exists():
        print("❌ app/main.py no encontrado")
        return False
    
    with open(main_py, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar elementos del nuevo fallback
    elementos_fallback = [
        "text-transform: uppercase",
        "padding: 12px 20px",
        "min-width: 120px",
        "box-shadow: 0 2px 4px",
        "transform: translateY(-2px)"
    ]
    
    fallback_encontrados = 0
    for elemento in elementos_fallback:
        if elemento in contenido:
            print(f"   ✅ {elemento}")
            fallback_encontrados += 1
        else:
            print(f"   ❌ {elemento}")
    
    print(f"\n📊 Fallback: {fallback_encontrados}/{len(elementos_fallback)} elementos correctos")
    return fallback_encontrados == len(elementos_fallback)

if __name__ == "__main__":
    print("🔘 VERIFICACIÓN COMPLETA DE BOTONES SOCIALES NUEVOS")
    print("=" * 70)
    
    resultado1 = verificar_botones_sociales()
    resultado2 = verificar_estilos_css()
    resultado3 = verificar_fallback_main()
    
    if resultado1 and resultado2 and resultado3:
        print(f"\n🎉 ¡ACTUALIZACIÓN COMPLETADA!")
        print(f"   Todos los botones sociales ahora usan el nuevo diseño rectangular.")
        print(f"   Los estilos están optimizados para Streamlit Cloud.")
        print(f"   El portafolio se verá más profesional y moderno.")
    else:
        print(f"\n⚠️  La actualización está casi completa.")
        print(f"   Revisa los detalles arriba para cualquier ajuste final.")
