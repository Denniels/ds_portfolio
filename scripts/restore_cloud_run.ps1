# Script para restaurar el servicio de Cloud Run (PowerShell)

# Variables de configuración
$ProjectId = "retc-emissions-analysis"  # Reemplaza con tu ID de proyecto real
$Region = "us-central1"
$ServiceName = "ds-portfolio-app"

Write-Host "==========================================================="
Write-Host "       RESTAURACIÓN DEL SERVICIO DE CLOUD RUN              "
Write-Host "==========================================================="
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

# 3. Restaurar el servicio con la configuración optimizada para costos
Write-Host "[INFO] Restaurando el servicio $ServiceName..." -ForegroundColor Cyan
gcloud run services update $ServiceName `
    --region=$Region `
    --min-instances=0 `
    --max-instances=1 `
    --memory=512Mi `
    --cpu=1 `
    --timeout=30s `
    --concurrency=40

if (-not $?) {
    Write-Host "[ERROR] Error al restaurar el servicio. Abortando..." -ForegroundColor Red
    exit 1
}

Write-Host "==========================================================="
Write-Host "  SERVICIO RESTAURADO EXITOSAMENTE                         "
Write-Host "==========================================================="
Write-Host "El servicio $ServiceName ha sido restaurado con configuración optimizada para costos."
Write-Host "La aplicación seguirá escalando automáticamente entre 0 y 1 instancia según el tráfico,"
Write-Host "lo que mantendrá los costos bajo control mientras permite que la aplicación esté disponible."
Write-Host "==========================================================="
