# Guía de Despliegue en Google Cloud Run

Este documento proporciona instrucciones detalladas para desplegar la aplicación de Análisis de Emisiones RETC Chile en Google Cloud Run, aprovechando los recursos de la capa gratuita y optimizando el rendimiento.

## Índice

1. [Características de Google Cloud Run](#características-de-google-cloud-run)
2. [Ventajas para Nuestra Aplicación](#ventajas-para-nuestra-aplicación)
3. [Requisitos Previos](#requisitos-previos)
4. [Crear una Cuenta en Google Cloud](#crear-una-cuenta-en-google-cloud)
5. [Configuración del Proyecto](#configuración-del-proyecto)
6. [Preparación del Código para Cloud Run](#preparación-del-código-para-cloud-run)
7. [Optimización de la Aplicación](#optimización-de-la-aplicación)
8. [Despliegue en Cloud Run](#despliegue-en-cloud-run)
9. [Configuración de Almacenamiento de Datos](#configuración-de-almacenamiento-de-datos)
10. [Monitoreo y Escalado](#monitoreo-y-escalado)
11. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
12. [Optimizaciones Adicionales](#optimizaciones-adicionales)

## Características de Google Cloud Run

Google Cloud Run ofrece un entorno serverless para ejecutar contenedores que se adapta automáticamente según la demanda:

- **Capa gratuita generosa**:
  - 2 millones de solicitudes gratuitas al mes
  - 360,000 GB-segundos de memoria (aproximadamente 50 GB de RAM durante 2 horas al día)
  - 180,000 vCPU-segundos
  - Sin costo por instancias inactivas (solo pagas cuando tu servicio está procesando solicitudes)

- **Características clave**:
  - Escala automáticamente de 0 a N instancias según la demanda
  - Soporte completo para contenedores Docker
  - Integraciones nativas con otros servicios de Google Cloud
  - Sin límite de tiempo de ejecución por solicitud (a diferencia de Cloud Functions)
  - Certificados HTTPS automáticos para dominios personalizados

## Ventajas para Nuestra Aplicación

- **Eficiencia de recursos**: Solo consumimos recursos cuando los usuarios acceden a la aplicación
- **Capacidad de memoria adecuada**: Podemos configurar hasta 32 GB de RAM por instancia
- **Escalabilidad**: Maneja fácilmente picos de tráfico
- **Implementación sencilla**: Usa nuestros Dockerfiles existentes con mínimas modificaciones
- **Costo predecible**: Comienza gratis y escala según las necesidades

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- Una tarjeta de crédito/débito válida (necesaria para la verificación, pero la capa gratuita es suficiente para nuestro caso)
- Una dirección de correo electrónico
- Git instalado en tu equipo local
- Docker instalado en tu equipo local
- Google Cloud SDK (opcional, pero recomendado)

## Crear una Cuenta en Google Cloud

1. Visita [https://cloud.google.com/](https://cloud.google.com/)

2. Haz clic en "Comenzar gratis"

3. Inicia sesión con tu cuenta de Google o crea una nueva

4. Completa el formulario de registro:
   - País
   - Aceptación de términos y condiciones
   - Información de facturación (tarjeta de crédito o débito)

5. Recibirás $300 USD en créditos gratuitos válidos por 90 días

6. Después de los 90 días, seguirás teniendo acceso a la capa gratuita de Google Cloud Run sin cargos adicionales si no excedes sus límites

## Configuración del Proyecto

### Crear un nuevo proyecto en Google Cloud:

1. Ve a la [Consola de Google Cloud](https://console.cloud.google.com/)

2. En la parte superior, haz clic en el selector de proyectos

3. Haz clic en "Nuevo proyecto"

4. Asigna un nombre descriptivo, por ejemplo: `retc-emissions-analysis`

5. Haz clic en "Crear"

6. Espera a que se cree el proyecto y luego selecciónalo en el selector de proyectos

### Habilitar las APIs necesarias:

1. En el menú de navegación, ve a "APIs y servicios" > "Biblioteca"

2. Busca y habilita las siguientes APIs:
   - Cloud Run API
   - Container Registry API
   - Cloud Build API
   - Artifact Registry API
   - Cloud Storage API (si planeas almacenar datos)
   - Firestore API (opcional, para almacenamiento de datos alternativo)

3. Para cada API, haz clic en "Habilitar"

### Instalar y configurar Google Cloud SDK (opcional pero recomendado):

**Para Windows:**

1. Descarga el instalador desde [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)

2. Ejecuta el instalador y sigue las instrucciones

3. Abre PowerShell y ejecuta:
   ```powershell
   gcloud init
   ```

4. Sigue las instrucciones para iniciar sesión y seleccionar tu proyecto:
   ```powershell
   gcloud auth login
   gcloud config set project retc-emissions-analysis
   ```

5. Configura Docker para usar Google Container Registry:
   ```powershell
   gcloud auth configure-docker
   ```

## Preparación del Código para Cloud Run

### 1. Adaptar el Dockerfile:

Cloud Run requiere que tu aplicación escuche en el puerto definido por la variable de entorno `PORT`. Modifica el archivo `docker/streamlit/Dockerfile` para incluir esta configuración:

1. Abre el archivo Dockerfile:

```bash
# Archivo: docker/streamlit/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copiar requirements.txt primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto definido por la variable de entorno PORT (Cloud Run)
# O usar 8501 por defecto (desarrollo local)
ENV PORT=8501

# Ejecutar Streamlit
CMD streamlit run app/Home.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. Crear un archivo `app.yaml` para configuraciones adicionales:

```yaml
# Archivo: app.yaml
runtime: custom
env: flex

manual_scaling:
  instances: 1

resources:
  cpu: 1
  memory_gb: 4
  disk_size_gb: 10

env_variables:
  PORT: 8501
```

### 3. Crear un archivo `.dockerignore` para optimizar el build:

```
# Archivo: .dockerignore
.git
.gitignore
.github
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
venv/
.venv/
.DS_Store
node_modules/
```

## Optimización de la Aplicación

Para optimizar el rendimiento de nuestra aplicación en Cloud Run, implementaremos algunas mejoras:

### 1. Optimización de carga de datos:

Modifica el archivo `utils/data_loader.py` para implementar carga perezosa (lazy loading) y almacenamiento en caché:

```python
import pandas as pd
import os
import streamlit as st
from functools import lru_cache

class DataLoader:
    def __init__(self):
        # Definir rutas de datos
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.raw_data_path = os.path.join(self.data_path, 'raw')
        self.emissions_file = os.path.join(self.raw_data_path, 'retc_emisiones_aire_2023.csv')
        
        # Variable para almacenar en caché el dataframe
        self._data = None
    
    @property
    @st.cache_data(ttl=3600)  # Caché de Streamlit con tiempo de vida de 1 hora
    def data(self):
        """Carga perezosa de datos con caché de Streamlit"""
        if self._data is None:
            # Si usamos en producción, podríamos cargar desde Cloud Storage o BigQuery
            self._data = pd.read_csv(self.emissions_file, low_memory=False)
            
            # Limpieza básica de datos
            self._data = self._data.fillna(0)
            
            # Convertir columnas numéricas
            numeric_cols = ['emision', 'latitud', 'longitud']
            for col in numeric_cols:
                if col in self._data.columns:
                    self._data[col] = pd.to_numeric(self._data[col], errors='coerce')
            
            # Reemplazar NaN por 0 después de conversión
            self._data = self._data.fillna(0)
        
        return self._data
    
    @st.cache_data(ttl=3600)
    def get_emissions_summary(self):
        """Obtener resumen de emisiones con caché"""
        df = self.data
        
        if df is not None and not df.empty:
            total_emissions = df['emision'].sum()
            num_facilities = df['nombre_establecimiento'].nunique()
            average_emissions = total_emissions / num_facilities if num_facilities > 0 else 0
            
            return {
                'total_emissions': total_emissions,
                'num_facilities': num_facilities,
                'average_emissions': average_emissions
            }
        return None
    
    @st.cache_data(ttl=3600)
    def get_emissions_by_region(self):
        """Obtener emisiones por región con caché"""
        df = self.data
        
        if df is not None and not df.empty:
            emissions_by_region = df.groupby('region')['emision'].sum().reset_index()
            return emissions_by_region
        return pd.DataFrame()
    
    @st.cache_data(ttl=3600)
    def get_top_emitters(self, limit=10):
        """Obtener principales emisores con caché"""
        df = self.data
        
        if df is not None and not df.empty:
            top_emitters = df.groupby(['nombre_establecimiento', 'region', 'comuna'])['emision'].sum().reset_index()
            top_emitters = top_emitters.sort_values('emision', ascending=False).head(limit)
            return top_emitters
        return pd.DataFrame()
    
    @st.cache_data(ttl=3600)
    def get_geographical_data(self):
        """Obtener datos geográficos con caché"""
        df = self.data
        
        if df is not None and not df.empty:
            # Filtrar solo registros con coordenadas válidas
            geo_data = df[
                (df['latitud'] != 0) & 
                (df['longitud'] != 0) &
                (df['latitud'].notna()) & 
                (df['longitud'].notna())
            ].copy()
            
            # Agregar emisiones por instalación
            geo_data = geo_data.groupby(['nombre_establecimiento', 'latitud', 'longitud', 'region', 'comuna'])['emision'].sum().reset_index()
            
            return geo_data
        return pd.DataFrame()
```

### 2. Configuración de límites de memoria:

Añade un archivo `.streamlit/config.toml` para optimizar el uso de memoria:

```toml
# Archivo: .streamlit/config.toml
[server]
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[runner]
# Límite de tamaño de caché de memoria para las funciones con @st.cache_data
magicEnabled = true
```

## Despliegue en Cloud Run

Hay dos métodos principales para desplegar en Cloud Run: usando Google Cloud Build o desplegando directamente desde tu máquina local. Veremos ambos:

### Método 1: Despliegue con Google Cloud Build (recomendado)

1. Crea un archivo `cloudbuild.yaml`:

```yaml
# Archivo: cloudbuild.yaml
steps:
  # Construir la imagen
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/retc-emissions-app:$COMMIT_SHA', '-f', 'docker/streamlit/Dockerfile', '.']
  
  # Subir la imagen a Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/retc-emissions-app:$COMMIT_SHA']
  
  # Desplegar en Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'retc-emissions-app'
      - '--image=gcr.io/$PROJECT_ID/retc-emissions-app:$COMMIT_SHA'
      - '--platform=managed'
      - '--region=us-central1'
      - '--memory=4Gi'
      - '--cpu=1'
      - '--allow-unauthenticated'
      - '--min-instances=0'
      - '--max-instances=1'

images:
  - 'gcr.io/$PROJECT_ID/retc-emissions-app:$COMMIT_SHA'
```

2. Ejecuta el build desde PowerShell:

```powershell
gcloud builds submit --config cloudbuild.yaml
```

3. Espera a que el build y despliegue se completen (puede tardar varios minutos)

### Método 2: Despliegue manual desde local

1. Construye la imagen Docker:

```powershell
docker build -t gcr.io/[PROJECT_ID]/retc-emissions-app:latest -f docker/streamlit/Dockerfile .
```

2. Envía la imagen a Google Container Registry:

```powershell
docker push gcr.io/[PROJECT_ID]/retc-emissions-app:latest
```

3. Despliega en Cloud Run:

```powershell
gcloud run deploy retc-emissions-app --image gcr.io/[PROJECT_ID]/retc-emissions-app:latest --platform managed --region us-central1 --memory 4Gi --cpu 1 --allow-unauthenticated --min-instances 0 --max-instances 1
```

4. Cuando el despliegue se complete, obtendrás una URL para acceder a tu aplicación (por ejemplo, `https://retc-emissions-app-abcdef123-uc.a.run.app`)

## Configuración de Almacenamiento de Datos

Para aplicaciones con conjuntos de datos grandes, es recomendable almacenar los datos en servicios de almacenamiento en la nube en lugar de incluirlos en la imagen Docker.

### Opción 1: Google Cloud Storage (recomendada)

1. Crea un bucket de almacenamiento:

```powershell
gsutil mb -l us-central1 gs://retc-emissions-data
```

2. Sube tus datos al bucket:

```powershell
gsutil cp data/raw/retc_emisiones_aire_2023.csv gs://retc-emissions-data/raw/
```

3. Modifica `utils/data_loader.py` para cargar datos desde GCS:

```python
# Añadir al inicio del archivo
from google.cloud import storage

# Modificar la clase DataLoader para usar GCS
class DataLoader:
    def __init__(self):
        # Configuración para entorno local o Cloud Run
        self.use_gcs = os.getenv('USE_GCS', 'False').lower() == 'true'
        self.bucket_name = os.getenv('GCS_BUCKET', 'retc-emissions-data')
        self.emissions_blob_path = 'raw/retc_emisiones_aire_2023.csv'
        
        # Rutas locales como fallback
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.raw_data_path = os.path.join(self.data_path, 'raw')
        self.emissions_file = os.path.join(self.raw_data_path, 'retc_emisiones_aire_2023.csv')
        
        # Variable para almacenar en caché el dataframe
        self._data = None
    
    @property
    @st.cache_data(ttl=3600)
    def data(self):
        """Carga datos desde GCS o local con caché"""
        if self._data is None:
            if self.use_gcs:
                # Cargar desde Google Cloud Storage
                try:
                    client = storage.Client()
                    bucket = client.get_bucket(self.bucket_name)
                    blob = bucket.blob(self.emissions_blob_path)
                    
                    # Descargar a un archivo temporal
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False) as temp:
                        blob.download_to_filename(temp.name)
                        self._data = pd.read_csv(temp.name, low_memory=False)
                    
                    # Eliminar archivo temporal
                    os.unlink(temp.name)
                except Exception as e:
                    st.error(f"Error al cargar datos desde GCS: {e}")
                    # Fallback a datos locales
                    if os.path.exists(self.emissions_file):
                        self._data = pd.read_csv(self.emissions_file, low_memory=False)
            else:
                # Cargar desde archivo local
                if os.path.exists(self.emissions_file):
                    self._data = pd.read_csv(self.emissions_file, low_memory=False)
            
            # Procesamiento de datos (como antes)
            if self._data is not None:
                # Limpieza básica de datos
                self._data = self._data.fillna(0)
                
                # Convertir columnas numéricas
                numeric_cols = ['emision', 'latitud', 'longitud']
                for col in numeric_cols:
                    if col in self._data.columns:
                        self._data[col] = pd.to_numeric(self._data[col], errors='coerce')
                
                # Reemplazar NaN por 0 después de conversión
                self._data = self._data.fillna(0)
        
        return self._data
    
    # El resto de métodos siguen igual...
```

4. Actualiza el Dockerfile para instalar la biblioteca de Google Cloud Storage:

```dockerfile
# Añadir a docker/streamlit/Dockerfile
RUN pip install --no-cache-dir google-cloud-storage
```

5. Actualiza el despliegue con las variables de entorno:

```powershell
gcloud run deploy retc-emissions-app --image gcr.io/[PROJECT_ID]/retc-emissions-app:latest --platform managed --region us-central1 --memory 4Gi --cpu 1 --allow-unauthenticated --set-env-vars="USE_GCS=true,GCS_BUCKET=retc-emissions-data"
```

### Opción 2: BigQuery para datos más grandes (opcional)

Para conjuntos de datos realmente grandes, BigQuery es una excelente opción:

1. Crea un dataset de BigQuery:

```powershell
bq mk --dataset retc_emissions
```

2. Carga los datos en BigQuery:

```powershell
bq load --autodetect --source_format=CSV retc_emissions.emissions_data gs://retc-emissions-data/raw/retc_emisiones_aire_2023.csv
```

3. Modifica `utils/data_loader.py` para consultar BigQuery en lugar de cargar todo el CSV (requiere código adicional que puede ser implementado según necesidad).

## Monitoreo y Escalado

### Configuración de monitoreo básico:

1. Ve a la [Consola de Google Cloud](https://console.cloud.google.com/)

2. Navega a "Cloud Run" > Selecciona tu servicio

3. Haz clic en la pestaña "Métricas" para ver:
   - Uso de CPU
   - Uso de memoria
   - Solicitudes por segundo
   - Latencia

### Configuración de alertas:

1. Navega a "Monitoring" > "Alerting"

2. Haz clic en "Create Policy"

3. Configura alertas para:
   - Uso elevado de memoria (>90%)
   - Errores de solicitud (>1%)
   - Latencia elevada (>2s)

4. Agrega canales de notificación (email, SMS, etc.)

### Configuración de escalado automático:

Cloud Run escala automáticamente, pero puedes ajustar los parámetros:

```powershell
gcloud run services update retc-emissions-app --min-instances=0 --max-instances=3 --concurrency=80
```

- `min-instances`: Instancias mínimas (0 para ahorro máximo)
- `max-instances`: Instancias máximas (limita los costos)
- `concurrency`: Solicitudes simultáneas por instancia (aumenta para mejor eficiencia)

## Solución de Problemas Comunes

### Problemas de memoria:

Si la aplicación se queda sin memoria:

1. Aumenta la memoria asignada:

```powershell
gcloud run services update retc-emissions-app --memory=8Gi
```

2. Implementa más optimizaciones en el código para reducir el uso de memoria (muestreo, procesamiento por lotes)

### Errores de tiempo de ejecución:

1. Verifica los logs:

```powershell
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=retc-emissions-app" --limit=20
```

2. Asegúrate de que todas las dependencias estén correctamente instaladas en el Dockerfile

### Problemas de despliegue:

1. Verifica que las API necesarias estén habilitadas

2. Asegúrate de tener los permisos IAM correctos

3. Comprueba que el Dockerfile se esté construyendo correctamente:

```powershell
docker build -t test-image -f docker/streamlit/Dockerfile . && docker run -p 8501:8501 test-image
```

## Optimizaciones Adicionales

### Implementación de caché con Redis (opcional):

1. Crea una instancia de Redis en Memorystore:

```powershell
gcloud redis instances create retc-cache --size=1 --region=us-central1 --redis-version=redis_6_x
```

2. Configura VPC Connector para acceder a Redis desde Cloud Run

3. Modifica la aplicación para usar Redis como caché

### Implementación de CDN para activos estáticos:

1. Almacena imágenes y otros activos estáticos en Cloud Storage

2. Configura Cloud CDN para esos activos

### Optimización de costos:

1. Configura `min-instances=0` para evitar costos cuando no hay tráfico

2. Usa regiones con menor costo (us-central1 suele ser económica)

3. Monitorea el uso y ajusta los recursos según sea necesario

---

## Conclusión

Esta guía te ha proporcionado los pasos detallados para desplegar tu aplicación de Análisis de Emisiones RETC Chile en Google Cloud Run. Con las optimizaciones implementadas, deberías poder ejecutar la aplicación completa dentro de los límites de la capa gratuita para la mayoría de los casos de uso.

Recuerda que Cloud Run es altamente escalable, por lo que si necesitas manejar más tráfico o conjuntos de datos más grandes, puedes aumentar gradualmente los recursos asignados.

Para cualquier problema no cubierto en esta guía, consulta la [documentación oficial de Google Cloud Run](https://cloud.google.com/run/docs).

---

## Referencias y Recursos Adicionales

- [Documentación oficial de Google Cloud Run](https://cloud.google.com/run/docs)
- [Guía de optimización de Streamlit](https://docs.streamlit.io/library/advanced-features/caching)
- [Mejores prácticas para contenedores en Cloud Run](https://cloud.google.com/run/docs/tips/general)
- [Tutorial oficial de Cloud Run + Streamlit](https://cloud.google.com/blog/topics/developers-practitioners/streamlit-google-cloud-platform)
