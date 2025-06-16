# Script para detener Cloud Run (versión simplificada)
$projectId = "retc-emissions-analysis" 
$region = "us-central1"
$serviceName = "ds-portfolio-app"

Write-Host "Deteniendo servicio Cloud Run de emergencia..."
Write-Host "Proyecto: $projectId"
Write-Host "Servicio: $serviceName"

# Configurar proyecto
gcloud config set project $projectId

# Detener servicio (0 instancias)
gcloud run services update $serviceName --region=$region --min-instances=0 --max-instances=0

# Desactivar acceso público
gcloud run services update $serviceName --region=$region --no-allow-unauthenticated

Write-Host "Servicio detenido exitosamente."
Write-Host "El servicio $serviceName ha sido configurado con 0 instancias."
