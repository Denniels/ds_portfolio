"""
Script para actualizar los datos de la aplicación Streamlit desde los notebooks.
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
import os
import sys
import shutil
import datetime
import subprocess

# Agregar directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

# Directorios
NOTEBOOK_DIR = ROOT_DIR / "notebooks"
DATA_DIR = ROOT_DIR / "app" / "data"
PROCESSED_DIR = DATA_DIR / "processed"
CACHE_DIR = DATA_DIR / "cache"
FEEDBACK_DIR = DATA_DIR / "feedback"

# Asegurar que existan los directorios
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)

def update_agua_data():
    """Actualiza específicamente los datos de calidad del agua"""
    print("🚀 Actualizando datos de calidad del agua...")
    
    # Ejecutar el script de extracción de calidad del agua
    extract_script = NOTEBOOK_DIR / "extract_agua_data.py"
    
    if not extract_script.exists():
        print(f"❌ Script de extracción no encontrado: {extract_script}")
        return False
    
    try:
        # Ejecutar el script de extracción
        result = subprocess.run(
            [sys.executable, str(extract_script)],
            cwd=str(NOTEBOOK_DIR),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos máximo
        )
        
        if result.returncode == 0:
            print("✅ Datos de calidad del agua actualizados exitosamente")
            return True
        else:
            print("❌ Error al actualizar datos de calidad del agua:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout: El script de calidad del agua tardó más de 5 minutos")
        return False
    except Exception as e:
        print(f"❌ Error al ejecutar script de calidad del agua: {e}")
        return False

def ensure_feedback_file():
    """Asegura que existe el archivo de comentarios para el sistema de feedback"""
    comments_file = FEEDBACK_DIR / "comments.json"
    
    if not comments_file.exists():
        # Crear un archivo de comentarios vacío
        with open(comments_file, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False)
        print(f"✅ Archivo de comentarios creado en {comments_file}")
    else:
        print(f"✓ Archivo de comentarios ya existe en {comments_file}")

def update_app_data():
    """Actualiza los datos de la aplicación desde los datos procesados"""
    # Verificar si existen los datos procesados
    if not PROCESSED_DIR.exists() or not any(PROCESSED_DIR.iterdir()):
        print("❌ No se encontraron datos procesados. Ejecuta primero process_notebooks.py")
        return False
    
    print("Actualizando datos de la aplicación...")
    
    # Copiar todos los archivos procesados al directorio de caché
    for file in PROCESSED_DIR.glob("*.json"):
        dest_file = CACHE_DIR / file.name
        shutil.copy2(file, dest_file)
        print(f"✅ Copiado: {file.name} -> {dest_file}")
    
    # Crear archivo de actualización
    with open(CACHE_DIR / "last_update.json", "w", encoding="utf-8") as f:
        update_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "files_updated": [f.name for f in PROCESSED_DIR.glob("*.json")]
        }
        json.dump(update_info, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos de la aplicación actualizados correctamente")
    return True

def create_servicios_json():
    """Crea el archivo de servicios para la aplicación"""
    servicios_file = DATA_DIR / "servicios.json"
    
    servicios = [
        {
            "id": 1,
            "nombre": "Análisis de Datos Ambientales",
            "descripcion": "Análisis detallado de datos ambientales para empresas y organizaciones.",
            "precio_base": 1200,
            "duracion_estimada": "2-4 semanas",
            "incluye": [
                "Recolección de datos",
                "Limpieza y procesamiento",
                "Visualización interactiva",
                "Informe detallado",
                "Presentación de resultados"
            ],
            "categoria": "ambiental",
            "imagen": "analisis_ambiental.webp"
        },
        {
            "id": 2,
            "nombre": "Dashboard Interactivo",
            "descripcion": "Creación de dashboards interactivos para visualizar datos de forma clara y eficiente.",
            "precio_base": 950,
            "duracion_estimada": "2-3 semanas",
            "incluye": [
                "Diseño personalizado",
                "Integración con fuentes de datos",
                "Filtros interactivos",
                "Exportación de resultados",
                "Capacitación de uso"
            ],
            "categoria": "visualizacion",
            "imagen": "dashboard.webp"
        },
        {
            "id": 3,
            "nombre": "Consultoría en Calidad de Agua",
            "descripcion": "Asesoría especializada en análisis de calidad de agua y cumplimiento normativo.",
            "precio_base": 1500,
            "duracion_estimada": "3-5 semanas",
            "incluye": [
                "Evaluación de situación actual",
                "Análisis de muestras",
                "Informe de cumplimiento normativo",
                "Recomendaciones de mejora",
                "Seguimiento de implementación"
            ],
            "categoria": "ambiental",
            "imagen": "consultoria_agua.webp"
        },
        {
            "id": 4,
            "nombre": "Análisis Demográfico",
            "descripcion": "Estudio detallado de datos demográficos para planificación urbana o empresarial.",
            "precio_base": 1100,
            "duracion_estimada": "2-3 semanas",
            "incluye": [
                "Recopilación de datos censales",
                "Segmentación poblacional",
                "Análisis de tendencias",
                "Proyecciones futuras",
                "Informe estratégico"
            ],
            "categoria": "demografia",
            "imagen": "analisis_demografico.webp"
        },
        {
            "id": 5,
            "nombre": "Automatización de Informes",
            "descripcion": "Implementación de sistemas para generar informes automáticos periódicos.",
            "precio_base": 800,
            "duracion_estimada": "1-2 semanas",
            "incluye": [
                "Diseño de plantillas",
                "Integración con fuentes de datos",
                "Programación de envíos",
                "Personalización de contenido",
                "Soporte técnico"
            ],
            "categoria": "automatizacion",
            "imagen": "automatizacion.webp"
        }
    ]
    
    # Guardar archivo de servicios
    with open(servicios_file, "w", encoding="utf-8") as f:
        json.dump(servicios, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Archivo de servicios creado en {servicios_file}")

def main():
    """Función principal"""
    print("Iniciando actualización de datos para la aplicación Streamlit...")
    
    # Ejecutar funciones de actualización
    ensure_feedback_file()
    create_servicios_json()
    
    # Actualizar datos específicos de calidad del agua
    agua_success = update_agua_data()
    
    # Actualizar el resto de datos desde archivos procesados
    update_success = update_app_data()
    
    # Verificar que los archivos de calidad del agua estén presentes
    agua_files = [
        "calidad_agua_metadata.json",
        "calidad_agua_estaciones.json", 
        "calidad_agua_conclusiones.json"
    ]
    
    agua_files_present = all((CACHE_DIR / f).exists() for f in agua_files)
    
    if agua_success and update_success and agua_files_present:
        print("\n✅ Actualización completada exitosamente")
        print(f"📂 Datos de la aplicación actualizados en: {DATA_DIR}")
        print("💧 Datos de calidad del agua incluidos y actualizados")
        print("🚀 La aplicación Streamlit está lista para ejecutarse")
        
        # Mostrar resumen de archivos generados
        print("\n📋 Archivos generados:")
        for file in CACHE_DIR.glob("*.json"):
            print(f"   ✓ {file.name}")
            
    else:
        print("\n⚠️ Actualización incompleta")
        if not agua_success:
            print("❌ Falló la actualización de datos de calidad del agua")
        if not update_success:
            print("❌ Falló la actualización de datos generales")
        if not agua_files_present:
            print("❌ Archivos de calidad del agua no encontrados")
        print("Revise los mensajes de error anteriores")

if __name__ == "__main__":
    main()
