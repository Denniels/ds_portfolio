"""
Herramienta de diagnóstico para el modelo inmobiliario en Streamlit Cloud
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import json
from pathlib import Path
import traceback
import platform

# Configuración de la página
st.set_page_config(
    page_title="Diagnóstico de Modelo Inmobiliario",
    page_icon="🔧",
    layout="wide"
)

# Mostrar título
st.title("🔧 Diagnóstico de Modelo Inmobiliario")
st.write("Esta herramienta ayuda a diagnosticar problemas con el modelo inmobiliario en Streamlit Cloud")

# Información del sistema
st.header("Información del Sistema")
sys_info = {
    "Python Version": sys.version,
    "Platform": platform.platform(),
    "OS": os.name,
    "Streamlit Version": st.__version__,
    "Working Directory": os.getcwd(),
}

# Mostrar información del sistema
for key, value in sys_info.items():
    st.text(f"{key}: {value}")

# Detectar versiones de paquetes
st.header("Versiones de Paquetes Críticos")

try:
    import numpy as np
    st.success(f"NumPy: {np.__version__}")
except ImportError:
    st.error("NumPy no está instalado")

try:
    import pandas as pd
    st.success(f"Pandas: {pd.__version__}")
except ImportError:
    st.error("Pandas no está instalado")

try:
    import sklearn
    st.success(f"Scikit-learn: {sklearn.__version__}")
except ImportError:
    st.error("Scikit-learn no está instalado")

try:
    import joblib
    st.success(f"Joblib: {joblib.__version__}")
except ImportError:
    st.error("Joblib no está instalado")

# Verificar archivos del modelo
st.header("Verificación de Archivos del Modelo")

# Rutas posibles del modelo
model_paths = [
    "app/data/inmobiliario/modelo_inmobiliario.pkl",
    "app/data/modelos/modelo_inmobiliario.pkl",
    "app/models/modelo_inmobiliario.pkl",
    "data/inmobiliario/modelo_inmobiliario.pkl",
]

# Rutas posibles del scaler
scaler_paths = [
    "app/data/inmobiliario/scaler_inmobiliario.pkl",
    "app/data/modelos/scaler_inmobiliario.pkl",
    "app/models/scaler_inmobiliario.pkl",
    "data/inmobiliario/scaler_inmobiliario.pkl",
]

# Rutas posibles del info
info_paths = [
    "app/data/inmobiliario/model_info.json",
    "app/data/modelos/model_info.json",
    "app/models/model_info.json",
    "data/inmobiliario/model_info.json",
]

# Verificar archivos
def check_file(file_path):
    abs_path = os.path.abspath(file_path)
    if os.path.exists(file_path):
        stat = os.stat(file_path)
        return {
            "exists": True,
            "size": stat.st_size,
            "last_modified": pd.Timestamp(stat.st_mtime, unit='s').strftime('%Y-%m-%d %H:%M:%S'),
            "abs_path": abs_path
        }
    else:
        return {
            "exists": False,
            "size": 0,
            "last_modified": "N/A",
            "abs_path": abs_path
        }

# Mostrar resultados
st.subheader("Archivos del Modelo")
for path in model_paths:
    result = check_file(path)
    if result["exists"]:
        st.success(f"✅ {path} (Tamaño: {result['size']} bytes, Modificado: {result['last_modified']})")
    else:
        st.warning(f"⚠️ {path} no encontrado")

st.subheader("Archivos del Scaler")
for path in scaler_paths:
    result = check_file(path)
    if result["exists"]:
        st.success(f"✅ {path} (Tamaño: {result['size']} bytes, Modificado: {result['last_modified']})")
    else:
        st.warning(f"⚠️ {path} no encontrado")

st.subheader("Archivos de Información")
for path in info_paths:
    result = check_file(path)
    if result["exists"]:
        st.success(f"✅ {path} (Tamaño: {result['size']} bytes, Modificado: {result['last_modified']})")
        # Mostrar contenido del archivo JSON si existe
        try:
            with open(path, 'r', encoding='utf-8') as f:
                info_content = json.load(f)
                with st.expander(f"Contenido de {path}"):
                    st.json(info_content)
        except Exception as e:
            st.error(f"Error al leer {path}: {str(e)}")
    else:
        st.warning(f"⚠️ {path} no encontrado")

# Prueba de carga del modelo
st.header("Prueba de Carga del Modelo")

# Función para cargar modelo desde una ruta
def load_model(model_path, scaler_path, info_path):
    try:
        import joblib
        
        # Verificar que todos los archivos existen
        if not all(os.path.exists(p) for p in [model_path, scaler_path, info_path]):
            return False, f"No se encontraron todos los archivos necesarios"
        
        # Cargar información del modelo
        with open(info_path, 'r', encoding='utf-8') as f:
            model_info = json.load(f)
        
        # Cargar modelo y scaler
        modelo = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        # Intentar una predicción simple para probar el modelo
        if hasattr(modelo, 'predict'):
            # Crear un array ficticio con el número correcto de características
            n_features = len(model_info.get('feature_names', []))
            if n_features == 0:
                n_features = 22  # Valor predeterminado basado en model_info.json
            
            X = np.zeros((1, n_features))
            try:
                # Intentar predecir
                prediction = modelo.predict(X)
                return True, f"Modelo cargado correctamente. Predicción de prueba: {prediction[0]}"
            except Exception as e:
                return False, f"Error al hacer predicción de prueba: {str(e)}"
        else:
            return False, f"El modelo cargado no tiene método 'predict'"
            
    except Exception as e:
        error_details = traceback.format_exc()
        return False, f"Error al cargar el modelo: {str(e)}\n\n{error_details}"

# Seleccionar rutas para probar
if model_paths and scaler_paths and info_paths:
    model_options = [p for p in model_paths if os.path.exists(p)]
    scaler_options = [p for p in scaler_paths if os.path.exists(p)]
    info_options = [p for p in info_paths if os.path.exists(p)]
    
    if model_options and scaler_options and info_options:
        st.subheader("Seleccionar archivos para probar")
        selected_model = st.selectbox("Archivo del modelo", model_options)
        selected_scaler = st.selectbox("Archivo del scaler", scaler_options)
        selected_info = st.selectbox("Archivo de información", info_options)
        
        if st.button("Probar carga de modelo"):
            with st.spinner("Cargando modelo..."):
                success, message = load_model(selected_model, selected_scaler, selected_info)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    else:
        st.error("No se encontraron todos los archivos necesarios para probar el modelo")
else:
    st.error("No se han definido rutas para los archivos del modelo")

# Prueba de predicción con modelo cargado
st.header("Prueba de Predicción")

# Seleccionar comuna para predicción
comunas = ["Las Condes", "Providencia", "Vitacura", "La Florida", "Ñuñoa", "Santiago", "La Reina", "Maipú"]
selected_comuna = st.selectbox("Comuna", options=comunas)

# Parámetros básicos
col1, col2 = st.columns(2)
with col1:
    tipo_propiedad = st.radio("Tipo de propiedad", ["Departamento", "Casa"], horizontal=True)
    metros_construidos = st.number_input("Metros construidos", min_value=25.0, max_value=200.0, value=90.0, step=10.0)
    dormitorios = st.slider("Dormitorios", min_value=1, max_value=5, value=2, step=1)
with col2:
    metros_totales = st.number_input("Metros totales", min_value=30.0, max_value=300.0, value=100.0, step=10.0)
    banos = st.slider("Baños", min_value=1, max_value=4, value=2, step=1)
    estacionamientos = st.slider("Estacionamientos", min_value=0, max_value=3, value=1, step=1)
    antiguedad_anos = st.slider("Antigüedad (años)", min_value=0, max_value=40, value=10, step=1)

# Función para realizar predicción de prueba
def test_prediction(model_path, scaler_path, info_path, input_data):
    try:
        import joblib
        
        # Cargar modelo, scaler e info
        modelo = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        with open(info_path, 'r', encoding='utf-8') as f:
            model_info = json.load(f)
        
        # Obtener lista de características
        feature_names = model_info.get('feature_names', [])
        
        # Crear diccionario con todas las características inicializadas a 0
        features_dict = {feature: 0 for feature in feature_names}
        
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
        comuna_key = f"comuna_{input_data['comuna']}"
        for feature in features_dict.keys():
            if feature.startswith('comuna_') and feature == comuna_key:
                features_dict[feature] = 1
        
        # Asignar variables dummy para tipo de propiedad
        tipo_key = f"tipo_propiedad_{input_data['tipo_propiedad']}"
        for feature in features_dict.keys():
            if feature.startswith('tipo_propiedad_') and feature == tipo_key:
                features_dict[feature] = 1
        
        # Asignar variables dummy para orientación
        if 'orientacion' in input_data:
            orientacion_key = f"orientacion_{input_data['orientacion']}"
            for feature in features_dict.keys():
                if feature.startswith('orientacion_') and feature == orientacion_key:
                    features_dict[feature] = 1
        
        # Crear array con las características en el orden correcto
        X = np.array([[features_dict[feature] for feature in feature_names]])
        
        # Aplicar el scaler si está disponible
        if scaler is not None:
            X = scaler.transform(X)
        
        # Predecir precio en UF
        precio_uf = float(modelo.predict(X)[0])
        
        # Convertir a diferentes formatos
        valor_uf = 36000  # Valor UF aproximado
        precio_clp = precio_uf * valor_uf
        precio_millones = precio_clp / 1_000_000
        
        return True, {
            "precio_uf": precio_uf,
            "precio_clp": precio_clp,
            "precio_millones": precio_millones,
            "features_used": features_dict
        }
        
    except Exception as e:
        error_details = traceback.format_exc()
        return False, f"Error al hacer predicción: {str(e)}\n\n{error_details}"

# Probar predicción
if st.button("Realizar predicción de prueba"):
    # Verificar que hay archivos disponibles
    if model_options and scaler_options and info_options:
        # Preparar datos de entrada
        input_data = {
            "comuna": selected_comuna,
            "tipo_propiedad": tipo_propiedad,
            "metros_totales": metros_totales,
            "metros_construidos": metros_construidos,
            "dormitorios": dormitorios,
            "banos": banos,
            "estacionamientos": estacionamientos,
            "antiguedad_anos": antiguedad_anos,
            "orientacion": "Norte",  # Valor predeterminado
            "piso": 5 if tipo_propiedad == "Departamento" else 1,
            "cercania_metro": False
        }
        
        with st.spinner("Realizando predicción..."):
            success, result = test_prediction(selected_model, selected_scaler, selected_info, input_data)
            
            if success:
                st.success("Predicción realizada correctamente")
                
                # Mostrar resultados
                col1, col2, col3 = st.columns(3)
                col1.metric("Precio (UF)", f"{result['precio_uf']:,.2f} UF")
                col2.metric("Precio (CLP)", f"${result['precio_clp']:,.0f}")
                col3.metric("Precio (Millones)", f"${result['precio_millones']:,.2f} M")
                
                # Mostrar características utilizadas
                with st.expander("Características utilizadas"):
                    st.json(result['features_used'])
            else:
                st.error(result)
    else:
        st.error("No se encontraron todos los archivos necesarios para probar la predicción")

# Consejos para solucionar problemas
st.header("Consejos para Solucionar Problemas")
st.markdown("""
### Problemas comunes y soluciones:

1. **Modelo no encontrado**: Verifica que los archivos existan en la ruta correcta y que estén siendo rastreados por git.

2. **Error de versión de scikit-learn**: Asegúrate de que el modelo fue guardado con la misma versión de scikit-learn que está instalada en Streamlit Cloud.

3. **Error de incompatibilidad de numpy**: Los errores relacionados con numpy.random.bit_generator pueden ocurrir cuando el modelo se guarda con una versión de numpy diferente.

4. **Predicciones siempre iguales**: Verifica que se están pasando correctamente las características al modelo y que se están utilizando las variables dummy correctas.

5. **Error en la transformación de características**: Asegúrate de que el scaler se está aplicando correctamente y que las características están en el mismo orden que durante el entrenamiento.

### Pasos recomendados:

1. Verifica que todos los archivos necesarios estén presentes en el repositorio y se suban a Streamlit Cloud.

2. Regenera el modelo usando exactamente las mismas versiones de las bibliotecas que usa Streamlit Cloud.

3. Asegúrate de que el código que prepara los datos para la predicción utiliza exactamente las mismas características y en el mismo orden que el modelo espera.

4. Agrega código de depuración para ver exactamente qué datos se están pasando al modelo y qué resultado está devolviendo.
""")

# Ejecutar diagnóstico
st.header("Ejecutar Diagnóstico Completo")
if st.button("Ejecutar diagnóstico completo"):
    with st.spinner("Ejecutando diagnóstico..."):
        # Verificar rutas y archivos
        st.subheader("Estructura de directorios")
        for root_dir in [".", "app", "data"]:
            if os.path.exists(root_dir):
                st.success(f"Directorio {root_dir} encontrado")
                # Mostrar estructura de directorios
                dir_structure = []
                for root, dirs, files in os.walk(root_dir, topdown=True, maxdepth=3):
                    level = root.replace(root_dir, '').count(os.sep)
                    indent = ' ' * 4 * level
                    dir_structure.append(f"{indent}{os.path.basename(root)}/")
                    sub_indent = ' ' * 4 * (level + 1)
                    for f in files:
                        dir_structure.append(f"{sub_indent}{f}")
                
                st.code("\n".join(dir_structure))
            else:
                st.warning(f"Directorio {root_dir} no encontrado")
        
        # Verificar variables de entorno
        st.subheader("Variables de entorno")
        env_vars = dict(os.environ)
        # Filtrar variables sensibles
        filtered_vars = {k: v for k, v in env_vars.items() if not any(s in k.lower() for s in ["key", "secret", "password", "token"])}
        st.json(filtered_vars)
        
        st.success("Diagnóstico completo finalizado")
