# Archivado de Herramientas de Diagnóstico

## Resumen

Se han movido las herramientas de diagnóstico (`98_diagnostico_inmobiliario.py` y `99_diagnostico_cloud.py`) desde la carpeta `app/pages/` a la carpeta `app/tests/` para mejorar la organización y evitar que aparezcan en la navegación principal de la aplicación.

## Cambios realizados

1. **Creación de directorio de tests**:
   - Se ha creado el directorio `app/tests/` para albergar herramientas de diagnóstico y pruebas

2. **Movimiento de archivos**:
   - `app/pages/98_diagnostico_inmobiliario.py` → `app/tests/diagnostico_inmobiliario.py`
   - `app/pages/99_diagnostico_cloud.py` → `app/tests/diagnostico_cloud.py`

3. **Adaptación de rutas**:
   - Se han actualizado las rutas relativas en los archivos movidos para que funcionen desde su nueva ubicación

4. **Documentación**:
   - Se ha creado `app/tests/README.md` con información detallada sobre el propósito y uso de estas herramientas

## Beneficios

- **Interfaz más limpia**: Los usuarios no verán herramientas de diagnóstico en la navegación principal
- **Mejor organización**: Separación clara entre funcionalidad de la aplicación y herramientas de desarrollo/diagnóstico
- **Mantenimiento futuro**: La estructura facilita la adición de nuevas herramientas de prueba sin afectar la navegación

## Cómo acceder a las herramientas de diagnóstico

Las herramientas de diagnóstico ya no aparecen en la navegación de Streamlit, pero siguen siendo accesibles a través de URLs directas:

1. Para diagnóstico del predictor inmobiliario:
   ```
   http://localhost:8501/tests/diagnostico_inmobiliario
   ```

2. Para diagnóstico de Streamlit Cloud:
   ```
   http://localhost:8501/tests/diagnostico_cloud
   ```

También se pueden ejecutar directamente con los comandos:

```
streamlit run app/tests/diagnostico_inmobiliario.py
streamlit run app/tests/diagnostico_cloud.py
```

## Conclusión

Este cambio mejora la experiencia del usuario final al ocultar las herramientas de diagnóstico de la navegación principal, a la vez que mantiene estas herramientas disponibles para los desarrolladores cuando sea necesario.
