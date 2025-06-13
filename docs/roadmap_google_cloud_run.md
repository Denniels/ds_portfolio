# 🚀 Despliegue del Portafolio de Data Science en Google Cloud Run

> **Guía Completa para Despliegue en la Nube (Junio 2025)**

Este documento proporciona instrucciones detalladas para desplegar el portafolio completo de Data Science en Google Cloud Run, utilizando Docker y aprovechando la capa gratuita de Google Cloud.

## 📋 Requisitos Previos

- Cuenta de Google Cloud (puedes registrarte en [cloud.google.com](https://cloud.google.com))
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) instalado localmente
- [Docker](https://www.docker.com/get-started) instalado localmente
- [Git](https://git-scm.com/downloads) instalado localmente

## 🔍 Capa Gratuita de Google Cloud Run

Google Cloud Run ofrece una generosa capa gratuita que incluye:
- 2 millones de solicitudes gratuitas por mes
- 360,000 GB-segundos de memoria gratuitos
- 180,000 vCPU-segundos gratuitos
- Solo pagas cuando tu servicio procesa solicitudes

## 🔄 Preparación del Proyecto

### 1. Configuración del Dockerfile

Crea un archivo `Dockerfile` en la raíz del proyecto con el siguiente contenido:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Puerto en el que se ejecutará la aplicación
ENV PORT 8080

# Comando para ejecutar la aplicación
CMD streamlit run --server.port=$PORT --server.enableCORS=false --server.enableXsrfProtection=false app/main.py
```

### 2. Actualización de Requirements.txt

Asegúrate de que tu archivo `requirements.txt` incluya todas las dependencias necesarias:

```
streamlit>=1.24.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.14.0
folium>=0.14.0
matplotlib>=3.7.0
seaborn>=0.12.0
google-cloud-bigquery>=3.9.0
pyarrow>=12.0.0
requests>=2.28.0
geopy>=2.3.0
python-dotenv>=1.0.0
```

### 3. Configuración para Cloud Run

Crea un archivo `.dockerignore` para excluir archivos innecesarios:

```
venv/
ds_portfolio_env/
.git
.gitignore
.github
*.pyc
__pycache__/
.vscode/
.idea/
*.md
LICENSE
```

### 4. Configuración de Variables de Entorno (Opcional)

Si tu aplicación utiliza credenciales o variables de entorno, crea un archivo `.env.example`:

```
# Credenciales de BigQuery
GOOGLE_APPLICATION_CREDENTIALS=credentials/your-credentials-file.json

# Otras configuraciones
CACHE_TTL=3600
API_KEY=your_api_key
```

## 🏗️ Construcción y Despliegue

### 1. Inicializa Google Cloud

```bash
# Iniciar sesión en Google Cloud
gcloud auth login

# Establecer el proyecto (reemplaza YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID
```

### 2. Habilitar las APIs necesarias

```bash
# Habilitar Cloud Run y Container Registry
gcloud services enable cloudbuild.googleapis.com containerregistry.googleapis.com run.googleapis.com
```

### 3. Construir y Publicar la Imagen Docker

```bash
# Construir la imagen con Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ds-portfolio

# Alternativamente, construir localmente y subir
docker build -t gcr.io/YOUR_PROJECT_ID/ds-portfolio .
docker push gcr.io/YOUR_PROJECT_ID/ds-portfolio
```

### 4. Desplegar en Cloud Run

```bash
# Desplegar el servicio
gcloud run deploy ds-portfolio \
  --image gcr.io/YOUR_PROJECT_ID/ds-portfolio \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 2
```

## 🔧 Optimizaciones para la Capa Gratuita

Para maximizar el uso de la capa gratuita:

1. **Configuración de Instancias**:
   ```bash
   # Configurar instancias para escalar a cero cuando no hay tráfico
   gcloud run services update ds-portfolio \
     --min-instances 0 \
     --max-instances 2
   ```

2. **Optimización de Memoria y CPU**:
   ```bash
   # Ajustar recursos para equilibrar rendimiento y costos
   gcloud run services update ds-portfolio \
     --memory 512Mi \
     --cpu 1
   ```

3. **Tiempo de Concurrencia**:
   ```bash
   # Configurar cuántas solicitudes puede manejar cada instancia
   gcloud run services update ds-portfolio --concurrency 80
   ```

## 📊 Preparaciones Específicas del Portafolio

### 1. Manejo de Credenciales de BigQuery

Para el módulo de análisis demográfico que usa BigQuery:

```bash
# Crear un secreto para las credenciales
gcloud secrets create bigquery-credentials --replication-policy="automatic"
gcloud secrets versions add bigquery-credentials --data-file="credentials/analicis-demografico-0fa332bfc9a7.json"

# Permitir que el servicio de Cloud Run acceda al secreto
SERVICE_ACCOUNT=$(gcloud run services describe ds-portfolio --platform managed --region us-central1 --format="value(spec.template.spec.serviceAccountName)")
gcloud secrets add-iam-policy-binding bigquery-credentials \
  --member="serviceAccount:$SERVICE_ACCOUNT" \
  --role="roles/secretmanager.secretAccessor"

# Montar el secreto en el servicio
gcloud run services update ds-portfolio \
  --update-secrets="/app/credentials/bigquery-credentials.json=bigquery-credentials:latest"
```

### 2. Configuración del Sistema de Caché

Modifica la configuración de caché para optimizar el rendimiento:

1. Crea un archivo `app/config/cloud_config.py`:

```python
"""
Configuración específica para despliegue en Cloud Run
"""
import os
from datetime import timedelta

# Configuración de caché
CACHE_TTL = int(os.getenv('CACHE_TTL', 3600))  # 1 hora por defecto
MEMORY_CACHE_SIZE = 500  # MB

# Ajustes de rendimiento
STREAMLIT_SERVER_WORKERS = 1
STREAMLIT_SERVER_TIMEOUT = 60  # segundos

# Rutas específicas para Cloud
CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'credentials/default.json')
```

2. Actualiza las referencias a la configuración en tus archivos principales.

### 3. Optimización de Imágenes y Archivos Estáticos

```bash
# Reducir el tamaño de la imagen Docker
docker build --no-cache --build-arg BUILDKIT_INLINE_CACHE=1 -t gcr.io/YOUR_PROJECT_ID/ds-portfolio .
```

## 📈 Monitoreo y Análisis

### 1. Configurar Monitoreo Básico

```bash
# Habilitar el dashboard de monitoreo
gcloud services enable monitoring.googleapis.com
```

### 2. Configurar Alertas de Costos

Configura alertas de presupuesto en Google Cloud Console para estar informado si te acercas a los límites de la capa gratuita.

### 3. Análisis de Rendimiento

Utiliza Google Cloud Operations (anteriormente Stackdriver) para analizar el rendimiento:

```bash
# Habilitar logging avanzado
gcloud services enable logging.googleapis.com

# Ver logs del servicio
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=ds-portfolio" --limit=10
```

## 🔒 Seguridad

### 1. Configuración de Https

Cloud Run proporciona HTTPS por defecto para todos los servicios.

### 2. Control de Acceso (Opcional)

Si deseas restringir el acceso:

```bash
# Requerir autenticación
gcloud run services update ds-portfolio --no-allow-unauthenticated

# Otorgar acceso a usuarios específicos
gcloud run services add-iam-policy-binding ds-portfolio \
  --member="user:ejemplo@gmail.com" \
  --role="roles/run.invoker"
```

## 🚀 Consideraciones Adicionales

### 1. Dominio Personalizado

Para configurar un dominio personalizado:

```bash
# Mapear un dominio personalizado
gcloud beta run domain-mappings create --service ds-portfolio --domain tu-dominio.com
```

### 2. Despliegue Continuo

Configura GitHub Actions para despliegue continuo:

1. Crea un archivo `.github/workflows/deploy.yml`:

```yaml
name: Build and Deploy to Cloud Run

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          
      - name: Build and push Docker image
        run: |
          gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/ds-portfolio
          
      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy ds-portfolio \
            --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/ds-portfolio \
            --platform managed \
            --region us-central1 \
            --allow-unauthenticated
```

### 3. Ajustes para APIs Externas

Si tu aplicación utiliza APIs externas (como datos.gob.cl), asegúrate de manejar tiempos de espera y reintentos adecuadamente:

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def get_api_data(url, max_retries=3):
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return None
```

## 📝 Solución de Problemas Comunes

### 1. Error de Memoria

Si encuentras errores de memoria:

```bash
# Aumentar la asignación de memoria
gcloud run services update ds-portfolio --memory 1Gi
```

### 2. Problemas de Dependencias

Si hay conflictos de dependencias:

1. Usa `pip-tools` para gestionar dependencias:
   ```bash
   pip install pip-tools
   pip-compile requirements.in
   ```

### 3. Tiempos de Carga Lentos

Si la aplicación tarda en cargar:

1. Optimiza las consultas de datos
2. Implementa un sistema de caché más agresivo
3. Considera pre-calcular algunos análisis

## 📚 Recursos Adicionales

- [Documentación oficial de Google Cloud Run](https://cloud.google.com/run/docs)
- [Guía de optimización de costos de Google Cloud](https://cloud.google.com/cost-management/docs/cost-optimization-best-practices)
- [Streamlit en producción](https://docs.streamlit.io/knowledge-base/deploy)
- [Mejores prácticas para Docker](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

Con esta guía detallada, podrás desplegar tu portafolio de Data Science en Google Cloud Run, aprovechando al máximo la capa gratuita mientras mantienes un servicio robusto, seguro y escalable.
