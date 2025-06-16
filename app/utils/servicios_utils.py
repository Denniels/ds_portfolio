"""
Utilidades para el manejo de servicios y precios
"""
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

def calcular_precio_referencial(tipo_servicio, complejidad, duracion_semanas):
    """
    Calcula un precio referencial basado en el tipo de servicio y su complejidad
    """
    # Tarifas base por tipo de servicio (CLP por semana)
    tarifas_base = {
        "dashboard": 400000,
        "mapa": 450000,
        "analisis": 500000,
        "integracion": 350000,
        "sectorial": 550000
    }
    
    # Multiplicadores por complejidad
    multiplicadores = {
        "basico": 1.0,
        "intermedio": 1.3,
        "avanzado": 1.6,
        "experto": 2.0
    }
    
    # Calcular precio base
    tarifa_semanal = tarifas_base.get(tipo_servicio, 400000)
    multiplicador = multiplicadores.get(complejidad, 1.0)
    
    precio_base = tarifa_semanal * duracion_semanas * multiplicador
    
    # Redondear a miles
    return round(precio_base / 1000) * 1000

def actualizar_precios_servicios():
    """
    Actualiza los precios de servicios basados en análisis de mercado
    """
    servicios_path = Path(__file__).parent.parent.parent / "data" / "servicios.json"
    
    if not servicios_path.exists():
        return None
    
    with open(servicios_path, 'r', encoding='utf-8') as f:
        servicios = json.load(f)
    
    # Actualizar precios
    for categoria in servicios:
        for servicio in servicios[categoria]:
            tipo = servicio.get('tipo', 'analisis')
            complejidad = servicio.get('complejidad', 'intermedio')
            duracion = servicio.get('duracion_semanas', 4)
            
            nuevo_precio = calcular_precio_referencial(tipo, complejidad, duracion)
            servicio['precio'] = nuevo_precio
            servicio['ultima_actualizacion'] = datetime.now().strftime("%Y-%m-%d")
    
    # Guardar actualizaciones
    with open(servicios_path, 'w', encoding='utf-8') as f:
        json.dump(servicios, f, indent=2, ensure_ascii=False)
    
    return servicios

def generar_reporte_servicios():
    """
    Genera un reporte comparativo de precios de servicios
    """
    servicios = actualizar_precios_servicios()
    if not servicios:
        return None
    
    # Convertir a DataFrame para análisis
    rows = []
    for categoria, items in servicios.items():
        for servicio in items:
            rows.append({
                'categoria': categoria,
                'servicio': servicio['nombre'],
                'precio': servicio['precio'],
                'complejidad': servicio.get('complejidad', 'intermedio'),
                'duracion_semanas': servicio.get('duracion_semanas', 4)
            })
    
    df = pd.DataFrame(rows)
    
    # Calcular estadísticas
    stats = {
        'precio_promedio': df['precio'].mean(),
        'precio_minimo': df['precio'].min(),
        'precio_maximo': df['precio'].max(),
        'total_servicios': len(df),
        'categorias': df['categoria'].nunique(),
        'ultima_actualizacion': datetime.now().strftime("%Y-%m-%d")
    }
    
    return df, stats
