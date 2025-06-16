"""
Módulo que define las fuentes de datos reales utilizadas en el portafolio.
Centraliza la información sobre orígenes de datos para mantener la consistencia.
"""

# Diccionario que describe las fuentes de datos reales utilizadas 
# y cómo se obtienen/procesan para mantenerlas en la capa gratuita

DATA_SOURCES = {
    # Emisiones CO2
    "01_Analisis_Emisiones_CO2_Chile": {
        "sources": [
            "Inventario Nacional de Gases de Efecto Invernadero (Chile)",
            "Banco Mundial - Indicadores de Desarrollo Mundial",
            "Climate Watch Data"
        ],
        "preprocessing": """
        Los datos son preprocesados mensualmente mediante un script automatizado 
        que descarga, limpia y agrega los datos necesarios, almacenándolos en 
        formato comprimido CSV.gz para optimizar el espacio y el tiempo de carga.
        """,
        "optimization": """
        - Preprocesamiento completo para evitar cálculos en tiempo real
        - Caché implementado con st.cache_data
        - Imágenes convertidas a formato WebP para reducir tamaño
        - Uso de datos agregados en lugar de registros detallados
        """
    },
    
    # Calidad del Agua
    "02_Analisis_Calidad_Del_Agua": {
        "sources": [
            "Superintendencia de Servicios Sanitarios (SISS)",
            "Dirección General de Aguas (DGA)",
            "Ministerio de Salud - Programa de Vigilancia de Agua Potable"
        ],
        "preprocessing": """
        Los datos son extraídos, procesados y almacenados en formato CSV.gz.
        Las coordenadas geográficas se almacenan en un archivo JSON para
        optimizar las visualizaciones de mapas.
        """,
        "optimization": """
        - Coordenadas geocodificadas preprocesadas y cacheadas
        - Mapas interactivos generados con abstracción de datos
        - Métricas precalculadas para evitar operaciones costosas
        - Uso de Folium con carga diferida para mapas
        """
    },
    
    # Análisis Demográfico
    "03_Analisis_BigQuery_Demografia": {
        "sources": [
            "Censo Nacional de Población y Vivienda",
            "Instituto Nacional de Estadísticas (INE)",
            "Banco Mundial - Indicadores de Desarrollo Social"
        ],
        "preprocessing": """
        Los datos son extraídos de fuentes públicas y procesados
        utilizando Google BigQuery dentro del límite gratuito (1TB/mes).
        Los resultados se exportan a archivos CSV.gz para acceso rápido.
        """,
        "optimization": """
        - Consultas SQL optimizadas con particionamiento y clustering
        - Resultados exportados para evitar múltiples consultas
        - Visualizaciones precalculadas para análisis complejos
        - Procesamiento por lotes programado mensualmente
        """
    },
    
    # Presupuesto Público
    "04_Analisis_Presupuesto_Publico": {
        "sources": [
            "Dirección de Presupuestos (DIPRES)",
            "Contraloría General de la República",
            "Banco Central de Chile (estadísticas fiscales)"
        ],
        "preprocessing": """
        Los datos son extraídos de API públicas mensualmente y almacenados
        en formato comprimido. Se realizan agregaciones para diferentes
        niveles de análisis temporal y sectorial.
        """,
        "optimization": """
        - Series temporales preprocesadas para diferentes periodos
        - Estructura jerárquica optimizada para visualización
        - Caché multinivel para resultados frecuentemente consultados
        - Imágenes estáticas para gráficos complejos
        """
    }
}

def get_data_source_info(notebook_name):
    """
    Retorna la información sobre la fuente de datos para un notebook específico.
    
    Args:
        notebook_name: Nombre del notebook/análisis
        
    Returns:
        dict: Información sobre fuentes, preprocesamiento y optimización
    """
    return DATA_SOURCES.get(notebook_name, {
        "sources": ["Datos simulados para demostración"],
        "preprocessing": "No aplica (datos de ejemplo)",
        "optimization": "No aplica (datos de ejemplo)"
    })
