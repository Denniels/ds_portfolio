# Script simple para detener Cloud Run
$projectId = "retc-emissions-analysis" 
$region = "us-central1"
$serviceName = "ds-portfolio-app"

Write-Host "Deteniendo servicio Cloud Run..."

# Configurar proyecto
gcloud config set project $projectId

# Detener servicio 
gcloud run services update $serviceName --region=$region --min-instances=0 --max-instances=0

Write-Host "Servicio detenido. Configurado con 0 instancias."
