# 📚 Guía Amigable del Proyecto

¡Hola! 👋 Este documento te ayudará a entender nuestro proyecto de análisis de emisiones de CO2 en Chile. Lo hemos organizado de manera que puedas encontrar fácilmente lo que buscas, ya sea que estés empezando o que quieras profundizar en aspectos técnicos específicos.

## 🎯 ¿Qué encontrarás aquí?
1. 📁 Cómo está organizado todo
2. 🛠️ Las herramientas que usamos
3. 📊 Cómo analizamos los datos
4. 🌐 Nuestra aplicación web
5. 🔧 Detalles técnicos para desarrolladores

> 💡 **Consejo**: Si eres nuevo en el proyecto, te recomiendo empezar por la estructura y luego ir a la sección que más te interese.

## 📁 ¿Cómo está organizado nuestro proyecto?

Imagina nuestro proyecto como una casa con diferentes habitaciones, cada una con su propósito específico:

```
📂 ds_portfolio/
├── 📓 notebooks/     → Donde escribimos nuestros análisis (como un diario de investigación)
├── 🔧 src/          → El cerebro del proyecto (todo el código principal)
├── 🎨 app/          → La cara bonita (nuestra aplicación web)
├── 📊 data/         → Nuestra biblioteca de datos
├── 🧪 tests/        → Donde nos aseguramos que todo funcione bien
├── 📚 docs/         → Donde explico todo esto
└── ⚙️ config/       → Configuraciones del proyecto
```

> 🌟 **Tip**: Si quieres empezar a explorar, te recomiendo comenzar por la carpeta `notebooks/` - ahí encontrarás análisis explicados paso a paso.

## 🛠️ Nuestras Herramientas y Cómo las Usamos

### 📊 El Corazón del Análisis

¿Alguna vez te has preguntado cómo analizamos toneladas de datos sobre emisiones de CO2? Todo comienza en nuestro notebook principal (`01_Analisis_Emisiones_CO2_Chile.ipynb`). Es como nuestra cocina, donde mezclamos diferentes ingredientes para crear algo especial.

#### 🧰 La Caja de Herramientas
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
import folium
```
- **Propósito**: Configuración inicial del ambiente de análisis
- **Bibliotecas**: Pandas (datos), Plotly (visualización), GeoPandas (datos geoespaciales)

#### Carga de Datos
```python
def detect_delimiter(file_path):
    delimiters = [',', ';', '\t']
    with open(file_path, 'r', encoding='utf-8') as f:
        header = f.readline().strip()
        for delimiter in delimiters:
            if delimiter in header:
                return delimiter
```
- **Función**: Detecta automáticamente el delimitador del CSV
- **Uso**: Mejora la robustez en la carga de datos

### 2. Aplicación Streamlit (`app/Home.py`)

#### Configuración de la Página
```python
st.set_page_config(
    page_title="Análisis de Datos Ambientales",
    page_icon="🌍",
    layout="wide"
)
```
- **Propósito**: Configura el layout y apariencia de la aplicación
- **Características**: Título, ícono y layout responsivo

#### Sistema de Temas (`app/components/theme.py`)
```python
def apply_theme():
    current_theme = st.session_state.get("theme", "light")
    if current_theme == "dark":
        background_color = "#0E1117"
        text_color = "#FFFFFF"
    else:
        background_color = "#FFFFFF"
        text_color = "#000000"
```
- **Función**: Gestiona el tema claro/oscuro
- **Implementación**: Usa variables de sesión de Streamlit
- **Estilos**: Aplica CSS personalizado para consistencia visual

### 3. Análisis de CO2 (`app/pages/co2_analysis.py`)

#### Visualización de Datos
```python
fig_bar = px.bar(
    emissions_by_region,
    orientation='h',
    title='Emisiones Totales por Región',
    labels={'value': 'Emisiones (toneladas)', 'region': 'Región'},
    color=emissions_by_region.values,
    color_continuous_scale='Viridis'
)
```
- **Propósito**: Crear gráficos interactivos de emisiones
- **Características**: Orientación horizontal, escala de colores Viridis
- **Interactividad**: Hover, zoom y filtros

## 📊 ¿Cómo Analizamos los Datos?

### 🧹 Limpieza y Preparación

Imagina que tienes una habitación desordenada - antes de poder trabajar cómodamente, necesitas organizarla, ¿verdad? Así mismo trabajamos con los datos:

#### 1. Ponemos Todo en Orden
```python
# Convertimos números que vienen como texto
df_clean['cantidad_toneladas'] = df_clean['cantidad_toneladas'].apply(convert_numeric)

# Arreglamos las coordenadas para poder hacer mapas
df_clean['latitud'] = df_clean['latitud'].apply(convert_numeric)
df_clean['longitud'] = df_clean['longitud'].apply(convert_numeric)
```

> 🎯 **¿Por qué hacemos esto?** 
> Imagina que tienes números escritos en papel - algunos usan comas, otros puntos... 
> Necesitamos que todos "hablen el mismo idioma" para poder trabajar con ellos.
- **Propósito**: Normalizar tipos de datos
- **Tratamiento**: Conversión de strings a números
- **Validación**: Manejo de formatos regionales (comas/puntos)

#### 2. Imputación de Datos
```python
# Imputación de potencia_kw por tipo de fuente
mediana_potencia = df[df['potencia_kw'].notna()].groupby('tipo_fuente')['potencia_kw'].median()
```
- **Método**: Mediana por tipo de fuente
- **Justificación**: Más robusto que la media para valores atípicos
- **Documentación**: Registro de valores imputados

### Análisis Estadístico

#### 1. Estadísticas Descriptivas
```python
df[['cantidad_toneladas', 'latitud', 'longitud', 'potencia_kw']].describe()
```
- **Métricas**: Media, mediana, desviación estándar
- **Distribución**: Análisis de cuartiles
- **Outliers**: Identificación de valores atípicos

#### 2. Análisis Geoespacial
```python
# Creación de mapa de calor
folium.Map(
    location=[-35.6751, -71.5430],
    zoom_start=4,
    tiles='CartoDB positron'
)
```
- **Visualización**: Mapas interactivos de emisiones
- **Clustering**: Agrupación de fuentes emisoras
- **Layers**: Capas de información geográfica

## 💻 Aplicación Web

### Componentes de UI

#### 1. Página Principal
```python
st.title("🌎 Análisis de Emisiones en Chile")
st.markdown("""
## Bienvenido al Dashboard de Análisis de Emisiones
Este proyecto presenta un análisis detallado de las emisiones de CO2...
""")
```
- **Estructura**: Layout jerárquico
- **Componentes**: Títulos, texto markdown, elementos interactivos
- **Navegación**: Menú lateral y secciones principales

#### 2. Visualizaciones Interactivas
```python
st.plotly_chart(fig_bar, use_container_width=True)
```
- **Gráficos**: Plotly para interactividad
- **Responsividad**: Adaptación a diferentes pantallas
- **Personalización**: Temas y estilos consistentes

## 🛠️ Funciones y Métodos Importantes

### 1. Procesamiento de Datos
```python
def convert_numeric(x):
    if isinstance(x, str):
        return float(x.replace(',', '.'))
    return x
```
- **Propósito**: Convertir strings a números
- **Manejo**: Formatos regionales de números
- **Validación**: Tipos de datos consistentes

### 🗺️ Creando Mapas Interactivos

¿Te has preguntado cómo hacemos esos mapas bonitos que muestran dónde hay más emisiones? Aquí está la magia:

```python
def create_heatmap(data, lat_col, lon_col, value_col):
    # Creamos un mapa interactivo que puedes explorar
    return folium.Map()
```

> 🎨 **¿Qué necesitamos?**
> - 📍 Ubicaciones (latitud y longitud)
> - 📊 Cantidad de emisiones
> - 🎯 Y ¡listo! El mapa se crea solo

Es como pintar un cuadro, pero en vez de usar pincel, usamos datos para crear algo que puedes explorar con el mouse.

## 💡 Trucos y Consejos

### 🚀 ¿Cómo Manejamos Tantos Datos?

#### 1. Memoria Inteligente
Es como tener una nevera bien organizada:
- 📦 Guardamos lo que usamos frecuentemente en un lugar de fácil acceso
- ⏰ Tenemos un sistema que limpia automáticamente lo que ya no necesitamos
- 🧹 Todo se mantiene ordenado y eficiente

#### 2. Trabajo por Partes
Como cuando comes un elefante... ¡bocado a bocado!
- 🔄 Cargamos los datos poco a poco
- 📊 Procesamos en pequeños grupos
- 💪 Así nuestra computadora no se agota

### Mejores Prácticas
1. **Código**
   - Documentación inline
   - Nombres descriptivos
   - Funciones modulares

2. **Rendimiento**
   - Caché estratégico
   - Optimización de consultas
   - Gestión eficiente de memoria

## 🌟 ¿Qué Viene Después?

### 🚀 Nuestros Planes a Futuro

#### 1. Hacer Todo Más Rápido
Estamos trabajando en:
- 🏃‍♂️ Hacer que los datos se carguen más rápido
- 🧠 Mejorar cómo recordamos información frecuente
- ⚡ Hacer las búsquedas más veloces

#### 2. Nuevas Funciones Emocionantes
¡Prepárate para ver!
- 🔮 Predicciones del futuro de las emisiones
- 📊 Más gráficos interactivos y bonitos
- 🤝 Una forma de compartir datos con otros proyectos

> 💡 **¿Tienes ideas?** ¡Nos encantaría escucharlas! Este proyecto crece con las sugerencias de todos.

## 📚 ¿Quieres Aprender Más?

### 📖 Recursos Útiles

¿Te picó la curiosidad? Aquí hay algunos lugares geniales para seguir aprendiendo:

1. 🎈 [Streamlit](https://docs.streamlit.io/) - Para crear apps web hermosas
2. 🐼 [Pandas](https://pandas.pydata.org/docs/) - El maestro del análisis de datos
3. 📊 [Plotly](https://plotly.com/python/) - Para hacer gráficos interactivos
4. 🗺️ [Folium](https://python-visualization.github.io/folium/) - El experto en mapas

> 🌟 **Consejo Final**: No tengas miedo de explorar y experimentar. 
> ¡Los mejores descubrimientos vienen de la curiosidad!

## 📊 Guía de Conceptos Estadísticos

### 📐 Cuartiles y Rango Intercuartil

#### ¿Qué son los cuartiles?
Imagina que tienes una lista de números (por ejemplo, emisiones de CO2) y los ordenas de menor a mayor. Los cuartiles dividen estos datos en cuatro partes iguales:

```
Menor valor ----[Q1]----[Q2/Mediana]----[Q3]---- Mayor valor
                25%        50%           75%
```

##### 1️⃣ Q1 (Primer Cuartil)
- Es el valor que está en el 25% de los datos
- Significa que el 25% de los valores están por debajo de este número
- Por ejemplo: Si Q1 = 100 toneladas, significa que el 25% de las emisiones son menores a 100 toneladas

##### 3️⃣ Q3 (Tercer Cuartil)
- Es el valor que está en el 75% de los datos
- Significa que el 75% de los valores están por debajo de este número
- Por ejemplo: Si Q3 = 300 toneladas, significa que el 75% de las emisiones son menores a 300 toneladas

##### 📏 IQR (Rango Intercuartil)
- Es la diferencia entre Q3 y Q1
- IQR = Q3 - Q1
- Nos dice qué tan dispersos están los datos en el "medio" de nuestra distribución
- Por ejemplo: Si Q1 = 100 y Q3 = 300, entonces IQR = 200 toneladas

#### 🎯 ¿Para qué usamos estos valores?

1. **Detectar Valores Atípicos**
   - Valores muy bajos: < Q1 - 1.5 × IQR
   - Valores muy altos: > Q3 + 1.5 × IQR

2. **Entender la Distribución**
   ```
   [--------|---------------------|---------------------|--------]
   Muy bajo     25% de datos         50% de datos      Muy alto
      ↑             ↑                     ↑                ↑
   Atípicos         Q1                   Q3           Atípicos
   ```

3. **Ejemplo Práctico**
   Si tenemos emisiones de CO2:
   - Q1 = 100 toneladas
   - Q3 = 300 toneladas
   - IQR = 200 toneladas
   
   Entonces los valores atípicos serían:
   - Valores muy bajos: < 100 - (1.5 × 200) = < -200
   - Valores muy altos: > 300 + (1.5 × 200) = > 600

> 💡 **Tip**: En nuestro análisis de emisiones, usamos estos valores para identificar empresas o instalaciones que tienen niveles de emisión inusualmente altos o bajos en comparación con el resto.
