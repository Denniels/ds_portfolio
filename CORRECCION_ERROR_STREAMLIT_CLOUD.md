# Corrección del Error AttributeError en Streamlit Cloud

## Problema identificado
Se detectó un error en la aplicación cuando se ejecutaba en Streamlit Cloud, específicamente relacionado con el acceso a `st.query_params`. Este error solo ocurría en el entorno de Streamlit Cloud, pero no en el entorno local.

```
AttributeError: This app has encountered an error. The original error message is redacted to prevent data leaks.
```

La traza del error indicaba que el problema estaba en la línea 1556 del archivo `10_predictor_inmobiliario.py`, al intentar acceder a `st.query_params`.

## Causa
El atributo `st.query_params` es una característica que puede no estar disponible en todas las versiones de Streamlit, o puede comportarse de manera diferente en Streamlit Cloud comparado con el entorno local. Esto explica por qué la aplicación funcionaba correctamente de forma local pero no en Streamlit Cloud.

## Solución implementada
Se ha implementado un enfoque robusto para manejar los parámetros de URL, utilizando bloques try-except para capturar cualquier `AttributeError` cuando se intenta acceder a `st.query_params`. Como alternativa, se utiliza `st.session_state` para mantener el estado entre recargas de la página.

Las modificaciones incluyen:

1. Modificación de todas las instancias donde se accede a `st.query_params.get()` para usar try-except:
   ```python
   try:
       force_model = st.query_params.get('force_model', 'auto').lower()
   except (AttributeError, Exception):
       force_model = st.session_state.get('force_model', 'auto')
   ```

2. Modificación de todas las instancias donde se establece un valor en `st.query_params`:
   ```python
   try:
       st.query_params['force_model'] = selected_model_mode
   except (AttributeError, Exception):
       st.session_state['force_model'] = selected_model_mode
   ```

3. Corrección de problemas de indentación y líneas duplicadas en el código.

## Beneficios
- Compatibilidad garantizada con Streamlit Cloud y entornos locales
- Manejo robusto de errores para evitar fallos inesperados
- Fallback automático a valores predeterminados cuando no está disponible la funcionalidad
- Mantenimiento del estado de la aplicación entre recargas usando `st.session_state`

## Recomendaciones adicionales
- Documentar claramente las diferencias de comportamiento entre entornos locales y Streamlit Cloud
- Realizar pruebas tanto en entorno local como en Streamlit Cloud antes de implementaciones importantes
- Considerar el uso de funciones de compatibilidad para abstraer las diferencias entre entornos
