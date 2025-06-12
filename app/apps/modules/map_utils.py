"""
Utilidades para mapas interactivos
==================================
"""

import folium
from folium import plugins
import streamlit as st
import pandas as pd
from .config import MAP_CONFIG, CHILE_REGIONS, DEMO_STATIONS
from .emissions_config import EMISSION_COLORS
from .emissions import classify_emission_level, get_emission_color
from .geo_utils import get_station_coordinates

def create_interactive_water_quality_map(df, filters):
    """Crea un mapa interactivo mejorado para calidad del agua"""
    
    try:
        # Crear mapa centrado en Chile
        m = folium.Map(
            location=MAP_CONFIG['chile_center'],
            zoom_start=MAP_CONFIG['chile_zoom'],
            tiles=None
        )
        
        # Capa base OpenStreetMap
        folium.TileLayer(
            'OpenStreetMap',
            attr='© OpenStreetMap contributors',
            name='OpenStreetMap'
        ).add_to(m)
        
        # Control de capas
        folium.LayerControl().add_to(m)
        
        # Validar datos de entrada
        if not filters.get('stations'):
            st.warning("⚠️ No hay estaciones seleccionadas")
            return m
            
        if 'GLS_ESTACION' not in df.columns:
            st.error("❌ El DataFrame no contiene la columna 'GLS_ESTACION'")
            return m
        
        # Crear clusters para mejor visualización
        marker_cluster = plugins.MarkerCluster(name='Estaciones').add_to(m)
        
        # Procesar cada estación seleccionada
        stations_found = []
        stations_not_found = []
        
        for station in filters['stations']:
            # Obtener coordenadas
            coords = get_station_coordinates(station)
            
            if not coords:
                stations_not_found.append(station)
                continue
            
            # Validar coordenadas para Chile continental e insular
            lat, lon = coords['lat'], coords['lon']
            if not (-56 <= lat <= -17 and -76 <= lon <= -66):
                continue
                
            # Obtener datos de la estación
            station_data = df[df['GLS_ESTACION'] == station]
            if len(station_data) == 0:
                continue
            
            # Crear popup con información detallada
            popup_html = f"""
            <div style='width:300px'>
                <h4 style='margin-bottom:10px'>{station}</h4>
                <table style='width:100%; border-collapse:collapse;'>
                    <tr>
                        <th style='text-align:left; padding:5px;'>Parámetro</th>
                        <th style='text-align:right; padding:5px;'>Último valor</th>
                    </tr>
            """
            
            latest_data = station_data.iloc[-1]
            for param in filters.get('parameters', []):
                if param in station_data.columns:
                    value = latest_data.get(param)
                    if pd.notna(value):
                        param_name = param
                        popup_html += f"""
                        <tr>
                            <td style='padding:5px;'>{param_name}</td>
                            <td style='text-align:right; padding:5px;'>{value:.2f}</td>
                        </tr>
                        """
            
            popup_html += """
                </table>
                <p style='margin-top:10px; font-size:0.9em;'>
                    Última actualización: {latest_data.name.strftime('%Y-%m-%d')}
                </p>
            </div>
            """
            
            # Crear marcador
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_html, max_width=350),
                tooltip=station,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(marker_cluster)
            
            stations_found.append(station)
        
        # Mostrar resumen solo si hay estaciones no encontradas
        if stations_not_found:
            total = len(stations_found) + len(stations_not_found)
            st.info(f"ℹ️ Estaciones visualizadas: {len(stations_found)} de {total}")
            
            # Expandible con detalles de estaciones no encontradas
            with st.expander("📋 Ver estaciones sin coordenadas"):
                st.write("Las siguientes estaciones no pudieron ser ubicadas en el mapa:")
                for station in stations_not_found:
                    st.write(f"- {station}")
        
        return m
        
    except Exception as e:
        st.error(f"❌ Error al crear el mapa: {str(e)}")
        return None

def create_interactive_emissions_map(df, region_col='region', emissions_col='emisiones_co2_ton'):
    """Crea un mapa interactivo de emisiones por región usando Folium"""
    
    try:
        # Crear mapa centrado en Chile
        m = folium.Map(
            location=MAP_CONFIG['chile_center'],
            zoom_start=MAP_CONFIG['chile_zoom'],
            tiles='OpenStreetMap'
        )
        
        # Agregar control de capas
        folium.LayerControl().add_to(m)
        
        # Obtener datos agregados por región
        if region_col in df.columns and emissions_col in df.columns:
            region_data = df.groupby(region_col).agg({
                emissions_col: ['sum', 'count', 'mean']
            }).round(2)
            
            region_data.columns = ['total_emissions', 'num_sources', 'avg_emissions']
            region_data = region_data.reset_index()
            
            # Agregar marcadores para cada región
            for _, row in region_data.iterrows():
                region_name = row[region_col]
                
                if region_name in CHILE_REGIONS:
                    coords = CHILE_REGIONS[region_name]
                    
                    # Determinar color y tamaño basado en emisiones
                    total_emissions = row['total_emissions']
                    num_sources = row['num_sources']
                    avg_emissions = row['avg_emissions']
                    
                    # Clasificar nivel de emisión
                    emission_level = classify_emission_level(total_emissions)
                    color = get_emission_color(emission_level)
                    
                    # Determinar tamaño del marcador
                    if total_emissions > 100000:
                        radius = 20
                    elif total_emissions > 10000:
                        radius = 15
                    elif total_emissions > 1000:
                        radius = 12
                    else:
                        radius = 8
                    
                    # Crear popup con información detallada
                    popup_html = f"""
                    <div style="width: 280px; font-family: Arial, sans-serif;">
                        <div style="background: linear-gradient(90deg, #dc2626, #ef4444); padding: 10px; margin: -10px -10px 10px -10px; border-radius: 5px 5px 0 0;">
                            <h4 style="margin: 0; color: white; text-align: center;">🏭 {region_name}</h4>
                        </div>
                        
                        <div style="padding: 10px 0;">
                            <div style="background: #fef2f2; padding: 8px; margin: 5px 0; border-radius: 5px; border-left: 3px solid #dc2626;">
                                <p style="margin: 0;"><strong>📊 Emisiones Totales:</strong><br>
                                   <span style="font-size: 1.2em; color: #dc2626; font-weight: bold;">{total_emissions:,.1f} ton CO₂ eq/año</span></p>
                            </div>
                            
                            <div style="background: #f8fafc; padding: 8px; margin: 5px 0; border-radius: 5px;">
                                <p style="margin: 3px 0;"><strong>🏢 Fuentes Emisoras:</strong> {num_sources:,} instalaciones</p>
                                <p style="margin: 3px 0;"><strong>📈 Promedio por Fuente:</strong> {avg_emissions:,.1f} ton CO₂ eq/año</p>
                            </div>
                        </div>
                        
                        <hr style="margin: 10px 0; border: none; border-top: 1px solid #e5e5e5;">
                        <p style="text-align: center; font-size: 0.8em; color: #666; margin: 5px 0;">
                            💡 Datos del RETC 2023 - Ministerio del Medio Ambiente
                        </p>
                    </div>
                    """
                    
                    # Agregar marcador circular
                    folium.CircleMarker(
                        location=[coords['lat'], coords['lon']],
                        radius=radius,
                        popup=folium.Popup(popup_html, max_width=320),
                        tooltip=f"{region_name}: {total_emissions:,.0f} ton CO₂ eq",
                        color='darkred',
                        fillColor=color,
                        weight=2,
                        fillOpacity=0.7
                    ).add_to(m)
                    
                    # Agregar etiqueta con nombre de región
                    folium.Marker(
                        location=[coords['lat'], coords['lon']],
                        icon=folium.DivIcon(
                            html=f"""
                            <div style="
                                background-color: rgba(255,255,255,0.9);
                                border: 2px solid #dc2626;
                                border-radius: 8px;
                                padding: 3px 8px;
                                font-size: 11px;
                                font-weight: bold;
                                color: #dc2626;
                                white-space: nowrap;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                            ">{region_name}</div>
                            """,
                            icon_size=(len(region_name)*8, 25),
                            icon_anchor=(len(region_name)*4, 12)
                        )
                    ).add_to(m)
        
        # Agregar leyenda personalizada
        legend_html = """
        <div style="
            position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 140px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:12px; padding: 10px; border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
        ">
        <h4 style="margin: 0 0 10px 0; color: #dc2626;">📊 Leyenda Emisiones</h4>
        <p style="margin: 3px 0;"><span style="color: #dc2626;">●</span> > 100,000 ton CO₂</p>
        <p style="margin: 3px 0;"><span style="color: #f59e0b;">●</span> 10,000 - 100,000 ton CO₂</p>
        <p style="margin: 3px 0;"><span style="color: #eab308;">●</span> 1,000 - 10,000 ton CO₂</p>
        <p style="margin: 3px 0;"><span style="color: #22c55e;">●</span> < 1,000 ton CO₂</p>
        <p style="margin: 5px 0 0 0; font-size: 10px; color: #666;">Tamaño = nivel de emisiones</p>
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Agregar plugin de pantalla completa
        plugins.Fullscreen().add_to(m)
        
        # Agregar medidor de coordenadas
        plugins.MousePosition().add_to(m)
        
        return m
        
    except Exception as e:
        st.error(f"❌ Error creando mapa de emisiones: {str(e)}")
        return None
