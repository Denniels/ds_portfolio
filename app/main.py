"""
Aplicación principal del portafolio - Presentación personal de aprendizaje autodidacta
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import os
import json
from datetime import datetime
from utils.navigation import navigate_to, nav_button, large_nav_button, create_robust_sidebar_nav
from utils.shared_styles import apply_shared_styles

# Configuración de página PRIMERO
st.set_page_config(
    page_title="Portfolio de Ciencia de Datos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importar y aplicar la configuración global
import sys
sys.path.append(str(Path(__file__).parent))
from config import apply_styles_only
apply_styles_only()

def main():
    """Función principal"""
    
    # Sidebar con navegación robusta y selector de temas
    with st.sidebar:
        # Agregar selector de temas
        from utils.theme_manager import create_theme_selector
        create_theme_selector()
        
        st.markdown("### 🔗 Contacto")
        st.markdown("**LinkedIn:** [Daniel Mardones](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)")
        st.markdown("**GitHub:** [Denniels](https://github.com/Denniels)")
        
        st.markdown("---")
    
    # Título principal
    st.markdown('<h1 class="main-title">Portfolio de Ciencia de Datos</h1>', unsafe_allow_html=True)
    
    # Sección hero con un enfoque más personal y humilde
    st.markdown("""
    <div class="hero-section">
        <h2>Hola, soy Daniel Mardones</h2>
        <p>Un autodidacta en el camino de la ciencia de datos, buscando mi primera oportunidad profesional</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sección de presentación personal interactiva con tabs
    tabs = st.tabs(["🧑‍💻 Sobre mí", "🛣️ Mi camino", "🔍 Mis habilidades", "🎯 Mis objetivos"])
    
    with tabs[0]:
        col_photo, col_text = st.columns([1, 2])
        with col_photo:
            st.image("https://img.icons8.com/color/240/000000/user-male-circle--v1.png", width=150)
        with col_text:
            st.markdown("""
            ### Mi historia

            Durante los últimos 10 años, he gestionado mi pequeño emprendimiento de **reparación de equipos industriales**, 
            donde he desarrollado habilidades técnicas y aprendido a resolver problemas complejos.

            Mientras continuaba con mi trabajo, descubrí mi pasión por la programación y el análisis de datos, lo que me llevó a 
            iniciar un camino de **aprendizaje autodidacta** en paralelo a mis responsabilidades laborales.

            En mi tiempo libre, me he formado en Python y ciencia de datos, construyendo este portafolio como muestra de 
            mis habilidades y conocimientos adquiridos por cuenta propia.
            """)
    
    with tabs[1]:
        # Timeline interactiva con un enfoque más honesto del proceso de aprendizaje
        st.markdown("### Mi trayectoria de aprendizaje")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**2019-2020**")
        with col2:
            st.markdown("""
            **Primeros pasos en programación**
            - Aprendizaje básico de Python a través de cursos gratuitos en línea
            - Primeros scripts para automatizar tareas simples en mi trabajo
            """)
            st.markdown("---")
            
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**2021**")
        with col2:
            st.markdown("""
            **Descubrimiento del análisis de datos**
            - Introducción a Pandas y NumPy
            - Primeros análisis de datos relacionados con mi negocio
            - Curso completo de Data Science (En Udemy)
            """)
            st.markdown("---")
            
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**2022**")
        with col2:
            st.markdown("""
            **Profundizando en la visualización**
            - Aprendizaje de Matplotlib, Seaborn y Plotly
            - Creación de dashboards básicos para análisis de ventas
            - Participación en foros y comunidades de datos
            - Curso completo de Data Science en Academia DesafioLATAM (con certificado)
            """)
            st.markdown("---")
            
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**2023**")
        with col2:
            st.markdown("""
            **Explorando machine learning**
            - Introducción a scikit-learn y modelos predictivos básicos
            - Primer proyecto completo de análisis de datos ambientales
            - Participación en un bootcamp intensivo de Data Science
            """)
            st.markdown("---")
            
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**2024**")
        with col2:
            st.markdown("""
            **Aplicaciones interactivas y portafolio**
            - Aprendizaje de Streamlit para crear aplicaciones interactivas
            - Desarrollo de este portafolio para mostrar mis proyectos
            - Búsqueda activa de oportunidades laborales en el campo
            """)
    
    with tabs[2]:
        st.markdown("### Mis habilidades técnicas")
        
        # Crear 3 columnas para mostrar habilidades por categorías
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### Programación")
            st.markdown("""
            - Python (intermedio)
            - SQL (básico)
            - Git (básico)
            - HTML/CSS (básico)
            """)
            
        with col2:
            st.markdown("#### Análisis de Datos")
            st.markdown("""
            - Pandas & NumPy
            - Visualización (Matplotlib, Plotly)
            - Limpieza y preparación de datos
            - Estadística descriptiva
            """)
            
        with col3:
            st.markdown("#### Herramientas")
            st.markdown("""
            - Streamlit
            - Jupyter Notebooks
            - Google Colab
            - Excel avanzado
            - Flask (básico)
            """)
            
        # Añadir sección de nivel de experiencia en machine learning
        st.markdown("### Conocimientos en Machine Learning")
        st.markdown("""
        Actualmente tengo conocimientos básicos en:
        - Modelos de regresión lineal y logística
        - Algoritmos de clustering (K-means)
        - Validación cruzada y evaluación de modelos
        - Procesamiento básico de lenguaje natural (NLP)
        """)
        
        # Añadir nota honesta sobre nivel de experiencia
        st.info("""
        **Nota:** Reconozco que mi experiencia es principalmente académica y basada en proyectos personales. 
        Estoy ansioso por aplicar estos conocimientos en un entorno profesional donde pueda crecer y aprender 
        junto a profesionales experimentados.
        """)
    
    with tabs[3]:
        st.markdown("""
        ### Lo que busco

        Mi objetivo principal es **integrarme a un equipo profesional de desarrollo o ciencia de datos** donde pueda:
        
        - Aplicar mis conocimientos autodidactas en un entorno real y colaborativo
        - Aprender las mejores prácticas de la industria junto a profesionales experimentados
        - Aportar una perspectiva única, combinando mi experiencia técnica previa con mis nuevas habilidades
        - Crecer como profesional en el campo de la ciencia de datos
        """)
        
        # Añadir sección de intereses específicos
        st.markdown("### Áreas de interés")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Me entusiasma trabajar en:
            - Análisis de datos ambientales
            - Optimización de procesos industriales
            - Visualización de datos complejos
            - Automatización de tareas repetitivas
            """)
            
        with col2:
            st.markdown("""
            #### Dispuesto a aprender:
            - Despliegue de modelos en producción
            - Trabajo con datos a gran escala
            - Nuevos lenguajes y frameworks
            - Metodologías ágiles de desarrollo
            """)
        
        st.write("---")
        
        # Mensaje final de motivación y humildad
        st.markdown("""
        Este portafolio es mi forma de mostrar lo que he aprendido de manera autodidacta y lo que puedo aportar, 
        siempre con la humildad de quien sabe que tiene mucho por aprender y con la motivación de quien 
        está listo para dar el salto al mundo profesional.
        """)

    # Proyectos destacados con títulos más descriptivos y enfoque en aprendizaje
    st.markdown("---")
    st.markdown("## Proyectos de aprendizaje")
    st.markdown("Estos son algunos de los proyectos en los que he trabajado para aplicar mis conocimientos:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="project-card">
            <h3>🏭 Análisis de Emisiones CO2</h3>
            <p>Estudio de datos públicos sobre emisiones industriales en Chile</p>
            <p><em>Habilidades aplicadas: Pandas, Plotly, Análisis exploratorio</em></p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="project-card">
            <h3>💧 Calidad del Agua</h3>
            <p>Análisis de parámetros de calidad en fuentes hídricas nacionales</p>
            <p><em>Habilidades aplicadas: Limpieza de datos, Visualización, Estadística</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Segunda fila
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class="project-card">
            <h3>👥 Análisis Demográfico</h3>
            <p>Exploración de datos poblacionales utilizando BigQuery</p>
            <p><em>Habilidades aplicadas: SQL, Google Cloud, Visualización</em></p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="project-card">
            <h3>💰 Presupuesto Público</h3>
            <p>Análisis de datos de gastos gubernamentales y tendencias</p>
            <p><em>Habilidades aplicadas: Series temporales, Matplotlib, Pandas</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Métricas destacadas con un enfoque más realista
    st.markdown("---")
    st.markdown("### Alcance de los proyectos")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("📊 Visualizaciones", "20+", "Gráficos interactivos")
    
    with col_b:
        st.metric("🗃️ Fuentes de datos", "8", "Datasets públicos")
    
    with col_c:
        st.metric("⏱️ Horas dedicadas", "500+", "Aprendizaje autodidacta")
    
    # Footer
    st.markdown("---")
    
    # Mensaje final más personal
    st.markdown("""
    <div class="final-message">
        <h3>👋 ¡Hasta pronto! Espero sinceramente tener la oportunidad de unirme a su equipo de trabajo.</h3>
        <p>
            Gracias por tomarte el tiempo de revisar mi portafolio. Este proyecto representa mi esfuerzo por aprender 
            nuevas habilidades mientras trabajo en mi emprendimiento de reparación de equipos industriales.
        </p>
        <p>
            Si eres un profesional experimentado, seguramente habrás notado áreas donde puedo mejorar, y eso es 
            exactamente lo que busco: la oportunidad de crecer y perfeccionarme en un entorno profesional.
        </p>
        <p>
            Si crees que mi perfil podría encajar en tu equipo o conoces a alguien que esté buscando a una persona motivada 
            y dispuesta a aprender, me encantaría conversar. A veces, todo lo que necesitamos es una primera oportunidad para demostrar nuestro potencial.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='text-align: center; color: #666; font-size: 0.8em;'>
        Última actualización: {datetime.now().strftime('%d/%m/%Y')} | 
        Desarrollado con Streamlit como parte de mi aprendizaje en Python
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
