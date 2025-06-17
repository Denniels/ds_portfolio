# Script PowerShell para configurar el entorno de notebooks

Write-Host "🔧 Configurando entorno de notebooks..." -ForegroundColor Green

# Verificar que estamos en el directorio correcto
if (-not (Test-Path ".\.venv_fresh\Scripts\python.exe")) {
    Write-Host "❌ No se encuentra el entorno virtual .venv_fresh" -ForegroundColor Red
    exit 1
}

# Activar entorno virtual
Write-Host "📦 Activando entorno virtual..." -ForegroundColor Yellow
.\.venv_fresh\Scripts\Activate.ps1

# Verificar Python
Write-Host "🐍 Verificando Python..." -ForegroundColor Yellow
python --version
python -c "import sys; print('Ejecutable:', sys.executable)"

# Verificar dependencias críticas
Write-Host "📚 Verificando dependencias..." -ForegroundColor Yellow
python -c @"
try:
    import pandas as pd
    import numpy as np
    import plotly
    import matplotlib
    import ipykernel
    print('✅ Todas las dependencias están disponibles')
    print(f'  • Pandas: {pd.__version__}')
    print(f'  • NumPy: {np.__version__}')
    print(f'  • Plotly: {plotly.__version__}')
    print(f'  • Matplotlib: {matplotlib.__version__}')
except ImportError as e:
    print(f'❌ Error importando: {e}')
"@

# Limpiar kernels anteriores problemáticos
Write-Host "🧹 Limpiando kernels anteriores..." -ForegroundColor Yellow
try {
    python -m jupyter kernelspec remove venv_fresh_ds -f 2>$null
} catch {
    # Ignorar errores si el kernel no existe
}

try {
    python -m jupyter kernelspec remove .venv_fresh -f 2>$null
} catch {
    # Ignorar errores si el kernel no existe
}

# Recrear kernel con nombre limpio
Write-Host "🎯 Creando nuevo kernel..." -ForegroundColor Yellow
python -m ipykernel install --user --name=venv_fresh_ds --display-name="DS Portfolio (venv_fresh)"

# Verificar kernel
Write-Host "📋 Kernels disponibles:" -ForegroundColor Yellow
python -m jupyter kernelspec list

Write-Host "✅ Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Instrucciones para VS Code:" -ForegroundColor Cyan
Write-Host "  1. Cierra VS Code completamente (Ctrl+Shift+P -> 'Developer: Reload Window')" -ForegroundColor White
Write-Host "  2. Abre el notebook: notebooks/01_Analisis_Emisiones_CO2_Chile.ipynb" -ForegroundColor White
Write-Host "  3. Cuando te pida el kernel, selecciona: 'DS Portfolio (venv_fresh)'" -ForegroundColor White
Write-Host "  4. Si sigue crasheado, ejecuta: Ctrl+Shift+P -> 'Python: Refresh Kernels'" -ForegroundColor White
