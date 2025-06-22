"""
Aplicación principal del portafolio - Versión simplificada
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
import json
from datetime import datetime
from utils.navigation import navigate_to, nav_button, large_nav_button

# Configuración de página PRIMERO
st.set_page_config(
    page_title="Portfolio de Ciencia de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS básico
st.markdown("""
<style>
    .main-title {
        color: #2E86AB;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }
    .project-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        width: 100%;
        background-color: #667eea;
        color: white;
        border: none;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #556cd6;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal"""
    
    # Título principal
    st.markdown('<h1 class="main-title">📊 Portfolio de Ciencia de Datos</h1>', unsafe_allow_html=True)
    
    # Sección hero
    st.markdown("""
    <div class="hero-section">
        <h2>Bienvenido a mi Portfolio</h2>
        <p>Explora mis proyectos de análisis de datos y visualizaciones interactivas</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔗 Contacto")
        st.markdown("**LinkedIn:** [Dennis Marambio](https://linkedin.com/in/dennismarambio)")
        st.markdown("**GitHub:** [Denniels](https://github.com/Denniels)")
        
        st.markdown("---")
        st.markdown("### 📊 Navegación")
        
    # Contenido principal
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>🏭 Análisis de Emisiones CO2</h3>
            <p>Estudio comprehensivo de emisiones industriales en Chile</p>        </div>        """, unsafe_allow_html=True)
        
        # Botón grande para navegación
        large_nav_button("Ver Análisis CO2", "01_emisiones_co2", key="btn_large_1")
    
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>💧 Calidad del Agua</h3>
            <p>Análisis de parámetros de calidad en fuentes hídricas</p>        </div>        """, unsafe_allow_html=True)
        
        # Botón grande para navegación
        large_nav_button("Ver Análisis Agua", "02_calidad_agua", key="btn_large_2")
    
    # Segunda fila
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h3>👥 Análisis Demográfico</h3>
            <p>Exploración de datos poblacionales de Chile</p>        </div>        """, unsafe_allow_html=True)
        
        # Botón grande para navegación 
        large_nav_button("Ver Demografía", "03_demografia", key="btn_large_3")
    
    with col4:
        st.markdown("""
        <div class="project-card">
            <h3>💰 Presupuesto Público</h3>
            <p>Análisis de gastos gubernamentales y tendencias</p>        </div>        """, unsafe_allow_html=True)
        
        # Botón grande para navegación
        large_nav_button("Ver Presupuesto", "04_presupuesto_publico", key="btn_large_4")
    
    # Objetivo del portfolio
    st.markdown("---")
    st.markdown("## 🎯 Objetivo del Portfolio")
    st.write("""
    Esta es mi forma de mostrar los resultados de 5 años de estudios, bootcamps 
    y mucho más contenido sobre Python y Data Science.
    """)
    
    # Métricas destacadas
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("🗺️ Regiones", "16", "Cobertura Nacional")
    
    with col_b:
        st.metric("📅 Años de Datos", "+10", "Datos Históricos")
    
    with col_c:
        st.metric("📊 Visualizaciones", "+20", "Gráficos Interactivos")
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Última actualización: {datetime.now().strftime('%d/%m/%Y')} | 
        Desarrollado con Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
