#!/bin/bash
# Script para configurar el entorno de notebooks correctamente

echo "🔧 Configurando entorno de notebooks..."

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source .\.venv_fresh\Scripts\Activate.ps1

# Verificar Python
echo "🐍 Verificando Python..."
python --version
python -c "import sys; print('Ejecutable:', sys.executable)"

# Verificar dependencias críticas
echo "📚 Verificando dependencias..."
python -c "
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
"

# Limpiar kernels anteriores
echo "🧹 Limpiando kernels anteriores..."
python -m jupyter kernelspec remove .venv_fresh -f 2>/dev/null || true

# Recrear kernel
echo "🎯 Creando nuevo kernel..."
python -m ipykernel install --user --name=venv_fresh_ds --display-name="DS Portfolio (venv_fresh)"

# Verificar kernel
echo "📋 Kernels disponibles:"
python -m jupyter kernelspec list

echo "✅ Configuración completada!"
echo ""
echo "📝 Instrucciones para VS Code:"
echo "  1. Reinicia VS Code completamente"
echo "  2. Abre el notebook: notebooks/01_Analisis_Emisiones_CO2_Chile.ipynb"
echo "  3. Selecciona el kernel: 'DS Portfolio (venv_fresh)'"
echo "  4. Si sigue sin funcionar, usa 'Python: Reload Interpreter' en VS Code"
