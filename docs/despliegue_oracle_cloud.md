# Guía de Despliegue en Oracle Cloud Free Tier

Este documento proporciona instrucciones detalladas para desplegar la aplicación de Análisis de Emisiones RETC Chile en Oracle Cloud Free Tier, aprovechando los recursos gratuitos que ofrece.

## Índice

1. [Características de Oracle Cloud Free Tier](#características-de-oracle-cloud-free-tier)
2. [Requisitos Previos](#requisitos-previos)
3. [Crear una Cuenta en Oracle Cloud](#crear-una-cuenta-en-oracle-cloud)
4. [Configuración de la Instancia VM](#configuración-de-la-instancia-vm)
5. [Configuración del Entorno en la VM](#configuración-del-entorno-en-la-vm)
6. [Despliegue de la Aplicación Streamlit](#despliegue-de-la-aplicación-streamlit)
7. [Configuración de Acceso Externo](#configuración-de-acceso-externo)
8. [Monitoreo y Mantenimiento](#monitoreo-y-mantenimiento)
9. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
10. [Optimizaciones Adicionales](#optimizaciones-adicionales)

## Características de Oracle Cloud Free Tier

Oracle Cloud Free Tier ofrece recursos gratuitos permanentes, lo que lo hace ideal para nuestro caso de uso:

- **2 VM.Standard.A1.Flex** (procesador ARM) con hasta:
  - 4 OCPU (Oracle CPU) en total
  - 24 GB de RAM en total
  - Puedes distribuir estos recursos en hasta 2 VMs (por ejemplo, 1 VM con 2 OCPU y 12 GB RAM, o 2 VMs con distinta configuración)
- **200 GB** de almacenamiento en bloque
- **10 TB** de transferencia de datos de salida por mes
- **2 bases de datos** Autonomous Database (1 OCPU y 20 GB cada una)
- Recursos adicionales como balanceadores de carga, almacenamiento de objetos, etc.

> **Nota importante**: Los recursos gratuitos son permanentes (no tienen fecha de expiración) siempre que mantengas activa la cuenta.

## Requisitos Previos

Antes de comenzar, asegúrate de tener:

- Una tarjeta de crédito/débito válida (necesaria para la verificación, pero no se realizarán cargos)
- Un número de teléfono móvil para verificación
- Una dirección de correo electrónico
- Nuestro código fuente de la aplicación de Análisis de Emisiones RETC Chile listo para desplegar

## Crear una Cuenta en Oracle Cloud

1. Visita [https://www.oracle.com/cloud/free/](https://www.oracle.com/cloud/free/)

2. Haz clic en "Empezar gratis"

3. Completa el formulario de registro con tus datos personales:
   - Dirección de correo electrónico
   - Nombre y apellido
   - País/territorio
   - Número de teléfono

4. Verifica tu correo electrónico con el código recibido

5. Continúa el proceso de registro:
   - Información de la compañía (puedes poner personal si es un proyecto individual)
   - Dirección completa
   - Información de la tarjeta de crédito (para verificación)
   - Información de verificación de teléfono móvil

6. Elige una región cercana a Chile para mejor rendimiento:
   - Se recomienda **Brazil East (Sao Paulo)** o **Chile Central (Santiago)** si está disponible

7. Establece una contraseña segura para tu cuenta

8. Espera a que se aprovisione tu cuenta (puede tardar unos minutos)

## Configuración de la Instancia VM

### Crear la instancia VM:

1. Inicia sesión en la [consola de Oracle Cloud](https://cloud.oracle.com/)

2. En el menú hamburguesa (≡), navega a **Compute** > **Instances**

3. Haz clic en **Create instance**

4. Configura la instancia:
   - **Name**: `retc-analysis-app` (o un nombre descriptivo)
   - **Compartment**: Elige tu compartment (por defecto es "root")
   - **Availability Domain**: Mantén el valor predeterminado
   - **Image and shape**: Haz clic en **Edit**
     - Selecciona **Oracle Linux 8**
     - En la sección **Shape**, elige **Ampere** (procesador ARM)
     - Selecciona **VM.Standard.A1.Flex**
     - Configura **OCPUs**: `2` (para aplicación con datos completos)
     - Configura **Memory**: `12` GB (suficiente para el conjunto completo de datos)
     - Haz clic en **Select shape**

5. Configura las opciones de red:
   - Crea una nueva VCN (Virtual Cloud Network) o utiliza una existente
   - Asegúrate de que el **Subnet** esté configurado
   - Marca la casilla **Assign a public IPv4 address**

6. Configura las opciones de SSH:
   - Opción 1: **Generate a key pair for me** (Oracle generará las claves y deberás descargarlas)
   - Opción 2: **Upload public key files (.pub)** (si ya tienes claves SSH)
   - Opción 3: **Paste public keys** (copia y pega tu clave pública)

   > **Importante**: Guarda las claves privadas en un lugar seguro. Las necesitarás para conectarte a la VM.

7. Revisa y crea la instancia haciendo clic en **Create**

8. Espera a que se aprovisione la instancia (aproximadamente 2-5 minutos)

### Configurar Firewall y Reglas de Seguridad:

1. Una vez creada la instancia, navega a su página de detalles

2. En la sección **Primary VNIC**, haz clic en el nombre de la **Subnet**

3. Haz clic en la **Security List** asociada a tu subnet

4. Haz clic en **Add Ingress Rules** y añade las siguientes reglas:
   - Para acceso SSH:
     - **Source CIDR**: `0.0.0.0/0` (o limita a tu IP para mayor seguridad)
     - **IP Protocol**: `TCP`
     - **Destination Port Range**: `22`
   - Para acceso a la aplicación Streamlit:
     - **Source CIDR**: `0.0.0.0/0`
     - **IP Protocol**: `TCP`
     - **Destination Port Range**: `8501` (puerto predeterminado de Streamlit)
   - Para acceso web (opcional, si planeas configurar Nginx):
     - **Source CIDR**: `0.0.0.0/0`
     - **IP Protocol**: `TCP`
     - **Destination Port Range**: `80,443`

5. Haz clic en **Add Ingress Rules** para guardar las reglas

## Configuración del Entorno en la VM

### Conectarse a la instancia:

**Para usuarios de Windows:**

1. Abre PowerShell o una terminal compatible con SSH

2. Navega a la carpeta donde guardaste la clave privada

3. Establece los permisos adecuados para la clave privada:
   ```powershell
   icacls <ruta-a-tu-clave-privada>.key /inheritance:r /grant:r "$($env:USERNAME):(R)"
   ```

4. Conéctate a la instancia:
   ```powershell
   ssh -i <ruta-a-tu-clave-privada>.key opc@<dirección-IP-pública>
   ```
   > La IP pública se muestra en la página de detalles de la instancia

**Para usuarios de Linux/macOS:**

1. Abre una terminal

2. Establece los permisos adecuados para la clave privada:
   ```bash
   chmod 400 <ruta-a-tu-clave-privada>.key
   ```

3. Conéctate a la instancia:
   ```bash
   ssh -i <ruta-a-tu-clave-privada>.key opc@<dirección-IP-pública>
   ```

### Actualizar el sistema e instalar dependencias:

1. Una vez conectado, actualiza el sistema:
   ```bash
   sudo dnf update -y
   ```

2. Instala dependencias básicas:
   ```bash
   sudo dnf install -y git wget curl python39 python39-devel gcc gcc-c++ make openssl-devel bzip2-devel libffi-devel zlib-devel
   ```

3. Instala Docker y Docker Compose:
   ```bash
   # Instalar Docker
   sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
   sudo dnf install -y docker-ce docker-ce-cli containerd.io
   sudo systemctl enable docker
   sudo systemctl start docker
   
   # Añadir usuario actual al grupo docker
   sudo usermod -aG docker $USER
   
   # Instalar Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/v2.18.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

4. Para que los cambios de grupo surtan efecto, cierra la sesión y vuelve a conectarte:
   ```bash
   exit
   # Vuelve a conectarte con SSH como en los pasos anteriores
   ```

## Despliegue de la Aplicación Streamlit

### Clonar el repositorio:

1. Clona tu repositorio (asumiendo que tienes un repositorio en GitHub):
   ```bash
   mkdir -p ~/projects
   cd ~/projects
   git clone https://github.com/tu-usuario/ds_portfolio.git
   cd ds_portfolio
   ```

   Si tu repositorio es privado, necesitarás configurar tus credenciales de GitHub:
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu.email@example.com"
   ```
   
   Y luego clonar usando HTTPS con tus credenciales o configurar una clave SSH.

### Opción 1: Despliegue usando Docker Compose (recomendado):

1. Navega a la carpeta de Docker:
   ```bash
   cd docker
   ```

2. Verifica el archivo `docker-compose.yml`:
   ```bash
   cat docker-compose.yml
   ```

3. Si es necesario, ajusta los volúmenes y puertos en el archivo `docker-compose.yml` para que coincidan con la estructura de tu proyecto.

4. Inicia los contenedores:
   ```bash
   docker-compose up -d
   ```

5. Verifica que los contenedores estén funcionando:
   ```bash
   docker-compose ps
   ```

### Opción 2: Instalación directa (sin Docker):

Si prefieres no usar Docker, puedes instalar directamente en la VM:

1. Navega a la carpeta del proyecto:
   ```bash
   cd ~/projects/ds_portfolio
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación Streamlit:
   ```bash
   cd app
   streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
   ```

5. Para mantener la aplicación funcionando en segundo plano, puedes usar `nohup` o configurar un servicio systemd.

## Configuración de Acceso Externo

### Configuración básica (acceso directo a Streamlit):

Streamlit estará disponible en `http://<dirección-IP-pública>:8501`

### Configuración avanzada con Nginx (recomendado para producción):

1. Instala Nginx:
   ```bash
   sudo dnf install -y nginx
   ```

2. Configura Nginx como proxy inverso para Streamlit:
   ```bash
   sudo nano /etc/nginx/conf.d/streamlit.conf
   ```

3. Añade la siguiente configuración:
   ```nginx
   server {
       listen 80;
       server_name <dirección-IP-pública> tu-dominio.com;  # Añade tu dominio si tienes uno
   
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

4. Guarda el archivo (Ctrl+O, Enter, Ctrl+X en nano)

5. Verifica la configuración de Nginx:
   ```bash
   sudo nginx -t
   ```

6. Inicia y habilita Nginx:
   ```bash
   sudo systemctl enable nginx
   sudo systemctl start nginx
   ```

7. Configura firewalld para permitir tráfico HTTP/HTTPS:
   ```bash
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --permanent --add-service=https
   sudo firewall-cmd --reload
   ```

### Configuración de HTTPS con Let's Encrypt (opcional):

Si tienes un nombre de dominio apuntando a tu instancia, puedes configurar HTTPS gratuitamente:

1. Instala Certbot:
   ```bash
   sudo dnf install -y epel-release
   sudo dnf install -y certbot python3-certbot-nginx
   ```

2. Obtén un certificado:
   ```bash
   sudo certbot --nginx -d tu-dominio.com
   ```

3. Sigue las instrucciones en pantalla para completar la configuración.

## Monitoreo y Mantenimiento

### Configurar servicio systemd para Streamlit (para instalación directa):

1. Crea un archivo de servicio systemd:
   ```bash
   sudo nano /etc/systemd/system/streamlit.service
   ```

2. Añade la siguiente configuración:
   ```ini
   [Unit]
   Description=Streamlit Application Service
   After=network.target
   
   [Service]
   User=opc
   WorkingDirectory=/home/opc/projects/ds_portfolio/app
   ExecStart=/home/opc/projects/ds_portfolio/venv/bin/streamlit run Home.py --server.port=8501 --server.address=0.0.0.0
   Restart=on-failure
   RestartSec=5s
   
   [Install]
   WantedBy=multi-user.target
   ```

3. Habilita e inicia el servicio:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   ```

4. Verifica el estado del servicio:
   ```bash
   sudo systemctl status streamlit
   ```

### Monitoreo de recursos:

1. Instala herramientas de monitoreo:
   ```bash
   sudo dnf install -y htop glances
   ```

2. Monitorea el uso de recursos:
   ```bash
   htop
   ```
   o
   ```bash
   glances
   ```

3. Monitorea los logs de Streamlit:
   Si usas Docker:
   ```bash
   docker-compose logs -f
   ```
   
   Si usas systemd:
   ```bash
   sudo journalctl -u streamlit -f
   ```

### Configuración de backup:

1. Crea un script de backup:
   ```bash
   mkdir -p ~/backups
   nano ~/backup_data.sh
   ```

2. Añade el siguiente contenido:
   ```bash
   #!/bin/bash
   TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
   BACKUP_DIR=~/backups
   
   # Backup de los datos
   tar -czf $BACKUP_DIR/retc_data_$TIMESTAMP.tar.gz ~/projects/ds_portfolio/data
   
   # Mantener solo los 5 backups más recientes
   ls -t $BACKUP_DIR/retc_data_*.tar.gz | tail -n +6 | xargs -r rm
   
   echo "Backup completado: $BACKUP_DIR/retc_data_$TIMESTAMP.tar.gz"
   ```

3. Haz el script ejecutable:
   ```bash
   chmod +x ~/backup_data.sh
   ```

4. Configura un cron job para ejecutar backups regulares:
   ```bash
   crontab -e
   ```
   
   Añade la siguiente línea para un backup diario a la 1 AM:
   ```
   0 1 * * * ~/backup_data.sh >> ~/backup.log 2>&1
   ```

## Solución de Problemas Comunes

### Problemas de conexión:

1. Verifica que las reglas de firewall permitan el tráfico:
   ```bash
   sudo firewall-cmd --list-all
   ```

2. Verifica que las reglas de ingreso de Oracle Cloud estén configuradas correctamente en la consola web.

3. Si no puedes conectarte por SSH, verifica:
   - La IP pública es correcta
   - La clave privada es la correcta
   - Los permisos de la clave privada son adecuados

### Problemas con Docker:

1. Si Docker no inicia:
   ```bash
   sudo systemctl status docker
   ```

2. Verifica los logs:
   ```bash
   sudo journalctl -u docker
   ```

3. Reinicia Docker:
   ```bash
   sudo systemctl restart docker
   ```

### Problemas con la aplicación Streamlit:

1. Verifica los logs de la aplicación.

2. Comprueba si hay errores relacionados con la memoria:
   ```bash
   free -h
   ```

3. Verifica el uso del CPU:
   ```bash
   top
   ```

4. Si la aplicación se cuelga, reiníciala:
   Con Docker:
   ```bash
   docker-compose restart
   ```
   
   Con systemd:
   ```bash
   sudo systemctl restart streamlit
   ```

## Optimizaciones Adicionales

### Optimización de memoria:

1. Ajusta la configuración de memoria virtual (swap):
   ```bash
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
   ```

2. Ajusta el comportamiento de la memoria del sistema:
   ```bash
   sudo sysctl -w vm.swappiness=10
   echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
   ```

### Optimización de rendimiento:

1. Si estás utilizando Oracle Linux con kernel UEK, puedes optimizar el rendimiento del kernel:
   ```bash
   sudo grubby --update-kernel=ALL --args="transparent_hugepage=madvise"
   ```

2. Reinicia el sistema para aplicar los cambios:
   ```bash
   sudo reboot
   ```

### Implementación de caché para los datos:

1. Instala Redis para caché de datos:
   ```bash
   sudo dnf install -y redis
   sudo systemctl enable redis
   sudo systemctl start redis
   ```

2. Ajusta tu aplicación para utilizar Redis como caché (esto requeriría modificaciones en el código).

---

## Conclusión

Esta guía te ha proporcionado los pasos detallados para desplegar tu aplicación de Análisis de Emisiones RETC Chile en Oracle Cloud Free Tier. Con los recursos gratuitos que ofrece Oracle Cloud (hasta 24 GB de RAM y 4 OCPU), deberías poder ejecutar tu aplicación con el conjunto completo de datos sin problemas de memoria.

Recuerda monitorear regularmente el uso de recursos y realizar backups periódicos de tus datos importantes.

Para cualquier problema que no esté cubierto en la sección de solución de problemas, consulta la [documentación oficial de Oracle Cloud](https://docs.oracle.com/en-us/iaas/Content/home.htm).
