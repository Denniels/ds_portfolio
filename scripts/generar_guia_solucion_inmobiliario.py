"""
Script para generar instrucciones de despliegue a Streamlit Cloud
y resolver problemas con predicciones inmobiliarias que siempre dan el mismo resultado
"""
import os
import sys
import json
from pathlib import Path
import datetime

def generar_guia_despliegue():
    """Genera una guía paso a paso para desplegar a Streamlit Cloud con éxito"""
    
    print("\n=== GUÍA DE DESPLIEGUE PARA STREAMLIT CLOUD ===\n")
    print("Paso 1: Preparación del repositorio")
    print("----------------------------------------")
    print("1. Asegúrate de que todos los archivos del modelo estén incluidos en el repositorio y no en .gitignore:")
    print("   - app/data/inmobiliario/modelo_inmobiliario.pkl")
    print("   - app/data/inmobiliario/scaler_inmobiliario.pkl")
    print("   - app/data/inmobiliario/model_info.json")
    print("   - app/models/modelo_inmobiliario.pkl (copia adicional)")
    print("   - app/models/scaler_inmobiliario.pkl (copia adicional)")
    print("   - app/models/model_info.json (copia adicional)")
    
    print("\nPaso 2: Verificar requirements.txt")
    print("----------------------------------------")
    print("Asegúrate de que requirements.txt y requirements_streamlit_cloud.txt contengan versiones compatibles:")
    print("scikit-learn==1.7.0")
    print("numpy==1.26.4")
    print("pandas==2.0.3")
    print("joblib==1.2.0")
    
    print("\nPaso 3: Añadir archivos de depuración")
    print("----------------------------------------")
    print("1. Añade el archivo diagnostico_modelo_inmobiliario.py a la carpeta app/")
    print("2. Este archivo permite verificar que los archivos del modelo se cargan correctamente en Streamlit Cloud")
    
    print("\nPaso 4: Implementar modo de depuración")
    print("----------------------------------------")
    print("1. Añade el parámetro ?debug=true a la URL de la página del predictor inmobiliario en Streamlit Cloud")
    print("2. Esto mostrará información adicional sobre la carga del modelo y las predicciones")
    
    print("\nPaso 5: Validar configuración en Streamlit Cloud")
    print("----------------------------------------")
    print("1. Verifica que Streamlit Cloud esté configurado para usar Python 3.10 o superior")
    print("2. Confirma que no haya errores en los logs de Streamlit Cloud")
    
    print("\nPaso 6: Problemas conocidos y soluciones")
    print("----------------------------------------")
    print("1. Problema: Las predicciones siempre dan el mismo resultado")
    print("   Solución: Verifica que el código de preparación de features esté creando correctamente")
    print("             las variables dummy para comuna, tipo de propiedad y orientación.")
    print("2. Problema: Error al cargar el modelo")
    print("   Solución: Regenera el modelo usando exactamente las mismas versiones de bibliotecas")
    print("             que usa Streamlit Cloud.")
    print("3. Problema: Incompatibilidades de versiones")
    print("   Solución: Añade un manejo de errores robusto en la carga del modelo para")
    print("             caer elegantemente al modo demo con un mensaje informativo.")

def verificar_codigo_predictor():
    """Verifica si el código del predictor inmobiliario contiene problemas comunes"""
    
    predictor_path = "app/pages/10_predictor_inmobiliario.py"
    
    if not os.path.exists(predictor_path):
        print(f"Error: No se encontró el archivo {predictor_path}")
        return
    
    print("\n=== VERIFICACIÓN DEL CÓDIGO DEL PREDICTOR ===\n")
    
    with open(predictor_path, 'r', encoding='utf-8') as f:
        codigo = f.read()
    
    # Lista de problemas potenciales a verificar
    problemas = [
        {
            "nombre": "Características incompletas en predicción",
            "patron": "X = np.array([",
            "recomendacion": "Verifica que todas las características requeridas por el modelo se incluyan en la predicción"
        },
        {
            "nombre": "Rutas de modelo hardcodeadas",
            "patron": "DATA_DIR",
            "recomendacion": "Usa rutas relativas y búsqueda en múltiples ubicaciones para mayor resilencia"
        },
        {
            "nombre": "Manejo de errores insuficiente",
            "patron": "except Exception as e:",
            "recomendacion": "Implementa manejo de errores específicos para problemas comunes en Streamlit Cloud"
        },
        {
            "nombre": "Falta de logging",
            "patron": "st.session_state",
            "recomendacion": "Añade logging detallado para diagnosticar problemas en producción"
        },
        {
            "nombre": "Modo de depuración",
            "patron": "debug_mode",
            "recomendacion": "Implementa un modo de depuración activable mediante parámetros de URL"
        }
    ]
    
    # Verificar cada problema potencial
    for problema in problemas:
        if problema["patron"] in codigo:
            print(f"✅ {problema['nombre']}: Implementado")
        else:
            print(f"❌ {problema['nombre']}: No implementado")
            print(f"   Recomendación: {problema['recomendacion']}")
    
    # Verificar si se están usando todas las características del modelo
    model_info_path = "app/data/inmobiliario/model_info.json"
    if os.path.exists(model_info_path):
        with open(model_info_path, 'r', encoding='utf-8') as f:
            model_info = json.load(f)
        
        feature_names = model_info.get('feature_names', [])
        
        # Verificar si el código incluye cada característica
        print("\nVerificación de características del modelo:")
        for feature in feature_names:
            if feature in codigo:
                print(f"✅ {feature}: Encontrada en el código")
            else:
                print(f"❌ {feature}: No encontrada en el código")
    
    # Verificar si hay código para manejar variables dummy
    if "comuna_" in codigo and "tipo_propiedad_" in codigo:
        print("\n✅ Manejo de variables dummy: Implementado")
    else:
        print("\n❌ Manejo de variables dummy: No implementado")
        print("   Recomendación: Implementa código para crear variables dummy para comuna, tipo_propiedad, etc.")

def generar_recomendaciones_finales():
    """Genera recomendaciones finales para resolver el problema de predicciones iguales"""
    
    print("\n=== SOLUCIÓN PARA PREDICCIONES IGUALES EN STREAMLIT CLOUD ===\n")
    print("Basado en el análisis, el problema de que todas las predicciones arrojen el mismo resultado")
    print("puede deberse a los siguientes factores:\n")
    
    print("1. Procesamiento incorrecto de características para el modelo:")
    print("   - El modelo requiere variables dummy para comuna, tipo de propiedad y orientación")
    print("   - Es posible que las variables no se estén creando correctamente en Streamlit Cloud")
    print("   - El modelo puede estar recibiendo siempre el mismo input efectivo")
    
    print("\n2. Fallback a modo demo silencioso:")
    print("   - Un error al cargar o usar el modelo puede estar provocando el uso del modo demo")
    print("   - El modo demo puede estar usando un valor semilla fijo sin el componente aleatorio")
    
    print("\n3. Cache de Streamlit:")
    print("   - Los resultados podrían estar siendo cacheados incorrectamente")
    print("   - Algunas entradas no se consideran correctamente para invalidar el cache")
    
    print("\nRECOMENDACIONES:\n")
    print("1. Añade un registro detallado de las características que se envían al modelo:")
    print("   ```")
    print("   st.session_state['debug_features'] = features_dict")
    print("   st.session_state['debug_input'] = input_data")
    print("   ```")
    
    print("\n2. Verifica que las variables dummy se estén creando correctamente:")
    print("   ```")
    print("   # Antes de la predicción, imprime las features")
    print("   feature_values = [features_dict[feature] for feature in model_info['feature_names']]")
    print("   st.write(\"Features:\", dict(zip(model_info['feature_names'], feature_values)))")
    print("   ```")
    
    print("\n3. Deshabilita el cache temporalmente para descartar problemas relacionados:")
    print("   ```")
    print("   @st.cache_data(ttl=0)")
    print("   def predecir_precio_sin_cache(modelo, input_data):")
    print("       # Tu código de predicción existente")
    print("   ```")
    
    print("\n4. Añade una bandera para forzar el uso del modo demo o modo real:")
    print("   ```")
    print("   # En la URL: ?mode=demo o ?mode=real")
    print("   params = st.experimental_get_query_params()")
    print("   mode = params.get('mode', ['auto'])[0]")
    print("   ```")
    
    print("\n5. Implementa un modo de depuración completo:")
    print("   Modifica la aplicación para mostrar información detallada cuando se accede con ?debug=true")
    
    print("\nIMPLEMENTACIÓN INMEDIATA:\n")
    print("1. Ejecuta la aplicación localmente con ?debug=true y verifica que las características")
    print("   se estén creando correctamente")
    print("2. Despliega la versión con debugging a Streamlit Cloud")
    print("3. Accede a la aplicación en Streamlit Cloud con ?debug=true y analiza:")
    print("   - Si el modelo se está cargando correctamente")
    print("   - Si las características se están creando correctamente")
    print("   - Si hay errores que provocan el uso del modo demo")
    print("4. Una vez identificado el problema específico, implementa la solución correspondiente")


def main():
    print("=" * 80)
    print("GUÍA DE SOLUCIÓN PARA PREDICTOR INMOBILIARIO EN STREAMLIT CLOUD")
    print("=" * 80)
    
    generar_guia_despliegue()
    verificar_codigo_predictor()
    generar_recomendaciones_finales()
    
    print("\n" + "=" * 80)
    print("Fin de la guía de solución")
    print("=" * 80)

if __name__ == "__main__":
    main()
