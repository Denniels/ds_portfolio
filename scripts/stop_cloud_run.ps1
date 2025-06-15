# Script para detener el servicio de Cloud Run (PowerShell)
# Versión EMERGENCIA - Detiene completamente el servicio para evitar costos

# Variables de configuración
$ProjectId = "retc-emissions-analysis"  # Reemplaza con tu ID de proyecto real
$Region = "us-central1"
$ServiceName = "ds-portfolio-app"

Write-Host "==============================================================="
Write-Host "       DETENCIÓN DEL SERVICIO DE CLOUD RUN                     "
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
Write-Host "[INFO] Deteniendo el servicio $ServiceName configurando instancias a 0..." -ForegroundColor Cyan
gcloud run services update $ServiceName --region=$Region --min-instances=0 --max-instances=0

if (-not $?) {
    Write-Host "[ERROR] Error al detener el servicio. Abortando..." -ForegroundColor Red
    exit 1
}

# 4. Desactivar el acceso público para asegurar que no se genere tráfico
Write-Host "[INFO] Desactivando el acceso público al servicio..." -ForegroundColor Cyan
gcloud run services update $ServiceName --region=$Region --no-allow-unauthenticated

if (-not $?) {
    Write-Host "[ADVERTENCIA] No se pudo desactivar el acceso público, pero el servicio está con 0 instancias." -ForegroundColor Yellow
}

Write-Host "==============================================================="
Write-Host "  SERVICIO DETENIDO EXITOSAMENTE                               "
Write-Host "==============================================================="
Write-Host "El servicio $ServiceName ha sido configurado con 0 instancias."
Write-Host "No se generarán costos adicionales hasta que se reciba tráfico o"
Write-Host "se reconfigure el servicio con instancias mínimas."
Write-Host ""
Write-Host "Para reactivar el servicio con la configuración anterior, ejecuta:"
Write-Host "./scripts/restore_cloud_run.ps1"
Write-Host "==============================================================="
Write-Host "El servicio $ServiceName ha sido configurado con 0 instancias."
Write-Host "No se generarán costos adicionales hasta que se reciba tráfico o"
Write-Host "se reconfigure el servicio con instancias mínimas."
Write-Host ""
Write-Host "Para reactivar el servicio con la configuración anterior, ejecuta:"
Write-Host "./scripts/restore_cloud_run.ps1"
Write-Host "===========================================================
