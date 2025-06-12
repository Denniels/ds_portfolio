"""
Aplicación de Análisis de Emisiones CO2 en Chile
==============================================

Aplicación basada en el análisis del RETC (Registro de Emisiones y Transferencias 
de Contaminantes) para visualizar y analizar las emisiones de gases de efecto 
invernadero en Chile.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import st_folium
from datetime import datetime
import os
import sys
from pathlib import Path

# Importar configuraciones y utilidades modularizadas
from modules.config import CHILE_REGIONS, MAP_CONFIG
from modules.emissions_config import CO2_EMISSION_SECTORS, POLLUTANT_TYPES, EMISSION_SCALES, EMISSION_COLORS
from modules.data_loaders import load_emissions_data
from modules.emissions import create_demo_emissions_data, process_real_emissions_data, classify_emission_level, get_emission_color
from modules.map_utils import create_interactive_emissions_map

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #dc2626, #ef4444);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #dc2626;
        margin-bottom: 1rem;
    }
    
    .insight-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .insight-box h4 {
        color: #dc2626;
        margin-top: 0;
    }
    
    .warning-box {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .warning-box h4 {
        color: #ea580c;
        margin-top: 0;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f8fafc;
        border-radius: 8px 8px 0 0;
        border: 1px solid #e2e8f0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #dc2626;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

class CO2EmissionsApp:
    """Aplicación principal para análisis de emisiones CO2"""
    
    def __init__(self):
        self.data = None
        self.filtered_data = None        # Configuración de datos de demostración basada en el análisis del RETC
        self.demo_data = create_demo_emissions_data()
        
    def load_data(self):
        """Intenta cargar datos reales, usa demo si no están disponibles"""
        try:
            # Intentar cargar datos del archivo CSV del RETC
            data_path = Path.cwd().parent / 'data' / 'raw' / 'retc_emisiones_aire_2023.csv'
            
            if data_path.exists():                # Leer CSV con parámetros específicos para el formato RETC
                raw_data = pd.read_csv(
                    data_path,
                    sep=';',  # Separador punto y coma
                    encoding='utf-8',  # Encoding UTF-8
                    low_memory=False,  # Para archivos grandes
                    on_bad_lines='skip'  # Saltar líneas mal formateadas (pandas 1.3+)
                )                # Procesar datos reales para crear estructura similar a demo_data
                self.data = process_real_emissions_data(raw_data)
                st.success(f"✅ Datos reales cargados: {len(raw_data):,} registros del RETC 2023")
                return True
            else:
                st.info("📊 Usando datos de demostración basados en el análisis del RETC 2023")
                self.data = self.demo_data
                return False                
        except Exception as e:
            st.warning(f"⚠️ Error al cargar datos: {str(e)}. Usando datos de demostración.")
            self.data = self.demo_data
            return False

    def render_header(self):
        """Renderiza el header principal"""
        st.markdown("""
        <div class="main-header">
            <h1>🏭 Análisis de Emisiones CO2 en Chile</h1>
            <p>Registro de Emisiones y Transferencias de Contaminantes (RETC) - 2023</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Información contextual
        st.markdown("""
        ### 📋 Sobre este Análisis
        
        Este dashboard presenta un análisis comprehensivo de las **emisiones de gases de efecto invernadero en Chile** 
        basado en datos oficiales del **RETC (Registro de Emisiones y Transferencias de Contaminantes)** del 
        Ministerio del Medio Ambiente.
        
        **Características del dataset:**
        - 📊 **285,403 registros** de emisiones
        - 🏭 **285 sectores económicos** (clasificación CIIU4)
        - 🌍 **16 regiones** de Chile
        - ☢️ **16 tipos de contaminantes**
        - 📅 **Año 2023** (datos más recientes disponibles)
        """)
    
    def render_overview_metrics(self):
        """Renderiza métricas generales"""
        
        if isinstance(self.data, dict):
            # Datos de demostración
            total_emissions = self.data['regions']['emisiones_totales_ton'].sum()
            total_sources = self.data['regions']['numero_fuentes'].sum()
            avg_emission = total_emissions / total_sources
            top_region = self.data['regions'].loc[0, 'region']
            
        else:
            # Datos reales (si están disponibles)
            total_emissions = 167000000  # Aproximado basado en análisis
            total_sources = 285403
            avg_emission = total_emissions / total_sources
            top_region = "Antofagasta"
        
        st.subheader("📊 Métricas Generales del RETC 2023")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #dc2626; margin: 0;">{total_emissions:,.0f}</h3>
                <p style="margin: 0; color: #64748b;">Toneladas CO2 eq/año</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #dc2626; margin: 0;">{total_sources:,}</h3>
                <p style="margin: 0; color: #64748b;">Fuentes Emisoras</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #dc2626; margin: 0;">{avg_emission:.1f}</h3>
                <p style="margin: 0; color: #64748b;">Promedio por Fuente (ton/año)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="color: #dc2626; margin: 0;">{top_region}</h3>
                <p style="margin: 0; color: #64748b;">Región con Mayor Emisión</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_regional_analysis(self):
        """Renderiza análisis por región"""
        st.subheader("🗺️ Análisis Regional de Emisiones")
        
        regions_df = self.data['regions']
        
        # Gráfico de emisiones por región
        fig_regions = px.bar(
            regions_df,
            x='region',
            y='emisiones_totales_ton',
            title='Emisiones Totales por Región (toneladas CO2 eq/año)',
            color='emisiones_totales_ton',
            color_continuous_scale='Reds'
        )
        
        fig_regions.update_layout(
            xaxis_tickangle=-45,
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_regions, use_container_width=True)
        
        # Insights regionales
        top_3_regions = regions_df.head(3)
        total_top_3 = top_3_regions['emisiones_totales_ton'].sum()
        total_emissions = regions_df['emisiones_totales_ton'].sum()
        percentage_top_3 = (total_top_3 / total_emissions) * 100
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>🔍 Insights Regionales Clave</h4>
            <ul>
                <li><strong>Concentración geográfica:</strong> Las 3 regiones con mayores emisiones 
                ({', '.join(top_3_regions['region'].tolist())}) representan el {percentage_top_3:.1f}% 
                del total nacional</li>
                <li><strong>Antofagasta lidera:</strong> Con {regions_df.iloc[0]['emisiones_totales_ton']:,.0f} 
                toneladas CO2 eq/año, principalmente por la minería del cobre</li>
                <li><strong>Santiago metropolitano:</strong> Segunda posición con 
                {regions_df.iloc[1]['emisiones_totales_ton']:,.0f} toneladas, 
                debido a la alta densidad industrial y poblacional</li>
                <li><strong>Biobío industrial:</strong> Tercera posición con 
                {regions_df.iloc[2]['emisiones_totales_ton']:,.0f} toneladas, 
                por su importante sector forestal e industrial</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Mapa de Chile (simplificado)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Gráfico de dispersión emisiones vs número de fuentes
            fig_scatter = px.scatter(
                regions_df,
                x='numero_fuentes',
                y='emisiones_totales_ton',
                size='promedio_por_fuente',
                hover_name='region',
                title='Relación entre Número de Fuentes y Emisiones Totales',
                labels={
                    'numero_fuentes': 'Número de Fuentes Emisoras',
                    'emisiones_totales_ton': 'Emisiones Totales (ton CO2 eq/año)',
                    'promedio_por_fuente': 'Promedio por Fuente'
                }
            )
            fig_scatter.update_layout(template='plotly_white')
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Top 5 Regiones")
            top_5 = regions_df.head(5)
            for idx, row in top_5.iterrows():
                percentage = (row['emisiones_totales_ton'] / total_emissions) * 100
                st.markdown(f"""
                **{idx + 1}. {row['region']}**  
                {row['emisiones_totales_ton']:,.0f} ton CO2 eq  
                ({percentage:.1f}% del total nacional)
                """)
    
    def render_sectoral_analysis(self):
        """Renderiza análisis por sector económico"""
        st.subheader("🏭 Análisis Sectorial (Clasificación CIIU4)")
        
        sectors_df = self.data['sectors']
        
        # Gráfico de sectores
        fig_sectors = px.treemap(
            sectors_df,
            path=['sector'],
            values='emisiones_totales_ton',
            title='Distribución de Emisiones por Sector Económico',
            color='emisiones_totales_ton',
            color_continuous_scale='Reds'
        )
        
        fig_sectors.update_layout(height=500)
        st.plotly_chart(fig_sectors, use_container_width=True)
        
        # Análisis sectorial detallado
        col1, col2 = st.columns(2)
        
        with col1:
            # Top sectores
            fig_top_sectors = px.bar(
                sectors_df.head(5),
                x='emisiones_totales_ton',
                y='sector',
                orientation='h',
                title='Top 5 Sectores por Emisiones',
                color='emisiones_totales_ton',
                color_continuous_scale='Reds'
            )
            fig_top_sectors.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_top_sectors, use_container_width=True)
        
        with col2:
            # Número de empresas por sector
            fig_companies = px.bar(
                sectors_df.head(5),
                x='numero_empresas',
                y='sector',
                orientation='h',
                title='Top 5 Sectores por Número de Empresas',
                color='numero_empresas',
                color_continuous_scale='Blues'
            )
            fig_companies.update_layout(template='plotly_white', height=400)
            st.plotly_chart(fig_companies, use_container_width=True)
        
        # Insights sectoriales
        top_sector = sectors_df.iloc[0]
        total_sectoral = sectors_df['emisiones_totales_ton'].sum()
        top_percentage = (top_sector['emisiones_totales_ton'] / total_sectoral) * 100
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>🏭 Insights Sectoriales Clave</h4>
            <ul>
                <li><strong>Sector energético domina:</strong> {top_sector['sector']} representa 
                el {top_percentage:.1f}% de las emisiones sectoriales</li>
                <li><strong>Minería del cobre:</strong> Segundo sector más contaminante, 
                refleja la importancia económica pero impacto ambiental</li>
                <li><strong>Metalurgia:</strong> Fundición de metales no ferrosos en tercera posición, 
                indica procesos industriales intensivos en energía</li>
                <li><strong>Distribución atomizada:</strong> Muchas pequeñas fuentes (panaderías, hospitales) 
                suman un impacto considerable</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sources_analysis(self):
        """Renderiza análisis por tipo de fuente"""
        st.subheader("⚙️ Análisis por Tipo de Fuente Emisora")
        
        sources_df = self.data['sources']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico circular de tipos de fuente
            fig_pie = px.pie(
                sources_df.head(6),
                values='emisiones_totales_ton',
                names='tipo_fuente',
                title='Distribución de Emisiones por Tipo de Fuente'
            )
            fig_pie.update_layout(template='plotly_white')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Intensidad de emisiones (promedio por fuente)
            fig_intensity = px.bar(
                sources_df.head(6),
                x='promedio_por_fuente',
                y='tipo_fuente',
                orientation='h',
                title='Intensidad de Emisiones por Tipo de Fuente',
                color='promedio_por_fuente',
                color_continuous_scale='Oranges'
            )
            fig_intensity.update_layout(template='plotly_white')
            st.plotly_chart(fig_intensity, use_container_width=True)
        
        # Análisis de fuentes
        st.markdown(f"""
        <div class="insight-box">
            <h4>⚙️ Insights sobre Tipos de Fuente</h4>
            <ul>
                <li><strong>Calderas industriales:</strong> Principal tipo de fuente emisora, 
                {sources_df.iloc[0]['emisiones_totales_ton']:,.0f} ton CO2 eq/año</li>
                <li><strong>Hornos de panadería:</strong> Sorprendentemente alto en el ranking, 
                refleja la distribución geográfica extensa</li>
                <li><strong>Grupos electrógenos:</strong> Ampliamente distribuidos, 
                especialmente en zonas remotas sin conexión a la red eléctrica</li>
                <li><strong>Alta variabilidad:</strong> La intensidad por fuente varía dramáticamente 
                entre tipos de equipos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def render_contaminants_analysis(self):
        """Renderiza análisis por contaminante"""
        st.subheader("☢️ Análisis por Tipo de Contaminante")
        
        contaminants_df = self.data['contaminants']
        
        # Gráfico de contaminantes
        fig_cont = px.bar(
            contaminants_df,
            x='contaminante',
            y='emisiones_totales_ton',
            title='Emisiones por Tipo de Contaminante',
            color='emisiones_totales_ton',
            color_continuous_scale='Reds'
        )
        
        fig_cont.update_layout(
            xaxis_tickangle=-45,
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_cont, use_container_width=True)
        
        # Insights de contaminantes
        co2_emissions = contaminants_df.iloc[0]['emisiones_totales_ton']
        total_emissions = contaminants_df['emisiones_totales_ton'].sum()
        co2_percentage = (co2_emissions / total_emissions) * 100
        
        st.markdown(f"""
        <div class="warning-box">
            <h4>☢️ Perfil de Contaminantes</h4>
            <ul>
                <li><strong>CO2 predomina:</strong> {co2_percentage:.1f}% de todas las emisiones 
                corresponden a dióxido de carbono</li>
                <li><strong>Monóxido de carbono:</strong> Segundo contaminante más emitido, 
                indica combustión incompleta</li>
                <li><strong>Óxidos de nitrógeno (NOx):</strong> Importantes para la formación 
                de smog y lluvia ácida</li>
                <li><strong>Material particulado:</strong> PM10 y PM2.5 críticos para 
                la salud respiratoria urbana</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    def render_insights_conclusions(self):
        """Renderiza conclusiones e insights principales"""
        st.subheader("💡 Conclusiones y Recomendaciones")
        
        tab1, tab2, tab3 = st.tabs(["🔍 Principales Hallazgos", "📊 Implicaciones", "🎯 Recomendaciones"])
        
        with tab1:
            st.markdown("""
            ### 🔍 Principales Hallazgos del Análisis RETC 2023
            
            #### Concentración Geográfica
            - **Tres regiones concentran >60% de emisiones:** Antofagasta, Santiago y Biobío
            - **Antofagasta lidera** con 32.3 millones de toneladas CO2 eq/año (19.4% del total nacional)
            - **Patrón minero-industrial** claro en la distribución espacial
            
            #### Dominancia Sectorial
            - **Sector energético** es el mayor emisor, seguido por minería del cobre
            - **Fundición de metales** muestra alta intensidad de emisiones
            - **Sectores atomizados** (panaderías, hospitales) suman impacto considerable
            
            #### Perfil de Fuentes
            - **Calderas industriales** dominan las emisiones totales
            - **Grupos electrógenos** muy distribuidos geográficamente
            - **Alta heterogeneidad** en intensidad de emisiones por tipo de fuente
            
            #### Composición de Contaminantes
            - **CO2 representa ~71%** de todas las emisiones registradas
            - **Óxidos de nitrógeno y azufre** significativos para calidad del aire
            - **Material particulado** crítico en zonas urbanas e industriales
            """)
        
        with tab2:
            st.markdown("""
            ### 📊 Implicaciones para Política Pública
            
            #### Priorización Geográfica
            - **Focalización regional necesaria:** Antofagasta, Santiago y Biobío requieren atención prioritaria
            - **Políticas diferenciadas** según perfil productivo regional
            - **Coordinación interregional** para abordar emisiones de gran escala
            
            #### Transición Energética
            - **Urgencia en descarbonización** del sector eléctrico
            - **Oportunidades en ERNC** especialmente en regiones del norte
            - **Eficiencia energética** crítica en procesos industriales
            
            #### Regulación Sectorial
            - **Estándares más estrictos** para minería y metalurgia
            - **Incentivos para modernización** de equipos industriales
            - **Monitoreo continuo** de grandes emisores
            
            #### Gestión Urbana
            - **Calidad del aire urbano** especialmente en Santiago
            - **Transporte público limpio** para reducir emisiones móviles
            - **Zonas de emisiones controladas** en centros urbanos
            """)
        
        with tab3:
            st.markdown("""
            ### 🎯 Recomendaciones Estratégicas
            
            #### Corto Plazo (1-2 años)
            1. **Fortalecimiento del RETC**
               - Mejorar cobertura y frecuencia de reporte
               - Implementar verificación independiente
               - Integrar con otros sistemas de monitoreo
            
            2. **Medidas Inmediatas**
               - Eficiencia energética en grandes emisores
               - Sustitución de combustibles en calderas
               - Optimización de procesos industriales
            
            #### Mediano Plazo (3-5 años)
            1. **Transición Energética Acelerada**
               - Cierre programado de centrales a carbón
               - Expansión masiva de ERNC
               - Desarrollo de almacenamiento energético
            
            2. **Modernización Industrial**
               - Incentivos para tecnologías limpias
               - Estándares de emisión más estrictos
               - Certificación de procesos sustentables
            
            #### Largo Plazo (5-10 años)
            1. **Transformación Estructural**
               - Economía circular en sectores clave
               - Hidrógeno verde como vector energético
               - Captura y utilización de carbono
            
            2. **Gobernanza Climática**
               - Integración con NDCs y metas de carbono neutralidad
               - Coordinación intersectorial
               - Participación ciudadana en monitoreo
            """)
    
    def render_methodology(self):
        """Renderiza información metodológica"""
        with st.expander("📖 Metodología y Fuentes de Datos", expanded=False):
            st.markdown("""
            ### 🔬 Metodología de Análisis
            
            **Fuente Principal:**
            - **RETC (Registro de Emisiones y Transferencias de Contaminantes)**
            - Ministerio del Medio Ambiente de Chile
            - Datos del año 2023 (más recientes disponibles)
            - URL: https://retc.mma.gob.cl/
            
            **Cobertura del Dataset:**
            - **285,403 registros** individuales de emisiones
            - **16 tipos de contaminantes** monitoreados
            - **285 sectores económicos** (clasificación CIIU4)
            - **16 regiones** de Chile
            - **55 tipos de fuentes emisoras**
            
            **Procesamiento de Datos:**
            - Limpieza y validación de registros
            - Normalización de unidades (toneladas CO2 equivalente/año)
            - Agregación por categorías de análisis
            - Imputación de valores faltantes por mediana sectorial
            
            **Limitaciones:**
            - Datos auto-reportados por empresas
            - Cobertura limitada a establecimientos sujetos a reporte obligatorio
            - Posibles sub-registros en sectores informales
            - Variabilidad en precisión de medición entre sectores
            
            **Estándares de Referencia:**
            - Guidelines IPCC para inventarios de GEI
            - Protocolo de Kioto para equivalencias CO2
            - Normativa nacional chilena de emisiones
            """)
    
    def render_interactive_map(self):
        """Renderiza mapa interactivo de emisiones por región"""
        st.subheader("🗺️ Mapa Interactivo de Emisiones por Región")        
        try:
            # Crear datos para el mapa
            regions_df = self.data['regions'].copy()
            
            # Información del mapa
            st.markdown("""
            <div class="info-box">
                <h4>🎯 Información del Mapa</h4>
                <p>• <strong>Círculos rojos</strong>: Regiones con emisiones > 100,000 ton CO₂</p>
                <p>• <strong>Círculos naranjas</strong>: Emisiones entre 10,000-100,000 ton CO₂</p>
                <p>• <strong>Círculos amarillos</strong>: Emisiones entre 1,000-10,000 ton CO₂</p>
                <p>• <strong>Círculos verdes</strong>: Emisiones < 1,000 ton CO₂</p>
                <p>• <strong>Tamaño del círculo</strong>: Proporcional al nivel de emisiones</p>
                <p>💡 <em>Haz click en los marcadores para ver detalles específicos</em></p>
            </div>
            """, unsafe_allow_html=True)            # Crear el mapa
            # Preparar datos para el mapa usando los datos de regiones
            map_data = regions_df.copy()
            map_data = map_data.rename(columns={'emisiones_totales_ton': 'emisiones_co2_ton'})
            
            emissions_map = create_interactive_emissions_map(
                map_data,
                region_col='region',
                emissions_col='emisiones_co2_ton'
            )
            
            if emissions_map:
                # Mostrar el mapa
                map_data = st_folium(
                    emissions_map, 
                    width=800, 
                    height=600
                )
                
                # Procesar interacciones del mapa
                if map_data.get('last_object_clicked_popup'):
                    st.success(f"🗺️ Región seleccionada: {map_data['last_object_clicked_popup']}")
                
                # Métricas del mapa
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_regions = len(regions_df)
                    st.metric(
                        "📍 Regiones con Datos",
                        total_regions,
                        help="Número total de regiones con datos de emisiones"
                    )
                
                with col2:
                    max_emission_region = regions_df.loc[regions_df['emisiones_totales_ton'].idxmax()]
                    st.metric(
                        "🔥 Región con Mayor Emisión",
                        max_emission_region['region'],
                        f"{max_emission_region['emisiones_totales_ton']:,.0f} ton CO₂",
                        help="Región que produce la mayor cantidad de emisiones"
                    )
                
                with col3:
                    total_sources = regions_df['numero_fuentes'].sum()
                    st.metric(
                        "🏭 Total Fuentes Emisoras",
                        f"{total_sources:,}",
                        help="Número total de instalaciones que reportan emisiones"
                    )
                
                # Análisis adicional del mapa
                st.markdown("---")
                st.subheader("📊 Análisis Geográfico")
                
                # Clasificar regiones por nivel de emisión
                high_emission = regions_df[regions_df['emisiones_totales_ton'] > 100000]
                medium_emission = regions_df[
                    (regions_df['emisiones_totales_ton'] >= 10000) & 
                    (regions_df['emisiones_totales_ton'] <= 100000)
                ]
                low_emission = regions_df[regions_df['emisiones_totales_ton'] < 10000]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🔴 Alto Impacto")
                    st.markdown(f"**{len(high_emission)} regiones**")
                    if len(high_emission) > 0:
                        for _, region in high_emission.iterrows():
                            st.markdown(f"• {region['region']}: {region['emisiones_totales_ton']:,.0f} ton")
                
                with col2:
                    st.markdown("### 🟡 Impacto Medio")
                    st.markdown(f"**{len(medium_emission)} regiones**")
                    if len(medium_emission) > 0:
                        for _, region in medium_emission.iterrows():
                            st.markdown(f"• {region['region']}: {region['emisiones_totales_ton']:,.0f} ton")
                
                with col3:
                    st.markdown("### 🟢 Bajo Impacto")
                    st.markdown(f"**{len(low_emission)} regiones**")
                    if len(low_emission) > 0:
                        for _, region in low_emission.iterrows():
                            st.markdown(f"• {region['region']}: {region['emisiones_totales_ton']:,.0f} ton")
            
            else:
                st.error("❌ No se pudo generar el mapa. Usando datos de demostración.")
                
        except Exception as e:
            st.error(f"❌ Error al cargar el mapa: {e}")
            st.info("💡 El mapa interactivo requiere datos válidos de ubicación.")
    
    def run(self):
        """Ejecuta la aplicación principal"""
        # Cargar datos
        data_loaded = self.load_data()
        
        # Renderizar interfaz
        self.render_header()
        
        # Métricas generales
        self.render_overview_metrics()
        
        # Separador
        st.markdown("---")
          # Crear tabs para diferentes análisis
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🗺️ Análisis Regional", 
            "🌍 Mapa Interactivo",
            "🏭 Análisis Sectorial", 
            "⚙️ Tipos de Fuente",
            "☢️ Contaminantes",
            "💡 Conclusiones"
        ])
        
        with tab1:
            self.render_regional_analysis()
        
        with tab2:
            self.render_interactive_map()
        
        with tab3:
            self.render_sectoral_analysis()
        
        with tab4:
            self.render_sources_analysis()
        
        with tab5:
            self.render_contaminants_analysis()
        
        with tab6:
            self.render_insights_conclusions()
        
        # Metodología
        self.render_methodology()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #64748b; padding: 1rem;'>
            🏭 <strong>Análisis de Emisiones CO2 Chile</strong> | 
            Datos: RETC 2023 - Ministerio del Medio Ambiente | 
            📊 <strong>Portafolio Data Science</strong>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Función principal para ejecutar desde línea de comandos"""
    # Configurar página solo si se ejecuta directamente
    st.set_page_config(
        page_title="🏭 Emisiones CO2 Chile - Análisis RETC",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    app = CO2EmissionsApp()
    app.run()

if __name__ == "__main__":
    main()
