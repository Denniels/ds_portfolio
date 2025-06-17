# 🚀 Guía de Despliegue - Streamlit Cloud

**Fecha:** 17 de junio de 2025  
**Versión:** 2.1 - Con datos reales CO2

---

## 📋 Checklist Pre-Despliegue

### ✅ **Requisitos Completados:**
- [x] **Pipeline CO2 conectado** con datos reales del RETC 2023
- [x] **Archivos JSON generados** en `app/data/cache/`
- [x] **Aplicación funcionando** localmente
- [x] **Dependencias optimizadas** para Streamlit Cloud
- [x] **Estructura de archivos** correcta

---

## 🎯 Pasos para Despliegue en Streamlit Cloud

### 1. **Preparación del Repositorio**

#### A. Generar Datos CO2 (CRÍTICO)
```bash
# 1. Ejecutar el notebook para generar datos reales
cd notebooks
jupyter notebook 01_Analisis_Emisiones_CO2_Chile.ipynb

# 2. Ejecutar TODAS las celdas para generar:
# - app/data/cache/emisiones_anuales.json
# - app/data/cache/emisiones_regionales.json  
# - app/data/cache/cache_metadata.json
# - app/data/cache/maps/*.geojson
```

#### B. Verificar Archivos Generados
```bash
# Verificar que existen los archivos necesarios
ls app/data/cache/
# Debe mostrar:
# ✅ emisiones_anuales.json
# ✅ emisiones_regionales.json
# ✅ cache_metadata.json
# ✅ maps/
```

#### C. Commit y Push
```bash
git add .
git commit -m "feat: add real CO2 data for Streamlit Cloud deployment"
git push origin main
```

### 2. **Configuración en Streamlit Cloud**

#### A. Acceder a Streamlit Cloud
1. Ir a [share.streamlit.io](https://share.streamlit.io)
2. Conectar con tu cuenta de GitHub
3. Dar permisos de acceso al repositorio

#### B. Crear Nueva App
```yaml
# Configuración recomendada:
Repository: tu-usuario/ds_portfolio
Branch: main
Main file path: app/main.py
Python version: 3.11
```

#### C. Variables de Entorno (Opcional)
```bash
# En Advanced settings, agregar si es necesario:
# No se requieren variables especiales para esta app
```

### 3. **Verificación Post-Despliegue**

#### A. Verificar Funcionalidad
- [ ] **Página principal** carga correctamente
- [ ] **Navegación** entre páginas funciona
- [ ] **Análisis CO2** muestra datos reales (15.0 Mt CO₂)
- [ ] **Mapas interactivos** se renderizan
- [ ] **Gráficos** se cargan correctamente

#### B. Verificar Datos CO2
- [ ] **Región Metropolitana**: 7.5 Mt CO₂ (49.9%)
- [ ] **16 regiones** listadas en tabla
- [ ] **Mapa de Chile** con coordenadas reales
- [ ] **Metadata** muestra fecha de generación

---

## 🔧 Configuración Avanzada

### Archivo .streamlit/config.toml
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false

[browser]
gatherUsageStats = false
```

### requirements.txt Optimizado
```txt
streamlit==1.45.0
pandas==2.3.0
plotly==5.24.1
folium==0.17.0
streamlit-folium==0.22.0
numpy==1.26.4
psutil==6.0.0
python-dateutil==2.9.0
cachetools==5.5.0
```

---

## ⚠️ Solución de Problemas Comunes

### Problema 1: Error "File not found" para archivos JSON
**Síntoma:** La app muestra error al cargar datos CO2

**Solución:**
```bash
# 1. Verificar que el notebook se ejecutó completamente
cd notebooks
jupyter notebook 01_Analisis_Emisiones_CO2_Chile.ipynb

# 2. Verificar que se generaron los archivos
ls -la app/data/cache/

# 3. Commit y push los archivos
git add app/data/cache/
git commit -m "add: CO2 data files for production"
git push
```

### Problema 2: App muy lenta en Streamlit Cloud
**Síntoma:** Carga lenta o timeouts

**Solución:**
- Los archivos JSON están optimizados (~50KB total)
- Verificar que no hay archivos grandes en el repo
- El sistema de caché de Streamlit manejará el rendimiento

### Problema 3: Mapas no se renderizan
**Síntoma:** Área en blanco donde debería estar el mapa

**Solución:**
```python
# Verificar que folium está importado correctamente
import folium
import streamlit.components.v1 as components

# El mapa se renderiza con:
components.html(mapa._repr_html_(), height=500)
```

---

## 📊 Métricas de Rendimiento Esperadas

### Streamlit Cloud (Esperado)
- **Tiempo de inicio:** 15-30 segundos
- **Carga de página CO2:** 3-5 segundos  
- **Navegación:** 1-2 segundos
- **Memoria utilizada:** 200-400 MB
- **Ancho de banda:** ~50KB datos + assets

### Comparación con Local
| Métrica | Local | Streamlit Cloud |
|---------|-------|-----------------|
| Inicio | 10-15s | 20-30s |
| Navegación | 1s | 1-2s |
| Mapas | 2-3s | 3-5s |
| Memoria | 200MB | 300-400MB |

---

## 🎉 Post-Despliegue

### Verificación Final
Una vez desplegado, verificar estos elementos:

#### ✅ Funcionalidad Básica
- [ ] URL de la app funciona
- [ ] Todas las páginas cargan
- [ ] No hay errores en la consola

#### ✅ Datos CO2 Correctos
- [ ] Total emisiones: **15.0 Mt CO₂** (no 85.2 Mt)
- [ ] Región líder: **Metropolitana** (7.5 Mt CO₂)
- [ ] Número de regiones: **16**
- [ ] Fuente: **RETC 2023**

#### ✅ Visualizaciones
- [ ] Gráfico de barras por región
- [ ] Mapa interactivo de Chile
- [ ] Tabla de datos ordenada
- [ ] Metadata del análisis

### Compartir la App
```markdown
🎉 ¡App desplegada exitosamente!
📊 URL: https://tu-app.streamlit.app
🏭 Análisis CO2 con datos reales del RETC 2023
🇨🇱 15+ Mt CO₂ analizados de Chile
```

---

## 📞 Soporte

Si encuentras problemas durante el despliegue:

1. **Revisar logs** en Streamlit Cloud
2. **Verificar archivos** JSON en el repositorio
3. **Comprobar estructura** de carpetas
4. **Contactar soporte** de Streamlit si es necesario

---

**Última actualización:** 17 de junio de 2025  
**Estado:** ✅ Listo para despliegue con datos reales
