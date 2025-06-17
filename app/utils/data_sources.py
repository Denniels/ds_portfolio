"""
Módulo para gestionar información sobre fuentes de datos
"""
import pandas as pd
from datetime import datetime
import streamlit as st

def get_data_source_info(source_id=None):
    """
    Obtiene información sobre las fuentes de datos utilizadas
    
    Args:
        source_id (str, optional): ID de la fuente específica
        
    Returns:
        dict: Información sobre las fuentes de datos
    """
    # Información de procesamiento y optimización para cada notebook
    notebooks_info = {
        "01_Analisis_Emisiones_CO2_Chile": {
            "sources": ["Ministerio del Medio Ambiente - Inventario Nacional de Gases de Efecto Invernadero", 
                       "Banco Mundial - Climate Change Knowledge Portal",
                       "EDGAR - Emissions Database for Global Atmospheric Research"],
            "preprocessing": """
                #### 1. Preprocesamiento de datos
                - Limpieza de valores nulos y atípicos
                - Normalización de nombres de regiones
                - Conversión de unidades a Mt CO2-eq
                - Geocodificación de coordenadas para visualización
            """,
            "optimization": """
                #### 2. Optimización de visualizaciones
                - Uso de técnicas de agregación para grandes conjuntos de datos
                - Implementación de caché para consultas frecuentes
                - Optimización de rendering para mapas interactivos
            """
        },
        "02_Analisis_Calidad_Del_Agua": {
            "sources": ["Dirección General de Aguas (DGA) - Red de monitoreo de calidad de aguas", 
                       "SISS - Superintendencia de Servicios Sanitarios",
                       "Ministerio de Salud - Normas de calidad del agua"],
            "preprocessing": """
                #### 1. Preprocesamiento de datos
                - Estandarización de parámetros fisicoquímicos
                - Consolidación de mediciones de múltiples estaciones
                - Conversión y normalización de unidades
            """,
            "optimization": """
                #### 2. Optimización de visualizaciones
                - Agrupación geoespacial de estaciones cercanas
                - Implementación de filtros dinámicos por parámetro
                - Optimización de mapas de calor para renderizado eficiente
            """
        },
        "03_Analisis_Demografia": {
            "sources": ["Instituto Nacional de Estadísticas (INE) - Censo 2017", 
                       "Google BigQuery Public Datasets - Population demographics",
                       "CEPAL - Proyecciones de población"],
            "preprocessing": """
                #### 1. Preprocesamiento de datos
                - Integración de datos de múltiples fuentes
                - Estandarización de categorías demográficas
                - Preparación de consultas optimizadas para BigQuery
            """,
            "optimization": """
                #### 2. Optimización de consultas y visualizaciones
                - Implementación de particionamiento de datos
                - Uso de vistas materializadas para consultas frecuentes
                - Optimización de consultas SQL para reducir procesamiento
            """
        },
        "04_Analisis_Presupuesto_Publico": {
            "sources": ["Dirección de Presupuestos (DIPRES) - Ley de Presupuestos", 
                       "Contraloría General de la República - Ejecución presupuestaria",
                       "Ministerio de Hacienda - Informes de finanzas públicas"],
            "preprocessing": """
                #### 1. Preprocesamiento de datos
                - Normalización de categorías presupuestarias
                - Ajuste por inflación para comparaciones históricas
                - Agregación por ministerios y programas
            """,
            "optimization": """
                #### 2. Optimización de análisis y visualizaciones
                - Implementación de técnicas de muestreo para grandes conjuntos
                - Optimización de gráficos de series temporales
                - Uso de estructuras de datos eficientes para análisis interactivo
            """
        }
    }
    
    # Si se proporciona un ID específico, buscar en notebooks_info primero
    if source_id:
        # Si es un ID de notebook, devolver esa información
        if source_id in notebooks_info:
            return notebooks_info[source_id]
        
        # Si es un ID de fuente de datos específica, buscar en sources
        source_keys = {
            "emisiones_co2": "emisiones_co2",
            "calidad_agua": "calidad_agua",
            "demografia": "demografia",
            "presupuesto": "presupuesto"
        }
        
        source_id_normalized = source_keys.get(source_id.lower().replace(" ", "_"), source_id)
        
        # Definir todas las fuentes de datos
        sources = {
            "emisiones_co2": {
                "name": "Emisiones de CO2 en Chile",
                "url": "https://datos.gob.cl/dataset/emisiones-co2",
                "last_update": "2023-11-15",
                "description": "Datos de emisiones de CO2 por región y sector económico en Chile",
                "license": "Creative Commons Attribution 4.0",
                "format": "CSV",
                "columns": ["Region", "Sector", "Año", "Emisiones_Mt", "lat", "lon"]
            },
            "calidad_agua": {
                "name": "Calidad del Agua en Chile",
                "url": "https://snia.mop.gob.cl/BNAConsultas/",
                "last_update": "2024-02-20",
                "description": "Datos de monitoreo de calidad del agua en ríos y lagos de Chile",
                "license": "Uso público",
                "format": "CSV, Excel",
                "columns": ["Estacion", "Fecha", "Parametro", "Valor", "Unidad", "lat", "lon"]
            },
            "demografia": {
                "name": "Datos Demográficos - INE Chile",
                "url": "https://www.ine.cl/estadisticas/sociales/demografia-y-vitales/",
                "last_update": "2023-12-10",
                "description": "Datos demográficos de Chile del Instituto Nacional de Estadísticas",
                "license": "Uso público",
                "format": "CSV, Excel, API",
                "columns": ["Comuna", "Región", "Población", "Densidad", "Edad_promedio"]
            },
            "presupuesto": {
                "name": "Presupuesto Sector Público",
                "url": "https://www.dipres.gob.cl/598/w3-propertyvalue-15407.html",
                "last_update": "2024-01-15",
                "description": "Datos del presupuesto público de Chile por ministerio y programa",
                "license": "Información pública",
                "format": "Excel, PDF",
                "columns": ["Año", "Ministerio", "Programa", "Monto_Inicial", "Monto_Ejecutado"]
            }
        }
        
        return sources.get(source_id_normalized, {})
    
    # Si no se proporciona un ID, devolver todas las fuentes
    return {
        "notebooks": notebooks_info,
        "sources": {
            "emisiones_co2": "Emisiones de CO2 en Chile",
            "calidad_agua": "Calidad del Agua en Chile",
            "demografia": "Datos Demográficos - INE Chile",
            "presupuesto": "Presupuesto Sector Público"
        }
    }

def get_citation_text(source_id):
    """
    Genera un texto de citación para una fuente de datos
    
    Args:
        source_id (str): ID de la fuente
        
    Returns:
        str: Texto de citación
    """
    source = get_data_source_info(source_id)
    
    if not source:
        return "Fuente no encontrada"
    
    # Formato de citación básico
    current_year = datetime.now().year
    
    citation = f"{source['name']}. ({current_year}). "
    citation += f"Recuperado de {source['url']} "
    citation += f"el {datetime.now().strftime('%d/%m/%Y')}. "
    citation += f"Última actualización: {source['last_update']}."
    
    return citation

def render_data_source_info(source_id, container=None):
    """
    Renderiza información sobre una fuente de datos en la interfaz
    
    Args:
        source_id (str): ID de la fuente
        container: Contenedor de Streamlit opcional
    """
    # Usar el contenedor proporcionado o el contexto actual
    target = container if container else st
    
    source = get_data_source_info(source_id)
    
    if not source:
        target.error("Información de fuente de datos no disponible")
        return
    
    # Renderizar información
    with target.expander("ℹ️ Fuente de Datos"):
        target.markdown(f"**{source['name']}**")
        target.markdown(f"* **Descripción**: {source['description']}")
        target.markdown(f"* **Última actualización**: {source['last_update']}")
        target.markdown(f"* **Licencia**: {source['license']}")
        target.markdown(f"* **Formato**: {source['format']}")
        target.markdown(f"* **URL**: [{source['url']}]({source['url']})")
        
        # Mostrar tabla de columnas si está disponible
        if "columns" in source:
            target.markdown("**Columnas principales:**")
            target.code(", ".join(source["columns"]))
            
        # Mostrar texto de citación
        target.markdown("**Cómo citar:**")
        target.code(get_citation_text(source_id), language="markdown")
