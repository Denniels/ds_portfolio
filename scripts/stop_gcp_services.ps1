# Script de parada de emergencia para servicios GCP
# UTF8 sin BOM
Write-Host "[ALERTA] Iniciando parada de emergencia de servicios GCP..." -ForegroundColor Red

try {
    # 1. Detener Cloud Run
    Write-Host "[PROCESO] Deteniendo servicios de Cloud Run..." -ForegroundColor Yellow
    gcloud run services list --platform managed --format="value(name)" | ForEach-Object {
        Write-Host "   Deteniendo servicio: $_"
        gcloud run services delete $_ --platform managed --region us-central1 --quiet
    }
    Write-Host "[OK] Servicios Cloud Run detenidos" -ForegroundColor Green    # 2. Detener instancias de Cloud Build
    Write-Host "[PROCESO] Cancelando builds activos..." -ForegroundColor Yellow
    gcloud builds list --ongoing --format="value(id)" | ForEach-Object {
        Write-Host "   Cancelando build: $_"
        gcloud builds cancel $_ --quiet
    }
    Write-Host "[OK] Builds cancelados" -ForegroundColor Green

    # 3. Limpiar imágenes de Container Registry
    Write-Host "[PROCESO] Limpiando Container Registry..." -ForegroundColor Yellow
    gcloud container images list --format="value(name)" | ForEach-Object {
        Write-Host "   Eliminando imagen: $_"
        gcloud container images delete $_ --quiet --force-delete-tags
    }
    Write-Host "[OK] Container Registry limpiado" -ForegroundColor Green    # 4. Detener trabajos de Cloud Functions
    Write-Host "[PROCESO] Deteniendo Cloud Functions..." -ForegroundColor Yellow
    gcloud functions list --format="value(name)" | ForEach-Object {
        Write-Host "   Deteniendo función: $_"
        gcloud functions delete $_ --quiet
    }
    Write-Host "[OK] Cloud Functions detenidas" -ForegroundColor Green

    # 5. Detener instancias de Compute Engine (si existen)
    Write-Host "[PROCESO] Deteniendo instancias de Compute Engine..." -ForegroundColor Yellow
    gcloud compute instances list --format="value(name,zone)" | ForEach-Object {
        $instance, $zone = $_.Split()
        Write-Host "   Deteniendo instancia: $instance en zona: $zone"
        gcloud compute instances stop $instance --zone=$zone --quiet
    }
    Write-Host "[OK] Instancias de Compute Engine detenidas" -ForegroundColor Green    # 6. Verificar estado final
    Write-Host "`n[VERIFICACION] Comprobando estado final de los servicios..." -ForegroundColor Cyan
    
    Write-Host "`n[ESTADO] Cloud Run:"
    gcloud run services list --platform managed
    
    Write-Host "`n[ESTADO] Cloud Build:"
    gcloud builds list --ongoing
    
    Write-Host "`n[ESTADO] Compute Engine:"
    gcloud compute instances list

    Write-Host "`n[OK] Parada de emergencia completada exitosamente" -ForegroundColor Green
    Write-Host "[AVISO] Algunos servicios pueden seguir generando costos minimos. Revisa la consola de GCP." -ForegroundColor Yellow

} catch {
    Write-Host "`n[ERROR] Error durante la parada de emergencia: $_" -ForegroundColor Red
    Write-Host "[ACCION] Por favor, verifica manualmente en la consola de GCP: https://console.cloud.google.com/" -ForegroundColor Red
    exit 1
}
