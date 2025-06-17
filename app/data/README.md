# 📊 Datos del Portafolio - README

**Última actualización:** 17 de junio de 2025

---

## 📁 Estructura de Datos

### `/cache/` - Datos Procesados (CRÍTICO PARA CO2)
```
cache/
├── ✅ emisiones_anuales.json       # Emisiones totales por año (RETC 2023)
├── ✅ emisiones_regionales.json    # Datos por región (16 regiones)
├── ✅ cache_metadata.json          # Metadatos del análisis CO2
└── maps/
    ├── ✅ regiones_chile_simplificadas.geojson
    └── ✅ regiones_chile_mobile.geojson
```

### `/static/` - Archivos Estáticos
```
static/
└── maps/                           # Mapas adicionales y recursos
```

### `/feedback/` - Sistema de Comentarios
```
feedback/
└── comments.json                   # Comentarios de usuarios
```

---

## 🎯 Archivos Críticos para Despliegue

### ⚠️ **IMPORTANTE:** Archivos JSON CO2

Los siguientes archivos son **OBLIGATORIOS** para que la página de análisis CO2 funcione:

#### 1. `emisiones_anuales.json`
```json
{
  "2023": 14994273.802618055
}
```
- **Propósito:** Total de emisiones por año
- **Tamaño:** ~50 bytes
- **Generado por:** Notebook `01_Analisis_Emisiones_CO2_Chile.ipynb`

#### 2. `emisiones_regionales.json`
```json
{
  "Antofagasta": {
    "lat": -21.458455733051906,
    "lon": -68.31522941169325,
    "emisiones": 567726.127816722,
    "region_original": "Antofagasta"
  },
  ...
}
```
- **Propósito:** Datos por región (16 regiones)
- **Tamaño:** ~3KB
- **Generado por:** Notebook `01_Analisis_Emisiones_CO2_Chile.ipynb`

#### 3. `cache_metadata.json`
```json
{
  "generado_en": "2025-06-17T13:03:28.846296",
  "version": "2.0",
  "estadisticas": {
    "total_regiones": 16,
    "total_emisiones_ton": 14994273.8,
    "total_instalaciones": 50,
    "region_mayor_emision": {
      "nombre": "Metropolitana",
      "emisiones": 7479605.55
    }
  }
}
```
- **Propósito:** Metadatos y estadísticas del análisis
- **Tamaño:** ~2KB
- **Generado por:** Notebook `01_Analisis_Emisiones_CO2_Chile.ipynb`

---

## 🔄 Generación de Datos

### Cómo Generar los Archivos JSON

#### 1. Ejecutar el Notebook
```bash
cd notebooks
jupyter notebook 01_Analisis_Emisiones_CO2_Chile.ipynb
```

#### 2. Ejecutar Todas las Celdas
- El notebook debe ejecutarse **completamente**
- Las últimas celdas generan los archivos JSON
- Los archivos se guardan automáticamente en `app/data/cache/`

#### 3. Verificar Archivos Generados
```bash
# Verificar que se crearon los archivos
ls -la app/data/cache/
# Debe mostrar todos los archivos JSON con tamaños > 0 bytes
```

---

## 📈 Fuentes de Datos

### Análisis CO2 - Datos Oficiales
- **Fuente:** Registro de Emisiones y Transferencias de Contaminantes (RETC)
- **Año:** 2023
- **Organismo:** Ministerio del Medio Ambiente, Chile
- **Datasets originales:**
  - `ruea-efd-2023-ckan.csv` (Emisiones Fugitivas Difusas)
  - `ruea-efp-2023-ckan.csv` (Emisiones Fugitivas Puntuales)
  - `ruea-tr-2023-ckan.csv` (Transferencias)

### Procesamiento Aplicado
1. **Filtrado:** Solo registros con CO2
2. **Limpieza:** Datos nulos y outliers tratados
3. **Agregación:** Por región y tipo de emisión
4. **Optimización:** Compresión para web (~50KB total)
5. **Validación:** Consistencia de datos verificada

---

## 🚫 ¿Qué NO incluir?

### Archivos Excluidos del Repositorio
```
# ❌ NO incluir datasets originales (muy grandes)
data/raw/*.csv                      # +100MB cada uno

# ❌ NO incluir archivos temporales
*.tmp
*.log
__pycache__/

# ❌ NO incluir datos sensibles
credentials/
api_keys/
```

### ✅ Solo Incluir Datos Procesados
- Archivos JSON optimizados (<5KB cada uno)
- Metadatos esenciales
- Mapas simplificados para web

---

## 🔧 Troubleshooting

### Problema: Archivos JSON No Existen
**Error:** `FileNotFoundError` al cargar datos CO2

**Solución:**
1. Ejecutar notebook completo
2. Verificar que las últimas celdas se ejecutaron
3. Comprobar permisos de escritura en `app/data/cache/`

### Problema: Datos Inconsistentes
**Error:** Métricas no coinciden entre notebook y app

**Solución:**
1. Re-ejecutar notebook desde el inicio
2. Verificar que no hay archivos JSON antiguos
3. Limpiar cache de Streamlit: `streamlit cache clear`

### Problema: Archivos Muy Grandes
**Error:** Despliegue lento en Streamlit Cloud

**Solución:**
- Los archivos JSON están optimizados (~50KB total)
- Si son más grandes, verificar que el notebook está optimizando correctamente
- Revisar que no se incluyeron datasets originales por error

---

## 📊 Métricas de Datos

### Tamaños Optimizados
| Archivo | Tamaño | Registros |
|---------|--------|-----------|
| `emisiones_anuales.json` | ~50 bytes | 1 año |
| `emisiones_regionales.json` | ~3KB | 16 regiones |
| `cache_metadata.json` | ~2KB | Estadísticas |
| **Total** | **~5KB** | Optimizado |

### Comparación con Datos Originales
| Formato | Original | Procesado | Reducción |
|---------|----------|-----------|-----------|
| **CSV crudo** | ~300MB | - | - |
| **JSON optimizado** | - | ~5KB | **99.998%** |

---

## 📝 Notas para Desarrolladores

### Al Modificar el Notebook
1. **Siempre** re-generar los archivos JSON después de cambios
2. **Verificar** que los nuevos datos son consistentes
3. **Actualizar** este README si cambia la estructura

### Al Desplegar
1. **Verificar** que todos los archivos JSON existen
2. **Comprobar** tamaños de archivo (deben ser > 0 bytes)
3. **Probar** localmente antes de desplegar

### Mantenimiento
- **Frecuencia de actualización:** Cuando haya nuevos datos RETC
- **Monitoreo:** Verificar que la app carga datos correctamente
- **Backup:** Los datos se regeneran desde el notebook, no necesitan backup especial

---

**Contacto:** daniel.mardones@integralservicespa.cl  
**Repositorio:** https://github.com/Denniels/ds_portfolio
