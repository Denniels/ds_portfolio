# 🌍 Análisis de Emisiones de Gases de Efecto Invernadero en Chile
## Sistema Nacional de Inventarios de GEI (SNICHILE)

### 📋 Introducción
[...contenido existente...]

## 2️⃣ Extracción y Carga de Datos

En esta sección:
1. Importaremos nuestros módulos personalizados
2. Inicializaremos el proceso de descarga de datos
3. Cargaremos los datos en nuestra base de datos local
4. Verificaremos la calidad de los datos importados

### 2.1 Configuración de Módulos

```python
# Importar nuestros módulos personalizados
import sys
from pathlib import Path

# Agregar directorio src al path de Python
sys.path.append(str(PROJECT_DIR / 'src'))

# Importar nuestros módulos
from data_processing.data_downloader import SNICHILEDownloader
from data_processing.data_explorer import SNICHILEExplorer

# Crear instancias
downloader = SNICHILEDownloader(DATA_DIR)
explorer = SNICHILEExplorer(DATA_DIR)

print('✅ Módulos personalizados importados correctamente')
```

### 2.2 Descarga Inicial de Datos

```python
# Obtener lista de datasets disponibles
datasets = downloader.get_available_datasets()

print('📊 Datasets disponibles:')
for ds in datasets:
    print(f"- {ds['name']} ({ds['type']})")

# Iniciar proceso de sincronización
print('\n🔄 Iniciando sincronización de datos...')
downloader.sync_data()
print('✅ Sincronización completada')
```

### 2.3 Exploración de Datos Importados

```python
# Analizar estructura de las tablas
print('📊 Estructura de las tablas:')

tablas = ['emisiones_sector']
for tabla in tablas:
    try:
        # Obtener información de la estructura
        estructura = explorer.analyze_table_structure(tabla)
        
        print(f"\n📌 Tabla: {tabla}")
        print("\nColumnas por tipo de dato:")
        for dtype, cols in estructura['dtype_summary'].items():
            print(f"  {dtype}: {', '.join(cols)}")
            
        # Obtener reporte de calidad
        calidad = explorer.get_data_quality_report(tabla)
        
        print(f"\nEstadísticas:")
        print(f"  - Total de filas: {calidad['total_rows']:,}")
        
        if calidad['null_percentages']:
            print("\nValores nulos:")
            for col, pct in calidad['null_percentages'].items():
                print(f"  - {col}: {pct:.2f}%")
                
        print("\nCardinalidad de columnas:")
        for col, info in calidad['cardinality'].items():
            print(f"  - {col}: {info['distinct_count']:,} valores únicos ({info['distinct_ratio']:.2f}%)")
            
    except Exception as e:
        print(f"❌ Error al analizar tabla {tabla}: {str(e)}")
```

### 2.4 Estrategia de Muestreo

```python
# Determinar estrategia de muestreo para cada tabla
print('📊 Estrategias de muestreo:')

for tabla in tablas:
    try:
        estrategia = explorer.get_sampling_strategy(tabla)
        
        print(f"\n📌 Tabla: {tabla}")
        print(f"  {'✅ Usar todos los datos' if not estrategia['use_sample'] else '🔄 Usar muestra'}")
        print(f"  Razón: {estrategia['reason']}")
        if estrategia['use_sample']:
            print(f"  Tamaño de muestra: {estrategia['sample_size']:,} filas")
            
    except Exception as e:
        print(f"❌ Error al determinar estrategia para {tabla}: {str(e)}")
```

### 2.5 Extracción de Datos para Análisis

```python
# Extraer datos según estrategia
dataframes = {}

for tabla in tablas:
    try:
        # Obtener estrategia
        estrategia = explorer.get_sampling_strategy(tabla)
        
        # Extraer datos
        print(f"\n🔄 Extrayendo datos de {tabla}...")
        df = explorer.extract_data(tabla, estrategia)
        dataframes[tabla] = df
        
        # Generar reporte resumen
        reporte = explorer.generate_summary_report(df)
        
        print(f"✅ Datos extraídos: {len(df):,} filas")
        print("\nEstadísticas básicas:")
        print(reporte['basic_stats'])
        
        if reporte['missing_values']:
            print("\nValores faltantes:")
            for col, count in reporte['missing_values'].items():
                print(f"  - {col}: {count:,}")
                
    except Exception as e:
        print(f"❌ Error al extraer datos de {tabla}: {str(e)}")
```

## Siguiente Paso

Con los datos cargados y analizados, en la siguiente sección procederemos a:
1. Realizar la limpieza y preprocesamiento de los datos
2. Crear las primeras visualizaciones exploratorias
3. Identificar patrones y tendencias iniciales
