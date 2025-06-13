# 🚀 Despliegue del Portafolio de Data Science en Instancia VM de Google Cloud Platform

> **Guía Completa para Despliegue usando Compute Engine y Docker (Junio 2025)**

Esta guía proporciona instrucciones detalladas para desplegar el portafolio completo de Data Science en una instancia de VM de Google Cloud Platform (GCP) utilizando Docker y aprovechando la capa gratuita de GCP.

## 📋 Capa Gratuita de Google Cloud Platform

Google Cloud Platform ofrece una generosa capa gratuita que incluye una instancia VM f1-micro:

- **Instancia e2-micro** (2 vCPU de rendimiento compartido, 1 GB de memoria)
- **30 GB** de almacenamiento estándar HDD
- **1 GB** de transferencia de datos desde Norteamérica a destinos mundiales (excepto China y Australia)
- Válido por **12 meses** o hasta agotar el crédito gratuito de $300

## 🔍 Requisitos Previos

- Cuenta de Google Cloud (puedes registrarte en [cloud.google.com](https://cloud.google.com))
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) instalado localmente
- [Docker](https://www.docker.com/get-started) instalado localmente
- [Git](https://git-scm.com/downloads) instalado localmente

## 🔄 Preparación del Proyecto

### 1. Verificación del Dockerfile

Verifica que el archivo `Dockerfile` en la raíz del proyecto contenga:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Crear directorio de cache si no existe
RUN mkdir -p /app/cache

# Variable de entorno para configurar el puerto
ENV PORT 8501

# Variables de entorno para Streamlit
ENV STREAMLIT_SERVER_PORT=$PORT
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Comando para ejecutar la aplicación
CMD streamlit run app/main.py
```

### 2. Optimización de Requirements.txt

Asegúrate de que tu archivo `requirements.txt` incluya todas las dependencias necesarias, pero sin paquetes innecesarios para mantener la imagen lo más pequeña posible.

### 3. Configuración para el Entorno de Producción

Crea un archivo `.env.production` con las configuraciones específicas para producción:

```
# Variables de entorno para producción
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
CACHE_TTL=3600
```

## 🏗️ Configuración de la Instancia VM

### 1. Crear Proyecto en Google Cloud

```bash
# Iniciar sesión en Google Cloud
gcloud auth login

# Crear un nuevo proyecto (reemplaza YOUR_PROJECT_ID y YOUR_PROJECT_NAME)
gcloud projects create YOUR_PROJECT_ID --name="YOUR_PROJECT_NAME"

# Configurar el proyecto como predeterminado
gcloud config set project YOUR_PROJECT_ID

# Habilitar facturación (necesario incluso para la capa gratuita)
# Esto se hace a través de la consola web de Google Cloud
```

### 2. Crear Instancia VM con Capa Gratuita

```bash
# Habilitar Compute Engine API
gcloud services enable compute.googleapis.com

# Crear instancia e2-micro (capa gratuita)
gcloud compute instances create ds-portfolio \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --subnet=default \
  --network-tier=STANDARD \
  --maintenance-policy=TERMINATE \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-standard \
  --boot-disk-device-name=ds-portfolio \
  --tags=http-server,https-server \
  --scopes=https://www.googleapis.com/auth/cloud-platform
```

### 3. Configurar Reglas de Firewall

```bash
# Permitir tráfico HTTP
gcloud compute firewall-rules create allow-http \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:80,tcp:8501 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=http-server

# Permitir tráfico HTTPS
gcloud compute firewall-rules create allow-https \
  --direction=INGRESS \
  --priority=1000 \
  --network=default \
  --action=ALLOW \
  --rules=tcp:443 \
  --source-ranges=0.0.0.0/0 \
  --target-tags=https-server
```

## 🚢 Despliegue del Proyecto

### 1. Conectarse a la Instancia VM

```bash
# Conectarse mediante SSH
gcloud compute ssh ds-portfolio --zone=us-central1-a
```

### 2. Instalar Docker en la VM

```bash
# Actualizar paquetes
sudo apt-get update

# Instalar dependencias
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Agregar clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Configurar repositorio estable
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Agregar usuario actual al grupo docker
sudo usermod -aG docker $USER
```

### 3. Clonar el Repositorio y Construir la Imagen

```bash
# Cerrar sesión y volver a conectar para aplicar permisos de Docker
exit
gcloud compute ssh ds-portfolio --zone=us-central1-a

# Clonar el repositorio (reemplaza URL_DEL_REPOSITORIO)
git clone URL_DEL_REPOSITORIO ds_portfolio
cd ds_portfolio

# Construir la imagen Docker
docker build -t ds-portfolio:latest .
```

### 4. Ejecutar el Contenedor

```bash
# Ejecutar el contenedor
docker run -d \
  --name ds-portfolio \
  -p 8501:8501 \
  --restart unless-stopped \
  ds-portfolio:latest
```

### 5. Configurar un Proxy Inverso con Nginx (Opcional)

Para servir la aplicación a través del puerto 80 (HTTP) o 443 (HTTPS):

```bash
# Instalar Nginx
sudo apt-get install -y nginx

# Crear configuración de sitio
sudo nano /etc/nginx/sites-available/ds-portfolio

# Añadir configuración
```

Contenido del archivo de configuración:

```nginx
server {
    listen 80;
    server_name YOUR_VM_IP;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Continuar con la configuración:

```bash
# Crear enlace simbólico
sudo ln -s /etc/nginx/sites-available/ds-portfolio /etc/nginx/sites-enabled/

# Probar configuración
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

## 🔧 Optimizaciones para la Capa Gratuita

### 1. Reducir el Uso de Memoria

Para asegurarte de que la aplicación funcione bien con solo 1 GB de RAM:

```bash
# Editar la configuración del contenedor
docker stop ds-portfolio
docker rm ds-portfolio

# Relanzar con límites de memoria
docker run -d \
  --name ds-portfolio \
  -p 8501:8501 \
  --restart unless-stopped \
  --memory="800m" \
  --memory-swap="1g" \
  ds-portfolio:latest
```

### 2. Configurar el Intercambio (Swap)

```bash
# Crear archivo swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Hacer el swap permanente
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 3. Implementar Servicio Systemd (Alternativa a Docker)

Para un mejor control de los recursos, puedes usar systemd en lugar de Docker:

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Crear servicio systemd
sudo nano /etc/systemd/system/ds-portfolio.service
```

Contenido del archivo de servicio:

```ini
[Unit]
Description=Data Science Portfolio
After=network.target

[Service]
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/ds_portfolio
ExecStart=/home/YOUR_USERNAME/ds_portfolio/venv/bin/streamlit run app/main.py
Restart=always
RestartSec=5
SyslogIdentifier=ds-portfolio
Environment="STREAMLIT_SERVER_PORT=8501"
Environment="STREAMLIT_SERVER_HEADLESS=true"

[Install]
WantedBy=multi-user.target
```

Activar el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ds-portfolio
sudo systemctl start ds-portfolio
```

## 📈 Monitoreo y Mantenimiento

### 1. Monitoreo de Recursos

```bash
# Instalar herramientas de monitoreo
sudo apt-get install -y htop glances

# Monitorear en tiempo real
htop
```

### 2. Configurar Registro de Logs

```bash
# Ver logs de Docker
docker logs ds-portfolio

# Ver logs continuamente
docker logs -f ds-portfolio

# Ver logs del servicio systemd
sudo journalctl -u ds-portfolio -f
```

### 3. Automatizar Actualizaciones

Crea un script para actualizar automáticamente la aplicación:

```bash
# Crear script de actualización
nano ~/update-portfolio.sh
```

Contenido del script:

```bash
#!/bin/bash
cd ~/ds_portfolio
git pull
docker build -t ds-portfolio:latest .
docker stop ds-portfolio
docker rm ds-portfolio
docker run -d \
  --name ds-portfolio \
  -p 8501:8501 \
  --restart unless-stopped \
  --memory="800m" \
  ds-portfolio:latest
```

Hacer el script ejecutable:

```bash
chmod +x ~/update-portfolio.sh
```

### 4. Programar Respaldos

```bash
# Crear script de respaldo
nano ~/backup-portfolio.sh
```

Contenido del script:

```bash
#!/bin/bash
BACKUP_DIR=~/backups
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +%Y%m%d%H%M%S)
cd ~/ds_portfolio
tar -czf $BACKUP_DIR/ds_portfolio_$TIMESTAMP.tar.gz .
# Mantener solo los últimos 5 respaldos
ls -tp $BACKUP_DIR/*.tar.gz | grep -v '/$' | tail -n +6 | xargs -I {} rm -- {}
```

Hacer el script ejecutable y programarlo:

```bash
chmod +x ~/backup-portfolio.sh
(crontab -l 2>/dev/null; echo "0 2 * * * ~/backup-portfolio.sh") | crontab -
```

## 🔒 Configuración de HTTPS con Let's Encrypt (Opcional)

Si tienes un dominio apuntando a tu instancia:

```bash
# Instalar Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tu-dominio.com

# Renovación automática
sudo certbot renew --dry-run
```

## 🚨 Solución de Problemas Comunes

### 1. Falta de Memoria

Si la aplicación falla por falta de memoria:

```bash
# Verificar uso de memoria
free -h

# Ajustar límites de memoria del contenedor
docker update --memory="700m" --memory-swap="1g" ds-portfolio
```

### 2. Problemas de Conexión

Si no puedes acceder a la aplicación:

```bash
# Verificar que el contenedor está ejecutándose
docker ps

# Verificar que la aplicación está respondiendo localmente
curl http://localhost:8501

# Verificar reglas de firewall
sudo iptables -L
```

### 3. Problemas de Disco

Si te quedas sin espacio en disco:

```bash
# Verificar espacio en disco
df -h

# Limpiar imágenes y contenedores no utilizados
docker system prune -a

# Eliminar archivos temporales
sudo find /tmp -type f -atime +10 -delete
```

## 📝 Consejos de Optimización Adicionales

1. **Modo de Solo Lectura**: Para ahorrar en operaciones de escritura y mejorar el rendimiento, monta algunos directorios en modo de solo lectura.

2. **Optimización de Base de Datos**: Si usas una base de datos SQLite, colócala en un volumen de memoria para operaciones más rápidas (pero recuerda hacer respaldos).

3. **Caché Agresivo**: Implementa estrategias de caché agresivas para reducir el uso de CPU.

4. **Precargar Datos**: Carga datos frecuentemente utilizados durante el inicio para mejorar la experiencia del usuario.

5. **Comprimir Respuestas**: Configura Nginx para comprimir respuestas y reducir el ancho de banda.

## 🌐 Dirección IP Estática (Opcional)

Para mantener la misma IP incluso después de reiniciar la instancia:

```bash
# Reservar una dirección IP estática
gcloud compute addresses create ds-portfolio-ip --region=us-central1

# Obtener la IP reservada
gcloud compute addresses describe ds-portfolio-ip --region=us-central1

# Asignar la IP estática a la instancia
gcloud compute instances delete ds-portfolio --zone=us-central1-a
gcloud compute instances create ds-portfolio \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --address=IP_RESERVADA \
  ... (resto de parámetros como antes)
```

## 📚 Recursos Adicionales

- [Documentación de Google Cloud Compute Engine](https://cloud.google.com/compute/docs)
- [Mejores prácticas para Docker en producción](https://docs.docker.com/engine/security/security/)
- [Documentación de Streamlit para despliegue](https://docs.streamlit.io/knowledge-base/deploy)
- [Optimización de Python para entornos con recursos limitados](https://pythonspeed.com/memory/)

---

Con esta guía detallada, podrás desplegar tu portafolio completo de Data Science en una instancia VM de Google Cloud Platform, aprovechando al máximo la capa gratuita mientras mantienes un servicio robusto, seguro y escalable.
