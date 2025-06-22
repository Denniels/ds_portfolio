"""
Herramienta de diagnóstico específica para el Predictor Inmobiliario
Esta herramienta ayuda a identificar y resolver problemas de caché y predicciones idénticas
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import time
import uuid
import json
import platform
import traceback
import plotly.express as px
import random

# Importar componentes necesarios desde el predictor inmobiliario
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
predictor_path = current_dir / "10_predictor_inmobiliario.py"

# Verificar si el archivo del predictor existe
if not predictor_path.exists():
    st.error(f"No se encontró el archivo del predictor inmobiliario en {predictor_path}")
    st.stop()

# Agregar el directorio padre al path para importaciones
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Configurar página
st.set_page_config(
    page_title="Diagnóstico del Predictor Inmobiliario",
    page_icon="🔍",
    layout="wide"
)

# Título
st.title("🔍 Diagnóstico del Predictor Inmobiliario")
st.write("Esta herramienta está diseñada para detectar y solucionar problemas específicos del predictor inmobiliario")

# Intentar importar funciones del predictor
try:
    # Importamos las funciones del predictor de manera más segura
    import importlib.util
    import sys
    
    # Construir ruta al módulo del predictor
    predictor_path_str = str(predictor_path)
    
    # Cargar el módulo del predictor inmobiliario
    spec = importlib.util.spec_from_file_location("predictor_inmobiliario", predictor_path_str)
    predictor = importlib.util.module_from_spec(spec)
    sys.modules["predictor_inmobiliario"] = predictor
    spec.loader.exec_module(predictor)
    
    # Ahora podemos acceder a las funciones
    cargar_modelo = predictor.cargar_modelo
    _predecir_precio_demo = predictor._predecir_precio_demo
    predecir_precio = predictor.predecir_precio
    precio_base_comuna = predictor.precio_base_comuna
    
    st.success("✅ Funciones del predictor importadas correctamente")
except Exception as e:
    st.error(f"❌ Error al importar funciones del predictor: {str(e)}")
    st.code(traceback.format_exc())
    st.warning("Algunas funcionalidades no estarán disponibles")
    
    # Definir funciones simuladas para que la página no falle
    def cargar_modelo():
        st.error("Función no disponible")
        return None
        
    def _predecir_precio_demo(input_data, request_id=None):
        st.error("Función no disponible")
        return 0, 0, 0
        
    def predecir_precio(modelo, input_data):
        st.error("Función no disponible")
        return 0, 0, 0
        
    def precio_base_comuna(comuna):
        return 40  # Valor por defecto

# Información del sistema
st.header("Información del Sistema")
system_info = {
    "Sistema operativo": platform.system(),
    "Versión del sistema": platform.release(),
    "Arquitectura": platform.machine(),
    "Python versión": platform.python_version(),
    "Streamlit versión": st.__version__,
    "Entorno Cloud": 'STREAMLIT_SHARING' in os.environ or 'STREAMLIT_CLOUD' in os.environ,
}

# Mostrar información del sistema
st.json(system_info)

# Prueba de predicciones consecutivas
st.header("Prueba de Predicciones Consecutivas")
st.write("""
Esta prueba realiza varias predicciones consecutivas con los mismos datos para verificar
si cada predicción produce resultados diferentes o si el caché está causando resultados idénticos.
""")

# Formulario para datos de prueba
with st.form("consistency_test_form"):
    st.subheader("Configuración de prueba")
    
    col1, col2 = st.columns(2)
    
    with col1:
        test_comunas = ["Las Condes", "Providencia", "La Reina", "Santiago Centro", "Independencia"]
        test_comuna = st.selectbox("Comuna", options=test_comunas)
        test_tipo = st.radio("Tipo de propiedad", ["Departamento", "Casa"], horizontal=True)
    
    with col2:
        test_metros = st.number_input("Metros construidos", min_value=30.0, max_value=200.0, value=90.0)
        test_dormitorios = st.slider("Dormitorios", min_value=1, max_value=5, value=3)
        test_banos = st.slider("Baños", min_value=1, max_value=4, value=2)
    
    col1, col2 = st.columns(2)
    with col1:
        num_tests = st.slider("Número de pruebas", min_value=3, max_value=10, value=5)
    
    with col2:
        test_mode = st.radio("Modo de prueba", ["demo", "real", "ambos"], horizontal=True)
    
    submit_tests = st.form_submit_button("Ejecutar pruebas de consistencia")

# Si se envió el formulario, ejecutar pruebas
if submit_tests:
    # Preparar datos de prueba
    base_data = {
        'comuna': test_comuna,
        'tipo_propiedad': test_tipo,
        'metros_totales': test_metros + 10,
        'metros_construidos': test_metros,
        'dormitorios': test_dormitorios,
        'banos': test_banos,
        'estacionamientos': 1,
        'antiguedad_anos': 10,
        'orientacion': 'Norte',
        'piso': 3 if test_tipo == 'Departamento' else 1,
        'cercania_metro': False
    }
    
    # Resultados para modo demo
    if test_mode in ["demo", "ambos"]:
        results_demo = []
        
        st.subheader("Pruebas en Modo Demo")
        with st.spinner(f"Ejecutando {num_tests} pruebas en modo demo..."):
            for i in range(num_tests):
                # Crear una copia de los datos base
                test_data = base_data.copy()
                
                # Añadir un ID único
                test_id = f"test_demo_{i+1}_{time.time():.6f}"
                test_data['test_id'] = test_id
                
                # Hacer predicción en modo demo
                start_time = time.time()
                try:
                    precio_clp, precio_millones, precio_uf = _predecir_precio_demo(test_data)
                    success = True
                except Exception as e:
                    precio_uf = None
                    st.error(f"Error en prueba {i+1}: {str(e)}")
                    success = False
                end_time = time.time()
                
                # Guardar resultado
                results_demo.append({
                    'test_id': i + 1,
                    'precio_uf': precio_uf if success else 0,
                    'tiempo': end_time - start_time if success else 0,
                    'success': success
                })
                
                # Mostrar progreso
                st.write(f"Prueba {i+1}: {'✅ Completada' if success else '❌ Error'}")
                
                # Pausa breve entre pruebas
                time.sleep(0.5)
        
        # Mostrar resultados de modo demo
        if results_demo:
            df_results_demo = pd.DataFrame(results_demo)
            
            st.subheader("Resultados de pruebas en modo demo")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.dataframe(df_results_demo)
                
                # Visualizar resultados si hay datos válidos
                valid_results = df_results_demo[df_results_demo['success']]
                if not valid_results.empty:
                    fig = px.line(valid_results, x='test_id', y='precio_uf', markers=True,
                                title=f"Predicciones Demo para {test_comuna} - {test_tipo}")
                    st.plotly_chart(fig)
            
            with col2:
                # Calcular estadísticas
                if not df_results_demo[df_results_demo['success']].empty:
                    prices = df_results_demo[df_results_demo['success']]['precio_uf']
                    
                    mean_price = prices.mean()
                    std_price = prices.std()
                    min_price = prices.min()
                    max_price = prices.max()
                    
                    st.metric("Precio promedio (UF)", f"{mean_price:.2f}")
                    st.metric("Desviación estándar", f"{std_price:.2f}")
                    st.metric("Precio mínimo", f"{min_price:.2f}")
                    st.metric("Precio máximo", f"{max_price:.2f}")
                    st.metric("Rango (max-min)", f"{max_price - min_price:.2f}")
                    
                    # Evaluar variabilidad
                    if std_price < 0.01 * mean_price:
                        st.error("❌ PROBLEMA DETECTADO: Variabilidad muy baja. Las predicciones son prácticamente idénticas.")
                    elif std_price > 0.1 * mean_price:
                        st.success("✅ Variabilidad normal alta: Las predicciones muestran diferencias significativas")
                    else:
                        st.success("✅ Variabilidad normal: Las predicciones muestran diferencias razonables")
                else:
                    st.warning("No hay datos válidos para calcular estadísticas")
    
    # Resultados para modo real
    if test_mode in ["real", "ambos"]:
        # Cargar el modelo real
        with st.spinner("Cargando modelo..."):
            try:
                modelo = cargar_modelo()
                st.success("✅ Modelo cargado correctamente")
            except Exception as e:
                st.error(f"❌ Error al cargar modelo: {str(e)}")
                st.code(traceback.format_exc())
                modelo = None
        
        if modelo:
            results_real = []
            
            st.subheader("Pruebas en Modo Real")
            with st.spinner(f"Ejecutando {num_tests} pruebas con modelo real..."):
                for i in range(num_tests):
                    # Crear una copia de los datos base
                    test_data = base_data.copy()
                    
                    # Añadir un ID único
                    test_id = f"test_real_{i+1}_{time.time():.6f}"
                    test_data['test_id'] = test_id
                    
                    # Hacer predicción con modelo real
                    start_time = time.time()
                    try:
                        precio_clp, precio_millones, precio_uf = predecir_precio(modelo, test_data)
                        success = True
                    except Exception as e:
                        precio_uf = None
                        st.error(f"Error en prueba real {i+1}: {str(e)}")
                        st.code(traceback.format_exc())
                        success = False
                    end_time = time.time()
                    
                    # Guardar resultado
                    results_real.append({
                        'test_id': i + 1,
                        'precio_uf': precio_uf if success else 0,
                        'tiempo': end_time - start_time if success else 0,
                        'success': success
                    })
                    
                    # Mostrar progreso
                    st.write(f"Prueba real {i+1}: {'✅ Completada' if success else '❌ Error'}")
                    
                    # Pausa breve entre pruebas
                    time.sleep(0.5)
            
            # Mostrar resultados de modo real
            if results_real:
                df_results_real = pd.DataFrame(results_real)
                
                st.subheader("Resultados de pruebas con modelo real")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.dataframe(df_results_real)
                    
                    # Visualizar resultados si hay datos válidos
                    valid_results = df_results_real[df_results_real['success']]
                    if not valid_results.empty:
                        fig = px.line(valid_results, x='test_id', y='precio_uf', markers=True,
                                    title=f"Predicciones Reales para {test_comuna} - {test_tipo}")
                        st.plotly_chart(fig)
                
                with col2:
                    # Calcular estadísticas
                    if not df_results_real[df_results_real['success']].empty:
                        prices = df_results_real[df_results_real['success']]['precio_uf']
                        
                        mean_price = prices.mean()
                        std_price = prices.std()
                        min_price = prices.min()
                        max_price = prices.max()
                        
                        st.metric("Precio promedio (UF)", f"{mean_price:.2f}")
                        st.metric("Desviación estándar", f"{std_price:.2f}")
                        st.metric("Precio mínimo", f"{min_price:.2f}")
                        st.metric("Precio máximo", f"{max_price:.2f}")
                        st.metric("Rango (max-min)", f"{max_price - min_price:.2f}")
                        
                        # Evaluar variabilidad
                        if std_price < 0.01 * mean_price:
                            st.error("❌ PROBLEMA DETECTADO: Variabilidad muy baja. Las predicciones son prácticamente idénticas.")
                        elif std_price > 0.1 * mean_price:
                            st.success("✅ Variabilidad normal alta: Las predicciones muestran diferencias significativas")
                        else:
                            st.success("✅ Variabilidad normal: Las predicciones muestran diferencias razonables")
                    else:
                        st.warning("No hay datos válidos para calcular estadísticas")

# Prueba de diferentes comunas
st.header("Prueba de Comunas Diferentes")
st.write("""
Esta prueba verifica si el predictor da resultados diferentes para distintas comunas.
Es útil para detectar si las características específicas de cada comuna se están usando correctamente.
""")

# Botón para ejecutar prueba de comunas
if st.button("Ejecutar prueba de comunas"):
    # Lista de comunas para probar
    comunas_test = ["Las Condes", "Providencia", "La Reina", "Santiago Centro", "Independencia", "Ñuñoa"]
    
    # Datos base
    base_data = {
        'tipo_propiedad': "Departamento",
        'metros_totales': 100,
        'metros_construidos': 90,
        'dormitorios': 3,
        'banos': 2,
        'estacionamientos': 1,
        'antiguedad_anos': 10,
        'orientacion': 'Norte',
        'piso': 3,
        'cercania_metro': False
    }
    
    results = []
    
    # Probar todas las comunas
    with st.spinner("Probando diferentes comunas..."):
        # Cargar modelo
        try:
            modelo = cargar_modelo()
            st.success("✅ Modelo cargado correctamente")
            
            # Probar cada comuna
            for comuna in comunas_test:
                # Crear datos de prueba para esta comuna
                test_data = base_data.copy()
                test_data['comuna'] = comuna
                
                # Ejecutar predicción en modo demo
                try:
                    precio_clp_demo, precio_millones_demo, precio_uf_demo = _predecir_precio_demo(test_data)
                    demo_success = True
                except Exception as e:
                    precio_uf_demo = None
                    demo_success = False
                
                # Ejecutar predicción con modelo real
                try:
                    precio_clp_real, precio_millones_real, precio_uf_real = predecir_precio(modelo, test_data)
                    real_success = True
                except Exception as e:
                    precio_uf_real = None
                    real_success = False
                
                # Guardar resultados
                results.append({
                    'comuna': comuna,
                    'precio_uf_demo': precio_uf_demo if demo_success else 0,
                    'precio_uf_real': precio_uf_real if real_success else 0,
                    'demo_success': demo_success,
                    'real_success': real_success
                })
                
                # Mostrar progreso
                st.write(f"Comuna {comuna}: {'✅' if demo_success and real_success else '❌'}")
                
                # Pausa breve
                time.sleep(0.3)
        
        except Exception as e:
            st.error(f"❌ Error al cargar modelo: {str(e)}")
            st.code(traceback.format_exc())
            
            # Intentar solo en modo demo
            st.warning("Intentando solo en modo demo...")
            
            for comuna in comunas_test:
                # Crear datos de prueba para esta comuna
                test_data = base_data.copy()
                test_data['comuna'] = comuna
                
                # Ejecutar predicción en modo demo
                try:
                    precio_clp_demo, precio_millones_demo, precio_uf_demo = _predecir_precio_demo(test_data)
                    demo_success = True
                except Exception as e:
                    precio_uf_demo = None
                    demo_success = False
                
                # Guardar resultados
                results.append({
                    'comuna': comuna,
                    'precio_uf_demo': precio_uf_demo if demo_success else 0,
                    'precio_uf_real': 0,
                    'demo_success': demo_success,
                    'real_success': False
                })
                
                # Mostrar progreso
                st.write(f"Comuna {comuna} (solo demo): {'✅' if demo_success else '❌'}")
                
                # Pausa breve
                time.sleep(0.3)
    
    # Mostrar resultados
    if results:
        df_results = pd.DataFrame(results)
        
        st.subheader("Resultados por comuna")
        st.dataframe(df_results)
        
        # Gráfico comparativo
        valid_results = df_results[(df_results['demo_success']) | (df_results['real_success'])]
        
        if not valid_results.empty:
            # Preparar datos para gráfico
            plot_data = []
            
            for _, row in valid_results.iterrows():
                if row['demo_success']:
                    plot_data.append({
                        'comuna': row['comuna'],
                        'precio_uf': row['precio_uf_demo'],
                        'modo': 'Demo'
                    })
                
                if row['real_success']:
                    plot_data.append({
                        'comuna': row['comuna'],
                        'precio_uf': row['precio_uf_real'],
                        'modo': 'Real'
                    })
            
            plot_df = pd.DataFrame(plot_data)
            
            # Gráfico de barras agrupadas
            fig = px.bar(
                plot_df, 
                x='comuna', 
                y='precio_uf', 
                color='modo',
                barmode='group',
                title="Comparación de predicciones por comuna",
                labels={'precio_uf': 'Precio (UF)', 'comuna': 'Comuna', 'modo': 'Modo de predicción'}
            )
            
            st.plotly_chart(fig)
            
            # Análisis de los resultados
            if 'precio_uf_demo' in valid_results.columns and 'precio_uf_real' in valid_results.columns:
                valid_both = valid_results[valid_results['demo_success'] & valid_results['real_success']]
                
                if not valid_both.empty:
                    # Verificar si hay diferencias significativas entre comunas
                    precio_min = valid_both['precio_uf_demo'].min()
                    precio_max = valid_both['precio_uf_demo'].max()
                    rango = precio_max - precio_min
                    
                    if rango < precio_min * 0.1:  # Menos del 10% de variación
                        st.error("❌ PROBLEMA DETECTADO: Muy poca variación entre comunas. Es posible que las características específicas de cada comuna no estén afectando el precio.")
                    else:
                        st.success(f"✅ Variación normal entre comunas: {rango:.2f} UF ({(rango/precio_min)*100:.1f}% del mínimo)")
                    
                    # Comparar real vs demo
                    valid_both['diff_pct'] = (valid_both['precio_uf_real'] - valid_both['precio_uf_demo']) / valid_both['precio_uf_demo'] * 100
                    
                    st.subheader("Comparación Real vs Demo")
                    st.dataframe(valid_both[['comuna', 'precio_uf_demo', 'precio_uf_real', 'diff_pct']].rename(
                        columns={'diff_pct': 'Diferencia (%)', 'precio_uf_demo': 'Demo (UF)', 'precio_uf_real': 'Real (UF)'}
                    ))

# Prueba de exploración de la sesión
st.header("Exploración de Variables de Sesión")
st.write("""
Esta herramienta muestra las variables de sesión que pueden estar influyendo en el comportamiento del predictor.
Útil para identificar problemas de caché o estado persistente.
""")

if st.button("Examinar variables de sesión"):
    # Mostrar todas las variables de sesión relevantes
    session_vars = {k: v for k, v in st.session_state.items() if 'precio' in k or 'predict' in k or 'model' in k or 'demo' in k or 'request' in k}
    
    if session_vars:
        st.json(session_vars)
    else:
        st.info("No se encontraron variables de sesión relevantes")

# Prueba de borrado de caché
st.header("Limpieza de Caché")
st.write("Esta herramienta permite limpiar diferentes niveles de caché para solucionar problemas persistentes.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Limpiar session_state"):
        # Eliminar variables de sesión específicas
        keys_to_delete = [k for k in st.session_state.keys() if 'precio' in k or 'predict' in k or 'model' in k or 'demo' in k or 'request' in k]
        
        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
        
        st.success(f"✅ {len(keys_to_delete)} variables de sesión eliminadas")

with col2:
    if st.button("Limpiar caché de Streamlit"):
        try:
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("✅ Caché de Streamlit limpiado")
        except Exception as e:
            st.error(f"❌ Error al limpiar caché: {str(e)}")

with col3:
    if st.button("Reiniciar aplicación"):
        st.warning("⚠️ Reiniciando aplicación...")
        # Limpiar todo el session_state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        # Forzar recarga
        st.experimental_rerun()

# Recomendaciones específicas
st.header("Recomendaciones para solucionar problemas")

st.markdown("""
### Solución para predicciones idénticas:

1. **Generación de IDs únicos**:
   - Añadir un ID único a cada solicitud de predicción basado en el tiempo, un UUID y un número aleatorio
   - Nunca reutilizar IDs de solicitud entre predicciones

2. **Manejo del estado aleatorio**:
   - Guardar y restaurar apropiadamente el estado aleatorio de NumPy y Python
   - Usar diferentes semillas para cada predicción

3. **Almacenamiento específico por ID**:
   - Guardar cada resultado con su ID único específico
   - No sobrescribir variables de estado global

4. **Evitar caché entre predicciones**:
   - Introducir pequeñas variaciones en los datos de entrada o resultados
   - Añadir parámetros únicos que no afecten significativamente el resultado

5. **Validación de resultados**:
   - Verificar que cada predicción produce un resultado diferente
   - Implementar pruebas de consistencia para detectar problemas
""")

# Footer
st.markdown("---")
st.markdown("🔍 Herramienta de Diagnóstico para Predictor Inmobiliario v1.0")
st.caption("Creada específicamente para solucionar el problema de predicciones idénticas en Streamlit Cloud")
