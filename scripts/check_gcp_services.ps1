# Script para verificar y detener servicios GCP
# UTF8 sin BOM
$Host.UI.RawUI.BackgroundColor = "Black"
Clear-Host

Write-Host "[INFO] Verificando servicios GCP activos..." -ForegroundColor Cyan

# Función para mostrar costos estimados
function Show-EstimatedCosts {
    param (
        [string]$ServiceName,
        [double]$EstimatedCost
    )
    Write-Host "   [COSTO] $ServiceName`: $${EstimatedCost}/día" -ForegroundColor Yellow
}

# 1. Verificar Cloud Run
Write-Host "`n[CLOUD RUN] Servicios activos:"
$cloudRunServices = gcloud run services list --platform managed --format="json" | ConvertFrom-Json
if ($cloudRunServices) {
    foreach ($service in $cloudRunServices) {
        Write-Host "   * $($service.metadata.name) - $($service.status.url)" -ForegroundColor Yellow
        Show-EstimatedCosts -ServiceName $service.metadata.name -EstimatedCost 0.05
    }
} else {
    Write-Host "   [OK] No hay servicios Cloud Run activos" -ForegroundColor Green
}

# 2. Verificar Cloud Build
Write-Host "`n[BUILD] Builds en progreso:"
$activeBuilds = gcloud builds list --ongoing --format="json" | ConvertFrom-Json
if ($activeBuilds) {
    foreach ($build in $activeBuilds) {
        Write-Host "   * Build ID: $($build.id) - Status: $($build.status)" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [OK] No hay builds activos" -ForegroundColor Green
}

# 3. Verificar Container Registry
Write-Host "`n[REGISTRY] Imágenes en Container Registry:"
$images = gcloud container images list --format="json" | ConvertFrom-Json
if ($images) {
    foreach ($image in $images) {
        Write-Host "   * $($image.name)" -ForegroundColor Yellow
    }
} else {
    Write-Host "   [OK] No hay imágenes almacenadas" -ForegroundColor Green
}

# Preguntar si desea detener servicios
Write-Host "`n[ACCION] Deseas detener todos los servicios activos? (S/N)" -ForegroundColor Cyan
$response = Read-Host

if ($response -eq "S" -or $response -eq "s") {
    Write-Host "`n[ALERTA] Deteniendo servicios..." -ForegroundColor Red
    
    # Ejecutar script de parada
    $stopScript = Join-Path $PSScriptRoot "stop_gcp_services.ps1"
    if (Test-Path $stopScript) {
        & $stopScript
    } else {
        Write-Host "[ERROR] No se encontró el script de parada (stop_gcp_services.ps1)" -ForegroundColor Red
    }
} else {
    Write-Host "`n[INFO] Operación cancelada por el usuario" -ForegroundColor Yellow
}

Write-Host "`n[INFO] Recuerda revisar la consola de GCP para más detalles: https://console.cloud.google.com/" -ForegroundColor Cyan
