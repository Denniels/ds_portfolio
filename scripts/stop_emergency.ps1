Write-Host "==============================================================="
Write-Host "       DETENCIÓN DE EMERGENCIA DEL SERVICIO DE CLOUD RUN"
Write-Host "==============================================================="
Write-Host ""
Write-Host "Proyecto: retc-emissions-analysis"
Write-Host "Región: us-central1"
Write-Host "Servicio: ds-portfolio-app"
Write-Host ""

# 1. Verificar autenticación en Google Cloud
Write-Host "[INFO] Verificando autenticación en Google Cloud..." -ForegroundColor Cyan
$authStatus = gcloud auth list 2>&1
if ($authStatus -like "*No credentialed accounts*") {
    Write-Host "[ERROR] No estás autenticado en Google Cloud. Ejecuta gcloud auth login primero." -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Autenticación correcta" -ForegroundColor Green

# 2. Configurar el proyecto
Write-Host "[INFO] Configurando el proyecto retc-emissions-analysis..." -ForegroundColor Cyan
gcloud config set project retc-emissions-analysis | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al configurar el proyecto. Abortando..." -ForegroundColor Red
    exit 1
}

# 3. Detener el servicio estableciendo instancias mínimas y máximas a 0
Write-Host "[INFO] DETENIENDO EL SERVICIO ds-portfolio-app (configurando instancias a 0)..." -ForegroundColor Red
gcloud run services update ds-portfolio-app --region=us-central1 --min-instances=0 --max-instances=0 | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al detener el servicio. Abortando..." -ForegroundColor Red
    exit 1
}

# 4. Desactivar el acceso público para asegurar que no se genere tráfico
Write-Host "[INFO] Desactivando el acceso público al servicio..." -ForegroundColor Cyan
gcloud run services update ds-portfolio-app --region=us-central1 --no-allow-unauthenticated | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ADVERTENCIA] No se pudo desactivar el acceso público pero el servicio está con 0 instancias." -ForegroundColor Yellow
}

Write-Host "==============================================================="
Write-Host "  SERVICIO DETENIDO EXITOSAMENTE - EVITANDO MÁS COSTOS"
Write-Host "==============================================================="
Write-Host "El servicio ds-portfolio-app ha sido configurado con 0 instancias."
Write-Host "No se generarán costos adicionales hasta que se reconfigure el servicio."
Write-Host ""
Write-Host "Para reactivar el servicio cuando lo necesites, ejecuta:"
Write-Host "gcloud run services update ds-portfolio-app --region=us-central1 --min-instances=0 --max-instances=1 --allow-unauthenticated"
Write-Host "==============================================================="
