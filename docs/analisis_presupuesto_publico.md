# 📊 Análisis del Presupuesto Público de Chile

## 📝 Descripción
Esta aplicación proporciona un análisis interactivo y detallado del Presupuesto del Sector Público de Chile, permitiendo explorar la distribución de recursos a través de diferentes niveles jerárquicos y visualizar patrones de concentración presupuestaria.

## 🌟 Características Principales

### 📈 Visualizaciones Interactivas
- **Top Entidades por Monto**: Gráficos de barras horizontales interactivos
- **Análisis de Concentración**: Gráficos combinados de barras y líneas
- **Distribución de Montos**: Histogramas en escala logarítmica
- **Datos Detallados**: Tablas interactivas con formato monetario

### 🔄 Integración de Datos
- Conexión directa con la API de datos.gob.cl
- Actualización automática de datos
- Sistema de caché inteligente (TTL: 1 hora)
- Validación y limpieza automática de datos

### 👥 Interfaz de Usuario
- Diseño responsivo y moderno
- Métricas principales destacadas
- Selector de nivel jerárquico intuitivo
- Tooltips informativos
- Estilos personalizados para mejor legibilidad

## 🛠️ Tecnologías Utilizadas
- **Frontend**: Streamlit
- **Visualizaciones**: Plotly
- **Procesamiento de Datos**: Pandas, NumPy
- **API**: urllib, json
- **Caché**: st.cache_data

## 📊 Niveles de Análisis
- **Partida**: Nivel superior de clasificación
- **Capítulo**: Subdivisión de partidas
- **Programa**: Unidades programáticas
- **Subtítulo**: Clasificación económica

## 🔍 Métricas Disponibles
- Total Presupuesto
- Número de Partidas
- Total Programas
- Distribución por nivel
- Concentración presupuestaria

## 🚀 Uso

1. Seleccionar "Análisis del Presupuesto Público" en el menú lateral
2. Elegir el nivel jerárquico deseado
3. Explorar las visualizaciones interactivas
4. Consultar datos detallados según necesidad

## 📈 Ejemplos de Análisis

### Análisis de Concentración
- Identificación de principales receptores de presupuesto
- Patrones de distribución presupuestaria
- Curvas de concentración acumulada

### Distribución de Recursos
- Visualización de disparidades presupuestarias
- Identificación de outliers
- Patrones de asignación por nivel

## 🔄 Actualizaciones Futuras
- Análisis temporal de tendencias
- Comparativas interanuales
- Exportación de datos y visualizaciones
- Indicadores de ejecución presupuestaria

## 📚 Referencias
- [Documentación de datos.gob.cl](https://datos.gob.cl/)
- [Ley de Presupuestos](https://www.dipres.gob.cl/)
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Documentación de Plotly](https://plotly.com/python/)
