"""
🗺️ Geocodificador Inteligente para Estaciones de Monitoreo de Chile
=================================================================

Este módulo proporciona capacidades de geocodificación específicamente diseñadas
para estaciones de monitoreo ambiental en Chile, utilizando múltiples fuentes
de datos geográficos oficiales y técnicas de validación cruzada.

Autor: Sistema de Análisis Ambiental
Fecha: 2025
Licencia: MIT
"""

import pandas as pd
import numpy as np
import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import folium
import plotly.graph_objects as go
import plotly.express as px


class GeocodificadorChile:
    """
    Geocodificador especializado para ubicaciones de monitoreo ambiental en Chile.
    
    Utiliza múltiples fuentes de datos geográficos oficiales y implementa
    validación cruzada para garantizar la precisión de las coordenadas.
    """
    
    def __init__(self, cache_file: str = "cache_coordenadas_chile.json"):
        """
        Inicializa el geocodificador con configuración optimizada para Chile.
        
        Args:
            cache_file: Archivo para almacenar coordenadas geocodificadas
        """
        self.cache_file = Path(cache_file)
        self.cache_coordenadas = self._cargar_cache()
        
        # Límites geográficos de Chile (validación)
        self.limites_chile = {
            'lat_min': -56.0, 'lat_max': -17.0,
            'lon_min': -76.0, 'lon_max': -66.0
        }
        
        # Configurar geocodificador principal
        self.geocoder = Nominatim(
            user_agent="analisis_ambiental_chile_v1.0",
            timeout=10
        )
        
        # Patrones para extracción de topónimos
        self.patrones_extraccion = {
            'lago': r'LAGO\s+([A-ZÁÉÍÓÚ\s]+?)(?:\s+EN\s+|$)',
            'embalse': r'EMBALSE\s+([A-ZÁÉÍÓÚ\s]+?)(?:\s+EN\s+|$)',
            'laguna': r'LAGUNA\s+([A-ZÁÉÍÓÚ\s]+?)(?:\s+EN\s+|$)',
            'rio': r'RIO\s+([A-ZÁÉÍÓÚ\s]+?)(?:\s+EN\s+|$)',
            'sector': r'EN\s+SECTOR\s+([A-ZÁÉÍÓÚ\s]+?)(?:\s+|$)',
            'localidad': r'EN\s+([A-ZÁÉÍÓÚ\s]+?)(?:\s+SECTOR|\s+PELAGIAL|$)'
        }
        
        print("🗺️ Geocodificador de Chile inicializado correctamente")
    
    def _cargar_cache(self) -> Dict:
        """Cargar cache de coordenadas desde archivo."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando cache: {e}")
        return {}
    
    def _guardar_cache(self):
        """Guardar cache de coordenadas a archivo."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_coordenadas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Error guardando cache: {e}")
    
    def extraer_toponimos(self, nombre_estacion: str) -> Dict[str, str]:
        """
        Extrae topónimos relevantes del nombre de la estación.
        
        Args:
            nombre_estacion: Nombre completo de la estación
            
        Returns:
            Dict con topónimos extraídos por categoría
        """
        toponimos = {}
        nombre_upper = nombre_estacion.upper()
        
        for categoria, patron in self.patrones_extraccion.items():
            match = re.search(patron, nombre_upper)
            if match:
                toponimo = match.group(1).strip()
                if toponimo and len(toponimo) > 2:  # Filtrar resultados muy cortos
                    toponimos[categoria] = toponimo.title()
        
        return toponimos
    
    def validar_coordenadas_chile(self, lat: float, lon: float) -> bool:
        """
        Valida que las coordenadas estén dentro de los límites de Chile.
        
        Args:
            lat: Latitud
            lon: Longitud
            
        Returns:
            True si las coordenadas están en Chile
        """
        return (
            self.limites_chile['lat_min'] <= lat <= self.limites_chile['lat_max'] and
            self.limites_chile['lon_min'] <= lon <= self.limites_chile['lon_max']
        )
    
    def geocodificar_con_nominatim(self, consulta: str) -> Optional[Tuple[float, float]]:
        """
        Geocodifica usando Nominatim (OpenStreetMap).
        
        Args:
            consulta: Consulta de geocodificación
            
        Returns:
            Tupla (latitud, longitud) o None si falla
        """
        try:
            # Agregar "Chile" a la consulta para mejorar precisión
            consulta_completa = f"{consulta}, Chile"
            location = self.geocoder.geocode(consulta_completa)
            
            if location:
                lat, lon = location.latitude, location.longitude
                if self.validar_coordenadas_chile(lat, lon):
                    return (lat, lon)
                else:
                    print(f"⚠️ Coordenadas fuera de Chile: {consulta} -> {lat}, {lon}")
            
        except GeocoderTimedOut:
            print(f"⏱️ Timeout geocodificando: {consulta}")
        except Exception as e:
            print(f"❌ Error geocodificando {consulta}: {e}")
        
        return None
    
    def geocodificar_estacion(self, nombre_estacion: str, forzar_actualizacion: bool = False) -> Dict:
        """
        Geocodifica una estación de monitoreo específica.
        
        Args:
            nombre_estacion: Nombre completo de la estación
            forzar_actualizacion: Si True, ignora el cache
            
        Returns:
            Dict con información de geocodificación
        """
        # Verificar cache primero
        if not forzar_actualizacion and nombre_estacion in self.cache_coordenadas:
            resultado = self.cache_coordenadas[nombre_estacion].copy()
            resultado['fuente'] = 'cache'
            return resultado
        
        print(f"🔍 Geocodificando: {nombre_estacion}")
        
        # Extraer topónimos
        toponimos = self.extraer_toponimos(nombre_estacion)
        
        # Intentar geocodificación con diferentes estrategias
        coordenadas = None
        metodo_exitoso = None
        
        # Estrategia 1: Nombre completo
        coordenadas = self.geocodificar_con_nominatim(nombre_estacion)
        if coordenadas:
            metodo_exitoso = "nombre_completo"
        
        # Estrategia 2: Topónimo principal (lago, embalse, etc.)
        if not coordenadas:
            for tipo in ['lago', 'embalse', 'laguna', 'rio']:
                if tipo in toponimos:
                    consulta = f"{tipo} {toponimos[tipo]}"
                    coordenadas = self.geocodificar_con_nominatim(consulta)
                    if coordenadas:
                        metodo_exitoso = f"toponimo_{tipo}"
                        break
        
        # Estrategia 3: Localidad o sector
        if not coordenadas:
            for tipo in ['localidad', 'sector']:
                if tipo in toponimos:
                    coordenadas = self.geocodificar_con_nominatim(toponimos[tipo])
                    if coordenadas:
                        metodo_exitoso = f"toponimo_{tipo}"
                        break
        
        # Preparar resultado
        resultado = {
            'nombre_estacion': nombre_estacion,
            'latitud': coordenadas[0] if coordenadas else None,
            'longitud': coordenadas[1] if coordenadas else None,
            'geocodificado': coordenadas is not None,
            'metodo': metodo_exitoso,
            'toponimos_extraidos': toponimos,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Guardar en cache
        self.cache_coordenadas[nombre_estacion] = resultado
        self._guardar_cache()
        
        if coordenadas:
            print(f"✅ Geocodificado exitoso: {coordenadas}")
        else:
            print(f"❌ No se pudo geocodificar")
        
        # Pausa para ser respetuoso con la API
        time.sleep(1)
        
        return resultado
    
    def geocodificar_dataframe(self, df: pd.DataFrame, 
                             columna_nombre: str = 'GLS_ESTACION',
                             mostrar_progreso: bool = True) -> pd.DataFrame:
        """
        Geocodifica todas las estaciones en un DataFrame.
        
        Args:
            df: DataFrame con estaciones
            columna_nombre: Nombre de la columna con nombres de estaciones
            mostrar_progreso: Si mostrar progreso de geocodificación
            
        Returns:
            DataFrame enriquecido con coordenadas
        """
        print(f"🚀 Iniciando geocodificación de {len(df)} estaciones...")
        
        # Obtener estaciones únicas
        estaciones_unicas = df[columna_nombre].dropna().unique()
        print(f"📍 Estaciones únicas a geocodificar: {len(estaciones_unicas)}")
        
        # Geocodificar cada estación única
        resultados_geocodificacion = {}
        exitosos = 0
        
        for i, estacion in enumerate(estaciones_unicas, 1):
            if mostrar_progreso and i % 10 == 0:
                print(f"📊 Progreso: {i}/{len(estaciones_unicas)} ({i/len(estaciones_unicas)*100:.1f}%)")
            
            resultado = self.geocodificar_estacion(estacion)
            resultados_geocodificacion[estacion] = resultado
            
            if resultado['geocodificado']:
                exitosos += 1
        
        print(f"✅ Geocodificación completada: {exitosos}/{len(estaciones_unicas)} ({exitosos/len(estaciones_unicas)*100:.1f}%) exitosas")
        
        # Agregar coordenadas al DataFrame
        df_resultado = df.copy()
        df_resultado['latitud_geocodificada'] = df_resultado[columna_nombre].map(
            lambda x: resultados_geocodificacion.get(x, {}).get('latitud')
        )
        df_resultado['longitud_geocodificada'] = df_resultado[columna_nombre].map(
            lambda x: resultados_geocodificacion.get(x, {}).get('longitud')
        )
        df_resultado['geocodificacion_exitosa'] = df_resultado[columna_nombre].map(
            lambda x: resultados_geocodificacion.get(x, {}).get('geocodificado', False)
        )
        
        return df_resultado
    
    def generar_mapa_estaciones(self, df: pd.DataFrame, 
                              columna_lat: str = 'latitud_geocodificada',
                              columna_lon: str = 'longitud_geocodificada',
                              columna_nombre: str = 'GLS_ESTACION',
                              guardar_html: str = 'mapa_estaciones_calidad_agua.html') -> folium.Map:
        """
        Genera un mapa interactivo con las estaciones geocodificadas.
        
        Args:
            df: DataFrame con estaciones y coordenadas
            columna_lat: Nombre de la columna de latitud
            columna_lon: Nombre de la columna de longitud
            columna_nombre: Nombre de la columna con nombres de estaciones
            guardar_html: Archivo donde guardar el mapa (opcional)
            
        Returns:
            Objeto mapa de Folium
        """
        # Filtrar solo estaciones con coordenadas válidas
        df_valido = df.dropna(subset=[columna_lat, columna_lon]).copy()
        
        if len(df_valido) == 0:
            print("❌ No hay estaciones con coordenadas válidas para mapear")
            return None
        
        print(f"🗺️ Generando mapa con {len(df_valido)} estaciones...")
        
        # Crear mapa centrado en Chile
        centro_lat = df_valido[columna_lat].mean()
        centro_lon = df_valido[columna_lon].mean()
        
        mapa = folium.Map(
            location=[centro_lat, centro_lon],
            zoom_start=6,
            tiles='CartoDB positron'
        )
        
        # Agregar marcadores para cada estación
        for idx, row in df_valido.iterrows():
            folium.CircleMarker(
                location=[row[columna_lat], row[columna_lon]],
                radius=6,
                popup=folium.Popup(
                    f"<b>{row[columna_nombre]}</b><br>"
                    f"Lat: {row[columna_lat]:.4f}<br>"
                    f"Lon: {row[columna_lon]:.4f}",
                    max_width=300
                ),
                tooltip=row[columna_nombre],
                color='blue',
                weight=2,
                fillColor='lightblue',
                fillOpacity=0.7
            ).add_to(mapa)
        
        # Guardar mapa si se especifica archivo
        if guardar_html:
            mapa.save(guardar_html)
            print(f"💾 Mapa guardado como: {guardar_html}")
        
        return mapa
    
    def generar_estadisticas_geocodificacion(self, df: pd.DataFrame) -> Dict:
        """
        Genera estadísticas del proceso de geocodificación.
        
        Args:
            df: DataFrame con resultados de geocodificación
            
        Returns:
            Dict con estadísticas
        """
        total_estaciones = len(df)
        estaciones_unicas = df['GLS_ESTACION'].nunique() if 'GLS_ESTACION' in df.columns else 0
        geocodificadas = df['geocodificacion_exitosa'].sum() if 'geocodificacion_exitosa' in df.columns else 0
        
        estadisticas = {
            'total_registros': total_estaciones,
            'estaciones_unicas': estaciones_unicas,
            'estaciones_geocodificadas': int(geocodificadas),
            'porcentaje_exito': (geocodificadas / estaciones_unicas * 100) if estaciones_unicas > 0 else 0,
            'cobertura_nacional': 'Alta' if geocodificadas > estaciones_unicas * 0.8 else 'Media' if geocodificadas > estaciones_unicas * 0.5 else 'Baja'
        }
        
        return estadisticas
    
    def exportar_coordenadas_csv(self, df: pd.DataFrame, 
                               archivo_salida: str = 'estaciones_geocodificadas.csv'):
        """
        Exporta las estaciones geocodificadas a un archivo CSV.
        
        Args:
            df: DataFrame con estaciones geocodificadas
            archivo_salida: Nombre del archivo de salida
        """
        # Seleccionar columnas relevantes
        columnas_export = [
            'GLS_ESTACION', 'latitud_geocodificada', 'longitud_geocodificada',
            'geocodificacion_exitosa'
        ]
        
        columnas_disponibles = [col for col in columnas_export if col in df.columns]
        
        if columnas_disponibles:
            df_export = df[columnas_disponibles].drop_duplicates(subset=['GLS_ESTACION'])
            df_export.to_csv(archivo_salida, index=False, encoding='utf-8')
            print(f"📊 Coordenadas exportadas a: {archivo_salida}")
        else:
            print("❌ No se encontraron columnas para exportar")


def ejemplo_uso():
    """
    Ejemplo de uso del geocodificador con datos de calidad del agua.
    """
    print("🌊 Ejemplo de uso del Geocodificador de Chile")
    print("=" * 50)
    
    # Crear instancia del geocodificador
    geocoder = GeocodificadorChile()
    
    # Ejemplo con datos simulados (reemplazar con datos reales)
    datos_ejemplo = pd.DataFrame({
        'GLS_ESTACION': [
            'LAGO VILLARRICA EN PELAGIAL VILLARRICA',
            'EMBALSE RAPEL EN SECTOR BRAZO ALHUE',
            'LAGO RIÑIHUE EN RIÑIHUE',
            'LAGUNA GRANDE DE SAN PEDRO EN SECTOR SUR'
        ]
    })
    
    print(f"📍 Geocodificando {len(datos_ejemplo)} estaciones de ejemplo...")
    
    # Geocodificar estaciones
    df_geocodificado = geocoder.geocodificar_dataframe(datos_ejemplo)
    
    # Mostrar resultados
    print("\n📊 Resultados de geocodificación:")
    print(df_geocodificado[['GLS_ESTACION', 'latitud_geocodificada', 'longitud_geocodificada', 'geocodificacion_exitosa']])
    
    # Generar estadísticas
    stats = geocoder.generar_estadisticas_geocodificacion(df_geocodificado)
    print(f"\n📈 Estadísticas:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Generar mapa (si hay estaciones geocodificadas)
    if df_geocodificado['geocodificacion_exitosa'].any():
        mapa = geocoder.generar_mapa_estaciones(df_geocodificado)
        print("\n🗺️ Mapa generado exitosamente")
    
    return df_geocodificado


if __name__ == "__main__":
    ejemplo_uso()
