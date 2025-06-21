"""
Componente para mostrar índices inmobiliarios
"""
import streamlit as st
import pandas as pd
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

def cargar_indices_inmobiliarios():
    """Carga los índices inmobiliarios desde el archivo JSON"""
    try:
        # Definir ruta del archivo
        json_path = Path(__file__).parent.parent / "data" / "inmobiliario" / "indices_inmobiliarios.json"
        
        # Cargar datos
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data
    except Exception as e:
        st.error(f"Error al cargar los índices inmobiliarios: {e}")
        return None

def crear_dataframe_indices(data):
    """Convierte los datos de índices a un DataFrame para visualización"""
    if not data or 'series' not in data:
        return None
    
    # Crear lista para almacenar todos los puntos de datos
    all_points = []
    
    # Procesar cada serie
    for serie_name, serie_data in data['series'].items():
        for date, value in serie_data['data_points'].items():
            all_points.append({
                'fecha': date,
                'indice': serie_name,
                'valor': value
            })
    
    # Convertir a DataFrame
    df = pd.DataFrame(all_points)
    
    # Convertir fechas
    df['fecha'] = pd.to_datetime(df['fecha'])
    
    # Ordenar por fecha
    df = df.sort_values('fecha')
    
    return df

def mostrar_grafico_indices(df):
    """Muestra un gráfico interactivo de los índices inmobiliarios"""
    if df is None or len(df) == 0:
        st.warning("No hay datos de índices disponibles para mostrar")
        return
    
    # Crear gráfico
    fig = px.line(
        df, 
        x='fecha', 
        y='valor', 
        color='indice',
        title='Evolución de Índices de Precios Inmobiliarios',
        labels={'fecha': 'Fecha', 'valor': 'Valor del Índice', 'indice': 'Índice'},
        markers=True
    )
    
    # Personalizar
    fig.update_layout(
        legend_title_text='Tipo de Índice',
        hovermode='x unified',
        template='plotly_white',
        xaxis=dict(
            title='Fecha',
            tickformat='%b %Y',
            tickangle=-45
        ),
        yaxis=dict(
            title='Valor del Índice'
        ),
        height=500
    )
    
    # Mostrar
    st.plotly_chart(fig, use_container_width=True)

def mostrar_tendencias_indices(df):
    """Muestra tendencias y análisis de los índices inmobiliarios"""
    if df is None or len(df) == 0:
        return
      # Calcular variaciones porcentuales mes a mes para cada índice
    indices = df['indice'].unique()
    
    for indice in indices:
        # Crear una copia profunda de los datos para este índice
        mask = df['indice'] == indice
        df_indice = pd.DataFrame(df[mask]).copy()
        df_indice = df_indice.sort_values('fecha')
        
        # Calcular variaciones usando loc para evitar advertencias
        df_indice.loc[:, 'valor_anterior'] = df_indice['valor'].shift(1)
        df_indice.loc[:, 'variacion_mensual'] = (df_indice['valor'] / df_indice['valor_anterior'] - 1) * 100
        
        # Calcular variación acumulada en 12 meses
        df_indice.loc[:, 'valor_12m_atras'] = df_indice['valor'].shift(12)
        df_indice.loc[:, 'variacion_anual'] = (df_indice['valor'] / df_indice['valor_12m_atras'] - 1) * 100
        
        # Mostrar últimas tendencias
        if len(df_indice) > 3:
            ultimo_dato = df_indice.iloc[-1]
            penultimo_dato = df_indice.iloc[-2]
            
            st.subheader(f"Tendencia: {indice}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Último valor",
                    value=f"{ultimo_dato['valor']:.2f}",
                    delta=f"{ultimo_dato['variacion_mensual']:.2f}%" if not pd.isna(ultimo_dato['variacion_mensual']) else None
                )
            
            with col2:
                # Variación mensual
                var_mensual = ultimo_dato['variacion_mensual']
                if not pd.isna(var_mensual):
                    st.metric(
                        label="Variación mensual",
                        value=f"{var_mensual:.2f}%",
                        delta="Subida" if var_mensual > 0 else "Bajada"
                    )
            
            with col3:
                # Variación anual
                var_anual = ultimo_dato['variacion_anual']
                if not pd.isna(var_anual):
                    st.metric(
                        label="Variación en 12 meses",
                        value=f"{var_anual:.2f}%",
                        delta="Subida" if var_anual > 0 else "Bajada"
                    )
            
            # Análisis de tendencia
            if not pd.isna(ultimo_dato['variacion_mensual']) and not pd.isna(penultimo_dato['variacion_mensual']):
                aceleracion = ultimo_dato['variacion_mensual'] > penultimo_dato['variacion_mensual']
                
                if aceleracion and ultimo_dato['variacion_mensual'] > 0:
                    st.info("📈 Tendencia alcista acelerada: los precios están subiendo a un ritmo mayor que el mes anterior.")
                elif not aceleracion and ultimo_dato['variacion_mensual'] > 0:
                    st.info("📈 Tendencia alcista moderada: los precios siguen subiendo pero a un ritmo menor que el mes anterior.")
                elif aceleracion and ultimo_dato['variacion_mensual'] < 0:
                    st.warning("📉 Tendencia bajista acelerada: los precios están bajando a un ritmo mayor que el mes anterior.")
                elif not aceleracion and ultimo_dato['variacion_mensual'] < 0:
                    st.warning("📉 Tendencia bajista moderada: los precios siguen bajando pero a un ritmo menor que el mes anterior.")
                else:
                    st.info("➡️ Tendencia estable: no se observan cambios significativos en los precios.")
                
            st.markdown("---")

def analizar_mercado_inmobiliario(df):
    """Realiza un análisis del mercado inmobiliario basado en los índices"""
    if df is None or len(df) == 0:
        return
    
    st.subheader("Análisis del Mercado Inmobiliario")
    
    # Calcular variaciones recientes
    indices = df['indice'].unique()
    tendencias = {}
    
    for indice in indices:
        # Crear una copia profunda de los datos para este índice
        mask = df['indice'] == indice
        df_indice = pd.DataFrame(df[mask]).copy()
        df_indice = df_indice.sort_values('fecha')
        
        if len(df_indice) >= 6:
            # Obtener últimos 6 meses (usando .copy() para evitar advertencias)
            df_reciente = pd.DataFrame(df_indice.tail(6)).copy()
            
            # Calcular tendencia usando .iloc para acceso seguro y conversión a float
            primer_valor = float(df_reciente.iloc[0]['valor'])
            ultimo_valor = float(df_reciente.iloc[-1]['valor'])
            variacion_total = (ultimo_valor / primer_valor - 1) * 100
            
            tendencias[indice] = {
                'variacion_semestral': variacion_total,
                'ultimo_valor': ultimo_valor,
                'tendencia': 'Alza' if variacion_total > 0 else 'Baja' if variacion_total < 0 else 'Estable'
            }
    
    # Determinar estado general del mercado
    if tendencias:
        var_promedio = sum(t['variacion_semestral'] for t in tendencias.values()) / len(tendencias)
        
        if var_promedio > 3:
            mercado = "🔥 MERCADO EN ALZA FUERTE"
            analisis = "El mercado inmobiliario muestra una clara tendencia alcista con aumentos de precios significativos en los últimos 6 meses. Este escenario favorece a vendedores y propietarios actuales."
        elif var_promedio > 1:
            mercado = "📈 MERCADO EN ALZA MODERADA"
            analisis = "Los precios inmobiliarios muestran un crecimiento moderado pero sostenido, indicando un mercado saludable con potencial de apreciación a mediano plazo."
        elif var_promedio > -1:
            mercado = "➡️ MERCADO ESTABLE"
            analisis = "El mercado inmobiliario se mantiene estable con variaciones mínimas en los precios, lo que indica un equilibrio entre oferta y demanda."
        elif var_promedio > -3:
            mercado = "📉 MERCADO EN AJUSTE"
            analisis = "Se observa un ajuste a la baja en los precios inmobiliarios, lo que puede representar oportunidades para compradores e inversionistas con visión de largo plazo."
        else:
            mercado = "⚠️ MERCADO EN CORRECCIÓN"
            analisis = "El mercado inmobiliario está experimentando una corrección significativa de precios, posiblemente relacionada con factores macroeconómicos o exceso de oferta."
        
        # Mostrar análisis
        st.markdown(f"""
        <div style='background-color:#f5f5f5; padding:1.5rem; border-radius:10px; margin-bottom:1rem'>
            <h3 style='text-align:center'>{mercado}</h3>
            <p style='font-size:1.1rem; margin-top:1rem'>{analisis}</p>
            <p style='font-style:italic; margin-top:1rem'>Variación promedio semestral: {var_promedio:.2f}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recomendaciones según el mercado
        if var_promedio > 2:
            st.markdown("""
            **Recomendaciones para este mercado:**
            * 🏠 Para propietarios: Momento favorable para vender si planeas realizar ganancias.
            * 💰 Para compradores: Considerar zonas emergentes con potencial de valorización.
            * 🔍 Para inversionistas: Enfocarse en propiedades que generen flujo de caja positivo.
            """)
        elif var_promedio > 0:
            st.markdown("""
            **Recomendaciones para este mercado:**
            * 🏠 Para propietarios: Buen momento para mejoras que aumenten el valor de la propiedad.
            * 💰 Para compradores: Oportunidad de compra con posibilidad de apreciación moderada.
            * 🔍 Para inversionistas: Balance entre propiedades para renta y para plusvalía.
            """)
        else:
            st.markdown("""
            **Recomendaciones para este mercado:**
            * 🏠 Para propietarios: Si no es necesario vender, considerar mantener la propiedad.
            * 💰 Para compradores: Momento favorable para negociar y encontrar buenas oportunidades.
            * 🔍 Para inversionistas: Enfocarse en zonas consolidadas y propiedades con buen potencial de renta.
            """)

def mostrar_dashboard_indices():
    """Muestra un dashboard completo de índices inmobiliarios"""
    st.header("📊 Dashboard de Índices Inmobiliarios")
    
    # Cargar datos
    data = cargar_indices_inmobiliarios()
    
    if data is None:
        st.error("No se pudieron cargar los datos de índices inmobiliarios")
        return
    
    # Convertir a DataFrame
    df = crear_dataframe_indices(data)
    
    # Mostrar información de la fuente
    st.markdown(f"""
    <div style='background-color:#f0f8ff; padding:1rem; border-radius:5px; margin-bottom:1rem; font-size:0.9rem'>
        <strong>Fuente:</strong> {data['metadata']['source']}<br>
        <strong>Descripción:</strong> {data['metadata']['description']}<br>
        <strong>Actualización:</strong> {data['metadata']['processed_date']}
    </div>
    """, unsafe_allow_html=True)
    
    # Mostrar pestañas para diferentes vistas
    tab1, tab2, tab3 = st.tabs(["📈 Gráfico de Índices", "📊 Tendencias", "🔍 Análisis de Mercado"])
    
    with tab1:
        # Filtro de índices
        if df is not None:
            indices = sorted(df['indice'].unique())
            selected_indices = st.multiselect(
                "Seleccionar índices a mostrar",
                options=indices,
                default=indices[:3] if len(indices) > 3 else indices
            )
            
            if selected_indices:
                df_filtered = df[df['indice'].isin(selected_indices)]
                mostrar_grafico_indices(df_filtered)
            else:
                st.info("Selecciona al menos un índice para visualizar")
    
    with tab2:
        # Mostrar tendencias
        if df is not None:
            indices = sorted(df['indice'].unique())
            selected_index = st.selectbox(
                "Seleccionar índice para análisis de tendencia",
                options=indices
            )
            
            df_filtered = df[df['indice'] == selected_index]
            mostrar_tendencias_indices(df_filtered)
    
    with tab3:
        # Análisis de mercado
        analizar_mercado_inmobiliario(df)
