import os
import sys
import warnings

# Configurar warnings
warnings.filterwarnings('ignore')

# Asegurar que estamos usando Python 3.9.x
if not (3, 9) <= sys.version_info[:2] < (3, 10):
    raise RuntimeError("Este proyecto requiere Python 3.9.x")

# Configurar variables de entorno
os.environ['PYTHONPATH'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.environ['STREAMLIT_SERVER_PORT'] = "8501"
os.environ['STREAMLIT_SERVER_ADDRESS'] = "0.0.0.0"
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = "false"

# Configurar opciones de pandas para evitar warnings
try:
    import pandas as pd
    pd.options.mode.chained_assignment = None
except ImportError:
    pass

# Configurar numpy para usar threading optimizado
try:
    import numpy as np
    np.set_printoptions(precision=3, suppress=True)
    # Intentar configurar BLAS para un solo thread para evitar problemas de memoria
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1'
except ImportError:
    pass
