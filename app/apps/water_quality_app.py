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

# Agregar el directorio de apps al path para imports
sys.path.insert(0, str(Path(__file__).parent))

# Importar configuración y utilidades modularizadas
from modules.config import COLORS, MAP_CONFIG, DEMO_STATIONS
from modules.water_quality_config import WATER_QUALITY_PARAMETERS, QUALITY_CLASSIFICATION
from modules.data_loaders import load_water_quality_data
from modules.water_quality import calculate_water_quality_index, get_water_quality_summary_statistics
from modules.chart_utils import create_temporal_chart, create_station_comparison_chart
from modules.map_utils import create_interactive_water_quality_map

# CSS personalizado optimizado
st.markdown("""
<style>
    /* CORRECCIÓN DE ESPACIADO PRINCIPAL */
    .main-header {
        background: linear-gradient(90deg, #0891b2, #06b6d4);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* CONTENEDOR DE MAPA OPTIMIZADO */
    .map-container {
        margin: 1rem 0;
        padding: 0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* ELIMINAR ESPACIOS EXCESIVOS DESPUÉS DEL MAPA */
    .streamlit-expanderHeader {
        margin-top: 0.5rem !important;
    }
    
    /* MÉTRICAS COMPACTAS */
    .metric-card {
        background: #f8fafc;
        padding: 0.8rem;
        border-radius: 8px;
        border-left: 4px solid #0891b2;
        margin: 0.3rem 0;
    }
    
    /* INFO BOXES SIN ESPACIOS EXCESIVOS */
    .info-box {
        background: #eff6ff;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #dbeafe;
        margin: 0.5rem 0;
    }
    
    .warning-box {
        background: #fef3c7;
        padding: 0.8rem;
        border-radius: 8px;
        border: 1px solid #fbbf24;
        margin: 0.5rem 0;
    }
    
    /* CONTENEDOR DE COLUMNAS SIN ESPACIOS */
    .row-widget.stHorizontal > div {
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    
    /* GRÁFICOS PLOTLY COMPACTOS */
    .js-plotly-plot {
        margin: 0.5rem 0 !important;
    }
    
    /* DATAFRAMES COMPACTOS */
    .dataframe {
        margin: 0.5rem 0;
    }
    
    /* SIDEBAR OPTIMIZADA */
    .sidebar .sidebar-content {
        background: #f1f5f9;
        padding-top: 1rem;
    }
    
    /* BOTONES Y CONTROLES COMPACTOS */
    .stSelectbox, .stMultiSelect, .stSlider {
        margin-bottom: 0.5rem;
    }
    
    /* SEPARADORES MINIMALISTAS */
    hr {
        margin: 1rem 0;
        border: none;
        border-top: 1px solid #e2e8f0;
    }
    
    /* FOLIUM MAP SIN MÁRGENES EXTRA */
    iframe[src*="folium"] {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* CONTENEDOR PRINCIPAL COMPACTO */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* TÍTULOS CON ESPACIADO CONTROLADO */
    h1, h2, h3 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* ELIMINACIÓN DE ESPACIAMENTO INNECESARIO ENTRE SECCIONES */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)

class WaterQualityApp:
    def __init__(self):
        self.data = None
        self.filtered_data = None
        self.is_official_data = False
        
    def load_data(self):
        """Carga los datos usando las utilidades"""
        self.data, self.is_official_data = load_water_quality_data()
        return self.data is not None
        
    def render_header(self):
        """Renderiza el encabezado principal"""
        st.markdown("""
        <div class="main-header">
            <h1>🌊 Sistema Informativo de Calidad del Agua en Chile</h1>
            <p>Análisis interactivo de datos oficiales de la Dirección General de Aguas (DGA)</p>
            <p><strong>Lagos, Lagunas y Embalses | Monitoreo Nacional</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    def render_sidebar(self):
        """Renderiza la barra lateral con controles"""
        st.sidebar.header("🎛️ Panel de Control")
        
        # Información del sistema
        with st.sidebar.expander("ℹ️ Información del Sistema", expanded=False):
            data_source = "🟢 Datos Oficiales DGA" if self.is_official_data else "🟡 Datos de Demostración"
            st.markdown(f"""
            - **Fuente**: {data_source}
            - **Cobertura**: Nacional (Chile)
            - **Tipo**: Lagos, lagunas y embalses  
            - **Actualización**: Tiempo real
            - **Parámetros**: Físico-químicos
            """)
        
        # Filtros temporales
        st.sidebar.subheader("📅 Filtros Temporales")
        
        if self.data is not None and 'año' in self.data.columns:
            min_year = int(self.data['año'].min())
            max_year = int(self.data['año'].max())
            
            year_range = st.sidebar.slider(
                "Rango de años",
                min_value=min_year,
                max_value=max_year,
                value=(max_year-2, max_year),
                step=1
            )
        else:
            year_range = (2022, 2024)
            
        # Filtros de estación
        st.sidebar.subheader("🗺️ Filtros Geográficos")
        
        if self.data is not None and 'GLS_ESTACION' in self.data.columns:
            available_stations = sorted(self.data['GLS_ESTACION'].dropna().unique())
            selected_stations = st.sidebar.multiselect(
                "Seleccionar estaciones",
                options=available_stations,
                default=available_stations[:5] if len(available_stations) > 5 else available_stations
            )
        else:
            selected_stations = []
            
        # Filtros de parámetros
        st.sidebar.subheader("🧪 Parámetros de Análisis")
        
        available_params = [param for param in WATER_QUALITY_PARAMETERS.keys() 
                          if param in self.data.columns] if self.data is not None else []
        
        selected_parameters = st.sidebar.multiselect(
            "Parámetros a analizar",
            options=available_params,
            default=available_params[:3] if len(available_params) > 3 else available_params,
            format_func=lambda x: WATER_QUALITY_PARAMETERS.get(x, {}).get('name', x)
        )
        
        return {
            'year_range': year_range,
            'stations': selected_stations,
            'parameters': selected_parameters
        }
        
    def apply_filters(self, filters):
        """Aplica los filtros seleccionados a los datos"""
        if self.data is None:
            return
            
        filtered = self.data.copy()
        
        # Filtro temporal
        if 'año' in filtered.columns:
            filtered = filtered[
                (filtered['año'] >= filters['year_range'][0]) & 
                (filtered['año'] <= filters['year_range'][1])
            ]
            
        # Filtro de estaciones
        if filters['stations'] and 'GLS_ESTACION' in filtered.columns:
            filtered = filtered[filtered['GLS_ESTACION'].isin(filters['stations'])]
            
        self.filtered_data = filtered
        
    def render_overview_metrics(self):
        """Renderiza métricas generales del sistema"""
        if self.filtered_data is None:
            return
            
        st.subheader("📊 Resumen Ejecutivo del Monitoreo")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_records = len(self.filtered_data)
            st.metric(
                label="🔬 Total de Mediciones",
                value=f"{total_records:,}",
                help="Número total de registros en el período seleccionado"
            )
            
        with col2:
            if 'GLS_ESTACION' in self.filtered_data.columns:
                unique_stations = self.filtered_data['GLS_ESTACION'].nunique()
                st.metric(
                    label="🗺️ Estaciones Activas",
                    value=f"{unique_stations}",
                    help="Estaciones de monitoreo con datos en el período"
                )
            
        with col3:
            if 'año' in self.filtered_data.columns:
                years_span = self.filtered_data['año'].max() - self.filtered_data['año'].min() + 1
                st.metric(
                    label="📅 Años de Cobertura",
                    value=f"{years_span}",
                    help="Período temporal cubierto por los datos"
                )
                
        with col4:
            # Calcular parámetros con datos
            numeric_cols = self.filtered_data.select_dtypes(include=[np.number]).columns
            params_with_data = sum(1 for col in numeric_cols if self.filtered_data[col].notna().sum() > 0)
            st.metric(
                label="🧪 Parámetros Monitoreados",
                value=f"{params_with_data}",
                help="Parámetros físico-químicos con datos disponibles"            )
            
    def render_temporal_analysis(self, filters):
        """Renderiza análisis temporal usando utilidades"""
        if self.filtered_data is None or not filters['parameters']:
            return
            
        st.subheader("📈 Análisis Temporal de Parámetros")
        
        # Seleccionar parámetro para análisis temporal detallado
        param_for_temporal = st.selectbox(
            "Selecciona parámetro para análisis temporal:",
            options=filters['parameters'],
            format_func=lambda x: WATER_QUALITY_PARAMETERS.get(x, {}).get('name', x),
            key="temporal_param"
        )
        
        if param_for_temporal:
            # Verificar que tengamos datos y columnas necesarias
            if self.filtered_data is not None and len(self.filtered_data) > 0:
                # Asegurar que tenemos las columnas de tiempo
                data_for_chart = self.filtered_data.copy()
                
                # Si no tenemos año/mes pero sí FEC_MEDICION, crearlas
                if ('año' not in data_for_chart.columns or 'mes' not in data_for_chart.columns) and 'FEC_MEDICION' in data_for_chart.columns:
                    try:
                        data_for_chart['FEC_MEDICION'] = pd.to_datetime(data_for_chart['FEC_MEDICION'])
                        data_for_chart['año'] = data_for_chart['FEC_MEDICION'].dt.year
                        data_for_chart['mes'] = data_for_chart['FEC_MEDICION'].dt.month
                    except:
                        st.warning("⚠️ No se pudo procesar la información temporal")
                        return
                
                # Crear gráfico temporal usando utilidades
                fig = create_temporal_chart(
                    data_for_chart, 
                    param_for_temporal,
                    WATER_QUALITY_PARAMETERS.get(param_for_temporal, {}).get('name', param_for_temporal)
                )
            else:
                fig = None
            
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                  # Estadísticas del parámetro
                stats = get_water_quality_summary_statistics(self.filtered_data, [param_for_temporal])
                if param_for_temporal in stats:
                    param_stats = stats[param_for_temporal]
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Promedio",
                            f"{param_stats['mean']:.2f} {param_stats['unit']}",
                            help="Valor promedio en el período seleccionado"
                        )
                    
                    with col2:
                        st.metric(
                            "Mediana", 
                            f"{param_stats['median']:.2f} {param_stats['unit']}",
                            help="Valor mediano (percentil 50)"
                        )
                    
                    with col3:
                        st.metric(
                            "Rango",
                            f"{param_stats['min']:.1f} - {param_stats['max']:.1f}",
                            help="Valores mínimo y máximo registrados"
                        )
                    
                    with col4:
                        if 'percent_optimal' in param_stats:
                            st.metric(
                                "% Óptimo",
                                f"{param_stats['percent_optimal']:.1f}%",
                                help="Porcentaje de mediciones en rango óptimo"
                            )
        
        # Análisis estacional
        if 'mes' in self.filtered_data.columns and filters['parameters']:
            st.subheader("📅 Patrones Estacionales")
            
            seasonal_param = st.selectbox(
                "Parámetro para análisis estacional:",
                options=filters['parameters'],
                format_func=lambda x: WATER_QUALITY_PARAMETERS.get(x, {}).get('name', x),
                key="seasonal_param"
            )
            
            if seasonal_param in self.filtered_data.columns:
                # Datos estacionales
                seasonal_data = self.filtered_data.groupby('mes')[seasonal_param].agg(['mean', 'std', 'count']).reset_index()
                
                # Nombres de meses
                month_names = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                             'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
                seasonal_data['mes_nombre'] = seasonal_data['mes'].map(lambda x: month_names[x-1])
                
                fig_seasonal = go.Figure()
                
                fig_seasonal.add_trace(go.Scatter(
                    x=seasonal_data['mes_nombre'],
                    y=seasonal_data['mean'],
                    mode='lines+markers',
                    name='Promedio mensual',
                    line=dict(width=3, color=COLORS['primary']),
                    marker=dict(size=8),
                    error_y=dict(type='data', array=seasonal_data['std'], visible=True),
                    hovertemplate="<b>%{x}</b><br>" +
                                "Promedio: %{y:.2f}<br>" +
                                "Desv. Est.: %{error_y.array:.2f}<br>" +
                                "N° mediciones: %{customdata}<br>" +
                                "<extra></extra>",
                    customdata=seasonal_data['count']
                ))
                
                param_info = WATER_QUALITY_PARAMETERS.get(seasonal_param, {})
                
                fig_seasonal.update_layout(
                    title=f"Variación Estacional - {param_info.get('name', seasonal_param)}",
                    xaxis_title="Mes",
                    yaxis_title=f"{param_info.get('name', seasonal_param)} ({param_info.get('unit', '')})",
                    height=400,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig_seasonal, use_container_width=True)
                
    def render_spatial_analysis(self, filters):
        """Renderiza análisis espacial"""
        if self.filtered_data is None:
            return
            
        st.subheader("🗺️ Análisis Espacial por Estaciones")
        
        if 'GLS_ESTACION' in self.filtered_data.columns and filters['stations']:
            # Análisis por estación
            station_summary = []
            
            for station in filters['stations']:
                station_data = self.filtered_data[self.filtered_data['GLS_ESTACION'] == station]
                
                if len(station_data) > 0:
                    summary = {
                        'Estación': station,
                        'N° Mediciones': len(station_data),
                        'Período': f"{station_data['año'].min()}-{station_data['año'].max()}"
                    }
                    
                    # Agregar estadísticas de parámetros seleccionados
                    for param in filters['parameters']:
                        if param in station_data.columns:
                            param_info = WATER_QUALITY_PARAMETERS.get(param, {})
                            param_name = param_info.get('name', param)
                            unit = param_info.get('unit', '')
                            
                            mean_val = station_data[param].mean()
                            std_val = station_data[param].std()
                            
                            if not pd.isna(mean_val):
                                summary[f'{param_name} (promedio)'] = f"{mean_val:.2f} {unit}"
                                summary[f'{param_name} (desv. est.)'] = f"{std_val:.2f} {unit}"
                    
                    station_summary.append(summary)
            
            if station_summary:
                summary_df = pd.DataFrame(station_summary)
                st.dataframe(summary_df, use_container_width=True)
                
                # Gráfico comparativo por estaciones
                if filters['parameters']:
                    param_for_comparison = st.selectbox(
                        "Parámetro para comparación entre estaciones:",
                        options=filters['parameters'],
                        format_func=lambda x: WATER_QUALITY_PARAMETERS.get(x, {}).get('name', x),
                        key="spatial_param"
                    )
                    
                    if param_for_comparison in self.filtered_data.columns:
                        # Usar utilidad para crear gráfico de comparación
                        fig_comparison = create_station_comparison_chart(
                            self.filtered_data, 
                            param_for_comparison, 
                            filters['stations']
                        )
                        
                        if fig_comparison:
                            st.plotly_chart(fig_comparison, use_container_width=True)
                        
    def render_quality_assessment(self, filters):
        """Renderiza evaluación de calidad del agua"""
        if self.filtered_data is None or not filters['parameters']:
            return
            
        st.subheader("⚡ Evaluación de Calidad del Agua")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Indicadores de Calidad")
            
            for param in filters['parameters']:
                if param in QUALITY_CLASSIFICATION and param in self.filtered_data.columns:
                    values = self.filtered_data[param].dropna()
                    
                    if len(values) > 0:
                        param_info = WATER_QUALITY_PARAMETERS.get(param, {})
                        param_name = param_info.get('name', param)
                        ranges = QUALITY_CLASSIFICATION[param]
                        
                        # Calcular porcentajes por categoría
                        excellent = sum((values >= ranges['Excelente'][0]) & (values <= ranges['Excelente'][1])) / len(values) * 100
                        good = sum((values >= ranges['Buena'][0]) & (values <= ranges['Buena'][1]) & 
                                 ~((values >= ranges['Excelente'][0]) & (values <= ranges['Excelente'][1]))) / len(values) * 100
                        
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{param_name}</h4>
                            <p>🟢 Excelente: {excellent:.1f}%</p>
                            <p>🟡 Buena: {good:.1f}%</p>
                            <p>📊 Mediciones: {len(values):,}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
        with col2:
            # Gráfico de distribución de calidad
            quality_param = st.selectbox(
                "Seleccionar parámetro para distribución:",
                options=[p for p in filters['parameters'] if p in QUALITY_CLASSIFICATION],
                format_func=lambda x: WATER_QUALITY_PARAMETERS.get(x, {}).get('name', x),
                key="quality_param"
            )
            
            if quality_param and quality_param in self.filtered_data.columns:
                values = self.filtered_data[quality_param].dropna()
                
                if len(values) > 0:
                    fig_quality = go.Figure()
                    
                    fig_quality.add_trace(go.Histogram(
                        x=values,
                        nbinsx=30,
                        name='Distribución',
                        marker_color=COLORS['primary'],
                        opacity=0.7
                    ))
                      # Agregar líneas de referencia
                    if quality_param in QUALITY_CLASSIFICATION:
                        ranges = QUALITY_CLASSIFICATION[quality_param]
                        excellent_range = ranges.get('Excelente', (None, None))
                        
                        if excellent_range[0] is not None:
                            fig_quality.add_vline(x=excellent_range[0], line_dash="dash", line_color="green", 
                                                annotation_text="Mínimo excelente")
                        if excellent_range[1] is not None:
                            fig_quality.add_vline(x=excellent_range[1], line_dash="dash", line_color="green",
                                                annotation_text="Máximo excelente")
                    
                    param_info = WATER_QUALITY_PARAMETERS.get(quality_param, {})
                    
                    fig_quality.update_layout(
                        title=f"Distribución de Valores - {param_info.get('name', quality_param)}",
                        xaxis_title=f"{param_info.get('name', quality_param)} ({param_info.get('unit', '')})",
                        yaxis_title="Frecuencia",
                        height=400,
                        template='plotly_white'                    )
                    st.plotly_chart(fig_quality, use_container_width=True)
                
    def render_map_visualization(self, filters):
        """Renderiza visualización de mapa mejorada e interactiva"""
        st.subheader("🗺️ Mapa Interactivo de Estaciones de Monitoreo")
        
        try:
            # Información del mapa
            st.markdown("""
            <div class="info-box" style="margin: 0.5rem 0;">
                <h4 style="margin: 0.5rem 0; color: #0891b2;">🎯 Información del Mapa</h4>
                <ul style="margin: 0.3rem 0; padding-left: 1.2rem;">
                    <li><strong>Marcadores azules</strong>: Estaciones de monitoreo activas</li>
                    <li><strong>Clusters</strong>: Agrupación automática para mejor visualización</li>
                    <li>💡 <em>Haz click en los marcadores para ver estadísticas detalladas</em></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if not filters.get('stations'):
                st.warning("⚠️ Selecciona al menos una estación en la barra lateral para ver el mapa")
                return
            
            # Validar datos
            if self.filtered_data is None or self.filtered_data.empty:
                st.error("❌ No hay datos disponibles para mostrar en el mapa")
                return
                
            # Crear y mostrar el mapa
            with st.spinner("🗺️ Generando mapa interactivo..."):
                water_map = create_interactive_water_quality_map(self.filtered_data, filters)
                
                if water_map:
                    # Contenedor optimizado para el mapa
                    st.markdown(
                        '<div class="map-container" style="margin:1rem 0; padding:0; border-radius:8px; overflow:hidden;">',
                        unsafe_allow_html=True
                    )
                    
                    # Mostrar mapa con dimensiones específicas
                    map_data = st_folium(
                        water_map,
                        width=800,
                        height=600,
                        returned_objects=["last_active_drawing", "last_clicked"]
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Procesar interacciones
                    if map_data and map_data.get("last_clicked"):
                        lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
                        st.info(f"📍 Coordenadas seleccionadas: {lat:.4f}, {lon:.4f}")
        
        except Exception as e:
            st.error(f"❌ Error al renderizar el mapa: {str(e)}")
            import traceback
            st.error(f"Detalles: {traceback.format_exc()}")
                
    def render_data_explorer(self):
        """Renderiza el explorador de datos"""
        if self.filtered_data is None:
            return
            
        st.subheader("🔍 Explorador de Datos")
        
        with st.expander("📋 Ver datos filtrados", expanded=False):
            st.markdown(f"**Total de registros mostrados:** {len(self.filtered_data):,}")
            
            # Seleccionar columnas a mostrar
            available_cols = self.filtered_data.columns.tolist()
            default_cols = ['GLS_ESTACION', 'FEC_MEDICION'] + [col for col in WATER_QUALITY_PARAMETERS.keys() if col in available_cols]
            
            display_cols = st.multiselect(
                "Seleccionar columnas a mostrar:",
                options=available_cols,
                default=default_cols[:8] if len(default_cols) > 8 else default_cols
            )
            
            if display_cols:
                st.dataframe(
                    self.filtered_data[display_cols].head(1000),
                    use_container_width=True
                )
                
                # Opción de descarga
                csv = self.filtered_data[display_cols].to_csv(index=False)
                st.download_button(
                    label="📥 Descargar datos filtrados (CSV)",
                    data=csv,
                    file_name=f"calidad_agua_chile_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
                
    def render_methodology(self):
        """Renderiza información metodológica"""
        with st.expander("📖 Metodología y Fuentes", expanded=False):
            st.markdown("""
            ### 🔬 Metodología de Análisis
            
            **Fuente de Datos:**
            - Dirección General de Aguas (DGA) - Gobierno de Chile
            - Portal de datos abiertos del gobierno
            - Monitoreo oficial de lagos, lagunas y embalses
            
            **Parámetros Analizados:**
            - **pH**: Potencial de hidrógeno (acidez/basicidad)
            - **Temperatura**: Temperatura del agua en °C
            - **Conductividad**: Capacidad de conducir electricidad (µS/cm)
            - **Oxígeno Disuelto**: Porcentaje de saturación
            - **Turbiedad**: Claridad del agua (NTU)
            - **Sólidos Suspendidos**: Partículas en suspensión (mg/L)
            
            **Criterios de Calidad:**
            - Basados en estándares nacionales e internacionales
            - Norma Chilena NCh 409/1.Of2005
            - Guías WHO para calidad del agua
            
            **Limitaciones:**
            - Los datos pueden tener gaps temporales
            - La frecuencia de muestreo varía por estación
            - Algunos parámetros pueden no estar disponibles en todas las estaciones
            """)
            
    def run(self):
        """Ejecuta la aplicación principal"""
        # Cargar datos
        if not self.load_data():
            st.info("⚠️ La aplicación está funcionando con datos de demostración")
            
        # Renderizar interfaz
        self.render_header()
        
        # Barra lateral con controles
        filters = self.render_sidebar()
        
        # Aplicar filtros
        self.apply_filters(filters)
        
        # Contenido principal
        if self.filtered_data is not None and len(self.filtered_data) > 0:
            # Métricas generales
            self.render_overview_metrics()
            
            # Separador
            st.markdown("---")
            
            # Análisis temporal
            self.render_temporal_analysis(filters)
            
            # Separador
            st.markdown("---")
            
            # Análisis espacial
            self.render_spatial_analysis(filters)
            
            # Separador
            st.markdown("---")
            
            # Evaluación de calidad
            self.render_quality_assessment(filters)
            
            # Separador
            st.markdown("---")
            
            # Mapa
            self.render_map_visualization(filters)
            
            # Separador
            st.markdown("---")
            
            # Explorador de datos
            self.render_data_explorer()
            
            # Metodología
            self.render_methodology()
            
        else:
            st.error("❌ No hay datos disponibles para mostrar con los filtros seleccionados")
            st.info("💡 Intenta ampliar los rangos de fechas o seleccionar más estaciones")
            
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #64748b; padding: 1rem;'>
            🌊 <strong>Sistema Informativo de Calidad del Agua en Chile</strong><br>
            Desarrollado como parte del DS Portfolio | Datos: Dirección General de Aguas (DGA)<br>
            <em>Última actualización: {}</em>
        </div>
        """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)

# Ejecutar aplicación
if __name__ == "__main__":
    # Configurar página solo si se ejecuta directamente
    st.set_page_config(
        page_title="🌊 Calidad del Agua en Chile - Sistema Informativo",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    app = WaterQualityApp()
    app.run()
