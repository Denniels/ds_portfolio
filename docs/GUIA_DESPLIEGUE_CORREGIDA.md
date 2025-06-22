# Guía de Despliegue en Streamlit Community Cloud (Corregida Junio 2025)

Esta guía proporciona los pasos necesarios para desplegar correctamente la aplicación de portafolio en Streamlit Community Cloud, con especial atención a los problemas de dependencias.

## Prerrequisitos

- Cuenta en [Streamlit Community Cloud](https://streamlit.io/cloud)
- Repositorio de GitHub con la aplicación
- Acceso de Streamlit Community Cloud a tu repositorio de GitHub
- Archivos de configuración correctamente configurados

## Archivos críticos para el despliegue

### 1. `runtime.txt`

Especifica la versión de Python:

```
python-3.9.13
```

### 2. `packages.txt`

Lista optimizada de dependencias del sistema:

```
build-essential
python3-dev
python3-pip
python3-setuptools
python3-wheel
libpango1.0-dev
python3-tk
libfreetype6-dev
pkg-config
libxft-dev
libopenblas-dev
liblapack-dev
gfortran
libblas-dev
libatlas-base-dev
libaec-dev
libsuitesparse-dev
cmake
python3-venv
python3-numpy
python3-scipy
```

### 3. `requirements_streamlit_cloud.txt`

Dependencias de Python con versiones compatibles:

```
# Core dependencies for Streamlit Cloud
streamlit>=1.28.0,<1.32.0
numpy>=1.22.0,<1.26.0
pandas>=2.0.0,<2.1.0
# Versiones específicas para evitar problemas con OpenBLAS
scipy>=1.10.0,<1.11.0
scikit-learn>=1.3.0,<1.4.0
...
```

### 4. `preinstall.py`

Script optimizado que se ejecuta antes de la instalación principal para configurar el entorno.

Características clave:
- Sistema de reintentos para instalaciones críticas
- Verificación de instalación de dependencias críticas
- Instalaciones alternativas cuando fallan las principales
- Mejor manejo de errores y logging

### 5. `.streamlit/config.toml`

Configuración optimizada de Streamlit para la nube:

```toml
[server]
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 200
maxMessageSize = 200
headless = true

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#333333"

[runner]
fastReruns = true

[client]
showErrorDetails = true
toolbarMode = "minimal"

[logger]
level = "info"

[global]
developmentMode = false
disableWatchdogWarning = true
suppressDeprecationWarnings = true
```

## Solución de problemas comunes

### Error en la instalación de dependencias del sistema

Si ves errores como `installer returned a non-zero exit code`:

- Verifica que no hay dependencias duplicadas en `packages.txt`
- Asegúrate de que `packages.txt` tiene las dependencias correctas para OpenBLAS y otras bibliotecas científicas
- Considera añadir más dependencias específicas del sistema para SciPy y NumPy

### Error en la instalación de SciPy/NumPy

Para solucionar problemas con SciPy o NumPy:

- Asegúrate de que las dependencias del sistema estén correctamente configuradas en `packages.txt`
- Verifica que `preinstall.py` instala correctamente NumPy antes de SciPy
- Utiliza versiones específicas y compatibles de estos paquetes
- Asegúrate de que OpenBLAS está correctamente instalado

### Optimización de memoria y rendimiento

Para mejorar el rendimiento en Streamlit Cloud:

1. **Utiliza caché eficientemente:**
   - Implementa `st.cache_data` y `st.cache_resource` para operaciones costosas
   - Utiliza TTL (Time To Live) apropiados para datos que cambian

2. **Manejo eficiente de datos:**
   - Carga datos solo cuando sea necesario
   - Libera memoria después de operaciones intensivas
   - Utiliza procesamiento por lotes para datos grandes

## Verificación final

Después de desplegar, verifica:

1. Los logs de instalación en Streamlit Cloud
2. Que todas las páginas se carguen correctamente
3. Que las visualizaciones interactivas funcionen
4. Que el predictor inmobiliario funcione como se espera

## Recursos adicionales

- Ver `SOLUCION_DESPLIEGUE_CLOUD.md` para detalles de la solución implementada
- Ver `ESTADO_FINAL_JUNIO_2025.md` para el estado final de la aplicación
- [Documentación oficial de Streamlit](https://docs.streamlit.io/)
- [Foro de Streamlit](https://discuss.streamlit.io/)
