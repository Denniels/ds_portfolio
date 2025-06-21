# Script de configuración de entorno para PowerShell
$ErrorActionPreference = 'Stop'

# Verificar Python 3.9
$pythonVersion = python --version 2>&1
if (-not ($pythonVersion -match '3\.9\.\d+')) {
    Write-Error "Se requiere Python 3.9.x. Versión actual: $pythonVersion"
    exit 1
}

# Crear entorno virtual si no existe
if (-not (Test-Path "ds_portfolio_env")) {
    Write-Host "Creando entorno virtual..."
    python -m venv ds_portfolio_env
}

# Activar entorno virtual
.\ds_portfolio_env\Scripts\Activate.ps1

# Actualizar pip y herramientas de build
python -m pip install --upgrade pip setuptools wheel

# Instalar dependencias con versiones fijas
pip install -r requirements.txt

# Verificar instalación
python -c "import numpy; import pandas; import streamlit; print('Entorno configurado correctamente')"

Write-Host "Configuración completada con éxito."
