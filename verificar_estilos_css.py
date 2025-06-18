#!/usr/bin/env python3
"""
Script para verificar que los estilos CSS se están aplicando correctamente
"""

import os
from pathlib import Path

def verificar_archivos_css():
    """
    Verifica que todos los archivos CSS necesarios existan y tengan contenido
    """
    print("🎨 VERIFICACIÓN DE ESTILOS CSS")
    print("=" * 50)
    
    archivos_css = [
        "app/static/css/streamlit_cloud.css",
        "app/static/css/style.css",
        "app/static/css/main.css",
        "app/static/css/components.css",
        "app/static/css/co2_analysis.css"
    ]
    
    archivos_encontrados = 0
    archivos_con_contenido = 0
    
    for archivo in archivos_css:
        ruta = Path(archivo)
        if ruta.exists():
            archivos_encontrados += 1
            print(f"✅ {archivo} - Existe")
            
            # Verificar que tenga contenido
            tamano = ruta.stat().st_size
            if tamano > 0:
                archivos_con_contenido += 1
                print(f"   📏 Tamaño: {tamano} bytes")
            else:
                print(f"   ⚠️  Archivo vacío")
        else:
            print(f"❌ {archivo} - No encontrado")
    
    print(f"\n📊 Resumen:")
    print(f"   • Archivos encontrados: {archivos_encontrados}/{len(archivos_css)}")
    print(f"   • Archivos con contenido: {archivos_con_contenido}/{len(archivos_css)}")
    
    return archivos_encontrados == len(archivos_css) and archivos_con_contenido == len(archivos_css)

def verificar_carga_css_en_main():
    """
    Verifica que el archivo main.py esté configurado correctamente para cargar CSS
    """
    print("\n🔍 VERIFICACIÓN DE CARGA CSS EN MAIN.PY")
    print("=" * 50)
    
    main_py = Path("app/main.py")
    if not main_py.exists():
        print("❌ app/main.py no encontrado")
        return False
    
    with open(main_py, 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Verificar elementos clave
    verificaciones = [
        ("streamlit_cloud.css", "streamlit_cloud.css" in contenido),
        ("st.markdown con CSS", "st.markdown(f'<style>{f.read()}</style>'," in contenido),
        ("Fallback CSS", 'st.markdown("""' in contenido and '.social-button' in contenido),
        ("Hero section CSS", 'class="hero-section"' in contenido),
        ("Page title CSS", 'class="page-title"' in contenido),
        ("Project cards CSS", 'class="project-card"' in contenido)
    ]
    
    errores = 0
    for nombre, condicion in verificaciones:
        if condicion:
            print(f"✅ {nombre}")
        else:
            print(f"❌ {nombre}")
            errores += 1
    
    print(f"\n📊 Resultado: {len(verificaciones) - errores}/{len(verificaciones)} verificaciones correctas")
    return errores == 0

def verificar_estilos_componentes():
    """
    Verifica que los componentes de contacto usen los estilos correctos
    """
    print("\n🧩 VERIFICACIÓN DE ESTILOS EN COMPONENTES")
    print("=" * 50)
    
    archivos_componentes = [
        "app/components/contact_links.py",
        "app/utils/contact_components.py"
    ]
    
    estilos_esperados = [
        "social-buttons",
        "social-button",
        "linkedin",
        "github",
        "social-icon"
    ]
    
    componentes_correctos = 0
    
    for archivo in archivos_componentes:
        ruta = Path(archivo)
        if ruta.exists():
            print(f"\n📁 Verificando {archivo}:")
            
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            estilos_encontrados = 0
            for estilo in estilos_esperados:
                if estilo in contenido:
                    print(f"   ✅ {estilo}")
                    estilos_encontrados += 1
                else:
                    print(f"   ❌ {estilo}")
            
            if estilos_encontrados == len(estilos_esperados):
                componentes_correctos += 1
                print(f"   🎯 Componente completo")
            else:
                print(f"   ⚠️  Faltan {len(estilos_esperados) - estilos_encontrados} estilos")
        else:
            print(f"❌ {archivo} no encontrado")
    
    print(f"\n📊 Componentes correctos: {componentes_correctos}/{len(archivos_componentes)}")
    return componentes_correctos == len(archivos_componentes)

def crear_informe_css():
    """
    Crea un informe detallado del estado de los estilos
    """
    print("\n📋 CREANDO INFORME DETALLADO...")
    
    informe = """# 🎨 INFORME DE ESTILOS CSS - PORTAFOLIO DATA SCIENCE

## Estado Actual (Junio 2025)

### ✅ Archivos CSS Disponibles:
- `app/static/css/streamlit_cloud.css` - Estilos consolidados para Streamlit Cloud
- `app/static/css/style.css` - Estilos principales
- `app/static/css/main.css` - Estilos base y variables
- `app/static/css/components.css` - Estilos para componentes
- `app/static/css/co2_analysis.css` - Estilos específicos para análisis CO2

### 🎯 Mejoras Implementadas:
1. **Archivo CSS consolidado**: Creado `streamlit_cloud.css` que no usa @import
2. **Estilos responsivos**: Adaptación para dispositivos móviles
3. **Mejores fallbacks**: CSS de respaldo mejorado en main.py
4. **Componentes estilizados**: Botones sociales y cards con estilos uniformes

### 🚀 Optimizaciones para Streamlit Cloud:
- CSS consolidado sin dependencias @import
- Estilos inline como fallback
- Variables CSS para consistencia
- Responsive design

### 📱 Elementos Estilizados:
- Hero section con gradiente
- Botones sociales (LinkedIn, GitHub)
- Cards de proyectos
- Sistema de colores consistente
- Tipografía optimizada

"""
    
    with open("INFORME_ESTILOS_CSS.md", "w", encoding="utf-8") as f:
        f.write(informe)
    
    print("📄 Informe guardado en: INFORME_ESTILOS_CSS.md")

if __name__ == "__main__":
    print("🎨 VERIFICACIÓN COMPLETA DE ESTILOS CSS")
    print("=" * 60)
    
    resultado1 = verificar_archivos_css()
    resultado2 = verificar_carga_css_en_main()
    resultado3 = verificar_estilos_componentes()
    
    if resultado1 and resultado2 and resultado3:
        print(f"\n🎉 ¡VERIFICACIÓN EXITOSA!")
        print(f"   Los estilos CSS están correctamente configurados y listos para Streamlit Cloud.")
        crear_informe_css()
    else:
        print(f"\n⚠️  Se encontraron algunos problemas en la configuración CSS.")
        print(f"   Revisa los detalles arriba para identificar qué necesita corrección.")
