# Script para desplegar la aplicación en Google Cloud Run (versión PowerShell)

# Variables
$ProjectId = "retc-emissions-analysis"  # Asegúrate de reemplazar esto con tu ID de proyecto real
$Region = "us-central1"
$ServiceName = "ds-portfolio-app"
$ImageName = "gcr.io/${ProjectId}/${ServiceName}"
$Tag = Get-Date -Format "yyyyMMddHHmmss"  # Generar tag basado en fecha/hora

Write-Host "==========================================================="
Write-Host "       REDESPLIEGUE COMPLETO DEL PORTAFOLIO DS             "
Write-Host "==========================================================="
Write-Host ""
Write-Host "Proyecto: ${ProjectId}"
Write-Host "Región: ${Region}"
Write-Host "Servicio: ${ServiceName}"
Write-Host "Imagen: ${ImageName}:${Tag}"
Write-Host ""

# 1. Verificar autenticación en Google Cloud
Write-Host "🔑 Verificando autenticación en Google Cloud..." -ForegroundColor Cyan
$authList = gcloud auth list 2>$null
if (-not ($authList -match "ACTIVE")) {
    Write-Host "⚠️ No estás autenticado en Google Cloud. Iniciando sesión..." -ForegroundColor Yellow
    gcloud auth login
} else {
    Write-Host "✅ Autenticación correcta" -ForegroundColor Green
}

# 2. Configurar el proyecto
Write-Host "🔧 Configurando el proyecto ${ProjectId}..." -ForegroundColor Cyan
gcloud config set project $ProjectId

# 3. Verificar que las APIs necesarias estén habilitadas
Write-Host "🔌 Verificando APIs necesarias..." -ForegroundColor Cyan
$Apis = @("run.googleapis.com", "containerregistry.googleapis.com", "cloudbuild.googleapis.com", "artifactregistry.googleapis.com", "storage.googleapis.com", "firestore.googleapis.com")

foreach ($Api in $Apis) {
    $enabled = gcloud services list --enabled | Select-String -Pattern $Api
    if (-not $enabled) {
        Write-Host "⚙️ Habilitando ${Api}..." -ForegroundColor Yellow
        gcloud services enable $Api
    } else {
        Write-Host "✅ ${Api} ya está habilitada" -ForegroundColor Green
    }
}

# 4. Construir la imagen Docker
Write-Host "🏗️ Construyendo imagen Docker..." -ForegroundColor Cyan
docker build -t "${ImageName}:${Tag}" .
if (-not $?) {
    Write-Host "❌ Error al construir la imagen Docker. Abortando..." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Imagen Docker construida exitosamente" -ForegroundColor Green

# 5. Subir la imagen a Google Container Registry
Write-Host "📤 Subiendo imagen a Google Container Registry..." -ForegroundColor Cyan
docker push "${ImageName}:${Tag}"
if (-not $?) {
    Write-Host "❌ Error al subir la imagen. Verificando autenticación Docker con GCR..." -ForegroundColor Yellow
    gcloud auth configure-docker
    # Intentar subir de nuevo después de autenticarse
    docker push "${ImageName}:${Tag}"
    if (-not $?) {
        Write-Host "❌ Error al subir la imagen después de autenticarse. Abortando..." -ForegroundColor Red
        exit 1
    }
}
Write-Host "✅ Imagen subida exitosamente" -ForegroundColor Green

# 6. Desplegar en Cloud Run
Write-Host "🚀 Desplegando en Cloud Run..." -ForegroundColor Cyan
gcloud run deploy $ServiceName `
    --image="${ImageName}:${Tag}" `
    --platform=managed `
    --region=$Region `
    --memory=4Gi `
    --cpu=1 `
    --allow-unauthenticated `
    --min-instances=0 `
    --max-instances=1 `
    --concurrency=80
if (-not $?) {
    Write-Host "❌ Error durante el despliegue en Cloud Run. Abortando..." -ForegroundColor Red
    exit 1
}

# 7. Obtener la URL del servicio
$ServiceUrl = gcloud run services describe $ServiceName --platform=managed --region=$Region --format='value(status.url)'

Write-Host ""
Write-Host "==========================================================="
Write-Host "  🎉 ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!  🎉" -ForegroundColor Green
Write-Host "==========================================================="
Write-Host ""
Write-Host "📱 Tu aplicación está disponible en:"
Write-Host "${ServiceUrl}" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Monitoreo y métricas:"
Write-Host "https://console.cloud.google.com/run/detail/${Region}/${ServiceName}/metrics" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Logs de la aplicación:"
Write-Host "https://console.cloud.google.com/logs/query;query=resource.type%3D%22cloud_run_revision%22%20AND%20resource.labels.service_name%3D%22${ServiceName}%22" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️ Recuerda que la aplicación escala a cero cuando no está en uso," -ForegroundColor Yellow
Write-Host "por lo que la primera carga puede tardar unos segundos." -ForegroundColor Yellow
Write-Host "==========================================================="
