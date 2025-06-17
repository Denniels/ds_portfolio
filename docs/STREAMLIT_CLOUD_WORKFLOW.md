# Despliegue en Streamlit Cloud - Portafolio Data Science

Este documento explica cómo el portafolio de Data Science está configurado para despliegue automático en Streamlit Cloud.

## 📋 Requisitos Previos

1. Repositorio conectado a [Streamlit Cloud](https://share.streamlit.io)
2. Estructura de proyecto correcta
3. Archivo de GitHub Actions configurado (`.github/workflows/streamlit-cloud-mode.yml`)

## 🚀 Proceso de Despliegue

El despliegue en Streamlit Cloud se realiza de forma automática cuando se detectan cambios en la rama principal (`main`). El proceso sigue estos pasos:

1. **Preparación**: El workflow de GitHub Actions (`streamlit-cloud-mode.yml`) prepara el proyecto:
   - Configura el entorno Python
   - Instala dependencias
   - Establece variables de entorno para Streamlit Cloud
   - Optimiza archivos estáticos y estructura del proyecto

2. **Verificación**: Se valida que la estructura del proyecto sea correcta:
   - Existencia de `app/main.py`
   - Directorio de páginas
   - Archivos de configuración

3. **Despliegue**: Streamlit Cloud detecta los cambios y realiza el despliegue automáticamente.

## 🔧 Configuración del Proyecto

### Estructura de Archivos

```
ds_portfolio/
├── app/                       # Directorio principal de la aplicación
│   ├── main.py                # Punto de entrada
│   ├── pages/                 # Páginas de la aplicación
│   │   ├── 01_emisiones_co2.py
│   │   ├── 02_calidad_agua.py
│   │   └── ...
│   ├── utils/                 # Utilidades
│   │   ├── cache_manager.py
│   │   ├── contact_components.py
│   │   └── ...
│   ├── data/                  # Datos y recursos
│   │   ├── cache/
│   │   └── feedback/
│   └── static/                # Recursos estáticos
├── .streamlit/               # Configuración de Streamlit
│   ├── config.toml
│   └── secrets.toml
├── .github/workflows/        # Workflows de GitHub Actions
│   └── streamlit-cloud-mode.yml
├── requirements.txt          # Dependencias del proyecto
└── prepare_for_streamlit_cloud.py # Script de preparación
```

### Variables de Entorno

En Streamlit Cloud, se establecen las siguientes variables:

- `IS_STREAMLIT_CLOUD=true` - Indica que el entorno es Streamlit Cloud
- `STREAMLIT_SERVER_ENABLE_CORS=false` - Mejora la seguridad
- `STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true` - Protección contra XSRF

## 🛠️ Optimizaciones para Streamlit Cloud

### 1. Compresión de Datos

Se comprimen archivos grandes para reducir el tiempo de carga:
- CSV → Parquet comprimido
- JSON → GZIP
- Imágenes → WebP optimizado

### 2. Manejo de Caché

```python
# Ejemplo en app/main.py
if IS_STREAMLIT_CLOUD:
    cache_dir = Path('/tmp/streamlit_cache')
```

### 3. CSS Minificado

Se usa una versión minificada de los archivos CSS para mejorar el rendimiento:
```python
css_path = 'static/css/style.min.css' if IS_STREAMLIT_CLOUD else 'static/css/style.css'
```

## 📊 Monitoreo y Mantenimiento

### Verificar Estado del Despliegue

Puedes verificar el estado del despliegue en:
1. [GitHub Actions](https://github.com/your-username/ds_portfolio/actions)
2. [Streamlit Cloud Dashboard](https://share.streamlit.io)

### Actualización de Dependencias

Para actualizar las dependencias, modifica `requirements.txt` y haz push a la rama principal.

---

## 🤝 Soporte

Si encuentras problemas con el despliegue, revisa:
- Logs de GitHub Actions
- Logs de la aplicación en Streamlit Cloud
- Confirma que todos los archivos requeridos estén presentes

## 🔄 Proceso de Actualización

1. Desarrolla localmente
2. Prueba exhaustivamente
3. Haz commit y push a la rama principal
4. El workflow prepara todo para Streamlit Cloud
5. Streamlit Cloud realiza el despliegue automáticamente
