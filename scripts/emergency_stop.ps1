# Script para detener EMERGENCIA el servicio de Cloud Run (PowerShell)
# Detiene por completo el servicio para evitar cualquier costo adicional

# Variables de configuración
$ProjectId = "retc-emissions-analysis" 
$Region = "us-central1"
$ServiceName = "ds-portfolio-app"

Write-Host "==============================================================="
Write-Host "       DETENCIÓN DE EMERGENCIA DEL SERVICIO DE CLOUD RUN       "
Write-Host "==============================================================="
Write-Host ""
Write-Host "Proyecto: $ProjectId"
Write-Host "Región: $Region"
Write-Host "Servicio: $ServiceName"
Write-Host ""

# 1. Verificar autenticación en Google Cloud
Write-Host "[INFO] Verificando autenticación en Google Cloud..." -ForegroundColor Cyan
$AuthCheck = gcloud auth list 2>&1
if ($AuthCheck -like "*No credentialed accounts*") {
    Write-Host "[ERROR] No estás autenticado en Google Cloud. Ejecuta 'gcloud auth login' primero." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Autenticación correcta" -ForegroundColor Green

# 2. Configurar el proyecto
Write-Host "[INFO] Configurando el proyecto $ProjectId..." -ForegroundColor Cyan
gcloud config set project $ProjectId
if (-not $?) {
    Write-Host "[ERROR] Error al configurar el proyecto. Abortando..." -ForegroundColor Red
    exit 1
}

# 3. Detener el servicio estableciendo instancias mínimas y máximas a 0
Write-Host "[INFO] DETENIENDO EL SERVICIO $ServiceName..." -ForegroundColor Red
gcloud run services update $ServiceName --region=$Region --min-instances=0 --max-instances=0

if (-not $?) {
    Write-Host "[ERROR] Error al detener el servicio. Abortando..." -ForegroundColor Red
    exit 1
}

# 4. Desactivar el acceso público para asegurar que no se genere tráfico
Write-Host "[INFO] Desactivando el acceso público al servicio..." -ForegroundColor Cyan
gcloud run services update $ServiceName --region=$Region --no-allow-unauthenticated

Write-Host "==============================================================="
Write-Host "  SERVICIO DETENIDO EXITOSAMENTE - NO SE GENERARÁN MÁS COSTOS  "
Write-Host "==============================================================="
Write-Host "El servicio $ServiceName ha sido configurado con 0 instancias."
Write-Host "Se ha desactivado también el acceso público para mayor seguridad."
Write-Host ""
Write-Host "No se generarán costos adicionales."
Write-Host ""
Write-Host "Para reactivar el servicio con la configuración anterior, ejecuta:"
Write-Host "./scripts/deploy_to_cloud_run.ps1"
Write-Host "==============================================================="
