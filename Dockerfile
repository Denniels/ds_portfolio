FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación y datos necesarios
COPY ./app ./app
COPY ./notebooks/data ./notebooks/data

# Crear directorio para visualizaciones
RUN mkdir -p ./notebooks/visualizaciones

# Configuración para producción
ENV PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_PORT=8080

# Comando para ejecutar la aplicación
CMD ["streamlit", "run", "--server.port=8080", "--server.address=0.0.0.0", "app/main.py"]
