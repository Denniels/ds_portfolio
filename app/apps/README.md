# 📊 Aplicaciones del Portafolio de Data Science

> **Actualización**: Junio 2025 - Mejoras significativas en la aplicación de análisis presupuestario

## 🚀 Aplicaciones Disponibles

Esta carpeta contiene las aplicaciones interactivas que componen el portafolio de Data Science, cada una enfocada en un área específica de análisis de datos gubernamentales, ambientales o demográficos.

### 💰 Análisis del Presupuesto Público (v2.0)
**Archivo**: `budget_analysis_app_v2.py`

**📋 Descripción**: Análisis interactivo y detallado del Presupuesto del Sector Público de Chile con visualizaciones avanzadas y análisis contextual.

**✨ Características**:
- Análisis jerárquico por niveles (Partidas, Capítulos, Programas, Subtítulos)
- Curvas de Lorenz para análisis de desigualdad en la distribución
- Métricas de concentración (Índice HHI, % Top 3, % Top 10)
- Simulación de evolución temporal de asignaciones presupuestarias
- Explicaciones contextuales para cada nivel jerárquico
- Exportación de datos en formato CSV
- Interfaz moderna con diseño responsivo
- Sistema optimizado de caché para mejor rendimiento

**🔄 Mejoras (Junio 2025)**:
- Refactorización completa de la arquitectura de la aplicación
- Nuevas visualizaciones (curvas de Lorenz, simulación temporal)
- Métricas avanzadas de concentración presupuestaria
- Optimización de rendimiento y sistema de caché
- Interfaz renovada con explicaciones contextuales
- Funcionalidad de exportación de datos

### 💧 Análisis de Calidad del Agua
**Archivo**: `water_quality_app.py`

**📋 Descripción**: Análisis comprehensivo de la calidad del agua en Chile basado en datos de la DGA.

**✨ Características**:
- Mapa interactivo de estaciones de monitoreo
- Análisis temporal de parámetros de calidad
- Evaluación según estándares internacionales
- Sistema de geocodificación con caché inteligente

### 🏭 Emisiones CO2 Chile
**Archivo**: `co2_emissions_app.py`

**📋 Descripción**: Análisis de emisiones de gases de efecto invernadero en Chile.

**✨ Características**:
- Análisis regional y sectorial
- Visualizaciones interactivas por tipo de fuente
- Datos oficiales del RETC 2023
- Métricas comparativas y tendencias

### 👤 Análisis Demográfico
**Archivo**: `demographics_app.py`

**📋 Descripción**: Análisis de tendencias demográficas utilizando BigQuery.

**✨ Características**:
- Análisis de nombres en EE.UU. (1910-2013)
- Tendencias por género y década
- Integración con Google Cloud
- Visualizaciones exportables

## 🧩 Módulos Compartidos

Los módulos reutilizables y componentes compartidos se encuentran en la carpeta `modules/`. Estos incluyen:

- **Configuraciones**: Parámetros globales y constantes
- **Utilidades**: Funciones auxiliares reutilizables
- **Componentes de UI**: Elementos de interfaz compartidos

## 🔄 Integración con Notebooks

Cada aplicación tiene su correspondiente notebook de desarrollo en la carpeta `/notebooks/` que sirve como laboratorio de prototipado antes de la integración con el portafolio.

## 📋 Convenciones de Código

- **Docstrings**: Todas las funciones y clases incluyen documentación
- **Type Hints**: Uso de anotaciones de tipo para mejor mantenibilidad
- **Modularidad**: Separación de lógica de negocio y presentación
- **Caché**: Optimización de rendimiento con decoradores de caché

## 🚀 Despliegue de las Aplicaciones

Las aplicaciones de este portafolio están diseñadas para ser desplegadas en diferentes entornos:

### 🔄 Entorno de Desarrollo Local
- Ejecutar con `streamlit run app/main.py` desde la raíz del proyecto
- Acceder desde `http://localhost:8501`

### 🐳 Despliegue con Docker
- Contenedor único con todas las aplicaciones
- Configurado para entornos de producción
- Optimizado para rendimiento y seguridad

### ☁️ Opciones de Despliegue en la Nube
- **Google Cloud Run**: Servicio serverless para contenedores
- **Google Compute Engine**: VM con capa gratuita (e2-micro)
- **GitHub Pages**: Documentación y visualizaciones estáticas exportadas

### 📝 Consideraciones para Producción
- Ajuste de cachés para optimizar rendimiento
- Manejo seguro de credenciales con variables de entorno
- Configuración de seguridad y HTTPS

Para instrucciones detalladas sobre cada opción de despliegue, consulta las guías en la carpeta `/docs/`.
