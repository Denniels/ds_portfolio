# Documentación del Sistema de Actualización de UF

## 📊 Implementación de Valores en UF para Contratos a Largo Plazo

> **Fecha**: 13 de junio de 2025  
> **Estado**: ✅ Implementado

Este documento describe la implementación del sistema para mantener actualizado el valor de la UF (Unidad de Fomento) en el portafolio de servicios, optimizado para la capa gratuita de Google Cloud Run.

## 💼 Justificación

Los contratos de servicios a largo plazo en Chile típicamente se valoran en UF (Unidad de Fomento) para protección contra la inflación. Esta implementación permite:

1. Mostrar valores en pesos chilenos (CLP) y su equivalente en UF
2. Ofrecer contratos a plazo fijo (mínimo un año) cotizados en UF
3. Facturar servicios según el valor de la UF del día de emisión
4. Mantener actualizado el valor de la UF sin costos adicionales

## 🛠️ Arquitectura del Sistema

El sistema de actualización de UF consta de los siguientes componentes:

### 1. Google Cloud Functions (Capa gratuita)

- **Función**: `update_uf_value`
- **Runtime**: Python 3.10
- **Memoria**: 128MB
- **Timeout**: 120s
- **Ejecución**: Programada diariamente a las 10:00 AM (hora de Chile)

Esta función consulta el valor actualizado de la UF desde APIs públicas (mindicador.cl) y lo almacena en Firestore.

### 2. Google Cloud Scheduler (Capa gratuita)

- **Job**: `daily-uf-update`
- **Schedule**: Diariamente a las 10:00 AM (zona horaria de Chile)
- **Target**: HTTP endpoint de la Cloud Function

### 3. Firestore (Capa gratuita)

- **Colección**: `indicadores_economicos`
- **Documento principal**: `valor_uf`
- **Histórico**: Un documento por día con formato `uf_history_YYYYMMDD`

### 4. Componente UF para Streamlit

- Muestra el valor actual de la UF en diferentes formatos
- Implementa cacheo para minimizar lecturas a Firestore
- Incluye fallback a valor por defecto en caso de error

## 📈 Optimización para la Capa Gratuita

El sistema está diseñado para mantenerse completamente dentro de los límites gratuitos de GCP:

| Servicio | Uso estimado | Límite gratuito | % Utilizado |
|----------|--------------|-----------------|-------------|
| Cloud Functions | 1 ejecución diaria (~30/mes) | 2 millones de ejecuciones/mes | <0.01% |
| Cloud Scheduler | 1 job con 1 ejecución diaria | 3 jobs gratuitos | 33% |
| Firestore (lecturas) | ~50 lecturas/día | 50,000 lecturas/día | <0.1% |
| Firestore (escrituras) | 1 escritura/día | 20,000 escrituras/día | <0.01% |
| Firestore (almacenamiento) | ~10KB/mes | 1GB | <0.01% |

## 🔄 Flujo de Actualización

1. **Obtención del valor**: La Cloud Function consulta el valor actual de la UF
    - Fuente primaria: mindicador.cl (API pública)
    - Fuente secundaria: cmfchile.cl (fallback)

2. **Almacenamiento**: Se guarda el valor en Firestore
    - Documento principal para consultas rápidas
    - Documento histórico para auditoría y análisis

3. **Distribución**: El componente de UF en Streamlit lee el valor desde Firestore
    - Implementa cacheo para minimizar lecturas
    - Maneja casos de error y desconexión

## 📋 Implementación en el Catálogo de Servicios

El sistema se integra con el catálogo de servicios para:

1. Mostrar valores en CLP y UF simultáneamente
2. Permitir al usuario alternar entre visualización de valores
3. Destacar la opción de contratos en UF para proyectos anuales
4. Informar del valor actual de la UF en tiempo real

## 🛠️ Despliegue del Sistema

El archivo `deploy_uf_updater.yaml` contiene la configuración para desplegar:
- La Cloud Function
- El Cloud Scheduler job

Para desplegar el sistema:

```bash
gcloud builds submit --config=scripts/deploy_uf_updater.yaml
```

## 📝 Consideraciones

- El sistema puede adaptarse fácilmente para otros indicadores económicos
- La arquitectura es resiliente a fallos temporales de las APIs externas
- Se implementa logging extensivo para monitoreo y depuración
- La solución es completamente serverless, minimizando mantenimiento

---

Para más detalles sobre la justificación de precios y políticas de UF, consulta [`JUSTIFICACION_PRECIOS.md`](JUSTIFICACION_PRECIOS.md).
