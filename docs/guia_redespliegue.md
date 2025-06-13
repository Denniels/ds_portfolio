# Guía de Redespliegue de la Aplicación de Portafolio DS

Este documento proporciona instrucciones paso a paso para realizar un redespliegue completo de la aplicación de Portafolio DS en Google Cloud Run, después de haber realizado actualizaciones en el código, como las mejoras en las aplicaciones de análisis demográfico y presupuesto público.

## Requisitos Previos

Antes de iniciar el proceso de redespliegue, asegúrate de tener:

1. **Google Cloud SDK** instalado en tu equipo
2. **Docker** instalado y configurado
3. **Acceso** a la cuenta de Google Cloud donde está desplegada la aplicación
4. Todos los **cambios de código** comprometidos en tu repositorio

## Pasos para el Redespliegue

### 1. Preparar el Entorno

Asegúrate de estar en el directorio raíz del proyecto:

```bash
cd e:\repos\ds_portfolio
```

### 2. Ejecutar el Script de Despliegue

Hemos creado scripts de despliegue automatizados para simplificar el proceso. Dependiendo de tu sistema operativo, puedes utilizar:

#### Para PowerShell (Windows):

```powershell
# Asegúrate de que PowerShell permite la ejecución de scripts
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Ejecuta el script de despliegue
.\scripts\deploy_to_cloud_run.ps1
```

#### Para Bash (Linux/Mac/WSL):

```bash
# Dar permisos de ejecución al script
chmod +x ./scripts/deploy_to_cloud_run.sh

# Ejecutar el script
./scripts/deploy_to_cloud_run.sh
```

### 3. Seguimiento del Proceso

El script realizará automáticamente las siguientes tareas:

1. Verificar tu autenticación en Google Cloud
2. Configurar el proyecto de GCP
3. Verificar que las APIs necesarias estén habilitadas
4. Construir la imagen Docker actualizada
5. Subir la imagen a Google Container Registry
6. Desplegar la nueva versión en Cloud Run
7. Proporcionar la URL de acceso a la aplicación

Durante la ejecución, verás mensajes informativos sobre el progreso de cada paso.

### 4. Verificación Post-Despliegue

Una vez completado el despliegue, realiza las siguientes verificaciones:

1. **Accede a la URL** proporcionada al final del despliegue para verificar que la aplicación funciona correctamente
2. **Revisa todas las secciones** de la aplicación, especialmente las que fueron actualizadas:
   - Análisis Demográfico
   - Análisis de Presupuesto Público
3. **Verifica los logs** para detectar posibles errores:
   ```
   gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ds-portfolio-app" --limit=50
   ```

## Solución de Problemas Comunes

### Problemas de Autenticación

Si encuentras problemas de autenticación:

```bash
# Vuelve a autenticarte en gcloud
gcloud auth login

# Configura la autenticación de Docker con GCR
gcloud auth configure-docker
```

### Errores en el Despliegue

Si el despliegue falla, verifica:

1. **Logs de construcción de Docker**:
   ```
   docker build -t temp-debug .
   ```

2. **Problemas de memoria o recursos**:
   - Verifica que los recursos asignados (4Gi de RAM) sean suficientes
   - Considera aumentar la memoria si la aplicación lo requiere

3. **Dependencias faltantes**:
   - Asegúrate de que todas las dependencias estén en `requirements.txt`
   - Verifica que el Dockerfile copie todos los archivos necesarios

## Consideraciones Adicionales

- **Capa gratuita**: El despliegue está configurado para aprovechar la capa gratuita de Google Cloud Run con:
  - Mínimo de 0 instancias (escala a cero cuando no hay tráfico)
  - Máximo de 1 instancia (para controlar costos)
  - 4GB de RAM (suficiente para la mayoría de las cargas de trabajo)

- **Primera carga**: Debido a la configuración de "escala a cero", la primera carga después de un período de inactividad puede tardar unos segundos mientras se inicia una nueva instancia.

- **Monitoreo**: Después del despliegue, monitorea el uso de recursos para asegurarte de que la aplicación funcione dentro de los límites configurados.

## Referencias

- [Documentación oficial de Google Cloud Run](https://cloud.google.com/run/docs)
- [Guía completa de despliegue en el repositorio](./despliegue_google_cloud_run.md)
- [Optimización de aplicaciones Streamlit](https://docs.streamlit.io/library/advanced-features/caching)
