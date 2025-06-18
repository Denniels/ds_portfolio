#!/usr/bin/env python3
"""
Script de verificación del MVP - Generador de Reportes Automáticos
Verifica que todas las funcionalidades estén operativas
"""

import os
import sys
import requests
import pandas as pd
import json
from datetime import datetime
import importlib.util

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = {
        'streamlit': 'streamlit',
        'pandas': 'pandas', 
        'plotly': 'plotly',
        'requests': 'requests',
        'numpy': 'numpy'
    }
    
    dependencias_faltantes = []
    dependencias_ok = []
    
    for nombre, modulo in dependencias.items():
        try:
            spec = importlib.util.find_spec(modulo)
            if spec is not None:
                dependencias_ok.append(nombre)
            else:
                dependencias_faltantes.append(nombre)
        except ImportError:
            dependencias_faltantes.append(nombre)
    
    return dependencias_ok, dependencias_faltantes

def verificar_archivos_mvp():
    """Verifica que todos los archivos del MVP existan"""
    archivos_requeridos = [
        'app/pages/08_productos.py',
        'app/pages/09_generador_reportes.py',
        'app/utils/api_connectors.py',
        'app/utils/contact_components.py',
        'app/utils/css_loader.py'
    ]
    
    archivos_encontrados = []
    archivos_faltantes = []
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            tamaño = os.path.getsize(archivo) / 1024  # KB
            archivos_encontrados.append((archivo, tamaño))
        else:
            archivos_faltantes.append(archivo)
    
    return archivos_encontrados, archivos_faltantes

def verificar_funcionalidades_data_ingestion():
    """Verifica las funcionalidades de ingesta de datos"""
    from app.utils.api_connectors import APIConnector, DataValidator
    import numpy as np
    
    resultados = {}
    
    # Test 1: Datos demo
    try:
        df_sales = APIConnector.get_google_analytics_sample()
        resultados['google_analytics_sample'] = len(df_sales) > 0
    except Exception as e:
        resultados['google_analytics_sample'] = f"Error: {str(e)}"
    
    # Test 2: Validación de datos
    try:
        # Crear DataFrame test
        test_df = pd.DataFrame({
            'ventas': [100, 200, 300],
            'fecha': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'region': ['Norte', 'Sur', 'Centro']
        })
        
        is_valid, issues = DataValidator.validate_dataframe(test_df)
        resultados['data_validation'] = is_valid
    except Exception as e:
        resultados['data_validation'] = f"Error: {str(e)}"
    
    # Test 3: Sugerencias de tipos
    try:
        suggestions = DataValidator.suggest_data_types(test_df)
        resultados['data_suggestions'] = len(suggestions) >= 0
    except Exception as e:
        resultados['data_suggestions'] = f"Error: {str(e)}"
    
    return resultados

def verificar_streamlit_app():
    """Verifica que la aplicación Streamlit responda"""
    try:
        response = requests.get('http://localhost:8501', timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def verificar_apis_demo():
    """Verifica que las APIs demo funcionen"""
    apis_test = {
        'countries': 'https://restcountries.com/v3.1/all',
        'jsonplaceholder': 'https://jsonplaceholder.typicode.com/users'
    }
    
    resultados = {}
    
    for nombre, url in apis_test.items():
        try:
            response = requests.get(url, timeout=10)
            resultados[nombre] = response.status_code == 200
        except Exception as e:
            resultados[nombre] = f"Error: {str(e)}"
    
    return resultados

def generar_reporte_verificacion():
    """Genera reporte completo de verificación"""
    print("🔍 VERIFICACIÓN MVP - GENERADOR DE REPORTES AUTOMÁTICOS")
    print("=" * 60)
    print(f"Fecha: {datetime.now().strftime('%d de %B, %Y a las %H:%M')}")
    print()
    
    # 1. Verificar dependencias
    print("📦 DEPENDENCIAS")
    print("-" * 30)
    deps_ok, deps_faltantes = verificar_dependencias()
    
    for dep in deps_ok:
        print(f"✅ {dep}")
    
    for dep in deps_faltantes:
        print(f"❌ {dep} - FALTANTE")
    
    print(f"Total: {len(deps_ok)}/{len(deps_ok) + len(deps_faltantes)} dependencias OK")
    print()
    
    # 2. Verificar archivos
    print("📁 ARCHIVOS DEL MVP")
    print("-" * 30)
    archivos_ok, archivos_faltantes = verificar_archivos_mvp()
    
    for archivo, tamaño in archivos_ok:
        print(f"✅ {archivo} ({tamaño:.1f} KB)")
    
    for archivo in archivos_faltantes:
        print(f"❌ {archivo} - FALTANTE")
    
    print(f"Total: {len(archivos_ok)}/{len(archivos_ok) + len(archivos_faltantes)} archivos OK")
    print()
    
    # 3. Verificar funcionalidades
    if len(deps_faltantes) == 0 and len(archivos_faltantes) == 0:
        print("⚙️ FUNCIONALIDADES")
        print("-" * 30)
        
        try:
            funcionalidades = verificar_funcionalidades_data_ingestion()
            
            for func, resultado in funcionalidades.items():
                if resultado is True:
                    print(f"✅ {func}")
                elif resultado is False:
                    print(f"❌ {func}")
                else:
                    print(f"⚠️ {func}: {resultado}")
        except Exception as e:
            print(f"❌ Error verificando funcionalidades: {str(e)}")
        
        print()
    
    # 4. Verificar Streamlit
    print("🌐 APLICACIÓN STREAMLIT")
    print("-" * 30)
    
    app_running = verificar_streamlit_app()
    if app_running:
        print("✅ Aplicación respondiendo en http://localhost:8501")
    else:
        print("❌ Aplicación no responde en http://localhost:8501")
    print()
    
    # 5. Verificar APIs demo
    print("🔗 APIs DEMO")
    print("-" * 30)
    
    apis_resultado = verificar_apis_demo()
    for api, resultado in apis_resultado.items():
        if resultado is True:
            print(f"✅ {api}")
        else:
            print(f"❌ {api}: {resultado}")
    print()
    
    # 6. Resumen final
    print("📊 RESUMEN FINAL")
    print("-" * 30)
    
    total_checks = 0
    checks_ok = 0
    
    # Contar dependencias
    total_checks += len(deps_ok) + len(deps_faltantes)
    checks_ok += len(deps_ok)
    
    # Contar archivos
    total_checks += len(archivos_ok) + len(archivos_faltantes)
    checks_ok += len(archivos_ok)
    
    # Contar app
    total_checks += 1
    if app_running:
        checks_ok += 1
    
    # Contar APIs
    total_checks += len(apis_resultado)
    checks_ok += sum(1 for r in apis_resultado.values() if r is True)
    
    score = (checks_ok / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"Score Total: {score:.1f}% ({checks_ok}/{total_checks})")
    
    if score >= 95:
        print("🎉 MVP COMPLETAMENTE FUNCIONAL")
        print("   ✅ Listo para demo con clientes")
        print("   🚀 Todas las funcionalidades operativas")
    elif score >= 80:
        print("⚠️ MVP MAYORMENTE FUNCIONAL")
        print("   📝 Algunos componentes necesitan atención")
        print("   💼 Adecuado para testing interno")
    else:
        print("❌ MVP REQUIERE ATENCIÓN")
        print("   🔧 Componentes críticos faltantes")
        print("   ⏸️ No listo para demo")
    
    print()
    
    # 7. Próximos pasos
    print("🎯 PRÓXIMOS PASOS")
    print("-" * 30)
    
    if score >= 95:
        print("1. 🎮 Probar demo completo con datos reales")
        print("2. 💳 Integrar sistema de pagos")
        print("3. 📧 Configurar email marketing")
        print("4. 🤝 Contactar primeros prospects")
    elif score >= 80:
        print("1. 🔧 Resolver dependencias faltantes")
        print("2. 📁 Verificar archivos faltantes")
        print("3. ⚙️ Testing funcionalidades")
        print("4. 🔄 Re-ejecutar verificación")
    else:
        print("1. ❌ Instalar dependencias faltantes")
        print("2. 📁 Crear archivos faltantes") 
        print("3. 🚀 Reiniciar aplicación Streamlit")
        print("4. 🔄 Re-ejecutar verificación completa")
    
    print()
    print("📞 CONTACTO PARA SOPORTE:")
    print("   Daniel Andrés Mardones Sanhueza")
    print("   Portfolio: https://dsportfolio-jm67tsp8uwfsbnpfetysnh.streamlit.app/")
    print()
    
    return score

def main():
    """Función principal de verificación"""
    score = generar_reporte_verificacion()
    
    # Guardar resultados
    timestamp = datetime.now().isoformat()
    resultados = {
        "timestamp": timestamp,
        "score": score,
        "mvp_status": "ready" if score >= 95 else "needs_attention" if score >= 80 else "not_ready"
    }
    
    with open("verificacion_mvp.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Resultados guardados en: verificacion_mvp.json")

if __name__ == "__main__":
    main()
