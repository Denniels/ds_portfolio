# Script de verificación exhaustiva de servicios GCP
# UTF8 sin BOM
$ErrorActionPreference = "Continue"

# Función para ejecutar comandos gcloud con timeout
function Invoke-GCloudCommand {
    param (
        [string]$Command,
        [int]$Timeout = 30
    )
    
    $job = Start-Job -ScriptBlock { 
        param($cmd)
        Invoke-Expression $cmd
    } -ArgumentList $Command

    if (Wait-Job $job -Timeout $Timeout) {
        $result = Receive-Job $job
        Remove-Job $job
        return $result
    } else {
        Remove-Job $job -Force
        Write-Host "[TIMEOUT] El comando tardó demasiado: $Command" -ForegroundColor Yellow
        return $null
    }
}

Write-Host "[INICIO] Verificación exhaustiva de servicios GCP" -ForegroundColor Cyan
Write-Host "Proyecto: $(gcloud config get-value project)" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Esto puede tomar unos minutos..." -ForegroundColor Yellow

function Write-ServiceStatus {
    param (
        [string]$ServiceName,
        [string]$Status,
        [string]$Details = ""
    )
    if ($Status -eq "Activo") {
        Write-Host "[ALERTA] $ServiceName : $Status $Details" -ForegroundColor Red
    } else {
        Write-Host "[OK] $ServiceName : $Status $Details" -ForegroundColor Green
    }
}

try {    # 1. Cloud Run
    Write-Host "`n[CHECANDO] Servicios Cloud Run..." -ForegroundColor Yellow
    $cloudRun = Invoke-GCloudCommand "gcloud run services list --platform managed --format='value(name)' 2>$null"
    if ($cloudRun) {
        Write-ServiceStatus "Cloud Run" "Activo" "($($cloudRun.Count) servicios encontrados)"
        $cloudRun | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "Cloud Run" "Inactivo"
    }    # 2. Compute Engine
    Write-Host "`n[CHECANDO] Instancias Compute Engine..." -ForegroundColor Yellow
    $instances = Invoke-GCloudCommand "gcloud compute instances list --format='value(name)' 2>$null"
    if ($instances) {
        Write-ServiceStatus "Compute Engine" "Activo" "($($instances.Count) instancias encontradas)"
        $instances | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "Compute Engine" "Inactivo"
    }    # 3. Cloud Functions
    Write-Host "`n[CHECANDO] Cloud Functions..." -ForegroundColor Yellow
    $functions = Invoke-GCloudCommand "gcloud functions list --format='value(name)' 2>$null"
    if ($functions) {
        Write-ServiceStatus "Cloud Functions" "Activo" "($($functions.Count) funciones encontradas)"
        $functions | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "Cloud Functions" "Inactivo"
    }    # 4. Container Registry
    Write-Host "`n[CHECANDO] Container Registry..." -ForegroundColor Yellow
    $containers = Invoke-GCloudCommand "gcloud container images list --format='value(name)' 2>$null"
    if ($containers) {
        Write-ServiceStatus "Container Registry" "Activo" "($($containers.Count) imágenes encontradas)"
        $containers | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "Container Registry" "Inactivo"
    }    # 5. Cloud Build
    Write-Host "`n[CHECANDO] Cloud Build..." -ForegroundColor Yellow
    $builds = Invoke-GCloudCommand "gcloud builds list --ongoing --format='value(id)' 2>$null"
    if ($builds) {
        Write-ServiceStatus "Cloud Build" "Activo" "($($builds.Count) builds activos)"
        $builds | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "Cloud Build" "Inactivo"
    }    # 6. Cloud Storage
    Write-Host "`n[CHECANDO] Cloud Storage..." -ForegroundColor Yellow
    $buckets = Invoke-GCloudCommand "gsutil ls 2>$null"
    if ($buckets) {
        Write-ServiceStatus "Cloud Storage" "Activo" "($($buckets.Count) buckets encontrados)"
        $buckets | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "Cloud Storage" "Inactivo"
    }    # 7. APIs Activas
    Write-Host "`n[CHECANDO] APIs activas..." -ForegroundColor Yellow
    $apis = Invoke-GCloudCommand "gcloud services list --enabled --format='value(config.name)' 2>$null"
    if ($apis) {
        Write-ServiceStatus "APIs" "Activas" "($($apis.Count) APIs habilitadas)"
        $apis | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
    } else {
        Write-ServiceStatus "APIs" "Sin APIs adicionales"
    }    # 8. BigQuery
    Write-Host "`n[CHECANDO] BigQuery..." -ForegroundColor Yellow
    $datasets = Invoke-GCloudCommand "bq ls --format=sparse 2>$null"
    if ($datasets -and $datasets.Count -gt 1) {
        Write-ServiceStatus "BigQuery" "Activo" "($($datasets.Count - 1) datasets encontrados)"
        $datasets | Select-Object -Skip 1 | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    } else {
        Write-ServiceStatus "BigQuery" "Inactivo"
    }

    # Resumen final
    Write-Host "`n[RESUMEN] Estado general de servicios" -ForegroundColor Cyan
    Write-Host "=============================================" -ForegroundColor Cyan
    
    if ($cloudRun -or $instances -or $functions -or $containers -or $builds -or $buckets -or ($datasets -and $datasets.Count -gt 1)) {
        Write-Host "`n[ALERTA] Se encontraron servicios activos que pueden generar costos." -ForegroundColor Red
        Write-Host "Ejecuta el script de parada de emergencia: .\scripts\stop_gcp_services.ps1" -ForegroundColor Yellow
    } else {
        Write-Host "`n[OK] No se encontraron servicios activos que puedan generar costos significativos." -ForegroundColor Green
    }    # Verificar facturación
    Write-Host "`n[CHECANDO] Estado de facturación..." -ForegroundColor Yellow
    $billing = Invoke-GCloudCommand "gcloud beta billing projects describe $(gcloud config get-value project) --format='value(billingEnabled)' 2>$null"
    if ($billing -eq "True") {
        Write-Host "[ALERTA] La facturación está HABILITADA para este proyecto" -ForegroundColor Red
        Write-Host "Considera deshabilitar la facturación en: https://console.cloud.google.com/billing" -ForegroundColor Yellow
    } else {
        Write-Host "[OK] La facturación está DESHABILITADA para este proyecto" -ForegroundColor Green
    }

} catch {
    Write-Host "`n[ERROR] Error durante la verificación: $_" -ForegroundColor Red
    Write-Host "[ACCION] Verifica manualmente en la consola: https://console.cloud.google.com/" -ForegroundColor Yellow
}
