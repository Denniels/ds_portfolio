#!/bin/bash
# Script para habilitar la API de Firestore en Google Cloud

# Asegurarse de que gcloud esté configurada correctamente
echo "Verificando autenticación de Google Cloud..."
gcloud auth list

# Establecer el proyecto
echo "Configurando proyecto retc-emissions-analysis..."
gcloud config set project retc-emissions-analysis

# Habilitar la API de Firestore
echo "Habilitando la API de Cloud Firestore..."
gcloud services enable firestore.googleapis.com

# Crear la base de datos de Firestore (en modo nativo)
echo "Creando la base de datos de Firestore en modo nativo..."
gcloud firestore databases create --region=us-central1

echo ""
echo "Configuración completada. La API de Firestore debería estar habilitada."
echo "Si acabas de habilitar la API, puede tomar unos minutos para que los cambios se propaguen."
echo ""
echo "Para verificar el estado, visita:"
echo "https://console.cloud.google.com/firestore/databases?project=retc-emissions-analysis"
