# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para la compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements.txt primero para aprovechar la cache
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt e instalar dependencias directamente
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app ./app

# Crear directorios necesarios para datos y visualizaciones
RUN mkdir -p ./notebooks/data
RUN mkdir -p ./notebooks/visualizaciones

# Crear archivos de datos vacíos si son necesarios
RUN touch ./notebooks/data/cache_coordenadas_chile.json
RUN touch ./notebooks/data/estaciones_coordenadas.json

# Configuración para producción
ENV PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8080
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Configuración de la cache de streamlit
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

# Verificar la instalación de streamlit
RUN which streamlit || echo "Streamlit no está instalado correctamente"

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "--server.port=8080", "--server.address=0.0.0.0", "app/main.py"]
