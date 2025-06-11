"""
🔄 Script para Actualizar Visualizaciones en Notebooks
====================================================

Este script actualiza automáticamente todas las llamadas a show_plot_safely
por llamadas a mostrar_grafico_calidad_agua en el notebook de calidad del agua.
"""

import re
import json
from pathlib import Path

def actualizar_visualizaciones_notebook():
    """Actualiza las visualizaciones en el notebook de calidad del agua."""
    notebook_path = Path("02_Analisis_Calidad_Del_Agua.ipynb")
    
    if not notebook_path.exists():
        print(f"❌ No se encontró el notebook: {notebook_path}")
        return False
    
    print(f"🔄 Actualizando visualizaciones en {notebook_path}...")
    
    # Leer notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Mapeo de reemplazos específicos
    reemplazos = [
        {
            "patron": r'show_plot_safely\(fig\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, "distribucion_muestras")',
            "descripcion": "Distribución general de muestras"
        },
        {
            "patron": r'show_plot_safely\(fig, \'muestras_por_anio\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, "evolucion_temporal_anual")',
            "descripcion": "Evolución temporal anual"
        },
        {
            "patron": r'show_plot_safely\(fig, \'muestras_por_mes\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, "distribucion_mensual")',
            "descripcion": "Distribución mensual"
        },
        {
            "patron": r'show_plot_safely\(fig, f\'distribucion_\{param\}\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, f"distribucion_{param}")',
            "descripcion": "Distribuciones de parámetros"
        },
        {
            "patron": r'show_plot_safely\(fig, f\'boxplot_estacion_\{param\}\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, f"boxplot_estacion_{param}")',
            "descripcion": "Boxplots por estación"
        },
        {
            "patron": r'show_plot_safely\(fig, f\'boxplot_region_\{param\}\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, f"boxplot_region_{param}")',
            "descripcion": "Boxplots por región"
        },
        {
            "patron": r'show_plot_safely\(fig, \'ph_critico\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, "valores_criticos_ph")',
            "descripcion": "Valores críticos de pH"
        },
        {
            "patron": r'show_plot_safely\(fig, \'oxigeno_critico\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, "valores_criticos_oxigeno")',
            "descripcion": "Valores críticos de oxígeno"
        },
        {
            "patron": r'show_plot_safely\(fig, \'correlaciones\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, "matriz_correlaciones")',
            "descripcion": "Matriz de correlaciones"
        },
        {
            "patron": r'show_plot_safely\(fig, f\'tendencia_\{param\}\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, f"tendencia_temporal_{param}")',
            "descripcion": "Tendencias temporales"
        },
        {
            "patron": r'show_plot_safely\(fig, f\'atipicos_\{param\}\.html\'\)',
            "reemplazo": 'mostrar_grafico_calidad_agua(fig, f"valores_atipicos_{param}")',
            "descripcion": "Valores atípicos"
        }
    ]
    
    actualizaciones = 0
    
    # Procesar cada celda del notebook
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            if isinstance(source, str):
                source = [source]
            
            nueva_source = []
            for linea in source:
                linea_original = linea
                
                # Aplicar cada reemplazo
                for reemplazo in reemplazos:
                    if re.search(reemplazo['patron'], linea):
                        linea = re.sub(reemplazo['patron'], reemplazo['reemplazo'], linea)
                        if linea != linea_original:
                            print(f"  ✅ {reemplazo['descripcion']}")
                            actualizaciones += 1
                
                nueva_source.append(linea)
            
            cell['source'] = nueva_source
    
    # Guardar notebook actualizado
    if actualizaciones > 0:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, ensure_ascii=False, indent=1)
        
        print(f"\n📊 Notebook actualizado con {actualizaciones} visualizaciones")
        print(f"✅ Cambios guardados en {notebook_path}")
        return True
    else:
        print("ℹ️ No se encontraron visualizaciones para actualizar")
        return False

def verificar_integracion():
    """Verifica que la integración se haya completado correctamente."""
    notebook_path = Path("02_Analisis_Calidad_Del_Agua.ipynb")
    
    if not notebook_path.exists():
        print("❌ Notebook no encontrado")
        return False
    
    # Leer y verificar contenido
    with open(notebook_path, 'r', encoding='utf-8') as f:
        contenido = f.read()
      # Verificaciones
    verificaciones = [
        ("mostrar_grafico_calidad_agua", "Función principal definida"),
        ("from visualizaciones_helper import", "Helper importado"),
        ("from geocodificador_chile import", "Geocodificador importado"),
        ("cache_coordenadas_agua.json", "Cache configurado")
    ]
    
    print("\n🔍 Verificando integración:")
    exitos = 0
    
    for patron, descripcion in verificaciones:
        if patron in contenido:
            print(f"  ✅ {descripcion}")
            exitos += 1
        else:
            print(f"  ❌ {descripcion}")
    
    porcentaje = (exitos / len(verificaciones)) * 100
    print(f"\n📊 Integración completada al {porcentaje:.1f}%")
    
    return porcentaje >= 75

def main():
    """Función principal."""
    print("🔄 ACTUALIZADOR DE VISUALIZACIONES")
    print("=" * 40)
    
    # Actualizar visualizaciones
    if actualizar_visualizaciones_notebook():
        print("\n🎉 Actualización exitosa!")
    else:
        print("\n⚠️ No se realizaron cambios")
    
    # Verificar integración
    if verificar_integracion():
        print("\n✅ Sistema integrado correctamente")
        print("\n📋 Próximos pasos:")
        print("  1. Ejecutar el notebook para probar las visualizaciones")
        print("  2. Verificar que los mapas HTML se generen correctamente")
        print("  3. Revisar la geocodificación de estaciones")
    else:
        print("\n⚠️ Integración incompleta - revisar manualmente")

if __name__ == "__main__":
    main()
