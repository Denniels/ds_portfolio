# Guía de Despliegue en Streamlit Community Cloud

Esta guía proporciona los pasos necesarios para desplegar correctamente la aplicación de portafolio en Streamlit Community Cloud.

## Prerrequisitos

- Cuenta en [Streamlit Community Cloud](https://streamlit.io/cloud)
- Repositorio de GitHub con la aplicación
- Acceso de Streamlit Community Cloud a tu repositorio de GitHub

## Preparación del repositorio

1. **Verificar estructura del proyecto**:
   ```
   app/
   ├── main.py               # Punto de entrada principal
   ├── components/           # Componentes reutilizables
   ├── config/               # Configuración
   ├── data/                 # Datos y caché
   ├── pages/                # Páginas de la aplicación
   ├── static/               # Archivos estáticos
   ├── tests/                # Herramientas de diagnóstico (no en navegación)
   └── utils/                # Utilidades
   ```

2. **Asegurar que el archivo de requisitos sea correcto**:
   - Utilizar `requirements_streamlit_cloud.txt` para el despliegue en Streamlit Cloud
   - Verificar que todas las dependencias necesarias estén listadas con sus versiones

3. **Comprobar configuración de entorno**:
   - Verificar que la aplicación detecte correctamente cuando está en entorno cloud
   - Asegurar que las rutas a archivos funcionen correctamente en la nube

## Proceso de despliegue

1. **Iniciar sesión en Streamlit Community Cloud**:
   - Ir a [https://streamlit.io/cloud](https://streamlit.io/cloud)
   - Iniciar sesión con tu cuenta (GitHub, Google, etc.)

2. **Nuevo despliegue**:
   - Hacer clic en "New app"
   - Seleccionar el repositorio que contiene la aplicación
   - Seleccionar la rama (normalmente `main` o `master`)

3. **Configuración del despliegue**:
   - **Ruta principal**: `app/main.py`
   - **Requisitos**: `requirements_streamlit_cloud.txt`
   - **Python versión**: 3.9 (recomendado para compatibilidad)
   - **Ajustes adicionales**: No son necesarios para esta aplicación

4. **Desplegar**:
   - Hacer clic en "Deploy!"
   - Esperar a que el despliegue se complete (puede tomar unos minutos)

## Verificación post-despliegue

1. **Prueba inicial**:
   - Navegar a la URL proporcionada por Streamlit Cloud
   - Verificar que la página principal cargue correctamente

2. **Pruebas de funcionalidad**:
   - Navegar a la página del predictor inmobiliario
   - Realizar varias predicciones y verificar que los resultados sean diferentes
   - Probar otras páginas para asegurar que funcionan según lo esperado

3. **Diagnóstico en caso de problemas**:
   - Si encuentras problemas, puedes ejecutar las herramientas de diagnóstico:
     - Navegar manualmente a: `[URL_de_tu_app]/tests/diagnostico_cloud`
     - Seguir las instrucciones en la herramienta para identificar problemas

## Solución de problemas comunes

### Problema: La aplicación no se inicia
**Solución**: Verificar los logs de Streamlit para identificar errores de instalación o inicialización.

### Problema: Error al cargar modelos
**Solución**: 
- Verificar que los archivos del modelo estén correctamente incluidos en el repositorio
- Asegurar que las rutas a los modelos sean correctas para el entorno cloud

### Problema: Predicciones idénticas
**Solución**: 
- Ya está solucionado con la implementación de IDs únicos
- Si persiste, usar la herramienta de diagnóstico para verificar el estado de la sesión y el caché

### Problema: Error en módulos o importaciones
**Solución**:
- Verificar que todos los requisitos estén correctamente especificados en `requirements_streamlit_cloud.txt`
- Comprobar que las importaciones relativas sean correctas

## Mantenimiento

### Actualizaciones
Para actualizar la aplicación desplegada:
1. Hacer cambios en el repositorio
2. Hacer commit y push a la rama conectada
3. Streamlit Cloud actualizará automáticamente la aplicación

### Reinicio manual
Si necesitas reiniciar la aplicación:
1. Ir al dashboard de Streamlit Cloud
2. Encontrar tu aplicación
3. Hacer clic en los tres puntos (⋮) y seleccionar "Reboot app"

## Recursos adicionales

- [Documentación oficial de Streamlit](https://docs.streamlit.io/)
- [Guía de despliegue de Streamlit](https://docs.streamlit.io/streamlit-cloud/get-started)
- Para problemas específicos: Utilizar las herramientas de diagnóstico en `app/tests/`

---

Actualizado: 22 de junio de 2024
