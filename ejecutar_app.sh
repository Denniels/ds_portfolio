#!/bin/bash

echo "Iniciando Portafolio de Ciencia de Datos..."
echo ""
echo "La aplicación estará disponible en: http://localhost:8080"
echo ""

# Activar entorno virtual si existe
if [ -d "ds_portfolio_env" ]; then
    source ds_portfolio_env/bin/activate 2>/dev/null || source ds_portfolio_env/Scripts/activate 2>/dev/null
    echo "Entorno virtual activado"
fi

# Ejecutar la aplicación
streamlit run app/main_simplified.py --server.address=127.0.0.1 --server.port=8080
