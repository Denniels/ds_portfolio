FROM python:3.9-slim-bookworm

WORKDIR /app

# Instalar dependencias del sistema necesarias y actualizar paquetes para mitigar vulnerabilidades
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && apt-get upgrade -y \
    && apt-get dist-upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio de cache si no existe
RUN mkdir -p /app/cache

# Variable de entorno para configurar el puerto (Cloud Run lo establece automáticamente)
ENV PORT 8080

# Variables de entorno para Streamlit
ENV STREAMLIT_SERVER_PORT=$PORT
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Comando para ejecutar la aplicación
CMD streamlit run --server.port=$PORT --server.enableCORS=false --server.enableXsrfProtection=false app/main.py
