# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para la compilación
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements.txt primero para aprovechar la cache
COPY requirements.txt .

# Instalar dependencias en una ubicación específica
RUN pip install --no-cache-dir -r requirements.txt --target=/python-deps

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# Copiar solo las dependencias necesarias del builder
COPY --from=builder /python-deps /usr/local/lib/python3.9/site-packages

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

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "--server.port=8080", "--server.address=0.0.0.0", "app/main.py"]
