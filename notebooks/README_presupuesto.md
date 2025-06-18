# 📊 Análisis del Presupuesto Público de Chile

## 🎯 Descripción General

Este módulo presenta un **análisis integral del presupuesto público de Chile** utilizando datos oficiales de la **Dirección de Presupuestos (DIPRES)** y el portal **datos.gob.cl**. El análisis integra múltiples fuentes de datos para proporcionar insights sobre asignación, ejecución y distribución de recursos públicos.

## 🌐 Fuentes de Datos

### 1. Portal datos.gob.cl - DIPRES (Principal)
- **URL**: [datos.gob.cl/organization/direccion_de_presupuestos](https://datos.gob.cl/organization/direccion_de_presupuestos)
- **Datasets**: 414 conjuntos oficiales disponibles
- **Formatos**: CSV, JSON, XLS
- **Acceso**: Público, sin autenticación

### 2. API Presupuesto Abierto Chile (Complementario)
- **URL**: [presupuestoabierto.gob.cl](https://presupuestoabierto.gob.cl/)
- **Cobertura**: 596 servicios públicos, 2.6M+ registros
- **Actualización**: Mensual
- **Rate Limit**: 1000 requests/hora

### 3. Sistema de Respaldo
- Datos sintéticos basados en estadísticas históricas
- Garantiza 100% disponibilidad del análisis
- Activación automática si fallan fuentes principales

## 🔄 Pipeline de Datos

### Estructura del Pipeline

```
📁 notebooks/
├── 04_Analisis_Presupuesto_Publico.ipynb  # Notebook principal
├── update_presupuesto_data.py              # Script de actualización
└── README_presupuesto.md                   # Esta documentación

📁 app/data/processed/                       # Datos procesados
├── presupuesto_chile_2024.csv             # Presupuesto por ministerio
├── ejecucion_presupuestaria_2024.csv      # Ejecución vs presupuestado
├── transferencias_regionales_2024.csv     # Transferencias por región
├── inversion_publica_2024.csv             # Proyectos de inversión
├── top_ministerios.csv                     # Ranking ministerios
├── top_regiones.csv                        # Ranking regiones
├── distribucion_sectores.csv              # Distribución sectorial
├── resumen_ejecutivo.json                 # Indicadores principales
├── datos_visualizacion.json               # Datos para gráficos
└── metadatos.json                          # Metadatos del análisis

📁 app/pages/
└── 04_presupuesto_publico.py              # Aplicación Streamlit
```

### Flujo de Procesamiento

1. **Extracción** → Descarga de CSVs + API calls
2. **Validación** → Verificación de integridad y esquemas
3. **Procesamiento** → Limpieza, normalización y cálculo de indicadores
4. **Análisis** → Estadísticas descriptivas y modelado predictivo
5. **Exportación** → Generación de archivos para Streamlit
6. **Visualización** → Aplicación web interactiva

## 🚀 Uso del Sistema

### Ejecución Manual

```bash
# 1. Ejecutar notebook completo
jupyter nbconvert --to notebook --execute --inplace 04_Analisis_Presupuesto_Publico.ipynb

# 2. Verificar datos generados
ls -la ../app/data/processed/

# 3. Ejecutar aplicación Streamlit
cd ../app
streamlit run pages/04_presupuesto_publico.py
```

### Actualización Automática

```bash
# Ejecutar script de actualización
python update_presupuesto_data.py
```

### Integración con Aplicación Principal

```bash
# Ejecutar aplicación completa
cd ../app
streamlit run main.py
```

## 📊 Indicadores y Métricas

### Indicadores Principales

| Métrica | Descripción | Valor Típico |
|---------|-------------|--------------|
| **Presupuesto Total** | Suma de presupuestos ministeriales | ~$94 mil millones |
| **Eficiencia Ejecución** | % ejecutado vs presupuestado | 84.4% |
| **Avance Proyectos** | % promedio de avance | 51.1% |
| **Eficiencia Inversión** | % inversión ejecutada | 50.9% |
| **Transferencias Totales** | Suma transferencias regionales | ~$117 mil millones |

### Clasificación de Eficiencia

- 🟢 **Excelente**: ≥95%
- 🟡 **Bueno**: 85-94%
- 🟠 **Regular**: 70-84%
- 🔴 **Deficiente**: <70%

## 🤖 Modelado Predictivo

### Modelos Implementados

1. **Random Forest Regressor**
   - Variables: Presupuesto, sector, región, año
   - Objetivo: Predicción de eficiencia presupuestaria
   - Precisión: R² variable según datos

2. **Regresión Lineal**
   - Modelo de comparación y validación
   - Interpretabilidad de coeficientes
   - Baseline para evaluación

### Variables de Importancia

1. **Log Presupuesto** (27.7%)
2. **Monto Presupuesto** (26.9%)
3. **Código Región** (21.4%)
4. **Código Sector** (16.6%)
5. **Año** (7.4%)

## 📈 Resultados del Análisis

### Hallazgos Principales

- **Concentración**: Top 5 ministerios = 50.1% del presupuesto
- **Distribución Regional**: Relativamente equitativa entre regiones
- **Sectores Críticos**: Asuntos Económicos (15.6%), Orden Público (14.7%)
- **Oportunidades**: 15-25% mejora potencial en eficiencia

### Recomendaciones Estratégicas

1. **Monitoreo en Tiempo Real** para proyectos <70% avance
2. **Redistribución** basada en eficiencia histórica
3. **Capacitación Regional** en gestión presupuestaria
4. **Incentivos** por cumplimiento de metas

## 🛠️ Mantenimiento y Troubleshooting

### Problemas Comunes

#### Error: "Datos no encontrados"
```bash
# Verificar existencia de archivos
ls -la app/data/processed/
# Re-ejecutar notebook si faltan
jupyter nbconvert --execute --inplace 04_Analisis_Presupuesto_Publico.ipynb
```

#### Error: "API no disponible"
- Sistema automáticamente usa datos de respaldo
- No requiere intervención manual
- Ver logs para detalles

#### Error: "Timeout en descarga"
```python
# Aumentar timeout en notebook (celda de configuración)
TIMEOUT_SECONDS = 60  # Aumentar de 30 a 60
```

### Monitoreo de Salud

```python
# Script de verificación rápida
python -c "
import json
with open('app/data/processed/resumen_ejecutivo.json') as f:
    data = json.load(f)
print(f'✅ Datos OK - Última actualización: {data[\"fecha_analisis\"]}')
"
```

## 📚 Referencias Técnicas

### Documentación Oficial
- [DIPRES - Dirección de Presupuestos](https://www.dipres.gob.cl/)
- [Portal datos.gob.cl](https://datos.gob.cl/)
- [Presupuesto Abierto Chile](https://presupuestoabierto.gob.cl/)

### Especificaciones Técnicas
- **Python**: 3.8+
- **Pandas**: 2.0+
- **Plotly**: 5.0+
- **Streamlit**: 1.28+
- **Scikit-learn**: 1.3+

### Contacto y Soporte
- **Desarrollo**: DS Portfolio Team
- **Documentación**: README files en cada módulo
- **Issues**: GitHub repository issues

---

## 🏁 Estado del Proyecto

✅ **Completado**: Análisis integral implementado  
✅ **Funcional**: Pipeline de datos operativo  
✅ **Documentado**: Metodología completamente documentada  
✅ **Integrado**: Aplicación Streamlit funcionando  
✅ **Optimizado**: Sistema de respaldo y manejo de errores  

**Última actualización**: 17 de junio de 2025  
**Versión**: 1.0  
**Estado**: Producción
