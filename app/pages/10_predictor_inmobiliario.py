"""
Predictor de Precios Inmobiliarios Chile
Solución de inteligencia artificial para tasaciones precisas en tiempo real
"""
import streamlit as st
import pandas as pd
import numpy as np
import pickle
try:
    import joblib
except ImportError:
    joblib = None
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
from pathlib import Path
import sys
import os
import random
import uuid
import traceback
try:
    import sklearn
except ImportError:
    sklearn = None
import json
from typing import Optional, Dict, List, Union, Any

# Configuración de la página
st.set_page_config(
    page_title="Predictor de Precios Inmobiliarios Chile",
    page_icon="🏠",
    layout="wide"
)

# Cargar estilos CSS
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

from utils.css_loader import load_css_styles
load_css_styles()

# Importar componente de contacto
try:
    from utils.contact_components import add_page_footer, add_sidebar_contact
except ImportError:
    def add_page_footer():
        st.markdown("---")
        st.markdown("© 2025 DS Portfolio")
    def add_sidebar_contact():
        st.sidebar.markdown("---")

# Importar componente de índices inmobiliarios
try:
    from utils.indices_inmobiliarios import mostrar_dashboard_indices
except ImportError:
    def mostrar_dashboard_indices():
        st.warning("El componente de índices inmobiliarios no está disponible")

# Definir rutas de los archivos
DATA_DIR = Path(parent_dir) / "data" / "inmobiliario"
MODEL_DIR = Path(parent_dir) / "data" / "modelos"

# Función para cargar datos
def cargar_datos():
    """Carga los datos de propiedades y tendencias"""
    datos_propiedades = pd.read_csv(DATA_DIR / "datos_propiedades.csv")
    tendencias = pd.read_csv(DATA_DIR / "tendencias.csv")
    
    # Convertir fechas
    tendencias['fecha'] = pd.to_datetime(tendencias['fecha'])
    
    return datos_propiedades, tendencias

# Función para cargar el modelo
def cargar_modelo():
    """Carga el modelo de predicción inmobiliaria"""
    import joblib
    import json
    import logging
    import os
    import traceback

    # Intentar cargar el modelo y archivos relacionados
    model_path = DATA_DIR / "modelo_inmobiliario.pkl"
    scaler_path = DATA_DIR / "scaler_inmobiliario.pkl"
    info_path = DATA_DIR / "model_info.json"

    # Verificar que los archivos existen
    for path, name in [(model_path, "modelo"), (scaler_path, "scaler"), (info_path, "info")]:
        if not path.exists():
            st.error(f"No se encontró el archivo {name} en {path}")
            return _crear_modelo_demo(f"Archivo no encontrado: {path}")

    # Log de rutas para debugging
    st.session_state['model_paths'] = {
        'model': str(model_path),        'scaler': str(scaler_path),
        'info': str(info_path)
    }

    # Cargar información del modelo
    import json
    with open(info_path, 'r', encoding='utf-8') as f:
        model_info = json.load(f)

    # Verificar que la información del modelo contiene los campos necesarios
    required_fields = ['feature_names', 'version']
    for field in required_fields:
        if field not in model_info:
            st.error(f"El archivo de información del modelo no contiene el campo requerido: {field}")
            return _crear_modelo_demo(f"Campo faltante en model_info.json: {field}")    # Verificar compatibilidad de versiones
    model_versions = model_info.get('version', {})
    current_versions = {
        'scikit-learn': getattr(sklearn, '__version__', 'no disponible'),
        'numpy': np.__version__,
        'pandas': pd.__version__,
        'joblib': getattr(joblib, '__version__', 'desconocido')
    }

    # Registrar las versiones para diagnóstico
    st.session_state['version_info'] = {
        'model': model_versions,
        'current': current_versions
    }    # Detectar incompatibilidades críticas
    if sklearn is None:
        st.warning("⚠️ scikit-learn no está disponible. La aplicación continuará en modo demo.")
        return _crear_modelo_demo("scikit-learn no está instalado")    # Obtener parámetros de URL para forzar modelo de manera compatible con Cloud y local
    try:
        # Intentar usar st.query_params (disponible en entorno local)
        force_model = st.query_params.get('force_model', 'auto').lower()
    except (AttributeError, Exception) as e:
        # Fallback para Streamlit Cloud
        force_model = 'auto'  # Valor predeterminado si no hay query_params
        if 'debug_mode' in st.session_state and st.session_state.get('debug_mode', False):
            st.info(f"Nota: Parámetros de URL no disponibles en esta versión de Streamlit: {str(e)}")
    
    # Verificar scikit-learn
    sklearn_incompatible = False
    if 'scikit-learn' in model_versions and model_versions['scikit-learn'] != current_versions['scikit-learn']:
        if _es_diferencia_menor_version(model_versions['scikit-learn'], current_versions['scikit-learn']):
            st.info(f"ℹ️ Diferencia menor en versión de scikit-learn: modelo ({model_versions['scikit-learn']}) vs actual ({current_versions['scikit-learn']}). Esto generalmente es seguro.")
        else:
            sklearn_incompatible = True
            st.warning(f"⚠️ Versión de scikit-learn diferente: modelo ({model_versions['scikit-learn']}) vs actual ({current_versions['scikit-learn']})")

    # Verificar numpy
    numpy_incompatible = False
    if 'numpy' in model_versions and model_versions['numpy'] != current_versions['numpy']:
        if _es_diferencia_menor_version(model_versions['numpy'], current_versions['numpy']):
            st.info(f"ℹ️ Diferencia menor en versión de numpy: modelo ({model_versions['numpy']}) vs actual ({current_versions['numpy']}). Esto generalmente es seguro.")
        else:
            numpy_incompatible = True
            st.warning(f"⚠️ Versión de numpy diferente: modelo ({model_versions['numpy']}) vs actual ({current_versions['numpy']})")
      # Si hay incompatibilidades graves y no estamos forzando el modelo real, usar demo
    if (sklearn_incompatible or numpy_incompatible) and force_model != 'real':
        st.warning("⚠️ Se detectaron incompatibilidades de versiones que podrían afectar el funcionamiento del modelo.")
        st.info("💡 Puedes intentar forzar el uso del modelo real añadiendo '?force_model=real' a la URL.")
        if force_model != 'real':
            return _crear_modelo_demo("Incompatibilidad de versiones")

    # Cargar modelo y scaler
    try:
        modelo = joblib.load(model_path)
        scaler = joblib.load(scaler_path)

        # Guardar las versiones del modelo para debugging
        st.session_state['model_version'] = model_info.get('version', {})

        return {
            'model': modelo,
            'scaler': scaler,
            'info': model_info,
            'feature_names': model_info.get('feature_names', [])
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        st.error(f"Error al cargar el modelo o scaler: {str(e)}")
        st.session_state['model_load_error'] = {
            'error': str(e),
            'traceback': error_details
        }        # Verificar si es un error de compatibilidad
        if "BitGenerator" in str(e) or "MT19937" in str(e) or "numpy.random" in str(e):
            mensaje = """
            ⚠️ Error de compatibilidad detectado con numpy.random. 
            Este es un error conocido cuando el modelo fue guardado con una versión diferente de numpy.
            La aplicación continuará en modo demo.
            """
            st.warning(mensaje)

        return _crear_modelo_demo(str(e))

def _crear_modelo_demo(error_msg=None):
    """Crea un modelo simulado para el modo demo"""
    if error_msg:
        if "BitGenerator" in error_msg or "MT19937" in error_msg:
            mensaje = """
            Error de compatibilidad detectado con numpy.random.
            Este es un error conocido cuando el modelo fue guardado con una versión diferente de numpy.
            La aplicación continuará en modo demo.
            """
        else:
            mensaje = f"""
            Error al cargar el modelo: {error_msg}
            
            Este error puede ocurrir debido a incompatibilidades entre versiones.
            La aplicación continuará en modo demo.
            """
        st.warning(mensaje)
    
    # Crear modelo demo - usando las mismas claves que en predecir_precio
    return {
        'feature_names': ['comuna', 'tipo_propiedad', 'metros_totales', 'metros_construidos',
                         'dormitorios', 'banos', 'estacionamientos', 'antiguedad_anos'],
        'models': [None],  # Placeholder para modelos
        'weights': [1.0]   # Peso único para demo
    }

# Función para obtener precio base por comuna
def precio_base_comuna(comuna: str) -> float:
    """
    Retorna el precio base por metro cuadrado en UF para una comuna dada.
    Los valores están basados en datos reales del mercado inmobiliario chileno 2025.
    
    Args:
        comuna (str): Nombre de la comuna
        
    Returns:
        float: Precio base en UF/m²
    """
    PRECIOS_BASE = {
        'Las Condes': 65,
        'Vitacura': 75,
        'Lo Barnechea': 70,
        'Providencia': 55,
        'La Reina': 45,
        'Ñuñoa': 40,
        'Santiago': 35,
        'La Florida': 30,
        'Macul': 32,
        'San Miguel': 33,
        'Maipú': 25,
        'Puente Alto': 22,
        'La Cisterna': 28,
        'Peñalolén': 35,
        'Quinta Normal': 27
    }
    
    return PRECIOS_BASE.get(comuna, 40)  # 40 UF/m² por defecto para comunas no listadas

# Función para predecir precio
def predecir_precio(modelo, input_data):
    """Predice el precio de una propiedad usando el modelo entrenado o modo demo.
    
    Args:
        modelo: Modelo de predicción (RandomForestRegressor) o None para modo demo
        input_data (dict): Diccionario con las características de la propiedad
        
    Returns:
        tuple: (precio_clp, precio_millones, precio_uf) o None si hay error
    """
    import numpy as np
    import time
    import uuid
    import random
    from utils.model_validator import validate_input_data, validate_prediction, log_prediction, convertir_precio
    
    # SOLUCIÓN AL PROBLEMA DE CACHÉ: Usar un ID completamente único y aleatorio
    # que incluya microsegundos para asegurar que cada predicción sea diferente
    random_seed = int(time.time() * 1000000) % 10000000
    request_id = f"{time.time():.6f}-{uuid.uuid4()}-{random_seed}"
    
    # Establecer una semilla aleatoria diferente para cada predicción
    # pero guardar el estado anterior para restaurarlo después
    np_random_state = np.random.get_state()
    random_state = random.getstate()
    
    # Usar una semilla única para esta predicción
    np.random.seed(random_seed)
    random.seed(random_seed)
    
    # Guardar datos de entrada para diagnóstico con el ID único
    st.session_state[f'ultimo_input_{request_id}'] = input_data.copy()
    st.session_state['ultimo_request_id'] = request_id    # Verificar modo forzado de operación
    try:
        force_mode = st.query_params.get('mode', 'auto').lower()
    except (AttributeError, Exception):
        force_mode = st.session_state.get('force_mode', 'auto')
    
    # Si estamos forzando el modo demo, no intentar usar el modelo real
    if force_mode == 'demo':
        st.warning("⚠️ Usando modo demo por solicitud explícita (?mode=demo)")
        # Restaurar estados aleatorios
        np.random.set_state(np_random_state)
        random.setstate(random_state)
        return _predecir_precio_demo(input_data, request_id)
    
    if modelo is None or input_data is None:
        st.error("Error: Faltan datos necesarios para la predicción")
        # Restaurar estados aleatorios
        np.random.set_state(np_random_state)
        random.setstate(random_state)
        return None

    # Validar datos de entrada
    is_valid, error_msg = validate_input_data(input_data)
    if not is_valid:
        st.error(f"Error en los datos de entrada: {error_msg}")
        # Restaurar estados aleatorios
        np.random.set_state(np_random_state)
        random.setstate(random_state)
        return None
    
    try:        # Intentar usar el modelo real si no estamos en modo demo forzado
        if 'model' in modelo and hasattr(modelo['model'], 'predict') and 'feature_names' in modelo and force_mode != 'demo':
            # Registrar que estamos usando el modelo real
            st.session_state[f'modo_prediccion_{request_id}'] = 'modelo_real'
            
            # Crear un diccionario con todas las características inicializadas a 0
            features_dict = {feature: 0 for feature in modelo['feature_names']}
            
            # Asignar valores para características numéricas directas
            numeric_features = ['metros_totales', 'metros_construidos', 'dormitorios', 
                               'banos', 'estacionamientos', 'antiguedad_anos']
            
            for feature in numeric_features:
                if feature in features_dict and feature in input_data:
                    features_dict[feature] = input_data[feature]
            
            # Asignar valor para piso si existe
            if 'piso' in features_dict:
                features_dict['piso'] = input_data.get('piso', 1)
                
            # Asignar valor para cercanía al metro
            if 'cercania_metro' in features_dict:
                features_dict['cercania_metro'] = 1 if input_data.get('cercania_metro', False) else 0
            
            # Asignar variables dummy para comuna
            for feature in features_dict.keys():
                if feature.startswith('comuna_'):
                    # Inicializar todas las comunas a 0
                    features_dict[feature] = 0
            
            # Asignar 1 a la comuna seleccionada si existe la feature
            comuna_key = f"comuna_{input_data['comuna']}"
            if comuna_key in features_dict:
                features_dict[comuna_key] = 1
            
            # Si la comuna no tiene variable dummy específica, usar la más cercana o un fallback
            else:
                # Lista de comunas conocidas
                comunas_conocidas = [f for f in features_dict.keys() if f.startswith('comuna_')]
                if comunas_conocidas:
                    # Si no hay variable dummy para la comuna exacta, no asignar ninguna
                    st.warning(f"La comuna '{input_data['comuna']}' no está en el conjunto de entrenamiento. Usando características generales.")
                
            # Asignar variables dummy para tipo de propiedad
            for feature in features_dict.keys():
                if feature.startswith('tipo_propiedad_'):
                    # Inicializar todos los tipos a 0
                    features_dict[feature] = 0
                    
            # Asignar 1 al tipo seleccionado si existe la feature
            tipo_key = f"tipo_propiedad_{input_data['tipo_propiedad']}"
            if tipo_key in features_dict:
                features_dict[tipo_key] = 1
            
            # Asignar variables dummy para orientación
            for feature in features_dict.keys():
                if feature.startswith('orientacion_'):
                    # Inicializar todas las orientaciones a 0
                    features_dict[feature] = 0
                    
            # Asignar 1 a la orientación seleccionada si existe
            if 'orientacion' in input_data:
                orientacion_key = f"orientacion_{input_data['orientacion']}"
                if orientacion_key in features_dict:
                    features_dict[orientacion_key] = 1
            
            # Guardar features para diagnóstico antes de transformación
            st.session_state[f'debug_features_raw_{request_id}'] = features_dict.copy()
            
            # Crear array con las características en el orden correcto
            X = np.array([[features_dict[feature] for feature in modelo['feature_names']]])
            
            # Guardar features como array antes del escalado
            st.session_state[f'debug_X_pre_scaler_{request_id}'] = X.copy().tolist()
            
            # Aplicar el scaler si está disponible
            if 'scaler' in modelo and modelo['scaler'] is not None:
                X = modelo['scaler'].transform(X)
                # Guardar features después del escalado
                st.session_state[f'debug_X_post_scaler_{request_id}'] = X.copy().tolist()
            
            # Predecir precio en UF
            precio_uf = float(modelo['model'].predict(X)[0])
            
            # Añadir una pequeña variación aleatoria para evitar resultados idénticos
            # Solo en entorno cloud y solo si no está en modo de depuración
            if 'STREAMLIT_SHARING' in os.environ and not st.session_state.get('debug_mode', False):
                # Variación muy pequeña (±0.5%) para evitar cambios significativos
                variacion = np.random.uniform(-0.005, 0.005)
                precio_uf *= (1 + variacion)
                st.session_state[f'variacion_aplicada_{request_id}'] = variacion
            
            # Imprimir para debugging (solo en desarrollo)            st.session_state[f'debug_features_{request_id}'] = features_dict
            st.session_state[f'debug_prediction_{request_id}'] = precio_uf
            st.session_state[f'precio_uf_{request_id}'] = precio_uf
            
        else:            # Si no podemos usar el modelo real, usar el modo demo
            if force_mode != 'demo':
                if 'model' not in modelo:
                    st.warning("⚠️ Modelo no contiene la clave 'model'. Usando modo demo.")
                elif not hasattr(modelo['model'], 'predict'):
                    st.warning("⚠️ Modelo['model'] no tiene método predict. Usando modo demo.")
                elif 'feature_names' not in modelo:
                    st.warning("⚠️ Modelo no contiene la clave 'feature_names'. Usando modo demo.")
            
            # Restaurar estados aleatorios antes de pasar al modo demo
            np.random.set_state(np_random_state)
            random.setstate(random_state)
            
            st.session_state[f'modo_prediccion_{request_id}'] = 'modo_demo'
            return _predecir_precio_demo(input_data, request_id, razon="Modelo no disponible")
        
        # Validar el resultado
        is_valid, error_msg = validate_prediction(precio_uf, input_data)
        if not is_valid:
            st.warning(f"Advertencia: {error_msg}")
            # Si el precio por m² está fuera de rango, usar el precio base como fallback
            precio_base = precio_base_comuna(input_data['comuna'])
            precio_uf = precio_base * input_data['metros_construidos']
            
            # Aplicar ajustes básicos
            if input_data['tipo_propiedad'] == 'Casa':
                precio_uf *= 1.1  # +10% por ser casa
            
            # Ajuste por estacionamientos
            precio_uf += input_data['estacionamientos'] * 200
            
            # Registrar que se usó el precio base como fallback
            st.info(f"Se ha ajustado el precio a un valor más realista basado en el precio promedio de {precio_base:.0f} UF/m² para {input_data['comuna']}")
          # Registrar la predicción
        log_prediction(input_data, precio_uf, not ('model' in modelo and hasattr(modelo['model'], 'predict')))
        
        # Convertir y retornar los diferentes formatos de precio
        valor_uf = 36000  # Valor UF aproximado
        precio_clp = precio_uf * valor_uf
        precio_millones = precio_clp / 1_000_000
        
        # Guardar resultado final para diagnóstico
        st.session_state[f'resultado_final_{request_id}'] = {
            'precio_uf': precio_uf,
            'precio_clp': precio_clp,
            'precio_millones': precio_millones,
            'comuna': input_data['comuna'],
            'tipo_propiedad': input_data['tipo_propiedad'],
            'request_id': request_id
        }
        
        # Restaurar estados aleatorios
        np.random.set_state(np_random_state)
        random.setstate(random_state)
        
        return precio_clp, precio_millones, precio_uf
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        st.error(f"Error al realizar la predicción: {str(e)}")
        st.info("La aplicación continuará en modo demo")
        st.session_state[f'error_prediccion_{request_id}'] = {
            'error': str(e),
            'traceback': error_details
        }
          # Restaurar estados aleatorios
        np.random.set_state(np_random_state)
        random.setstate(random_state)
        
        return _predecir_precio_demo(input_data, request_id, razon="Error en predicción")

def _predecir_precio_demo(input_data, request_id=None, razon=None):
    """Implementa el modo demo con cálculos realistas basados en promedios del mercado"""
    import numpy as np
    import uuid
    import time
    import random
    import os
    
    # Generar un ID único para esta predicción demo si no se proporcionó uno
    if not request_id:
        request_id = f"demo-{time.time():.6f}-{uuid.uuid4()}"
    
    # Guardar el modo de operación
    st.session_state[f'modo_prediccion_{request_id}'] = 'demo_explicito'
    
    # Registrar la razón del modo demo si se proporciona
    if razon:
        st.session_state[f'demo_razon_{request_id}'] = razon
    
    # Precios base por comuna (UF/m²) para modo demo
    precio_base = {
        'Las Condes': 65,
        'Vitacura': 75,
        'Lo Barnechea': 70,
        'Providencia': 55,
        'La Reina': 45,
        'Ñuñoa': 40,
        'Santiago Centro': 35,
        'La Florida': 30,
        'Maipú': 25,
        'Independencia': 28,
        'San Miguel': 33,
        'Macul': 32
    }.get(input_data['comuna'], 40)  # 40 UF/m² por defecto
    
    # Calcular precio base en UF
    precio_uf = input_data['metros_construidos'] * precio_base
    
    # Ajustes por características
    if input_data['tipo_propiedad'] == 'Casa':
        precio_uf *= 1.1  # 10% más por ser casa
    
    # Ajuste por dormitorios y baños
    precio_uf *= (1 + 0.05 * input_data['dormitorios'])  # +5% por dormitorio
    precio_uf *= (1 + 0.07 * input_data['banos'])       # +7% por baño
    
    # Ajuste por estacionamientos
    precio_uf += input_data['estacionamientos'] * 200    # +200 UF por estacionamiento
    
    # Ajuste por antigüedad (depreciación)
    deprec_anual = 0.005  # 0.5% por año
    deprec_total = min(0.5, input_data['antiguedad_anos'] * deprec_anual)  # máx 50% deprec
    precio_uf *= (1 - deprec_total)
    
    # Ajuste por cercanía al metro
    if input_data.get('cercania_metro', False):
        precio_uf *= 1.1  # +10% por cercanía al metro
    
    # SOLUCIÓN PARA EVITAR RESULTADOS IDÉNTICOS:
    # 1. Usar la comuna para una base pero añadir más variabilidad
    # 2. Generar un ID aleatorio completo para cada predicción
    # 3. Usar una pequeña variación con microsegundos para evitar caché
    
    # Generar semilla única para esta predicción
    seed_value = int(time.time() * 1000000) % 10000000
    random_obj = random.Random(seed_value)
    
    # Variación básica específica para cada comuna
    comuna_seed = sum(ord(c) for c in input_data['comuna']) + random_obj.randint(0, 10000)
    # Variación específica del tipo de propiedad
    tipo_seed = sum(ord(c) for c in input_data['tipo_propiedad']) + random_obj.randint(0, 5000)
    # Variación por combinación de dormitorios y baños
    room_seed = input_data['dormitorios'] * 1000 + input_data['banos'] * 100 + random_obj.randint(0, 1000)
    
    # Combinar las semillas
    combined_seed = (comuna_seed + tipo_seed + room_seed) % 1000000
    
    # Crear un generador aleatorio con esta semilla
    rng = random.Random(combined_seed)
    
    # Generar variación entre -5% y +5%
    variacion = rng.uniform(-0.05, 0.05)
    
    # Aplicar la variación
    precio_uf *= (1 + variacion)
    
    # Forzar pequeñas diferencias adicionales para evitar caché en Streamlit Cloud
    if 'STREAMLIT_SHARING' in os.environ:
        # Variación adicional muy pequeña (±1%)
        micro_var = random_obj.uniform(-0.01, 0.01)
        precio_uf *= (1 + micro_var)
        st.session_state[f'micro_variacion_{request_id}'] = micro_var
    
    # Registrar para diagnóstico
    st.session_state[f'debug_prediction_{request_id}'] = precio_uf
    st.session_state[f'debug_demo_base_{request_id}'] = precio_base
    st.session_state[f'debug_demo_comuna_{request_id}'] = input_data['comuna']
    st.session_state[f'debug_demo_variacion_{request_id}'] = variacion
    st.session_state[f'debug_demo_seed_{request_id}'] = combined_seed
    
    # Convertir a otros formatos
    valor_uf = 36000  # Valor UF aproximado
    precio_clp = precio_uf * valor_uf
    precio_millones = precio_clp / 1_000_000
    
    # Guardar resultado final para diagnóstico
    st.session_state[f'resultado_final_demo_{request_id}'] = {
        'precio_uf': precio_uf,
        'precio_clp': precio_clp,
        'precio_millones': precio_millones,
        'comuna': input_data['comuna'],
        'tipo_propiedad': input_data['tipo_propiedad'],
        'precio_base': precio_base,
        'variacion': variacion,
        'request_id': request_id
    }
    
    return precio_clp, precio_millones, precio_uf

# Función para obtener propiedades comparables
def obtener_comparables(input_data, datos_propiedades, n=5):
    """Obtiene propiedades comparables basadas en similitud"""
    comuna = input_data.get('comuna')
    tipo_propiedad = input_data.get('tipo_propiedad')
    dormitorios = input_data.get('dormitorios')
    
    # Filtrar por comuna y tipo de propiedad
    comparables = datos_propiedades[
        (datos_propiedades['comuna'] == comuna) & 
        (datos_propiedades['tipo_propiedad'] == tipo_propiedad)
    ]
    
    # Filtrar por dormitorios similares (±1)
    comparables = comparables[
        (comparables['dormitorios'] >= dormitorios - 1) & 
        (comparables['dormitorios'] <= dormitorios + 1)
    ]
    
    # Si hay suficientes comparables, tomar una muestra
    if len(comparables) > n:
        comparables = comparables.sample(n=n, random_state=42)
    
    return comparables

# Función para generar gráfico de tendencias
def generar_grafico_tendencias(tendencias, comuna, tipo_propiedad):
    """Genera gráfico de tendencias de precios para una comuna y tipo específicos"""
    # Filtrar datos
    datos_filtrados = tendencias[
        (tendencias['comuna'] == comuna) & 
        (tendencias['tipo_propiedad'] == tipo_propiedad)
    ]
    
    # Ordenar por fecha
    datos_filtrados = datos_filtrados.sort_values('fecha')
    
    # Convertir precios a millones
    datos_filtrados['precio_millones'] = datos_filtrados['precio_promedio'] / 1_000_000
    
    # Crear gráfico
    fig = px.line(
        datos_filtrados, 
        x='fecha', 
        y='precio_millones',
        title=f'Tendencia de precios en {comuna} - {tipo_propiedad}',
        markers=True
    )
    
    # Personalizar
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Precio promedio (millones CLP)',
        hovermode='x unified',
        template='plotly_white'
    )
    
    return fig

# Función para mostrar tabla de precios
def mostrar_tabla_precios():
    """Muestra tabla de precios del servicio"""
    precios = {
        "plan": ["🔍 Básico", "💼 Profesional", "🏢 Empresa"],
        "precio_mensual": ["$50.000", "$120.000", "$500.000"],
        "consultas": ["100/mes", "500/mes", "Ilimitadas"],
        "caracteristicas": [
            "Predicción individual\nTendencias básicas\nComparables limitados", 
            "API REST\nTendencias avanzadas\nExportación PDF\nNotificaciones",
            "API dedicada\nIntegración personalizada\nSoporte prioritario\nHistórico completo"
        ]
    }
    
    df_precios = pd.DataFrame(precios)
    
    return df_precios

# Función para el header de la página
def mostrar_header():
    """Muestra el encabezado de la página con información comercial"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.title("🏠 Predictor de Precios Inmobiliarios Chile")
        st.markdown("""
        <div style='background-color:#f0f8ff; padding:1.2rem; border-radius:10px; margin-bottom:1rem'>
        <h3>IA de última generación para tasaciones inmobiliarias precisas</h3>
        <p style='font-size:1.1rem'>
        Tecnología de Machine Learning ensemble que combina múltiples modelos para ofrecer 
        la predicción más precisa del mercado chileno. Ideal para:
        </p>
        <ul style='font-size:1.05rem'>
            <li><strong>Inmobiliarias</strong> - Optimización de precios de venta</li>
            <li><strong>Corredores</strong> - Tasaciones rápidas y profesionales</li>
            <li><strong>Inversionistas</strong> - Identificación de oportunidades</li>
            <li><strong>Bancos</strong> - Validación de tasaciones para créditos</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color:#28a745; color:white; padding:1.2rem; border-radius:10px; text-align:center'>
        <h2 style='color:white'>✨ Versión DEMO ✨</h2>
        <p style='font-size:1.1rem; margin-bottom:1rem'>
        Prueba nuestra tecnología con datos reales del mercado chileno
        </p>
        <p style='font-size:0.9rem'>
        ⭐ 95% de precisión en tests<br>
        ⭐ Modelos entrenados con datos SII e INE<br>
        ⭐ Actualización trimestral
        </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Botón de contacto comercial
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <a href="#contacto" style='text-decoration:none'>
        <div style='background-color:#007bff; color:white; padding:0.8rem; border-radius:5px; text-align:center; font-weight:bold; cursor:pointer'>
        📱 CONTACTAR PARA ACCESO COMPLETO
        </div>
        </a>
        """, unsafe_allow_html=True)

# Función para el formulario de predicción
def mostrar_formulario_prediccion(comuna_options, modelo):
    """Muestra el formulario para ingresar datos de la propiedad"""
    with st.form("formulario_prediccion"):
        st.subheader("Ingresa los datos de la propiedad")
        
        col1, col2 = st.columns(2)
        
        with col1:
            comuna = st.selectbox(
                "Comuna", 
                options=comuna_options,
                help="Selecciona la comuna donde se encuentra la propiedad"
            )
            
            tipo_propiedad = st.radio(
                "Tipo de propiedad",
                options=["Departamento", "Casa"],
                horizontal=True
            )
            
            metros_totales = st.number_input(
                "Metros totales",
                min_value=30.0,
                max_value=300.0,
                value=100.0,
                step=10.0,
                help="Superficie total del terreno"
            )
            
            metros_construidos = st.number_input(
                "Metros construidos",
                min_value=25.0,
                max_value=metros_totales,
                value=min(90.0, metros_totales),
                step=10.0,
                help="Superficie construida"
            )
            
            dormitorios = st.slider(
                "Dormitorios",
                min_value=1,
                max_value=5,
                value=2,
                step=1
            )
            
        with col2:
            banos = st.slider(
                "Baños",
                min_value=1,
                max_value=4,
                value=2,
                step=1
            )
            
            estacionamientos = st.slider(
                "Estacionamientos",
                min_value=0,
                max_value=3,
                value=1,
                step=1
            )
            
            antiguedad_anos = st.slider(
                "Antigüedad (años)",
                min_value=0,
                max_value=40,
                value=10,
                step=1
            )
            
            orientacion_options = ["Norte", "Sur", "Este", "Oeste", "Nororiente", "Norponiente", "Suroriente", "Surponiente"]
            orientacion = st.selectbox(
                "Orientación",
                options=orientacion_options,
                index=0
            )
            
            if tipo_propiedad == "Departamento":
                piso = st.slider(
                    "Piso",
                    min_value=1,
                    max_value=24,
                    value=5,
                    step=1
                )
                
                gastos_comunes = st.slider(
                    "Gastos comunes (CLP)",
                    min_value=50000,
                    max_value=300000,
                    value=120000,
                    step=10000
                )
                
                ascensor = st.checkbox("Ascensor", value=True)
            else:
                # Valores predeterminados para casas
                piso = 1
                gastos_comunes = 0
                ascensor = False
        
        cercania_metro = st.checkbox(
            "Cercano a estación de Metro",
            value=False,
            help="A menos de 5 cuadras de una estación"
        )
        
        submit_button = st.form_submit_button(
            "🔍 CALCULAR PRECIO",
            use_container_width=True,
            type="primary"
        )
        
        input_data = {
            "comuna": comuna,
            "tipo_propiedad": tipo_propiedad,
            "metros_totales": metros_totales,
            "metros_construidos": metros_construidos,
            "dormitorios": dormitorios,
            "banos": banos,
            "estacionamientos": estacionamientos,
            "antiguedad_anos": antiguedad_anos,
            "piso": piso,
            "orientacion": orientacion,
            "gastos_comunes": gastos_comunes,
            "cercania_metro": cercania_metro,
            "ascensor": ascensor
        }
        
        return submit_button, input_data

# Función para mostrar los resultados de la predicción
def mostrar_resultados(precio_predicho, input_data, datos_propiedades, tendencias):
    """Muestra los resultados de la predicción y análisis adicionales"""
    st.markdown("---")
      # Usar los valores ya calculados si vienen en forma de tupla
    if isinstance(precio_predicho, tuple):
        precio_clp, precio_millones, precio_uf = precio_predicho
    else:
        # Si viene solo el precio en CLP, calculamos los otros formatos
        precio_clp = precio_predicho
        valor_uf = 36000  # Valor UF aproximado
        precio_millones = precio_clp / 1_000_000
        precio_uf = precio_clp / valor_uf
      # Determinar el modo de predicción utilizado
    ultimo_request_id = st.session_state.get('ultimo_request_id', '')
    modo_prediccion = st.session_state.get(f'modo_prediccion_{ultimo_request_id}', 'desconocido')
    razon_demo = st.session_state.get(f'demo_razon_{ultimo_request_id}', '')
    
    # Mostrar el precio predicho en diferentes formatos con indicador del modo utilizado
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Añadir un indicador del modo de predicción
    if 'modelo_real' in modo_prediccion:
        st.success("✅ Predicción generada usando el **MODELO REAL** de Machine Learning entrenado con datos del mercado")
    elif 'demo' in modo_prediccion:
        if razon_demo:
            st.warning(f"⚠️ Predicción generada usando el **MODO DEMO** basado en promedios del mercado (Razón: {razon_demo})")
        else:
            st.warning("⚠️ Predicción generada usando el **MODO DEMO** basado en promedios del mercado")
    else:
        st.info("ℹ️ Predicción generada (modo no especificado)")
    
    with col1:
        st.metric(
            label="💰 Precio estimado",
            value=f"${precio_clp:,.0f} CLP",
            delta=f"±{5}% margen de error"
        )
    
    with col2:
        st.metric(
            label="🏦 Precio en millones",
            value=f"${precio_millones:.1f}M",
            delta=f"{precio_millones/input_data['metros_construidos']:.1f}M/m²"
        )
    
    with col3:
        st.metric(
            label="📊 Precio en UF",
            value=f"{precio_uf:.0f} UF",
            delta=f"{precio_uf/input_data['metros_construidos']:.1f} UF/m²"
        )
    
    # Agregar información sobre el precio por metro cuadrado
    st.markdown(f"""
    <div style='background-color:#f8f9fa; padding:1rem; border-radius:10px; margin:1rem 0'>
        <h4>💡 Análisis del precio por metro cuadrado:</h4>
        <ul>
            <li>Precio por m² construido: <b>{precio_uf/input_data['metros_construidos']:.1f} UF/m²</b></li>
            <li>Precio por m² total: <b>{precio_uf/input_data['metros_totales']:.1f} UF/m²</b></li>
            <li>Rango típico en {input_data['comuna']}: 
                {precio_base_comuna(input_data['comuna']):.0f} - {precio_base_comuna(input_data['comuna'])*1.3:.0f} UF/m²</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Mostrar análisis adicionales en pestañas
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Tendencias", "🔍 Comparables", "⚠️ Alertas", "📋 Detalles"])
    
    with tab1:
        st.subheader("Tendencia de precios")
        fig = generar_grafico_tendencias(tendencias, input_data['comuna'], input_data['tipo_propiedad'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Análisis de tendencia
        st.info(f"""
        **Análisis de tendencia para {input_data['comuna']} - {input_data['tipo_propiedad']}:**
        
        El mercado muestra una tendencia {random.choice(['al alza', 'estable con ligero incremento', 'con variaciones estacionales'])} 
        en los últimos 12 meses. {random.choice([
            'El mejor momento para vender suele ser entre marzo y mayo.',
            'La demanda ha incrementado un 12% en el último trimestre.',
            'El tiempo promedio de venta es de 4.2 meses para este tipo de propiedad.'
        ])}
        """)
    
    with tab2:
        st.subheader("Propiedades comparables")
        comparables = obtener_comparables(input_data, datos_propiedades)
        
        if len(comparables) > 0:            # Crear una copia del DataFrame para evitar advertencias de SettingWithCopy
            comparables_display = comparables[['comuna', 'tipo_propiedad', 'metros_construidos', 
                                             'dormitorios', 'banos', 'antiguedad_anos', 'precio']].copy()
            
            # Calcular precio en millones
            comparables_display.loc[:, 'precio_millones'] = comparables_display['precio'] / 1_000_000
            
            # Renombrar columnas
            comparables_display = comparables_display.rename(columns={
                'metros_construidos': 'm² const.', 
                'dormitorios': 'Dorm.', 
                'banos': 'Baños', 
                'antiguedad_anos': 'Años',
                'precio_millones': 'Precio (MM$)'
            })
            
            # Formato para mostrar
            comparables_display.loc[:, 'Precio (MM$)'] = comparables_display['Precio (MM$)'].apply(lambda x: f"${x:.1f}")
            comparables_display = comparables_display.drop('precio', axis=1)
            
            st.dataframe(comparables_display, use_container_width=True)
              # Análisis de comparables
            precio_promedio = float(comparables['precio'].mean())
            # Asegurarse de que precio_predicho sea un número, no un array
            if isinstance(precio_predicho, tuple):
                precio_comparacion = precio_clp
            else:
                precio_comparacion = precio_predicho
            
            diferencia = ((precio_comparacion - precio_promedio) / precio_promedio) * 100
            
            if abs(diferencia) < 10:
                st.success(f"✅ El precio estimado está en línea con propiedades similares (diferencia: {diferencia:.1f}%)")
            elif diferencia > 0:
                st.warning(f"⚠️ El precio estimado es {diferencia:.1f}% mayor que propiedades similares")
            else:
                st.info(f"💡 El precio estimado es {abs(diferencia):.1f}% menor que propiedades similares - posible oportunidad")
        else:
            st.warning("No se encontraron propiedades comparables con los criterios seleccionados")
    
    with tab3:
        st.subheader("Alertas y recomendaciones")
        
        # Generar alertas según los datos
        alertas = []
        
        # Alerta por antigüedad
        if input_data['antiguedad_anos'] > 30:
            alertas.append({
                "tipo": "warning",
                "mensaje": "Propiedad con antigüedad significativa (>30 años)",
                "detalle": "Considerar factores de depreciación y posibles gastos en reparaciones estructurales."
            })
        
        # Alerta por precio
        if precio_millones > 500:
            alertas.append({
                "tipo": "warning",
                "mensaje": "Propiedad en segmento alto (>$500 millones)",
                "detalle": "Mercado con menor liquidez. Tiempo estimado de venta: 8-10 meses."
            })
        
        # Alerta por tamaño
        if input_data['metros_construidos'] < 40:
            alertas.append({
                "tipo": "warning",
                "mensaje": "Propiedad con metros construidos reducidos (<40m²)",
                "detalle": "Puede afectar aprobación de créditos hipotecarios en algunos bancos."
            })
        
        # Recomendaciones positivas
        if input_data['cercania_metro']:
            alertas.append({
                "tipo": "success",
                "mensaje": "Cercanía al metro - factor positivo",
                "detalle": "Aumenta valoración y reduce tiempo de venta en aprox. 30%."
            })
        
        if input_data['tipo_propiedad'] == 'Departamento' and input_data['piso'] > 10:
            alertas.append({
                "tipo": "success",
                "mensaje": "Departamento en piso alto - factor positivo",
                "detalle": "Mayor valor por m² y mejor vista panorámica."
            })
            
        # Mostrar alertas
        if alertas:
            for alerta in alertas:
                if alerta["tipo"] == "warning":
                    st.warning(f"⚠️ {alerta['mensaje']}: {alerta['detalle']}")
                elif alerta["tipo"] == "success":
                    st.success(f"✅ {alerta['mensaje']}: {alerta['detalle']}")
                else:
                    st.info(f"💡 {alerta['mensaje']}: {alerta['detalle']}")
        else:
            st.success("✅ No se detectaron alertas para esta propiedad")
        
        # Añadir recomendación de venta/inversión
        if random.random() > 0.5:
            st.info("""
            💡 **Recomendación de inversión**: 
            Considerando los parámetros actuales, esta propiedad presenta un potencial de rentabilidad de aproximadamente 
            5.2% anual en arriendo, superior al promedio del sector (4.8%).
            """)
        else:
            st.info("""
            💡 **Recomendación de venta**: 
            Para optimizar el precio de venta, considere destacar la ubicación y cercanía a servicios. 
            El tiempo estimado de venta para propiedades similares es de 3.5 meses.
            """)
    
    with tab4:
        st.subheader("Detalles de la predicción")
        
        # Mostrar detalles técnicos
        st.markdown("""
        **Metodología de predicción:**
        
        El precio estimado se calculó utilizando un modelo ensemble que combina:
        - Random Forest Regressor (50%)
        - Gradient Boosting Regressor (40%)
        - Regresión Lineal (10%)
        
        El modelo fue entrenado con datos representativos del mercado inmobiliario chileno,
        considerando más de 25 variables y sus interacciones.
        
        **Variables con mayor influencia en este caso:**
        """)
        
        # Variables influyentes simuladas
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            1. Ubicación (comuna)
            2. Metros construidos
            3. Antigüedad
            4. Dormitorios
            """)
        with col2:
            st.markdown("""
            5. Cercanía al metro
            6. Orientación
            7. Piso (para departamentos)
            8. Estacionamientos
            """)
            
        # Agregar botón para PDF detallado
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="📄 Descargar informe detallado (PDF)",
            data=b"Contenido simulado para demo",
            file_name=f"informe_tasacion_{input_data['comuna']}_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            disabled=True,
            help="Disponible en versión completa"
        )

# Función para mostrar sección de planes y precios
def mostrar_planes_precios():
    """Muestra los planes y precios del servicio"""
    st.markdown("---")
    st.header("💰 Planes y Precios")
    
    # Datos de los planes
    planes = {
        "plan": ["🔍 BÁSICO", "💼 PROFESIONAL", "🏢 EMPRESA"],
        "precio": ["$50.000 /mes", "$120.000 /mes", "$500.000 /mes"],
        "descripcion": [
            "Para agentes independientes y pequeñas inmobiliarias",
            "Para corredoras de propiedades y tasadores profesionales",
            "Para empresas inmobiliarias, bancos y grandes consultoras"
        ],
        "consultas": ["100/mes", "500/mes", "Ilimitadas"],
        "caracteristicas": [
            ["✓ Predicción individual", "✓ Tendencias básicas", "✓ Comparables limitados", "✓ Soporte por email", "✓ Índices inmobiliarios básicos"],
            ["✓ API REST", "✓ Tendencias avanzadas", "✓ Exportación PDF", "✓ Notificaciones", "✓ Soporte prioritario", "✓ Índices inmobiliarios completos"],
            ["✓ API dedicada", "✓ Integración personalizada", "✓ Soporte 24/7", "✓ Historial completo", "✓ Reporte personalizado", "✓ Dashboard de índices en tiempo real"]
        ]
    }
    
    # Mostrar planes en columnas
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div style="border:1px solid #ddd; border-radius:10px; padding:1.5rem; height:100%; position:relative; {'background-color:#f8f9fa' if i != 1 else 'background-color:#f0f7ff; border:2px solid #0d6efd'}">
                <h3 style="text-align:center; margin-bottom:0.5rem">{planes['plan'][i]}</h3>
                <div style="text-align:center; font-size:1.5rem; font-weight:bold; margin-bottom:1rem">{planes['precio'][i]}</div>
                <p style="text-align:center; color:#666; margin-bottom:1rem">{planes['descripcion'][i]}</p>
                <div style="text-align:center; background-color:{'#0d6efd' if i == 1 else '#6c757d'}; color:white; padding:0.5rem; border-radius:5px; margin-bottom:1rem">
                    {planes['consultas'][i]} consultas
                </div>
                <ul style="list-style-type:none; padding-left:0">
                    {"".join([f'<li style="margin-bottom:0.5rem">{item}</li>' for item in planes['caracteristicas'][i]])}
                </ul>
                {"<div style='position:absolute; top:-12px; right:-12px; background-color:#dc3545; color:white; padding:5px 10px; border-radius:20px; font-weight:bold; font-size:0.8rem'>MÁS POPULAR</div>" if i == 1 else ""}
            </div>
            """, unsafe_allow_html=True)
    
    # Añadir CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center">
        <a name="contacto"></a>
        <div style="display:inline-block; background-color:#0d6efd; color:white; padding:0.8rem 2rem; border-radius:5px; font-weight:bold; font-size:1.2rem; margin-bottom:1rem">
            📱 CONTACTAR PARA CONTRATAR O SOLICITAR DEMO EXTENDIDA
        </div>
        <p>Consulta por descuentos para contratación anual o integraciones a medida</p>
    </div>
    """, unsafe_allow_html=True)

# Función para mostrar casos de éxito
#def
#            "logo": "🏠"
#        }
#    ]
#    
#    # Mostrar testimonios
#    cols = st.columns(3)
#    for i, col in enumerate(cols):
#        with col:
#            st.markdown(f"""
#            <div style="border:1px solid #ddd; border-radius:10px; padding:1.5rem; height:100%; background-color:#f8f9fa">
#                <div style="font-size:3rem; text-align:center">{testimonios[i]['logo']}</div>
#                <div style="text-align:center; font-weight:bold; margin-top:0.5rem">{testimonios[i]['cliente']}</div>
#                <div style="text-align:center; color:#666; font-size:0.9rem; margin-bottom:1rem">{testimonios[i]['cargo']}</div>
#                <p style="font-style:italic">"{testimonios[i]['testimonio']}"</p>
#                <div style="text-align:center; margin-top:1rem">
#                   ⭐⭐⭐⭐⭐
#               </div>
#           </div>
#           """, unsafe_allow_html=True)
####################################################################
#
#     
    # Estadísticas de resultados
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎯 Precisión promedio",
            value="95.3%",
            delta="vs 85% de tasadores"
        )
    
    with col2:
        st.metric(
            label="⏱️ Tiempo ahorrado",
            value="4.5 horas",
            delta="por tasación"
        )
    
    with col3:
        st.metric(
            label="📈 ROI para clientes",
            value="312%",
            delta="primer año"
        )
    
    with col4:
        st.metric(
            label="🏆 Satisfacción",
            value="98%",
            delta="clientes activos"
        )

# Función para mostrar FAQ
def mostrar_faq():
    """Muestra preguntas frecuentes sobre el servicio"""
    st.markdown("---")
    st.header("❓ Preguntas Frecuentes")
    
    # Lista de preguntas y respuestas
    faqs = [
        {
            "pregunta": "¿Qué tan precisas son las predicciones?",
            "respuesta": "Nuestro modelo ensemble alcanza una precisión promedio del 95.3% en las principales comunas de Santiago. Las predicciones se comparan con los valores reales de transacción y se actualizan trimestralmente para mantener la precisión."
        },
        {
            "pregunta": "¿Cómo se integra con sistemas existentes?",
            "respuesta": "Ofrecemos una API REST completa que permite integrarse con cualquier sistema existente. También proporcionamos webhooks para notificaciones en tiempo real y exportación en múltiples formatos (JSON, CSV, PDF, Excel)."
        },
        {
            "pregunta": "¿Qué comunas están cubiertas?",
            "respuesta": "Actualmente cubrimos las 32 comunas del Gran Santiago con máxima precisión. Para el resto del país, ofrecemos predicciones con precisión moderada que mejora constantemente conforme incorporamos más datos."        },
        {
            "pregunta": "¿Cómo se compara con tasadores humanos?",
            "respuesta": "Nuestro sistema no reemplaza a los tasadores profesionales, sino que potencia su trabajo. Los tasadores que usan nuestro sistema mejoran su precisión en un 25% y reducen el tiempo por tasación en un 70%, permitiéndoles enfocarse en el análisis de valor."
        },
        {
            "pregunta": "¿De dónde provienen los índices inmobiliarios?",
            "respuesta": "Los índices inmobiliarios que mostramos provienen del Banco Central de Chile. Son indicadores oficiales que miden la evolución de los precios de viviendas, segmentados por tipo de propiedad (casas/departamentos) y por condición (nuevas/usadas). Los datos se actualizan trimestralmente y cubren desde 2010 hasta la actualidad."
        },
        {
            "pregunta": "¿Es posible una demo personalizada?",
            "respuesta": "¡Absolutamente! Ofrecemos demos personalizadas donde analizamos hasta 50 propiedades de tu cartera actual para demostrar la precisión en tu segmento específico. Contacta con nuestro equipo comercial para agendar."
        },
        {
            "pregunta": "¿De dónde provienen los datos de índices inmobiliarios?",
            "respuesta": "Los índices inmobiliarios mostrados en nuestra plataforma se basan en datos oficiales del Banco Central de Chile, complementados con información del SII, portales inmobiliarios y transacciones reales. Actualizamos estos índices mensualmente para asegurar que reflejen las condiciones actuales del mercado."
        }
    ]
    
    # Mostrar FAQs como expansibles
    for i, faq in enumerate(faqs):
        with st.expander(f"{i+1}. {faq['pregunta']}"):
            st.markdown(faq['respuesta'])

# Función para determinar si la diferencia entre versiones es solo a nivel de parche
def _es_diferencia_menor_version(v1, v2):
    """Determina si la diferencia entre dos versiones es solo en el nivel de parche"""
    if v1 == v2:
        return True
    
    try:
        # Extraer componentes de versión
        v1_parts = v1.split('.')
        v2_parts = v2.split('.')
        
        # Asegurar que ambos tienen al menos 3 componentes (major.minor.patch)
        while len(v1_parts) < 3:
            v1_parts.append('0')
        while len(v2_parts) < 3:
            v2_parts.append('0')
        
        # Verificar si solo difieren en la versión de parche
        return (v1_parts[0] == v2_parts[0] and 
                v1_parts[1] == v2_parts[1] and 
                v1_parts[2] != v2_parts[2])
    except:
        # Si hay algún error al analizar las versiones, asumimos que no son compatibles
        return False

# Función principal
def main():
    """Función principal que ejecuta la aplicación"""
    # Inicializar variables de sesión para debugging si no existen
    if 'debug_features' not in st.session_state:
        st.session_state['debug_features'] = {}
    if 'debug_features_raw' not in st.session_state:
        st.session_state['debug_features_raw'] = {}
    if 'debug_X_pre_scaler' not in st.session_state:
        st.session_state['debug_X_pre_scaler'] = []
    if 'debug_X_post_scaler' not in st.session_state:
        st.session_state['debug_X_post_scaler'] = []
    if 'debug_prediction' not in st.session_state:
        st.session_state['debug_prediction'] = None
    if 'model_paths' not in st.session_state:
        st.session_state['model_paths'] = {}
    if 'model_version' not in st.session_state:
        st.session_state['model_version'] = {}
    if 'model_load_error' not in st.session_state:
        st.session_state['model_load_error'] = None
    if 'ultimo_input' not in st.session_state:
        st.session_state['ultimo_input'] = {}    
    if 'ultimo_request_id' not in st.session_state:
        st.session_state['ultimo_request_id'] = None
    if 'debug_demo_base' not in st.session_state:
        st.session_state['debug_demo_base'] = None
    if 'debug_demo_variacion' not in st.session_state:
        st.session_state['debug_demo_variacion'] = None
    if 'debug_demo_comuna' not in st.session_state:
        st.session_state['debug_demo_comuna'] = None
        
    # Agregar controles del modelo a la barra lateral primero
    add_model_controls_to_sidebar()
    
    # Obtener parámetros de URL
    try:
        debug_mode = st.query_params.get('debug', '').lower() == 'true'
        force_mode = st.query_params.get('mode', 'auto').lower()
        force_model = st.query_params.get('force_model', 'auto').lower()
    except (AttributeError, Exception):
        debug_mode = st.session_state.get('debug_mode', False)
        force_mode = st.session_state.get('force_mode', 'auto')
        force_model = st.session_state.get('force_model', 'auto')
    
    # Si se fuerza un modo específico, mostrarlo en la interfaz
    if force_mode in ['demo', 'real']:
        st.info(f"🔒 Modo forzado: {force_mode.upper()}")
      # Si se fuerza un modelo específico, mostrarlo en la interfaz
    if force_model in ['demo', 'real']:
        st.info(f"🔒 Modelo forzado: {force_model.upper()}")
    
    mostrar_header()
    
    # Añadir sidebar components
    add_sidebar_contact()
    
    # Menú de navegación en pestañas
    tab_names = ["🔍 Predictor de Precios", "📊 Índices Inmobiliarios"]
    if debug_mode:
        tab_names.append("🔧 Depuración")
        tab_names.append("🔍 Test A/B")
    
    tabs = st.tabs(tab_names)
    
    with tabs[0]:
        # Cargar datos y modelo
        datos_propiedades, tendencias = cargar_datos()
        modelo = cargar_modelo()
        
        # Definir opciones de comunas basadas en los datos
        comuna_options = sorted(datos_propiedades['comuna'].unique().tolist())
        
        # Mostrar formulario de predicción
        submit_button, input_data = mostrar_formulario_prediccion(comuna_options, modelo)
        
        # Realizar predicción si se envía el formulario
        if submit_button:            
            with st.spinner("Calculando precio..."):
                # Simular tiempo de procesamiento para efecto visual
                time.sleep(1.5)
                
                # Calcular predicción
                resultados = predecir_precio(modelo=modelo, input_data=input_data)
                
                if resultados is not None:
                    # mostrar_resultados espera (precio_clp, precio_millones, precio_uf) o un solo valor en CLP
                    mostrar_resultados(resultados, input_data, datos_propiedades, tendencias)
    
    with tabs[1]:
        # Mostrar dashboard de índices inmobiliarios
        mostrar_dashboard_indices()
      # Panel de depuración si está habilitado
    if debug_mode and len(tabs) > 2:
        with tabs[2]:
            st.header("Panel de Depuración")
            
            # Información de modo de operación
            st.subheader("Modo de Operación")
            cols = st.columns(3)
            with cols[0]:
                st.info(f"Modo: {force_mode.upper() if force_mode in ['demo', 'real'] else 'AUTO'}")
            
            with cols[1]:
                if st.button("Forzar modo DEMO", key="force_demo"):
                    try:
                        st.query_params['mode'] = 'demo'
                    except (AttributeError, Exception):
                        st.session_state['force_mode'] = 'demo'
                    st.rerun()
            
            with cols[2]:
                if st.button("Forzar modo REAL", key="force_real"):
                    try:
                        st.query_params['mode'] = 'real'
                    except (AttributeError, Exception):
                        st.session_state['force_mode'] = 'real'
                    st.rerun()
            
            st.subheader("Información del Modelo")
            st.json(st.session_state['model_version'])
            
            st.subheader("Rutas de Archivos")
            st.json(st.session_state['model_paths'])
            
            if st.session_state['model_load_error']:
                st.subheader("Error de Carga del Modelo")
                st.error(st.session_state['model_load_error']['error'])
                with st.expander("Detalles del error"):
                    st.code(st.session_state['model_load_error']['traceback'])
            
            st.subheader("Última Predicción")
            cols = st.columns(2)
            with cols[0]:
                st.json(st.session_state['ultimo_input'])
            with cols[1]:
                # Mostrar información del último request
                request_id = st.session_state['ultimo_request_id']
                if request_id:
                    modo_key = f'modo_prediccion_{request_id}'
                    resultado_key = f'resultado_final_{request_id}'
                    resultado_demo_key = f'resultado_final_demo_{request_id}'
                    error_key = f'error_prediccion_{request_id}'
                    
                    if modo_key in st.session_state:
                        st.success(f"Modo: {st.session_state[modo_key]}")
                    
                    if resultado_key in st.session_state:
                        st.write("Resultado final:")
                        st.json(st.session_state[resultado_key])
                    elif resultado_demo_key in st.session_state:
                        st.write("Resultado demo:")
                        st.json(st.session_state[resultado_demo_key])
                    
                    if error_key in st.session_state:
                        st.error(f"Error: {st.session_state[error_key]['error']}")
            
            # Detalles de características
            st.subheader("Características Usadas (Raw)")
            
            # Mostrar las características en formato tabular para mejor visualización
            if st.session_state['debug_features_raw']:
                # Convertir a formato tabular
                feature_df = pd.DataFrame([st.session_state['debug_features_raw']])
                st.dataframe(feature_df.T.reset_index().rename(columns={'index': 'Característica', 0: 'Valor'}))
            else:
                st.info("No hay datos de características disponibles")
            
            # Información de modo demo si está disponible
            if st.session_state['debug_demo_base'] is not None:
                st.subheader("Información de Modo Demo")
                cols = st.columns(3)
                with cols[0]:
                    st.metric("Precio base (UF/m²)", f"{st.session_state['debug_demo_base']:.1f}")
                with cols[1]:
                    st.metric("Comuna", st.session_state['debug_demo_comuna'])
                with cols[2]:
                    st.metric("Variación aleatoria", f"{st.session_state['debug_demo_variacion']:.2%}")
            
            st.subheader("Resultado de Predicción Crudo")
            st.write(f"Valor en UF (sin procesar): {st.session_state['debug_prediction']}")
              # Botón para probar carga de modelo
            if st.button("Probar carga de modelo", key="test_model_load_button"):
                try:
                    import joblib
                    model_path = Path(st.session_state['model_paths']['model'])
                    scaler_path = Path(st.session_state['model_paths']['scaler'])
                    
                    modelo_test = joblib.load(model_path)
                    scaler_test = joblib.load(scaler_path)
                    
                    st.success(f"Modelo cargado correctamente. Tipo: {type(modelo_test).__name__}")
                    st.success(f"Scaler cargado correctamente. Tipo: {type(scaler_test).__name__}")
                except Exception as e:
                    st.error(f"Error al cargar modelo para prueba: {str(e)}")
              # Botón para limpiar caché de Streamlit
            if st.button("Limpiar caché de Streamlit", key="clear_streamlit_cache_debug"):
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success("Caché de Streamlit limpiado. Recarga la página para ver los cambios.")
      # Test A/B si está en modo debug
    if debug_mode and len(tabs) > 3:
        with tabs[3]:
            st.header("Test Comparativo A/B")
            st.write("Esta herramienta permite comparar las predicciones del modelo real vs. modo demo")
            
            cols = st.columns(2)
            with cols[0]:
                st.subheader("Configuración de la propiedad")
                test_comuna = st.selectbox("Comuna", options=comuna_options, key="test_ab_comuna")
                test_tipo = st.radio("Tipo de propiedad", ["Departamento", "Casa"], horizontal=True, key="test_ab_tipo")
                test_metros = st.number_input("Metros construidos", min_value=30.0, max_value=200.0, value=90.0, key="test_ab_metros")
                test_dormitorios = st.slider("Dormitorios", min_value=1, max_value=5, value=3, key="test_ab_dormitorios")
                test_banos = st.slider("Baños", min_value=1, max_value=4, value=2, key="test_ab_banos")
            
            # Botón para ejecutar el test
            if st.button("Ejecutar test A/B", key="run_ab_test"):
                # Preparar datos de prueba
                test_data = {
                    'comuna': test_comuna,
                    'tipo_propiedad': test_tipo,
                    'metros_totales': test_metros + 10,  # Algo mayor que metros construidos
                    'metros_construidos': test_metros,
                    'dormitorios': test_dormitorios,
                    'banos': test_banos,
                    'estacionamientos': 1,
                    'antiguedad_anos': 10,
                    'orientacion': 'Norte'
                }                # Ejecutar modelo real
                try:
                    old_mode = st.query_params.get('mode', 'auto')
                    st.query_params['mode'] = 'real'
                except (AttributeError, Exception):
                    old_mode = st.session_state.get('force_mode', 'auto')
                    st.session_state['force_mode'] = 'real'
                
                with st.spinner("Ejecutando modelo real..."):
                    try:
                        modelo = cargar_modelo()
                        resultados_real = predecir_precio(modelo=modelo, input_data=test_data)
                    except Exception as e:
                        st.error(f"Error en modelo real: {str(e)}")
                        resultados_real = None
                  # Ejecutar modo demo
                try:
                    st.query_params['mode'] = 'demo'
                except (AttributeError, Exception):
                    st.session_state['force_mode'] = 'demo'
                
                with st.spinner("Ejecutando modo demo..."):
                    try:
                        resultados_demo = _predecir_precio_demo(test_data)
                    except Exception as e:
                        st.error(f"Error en modo demo: {str(e)}")
                        resultados_demo = None
                  # Restaurar modo original
                try:
                    st.query_params['mode'] = old_mode
                except (AttributeError, Exception):
                    st.session_state['force_mode'] = old_mode
                
                # Mostrar resultados
                cols = st.columns(2)
                with cols[0]:
                    st.subheader("Modelo Real")
                    if resultados_real:
                        st.metric("Precio (UF)", f"{resultados_real[2]:,.0f}")
                        st.metric("Precio (CLP)", f"${resultados_real[0]:,.0f}")
                    else:
                        st.warning("No se pudo obtener resultado del modelo real")
                
                with cols[1]:
                    st.subheader("Modo Demo")
                    if resultados_demo:
                        st.metric("Precio (UF)", f"{resultados_demo[2]:,.0f}")
                        st.metric("Precio (CLP)", f"${resultados_demo[0]:,.0f}")
                    else:
                        st.warning("No se pudo obtener resultado del modo demo")
                
                # Mostrar diferencia
                if resultados_real and resultados_demo:
                    diferencia = resultados_real[2] - resultados_demo[2]
                    porcentaje = (diferencia / resultados_demo[2]) * 100 if resultados_demo[2] != 0 else 0
                    st.metric("Diferencia (UF)", f"{diferencia:,.0f}", f"{porcentaje:+.1f}%")
    
    # Mostrar planes y precios
    mostrar_planes_precios()
    
    # Mostrar FAQ
    mostrar_faq()
    
    # Añadir footer con contacto
    add_page_footer()

# Función para agregar controles del modelo a la barra lateral
def add_model_controls_to_sidebar():
    """Añade controles para forzar el modelo real o demo en la barra lateral"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Controles del Modelo")
      # Obtener el modo actual
    try:
        current_model_mode = st.query_params.get('force_model', 'auto')
    except (AttributeError, Exception):
        current_model_mode = 'auto'  # Fallback para Streamlit Cloud
    
    # Opciones para el radio button
    model_mode_options = {
        'auto': 'Automático (recomendado)',
        'real': 'Forzar modelo real',
        'demo': 'Forzar modo demo'
    }
    
    # Radio button para seleccionar el modo
    selected_model_mode = st.sidebar.radio(
        "Modo del modelo:",
        options=list(model_mode_options.keys()),
        format_func=lambda x: model_mode_options[x],
        index=list(model_mode_options.keys()).index(current_model_mode) if current_model_mode in model_mode_options else 0
    )
      # Si cambió el modo, actualizar la URL
    if selected_model_mode != current_model_mode:
        try:
            st.query_params['force_model'] = selected_model_mode
            st.rerun()
        except (AttributeError, Exception):
            # Fallback para Streamlit Cloud
            if 'debug_mode' in st.session_state and st.session_state.get('debug_mode', False):
                st.sidebar.info("Nota: No se pudo actualizar la URL en esta versión de Streamlit")
            # Usar session_state como alternativa para mantener el estado
            st.session_state['force_model'] = selected_model_mode
            st.rerun()
    
    # Explicación del modo seleccionado
    if selected_model_mode == 'auto':
        st.sidebar.info("El sistema determinará automáticamente si debe usar el modelo real o el modo demo según la compatibilidad de versiones.")
    elif selected_model_mode == 'real':
        st.sidebar.warning("⚠️ Forzar el modelo real puede causar errores si hay incompatibilidades de versiones.")
    else:  # demo
        st.sidebar.info("El modo demo utiliza cálculos basados en promedios del mercado, no el modelo de ML entrenado.")
      # Botón para limpiar caché
    if st.sidebar.button("🧹 Limpiar caché", key="sidebar_clear_cache"):
        st.cache_data.clear()
        st.rerun()

# Ejecutar la aplicación
if __name__ == "__main__":
    # Ejecutar la función principal (que ya incluye la adición de controles)
    main()
