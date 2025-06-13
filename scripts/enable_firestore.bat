@echo off
:: Script para habilitar la API de Firestore en Google Cloud desde Windows

cd e:\repos\ds_portfolio

:: Asegurarse de que gcloud esté configurada correctamente
echo Verificando autenticacion de Google Cloud...
gcloud auth list

:: Establecer el proyecto
echo Configurando proyecto retc-emissions-analysis...
gcloud config set project retc-emissions-analysis

:: Habilitar la API de Firestore
echo Habilitando la API de Cloud Firestore...
gcloud services enable firestore.googleapis.com

:: Crear la base de datos de Firestore (en modo nativo)
echo Creando la base de datos de Firestore en modo nativo...
gcloud firestore databases create --region=us-central1 --type=firestore-native

:: Verificar si la creación fue exitosa
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo AVISO: No se pudo crear la base de datos automáticamente.
    echo Por favor, crea la base de datos manualmente en:
    echo https://console.cloud.google.com/firestore/databases?project=retc-emissions-analysis
    echo.
    echo Instrucciones:
    echo 1. Haz clic en "Crear base de datos"
    echo 2. Selecciona "Modo nativo"
    echo 3. Selecciona la región "us-central1"
    echo 4. Haz clic en "Crear"
    echo.
    pause
)

echo.
echo Configuracion completada. La API de Firestore deberia estar habilitada.
echo Si acabas de habilitar la API, puede tomar unos minutos para que los cambios se propaguen.
echo.
echo Para verificar el estado, visita:
echo https://console.cloud.google.com/firestore/databases?project=retc-emissions-analysis
