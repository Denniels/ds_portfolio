#!/bin/bash
# Script para desplegar la aplicación en Google Cloud Run

# Variables
PROJECT_ID="retc-emissions-analysis"  # Asegúrate de reemplazar esto con tu ID de proyecto real
REGION="us-central1"
SERVICE_NAME="ds-portfolio-app"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"
TAG=$(date +%Y%m%d%H%M%S)  # Generar tag basado en fecha/hora

echo "==========================================================="
echo "       REDESPLIEGUE COMPLETO DEL PORTAFOLIO DS             "
echo "==========================================================="
echo ""
echo "Proyecto: ${PROJECT_ID}"
echo "Región: ${REGION}"
echo "Servicio: ${SERVICE_NAME}"
echo "Imagen: ${IMAGE_NAME}:${TAG}"
echo ""

# 1. Verificar autenticación en Google Cloud
echo "🔑 Verificando autenticación en Google Cloud..."
if ! gcloud auth list 2>/dev/null | grep -q "ACTIVE"; then
    echo "⚠️ No estás autenticado en Google Cloud. Iniciando sesión..."
    gcloud auth login
else
    echo "✅ Autenticación correcta"
fi

# 2. Configurar el proyecto
echo "🔧 Configurando el proyecto ${PROJECT_ID}..."
gcloud config set project ${PROJECT_ID}

# 3. Verificar que las APIs necesarias estén habilitadas
echo "🔌 Verificando APIs necesarias..."
APIS=("run.googleapis.com" "containerregistry.googleapis.com" "cloudbuild.googleapis.com" "artifactregistry.googleapis.com" "storage.googleapis.com" "firestore.googleapis.com")

for API in "${APIS[@]}"; do
    if ! gcloud services list --enabled | grep -q "${API}"; then
        echo "⚙️ Habilitando ${API}..."
        gcloud services enable ${API}
    else
        echo "✅ ${API} ya está habilitada"
    fi
done

# 4. Construir la imagen Docker
echo "🏗️ Construyendo imagen Docker..."
if ! docker build -t ${IMAGE_NAME}:${TAG} .; then
    echo "❌ Error al construir la imagen Docker. Abortando..."
    exit 1
fi
echo "✅ Imagen Docker construida exitosamente"

# 5. Subir la imagen a Google Container Registry
echo "📤 Subiendo imagen a Google Container Registry..."
if ! docker push ${IMAGE_NAME}:${TAG}; then
    echo "❌ Error al subir la imagen. Verificando autenticación Docker con GCR..."
    gcloud auth configure-docker
    # Intentar subir de nuevo después de autenticarse
    if ! docker push ${IMAGE_NAME}:${TAG}; then
        echo "❌ Error al subir la imagen después de autenticarse. Abortando..."
        exit 1
    fi
fi
echo "✅ Imagen subida exitosamente"

# 6. Desplegar en Cloud Run
echo "🚀 Desplegando en Cloud Run..."
if ! gcloud run deploy ${SERVICE_NAME} \
    --image=${IMAGE_NAME}:${TAG} \
    --platform=managed \
    --region=${REGION} \
    --memory=4Gi \
    --cpu=1 \
    --allow-unauthenticated \
    --min-instances=0 \
    --max-instances=1 \
    --concurrency=80; then
    echo "❌ Error durante el despliegue en Cloud Run. Abortando..."
    exit 1
fi

# 7. Obtener la URL del servicio
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --platform=managed --region=${REGION} --format='value(status.url)')

echo ""
echo "==========================================================="
echo "  🎉 ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!  🎉"
echo "==========================================================="
echo ""
echo "📱 Tu aplicación está disponible en:"
echo "${SERVICE_URL}"
echo ""
echo "📊 Monitoreo y métricas:"
echo "https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}/metrics"
echo ""
echo "📝 Logs de la aplicación:"
echo "https://console.cloud.google.com/logs/query;query=resource.type%3D%22cloud_run_revision%22%20AND%20resource.labels.service_name%3D%22${SERVICE_NAME}%22"
echo ""
echo "⚠️ Recuerda que la aplicación escala a cero cuando no está en uso,"
echo "por lo que la primera carga puede tardar unos segundos."
echo "==========================================================="
