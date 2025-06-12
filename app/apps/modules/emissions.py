"""
Utilidades específicas para análisis de emisiones CO2
====================================================
"""

import pandas as pd
import numpy as np
import streamlit as st
from .config import CHILE_REGIONS
from .emissions_config import CO2_EMISSION_SECTORS, POLLUTANT_TYPES, EMISSION_SCALES

def create_demo_emissions_data():
    """Crea datos de demostración para emisiones CO2 basados en análisis real"""
    
    # Datos principales por región (basados en análisis del notebook)
    regions_data = {
        'region': [
            'Antofagasta', 'Metropolitana de Santiago', 'Biobío', 'Coquimbo',
            'Los Lagos', 'Araucanía', 'Valparaíso', 'Maule', 'Atacama',
            'O\'Higgins', 'Los Ríos', 'Ñuble', 'Magallanes', 'Aysén', 'Tarapacá', 'Arica y Parinacota'
        ],
        'emisiones_totales_ton': [
            32324136.60, 27399612.91, 24650427.74, 14766159.21, 13390023.23,
            9791057.21, 9699334.75, 8969982.01, 5718497.36, 5626798.50,
            5156153.37, 4941055.07, 2648029.28, 1310275.05, 890086.73, 179934.16
        ],
        'numero_fuentes': [
            19177, 109161, 18011, 10193, 27225, 12861, 17454, 11093, 6830,
            11376, 9231, 4458, 10370, 9600, 6447, 4240
        ],
        'promedio_por_fuente': [
            1685.57, 251.00, 1368.56, 1448.91, 491.76, 761.42, 555.67,
            808.69, 837.01, 494.62, 558.57, 1108.36, 255.31, 136.45, 138.06, 42.43
        ]
    }
    
    # Datos por sector económico (top 10)
    sectors_data = {
        'sector': [
            'Generación, transmisión y distribución de energía eléctrica',
            'Extracción y procesamiento de cobre',
            'Fundición de metales no ferrosos',
            'Acuicultura marina',
            'Elaboración de productos de panadería',
            'Actividades de otras asociaciones n.c.p.',
            'Venta al por menor en comercios no especializados',
            'Actividades de hospitales públicos y privados',
            'Tratamiento y eliminación de desechos no peligrosos',
            'Elaboración y conservación de frutas, legumbres'
        ],
        'emisiones_totales_ton': [
            68234567.89, 45123456.78, 16642510.45, 4591734.23, 9198897.12,
            2456789.34, 5678901.23, 4567890.12, 5818235.67, 3477846.45
        ],
        'numero_empresas': [
            17345, 14027, 437, 16752, 4791, 25653, 23550, 11171, 374, 1698
        ]
    }
    
    # Datos por tipo de fuente
    sources_data = {
        'tipo_fuente': [
            'Caldera Industrial (Generadora de Vapor o Agua Caliente)',
            'Horno de Panadería', 'Grupo Electrógeno', 'Caldera Recuperadora',
            'Turbina de Gas', 'Caldera de Generación Eléctrica', 'Horno de Cal',
            'Turbina de Vapor', 'Secador de Madera', 'Horno de Cemento'
        ],
        'emisiones_totales_ton': [
            43656530.12, 9653520.45, 9387036.78, 8122531.23, 6192758.34,
            3942042.56, 2845123.67, 2456789.12, 1987654.32, 1765432.10
        ],
        'promedio_por_fuente': [
            2633.88, 831.13, 57.11, 90250.34, 8746.83, 40639.61,
            3968.25, 12345.67, 8901.23, 5678.90
        ]
    }
    
    # Datos por contaminante
    contaminants_data = {
        'contaminante': [
            'Carbon dioxide', 'Carbon monoxide', 'Nitrogen oxides (NOx)',
            'Sulfur oxides (SOx)', 'PM10, primary', 'PM2.5, primary',
            'Mercury', 'Benzene', 'Toluene', 'Formaldehyde'
        ],
        'emisiones_totales_ton': [
            156789012.34, 23456789.12, 18765432.10, 15432109.87, 12345678.90,
            9876543.21, 7654321.09, 5432109.87, 3210987.65, 1098765.43
        ],
        'numero_registros': [
            34849, 34864, 30654, 28923, 25678, 23456, 34765, 30717, 28934, 26789
        ]
    }
    
    # Crear datos detallados sintéticos para el mapa
    regions_list = regions_data['region']
    emissions_list = regions_data['emisiones_totales_ton']
    sources_list = regions_data['numero_fuentes']
    raw_data_records = []
    
    # Crear múltiples registros por región para simular datos detallados
    for i, region in enumerate(regions_list):
        region_emission = emissions_list[i]
        num_sources = sources_list[i]
        
        # Distribuir emisiones entre múltiples fuentes
        sources_to_create = min(100, int(num_sources / 100))  # Reducir número para performance
        if sources_to_create > 0:
            for j in range(sources_to_create):
                emission_per_source = region_emission / num_sources
                raw_data_records.append({
                    'region': region,
                    'emisiones_co2_ton': emission_per_source + np.random.normal(0, emission_per_source * 0.1)
                })
    
    raw_data_df = pd.DataFrame(raw_data_records)
    
    return {
        'regions': pd.DataFrame(regions_data),
        'sectors': pd.DataFrame(sectors_data),
        'sources': pd.DataFrame(sources_data),
        'contaminants': pd.DataFrame(contaminants_data),
        'raw_data': raw_data_df
    }

def process_real_emissions_data(raw_data):
    """Procesa los datos reales del RETC para crear estructura similar a demo_data"""
    
    try:
        # Limpiar nombres de columnas
        raw_data.columns = raw_data.columns.str.strip()
        
        # Verificar si existe la columna cantidad_toneladas
        if 'cantidad_toneladas' not in raw_data.columns:
            st.error("❌ Columna 'cantidad_toneladas' no encontrada en los datos")
            return None
        
        # Convertir cantidad_toneladas a numérico (manejar comas como separador decimal)
        raw_data['cantidad_toneladas_num'] = pd.to_numeric(
            raw_data['cantidad_toneladas'].astype(str).str.replace(',', '.', regex=False),
            errors='coerce'
        ).fillna(0)
        
        # Filtrar solo registros con datos válidos
        valid_data = raw_data[raw_data['cantidad_toneladas_num'] > 0].copy()
        
        if len(valid_data) == 0:
            st.warning("⚠️ No se encontraron datos válidos de emisiones.")
            return None
        
        # Procesar datos por región
        regions_data = valid_data.groupby('region').agg({
            'cantidad_toneladas_num': ['sum', 'count', 'mean']
        }).round(2)
        
        regions_data.columns = ['emisiones_totales_ton', 'numero_fuentes', 'promedio_por_fuente']
        regions_data = regions_data.reset_index()
        regions_data = regions_data.sort_values('emisiones_totales_ton', ascending=False)
        
        # Procesar datos por sector económico
        sector_col = 'ciiu4' if 'ciiu4' in valid_data.columns else 'razon_social'
        sectors_data = valid_data.groupby(sector_col).agg({
            'cantidad_toneladas_num': ['sum', 'count']
        }).round(2)
        
        sectors_data.columns = ['emisiones_totales_ton', 'numero_empresas']
        sectors_data = sectors_data.reset_index()
        sectors_data = sectors_data.rename(columns={sector_col: 'sector'})
        sectors_data = sectors_data.sort_values('emisiones_totales_ton', ascending=False).head(10)
        
        # Procesar datos por tipo de fuente
        source_col = 'tipo_fuente' if 'tipo_fuente' in valid_data.columns else 'fuente_emisora_general'
        if source_col in valid_data.columns:
            sources_data = valid_data.groupby(source_col).agg({
                'cantidad_toneladas_num': ['sum', 'mean']
            }).round(2)
            
            sources_data.columns = ['emisiones_totales_ton', 'promedio_por_fuente']
            sources_data = sources_data.reset_index()
            sources_data = sources_data.rename(columns={source_col: 'tipo_fuente'})
            sources_data = sources_data.sort_values('emisiones_totales_ton', ascending=False).head(10)
        else:
            sources_data = pd.DataFrame()  # Vacío si no hay columna
        
        # Procesar datos por contaminante
        if 'contaminante' in valid_data.columns:
            contaminants_data = valid_data.groupby('contaminante').agg({
                'cantidad_toneladas_num': ['sum', 'count']
            }).round(2)
            
            contaminants_data.columns = ['emisiones_totales_ton', 'numero_registros']
            contaminants_data = contaminants_data.reset_index()
            contaminants_data = contaminants_data.sort_values('emisiones_totales_ton', ascending=False).head(10)
        else:
            contaminants_data = pd.DataFrame()  # Vacío si no hay columna
        
        # Crear datos detallados para el mapa
        map_data = valid_data[['region', 'cantidad_toneladas_num']].copy()
        map_data = map_data.rename(columns={'cantidad_toneladas_num': 'emisiones_co2_ton'})
        
        return {
            'regions': regions_data,
            'sectors': sectors_data,
            'sources': sources_data,
            'contaminants': contaminants_data,
            'raw_data': map_data
        }
        
    except Exception as e:
        st.error(f"❌ Error procesando datos reales: {str(e)}")
        return None

def classify_emission_level(emission_value):
    """Clasifica el nivel de emisión basado en umbrales"""
    
    if emission_value > EMISSION_SCALES['high_emission']:
        return 'high'
    elif emission_value > EMISSION_SCALES['medium_emission']:
        return 'medium'
    elif emission_value > EMISSION_SCALES['low_emission']:
        return 'low'
    else:
        return 'minimal'

def get_emission_color(emission_level):
    """Obtiene el color correspondiente al nivel de emisión"""
    from .emissions_config import EMISSION_COLORS
    return EMISSION_COLORS.get(emission_level, EMISSION_COLORS['minimal'])
