@echo off
echo Iniciando Portafolio de Ciencia de Datos...
echo.
echo La aplicacion estara disponible en: http://localhost:8080
echo.
cd /d "%~dp0"
streamlit run app/main_simplified.py --server.address=127.0.0.1 --server.port=8080
pause
