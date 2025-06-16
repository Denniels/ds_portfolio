# Script para detener servicios de Cloud Run en caso de emergencia
# Este script configura las instancias a 0 y desactiva el acceso público

# Variables de configuración
$projectId = "retc-emissions-analysis" 
$region = "us-central1"
$serviceName = "ds-portfolio-app"

Write-Host "=========================================================="
Write-Host "      DETENCIÓN DE EMERGENCIA DEL SERVICIO CLOUD RUN      "
Write-Host "=========================================================="
Write-Host ""
Write-Host "Proyecto: $projectId"
Write-Host "Región: $region"
Write-Host "Servicio: $serviceName"
Write-Host ""

# 1. Verificar autenticación en Google Cloud
Write-Host "[INFO] Verificando autenticación en Google Cloud..." -ForegroundColor Cyan
try {
    $authStatus = gcloud auth list
    if ($authStatus -like "*No credentialed accounts*") {
        Write-Host "[ERROR] No estás autenticado en Google Cloud. Ejecuta 'gcloud auth login' primero." -ForegroundColor Red
        exit 1
    }
    Write-Host "[OK] Autenticación correcta" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Error al verificar la autenticación: $_" -ForegroundColor Red
    exit 1
}

# 2. Configurar el proyecto
Write-Host "[INFO] Configurando el proyecto $projectId..." -ForegroundColor Cyan
try {
    gcloud config set project $projectId
    Write-Host "[OK] Proyecto configurado correctamente" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Error al configurar el proyecto: $_" -ForegroundColor Red
    exit 1
}

# 3. Detener el servicio estableciendo instancias mínimas y máximas a 0
Write-Host "[INFO] DETENIENDO EL SERVICIO $serviceName..." -ForegroundColor Red
try {
    gcloud run services update $serviceName --region=$region --min-instances=0 --max-instances=0
    Write-Host "[OK] Servicio configurado con 0 instancias" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Error al detener el servicio: $_" -ForegroundColor Red
    exit 1
}

# 4. Desactivar el acceso público para asegurar que no se genere tráfico
Write-Host "[INFO] Desactivando el acceso público al servicio..." -ForegroundColor Cyan
try {
    gcloud run services update $serviceName --region=$region --no-allow-unauthenticated
    Write-Host "[OK] Acceso público desactivado correctamente" -ForegroundColor Green
}
catch {
    Write-Host "[ADVERTENCIA] No se pudo desactivar el acceso público pero el servicio está con 0 instancias." -ForegroundColor Yellow
}

Write-Host "=========================================================="
Write-Host "  SERVICIO DETENIDO EXITOSAMENTE - NO MÁS COSTOS  "
Write-Host "=========================================================="
Write-Host "El servicio $serviceName ha sido configurado con 0 instancias."
Write-Host "No se generarán costos adicionales hasta que se reconfigure."
Write-Host ""
Write-Host "Para reactivar el servicio cuando lo necesites, ejecuta:"
Write-Host "gcloud run services update $serviceName --region=$region --min-instances=0 --max-instances=1 --allow-unauthenticated"
