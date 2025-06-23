"""
Estilos compartidos para mantener consistencia visual en todas las páginas
"""
import streamlit as st
from pathlib import Path
import os

def apply_shared_styles():
    """
    Aplica estilos CSS compartidos a todas las páginas.
    Debe ser llamado DESPUÉS de st.set_page_config().
    """
    # CSS básico compartido
    st.markdown("""
    <style>
        /* Estilos principales */
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
        .hero-section h2 {
            font-size: 2.2rem;
            margin-bottom: 0.5rem;
        }
        .hero-section p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .project-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 1rem 0;
            border-left: 4px solid #667eea;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .project-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }
        .project-card h3 {
            color: #4a4a4a;
            margin-bottom: 0.8rem;
        }
        .project-card p {
            color: #666;
            font-size: 0.95rem;
        }
        .project-card p em {
            color: #667eea;
            font-size: 0.85rem;
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
        
        /* Estilizar los tabs para mejor visibilidad */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 40px;
            white-space: pre-wrap;
            background-color: #f8f9fa;
            border-radius: 4px 4px 0 0;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #667eea !important;
            color: white !important;
        }
        
        /* Mensaje final personal */
        .final-message {
            background: linear-gradient(to right, #f6f9fc, #ffffff);
            padding: 2rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 2rem 0;
        }
        
        .final-message h3 {
            color: #4a4a4a;
            margin-bottom: 1rem;
        }
        
        .final-message p {
            color: #555;
            line-height: 1.6;
            font-size: 1.05rem;
            margin-bottom: 1rem;
        }
        
        /* Animación para la línea de tiempo */
        div[data-testid="column"]:nth-of-type(odd) {
            animation: fadeInLeft 0.5s ease-out;
        }
        
        div[data-testid="column"]:nth-of-type(even) {
            animation: fadeInRight 0.5s ease-out;
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        /* Personalización del menú lateral de navegación */
        section[data-testid="stSidebar"] .css-1d391kg {
            padding-top: 2rem;
        }
        
        /* Estilo para todos los elementos del menú */
        section[data-testid="stSidebar"] ul {
            padding-left: 0;
        }
        
        section[data-testid="stSidebar"] .css-17lntkn {
            font-weight: 500;
            padding: 0.5rem 0;
        }
        
        /* Enlaces del menú lateral */
        section[data-testid="stSidebar"] a {
            color: #4a4a4a;
            text-decoration: none;
            padding: 0.5rem 1rem;
            margin-bottom: 0.3rem;
            border-radius: 4px;
            display: block;
            transition: all 0.2s ease;
        }
        
        /* Efecto hover para los enlaces */
        section[data-testid="stSidebar"] a:hover {
            color: #667eea;
            background-color: rgba(102, 126, 234, 0.1);
            transform: translateX(5px);
            border-left: 3px solid #667eea;
        }
        
        /* Estilo para enlace activo/seleccionado */
        section[data-testid="stSidebar"] a.active {
            color: #667eea;
            background-color: rgba(102, 126, 234, 0.15);
            border-left: 3px solid #667eea;
            font-weight: 600;
        }
        
        /* Iconos en el menú (se aplica a los emojis al inicio de los textos) */
        section[data-testid="stSidebar"] span.emoji {
            margin-right: 8px;
            font-size: 1.2rem;
        }
        
        /* Separador en el sidebar */
        section[data-testid="stSidebar"] hr {
            margin: 1rem 0;
            border-color: rgba(102, 126, 234, 0.2);
        }
        
        /* Título del menú de navegación */
        section[data-testid="stSidebar"] .css-zt5igj {
            color: #667eea;
            font-weight: 600;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        /* Estilos para páginas específicas */
        /* Selector para la página principal */
        section[data-testid="stSidebar"] a:contains("principal") {
            color: #667eea;
        }
        section[data-testid="stSidebar"] a:contains("principal")::before {
            content: "🏠 ";
        }
        
        /* Selector para la página de emisiones de CO2 */
        section[data-testid="stSidebar"] a:contains("emisiones de CO2")::before {
            content: "🏭 ";
        }
        
        /* Selector para la página de agua de calidad */
        section[data-testid="stSidebar"] a:contains("agua de calidad")::before {
            content: "💧 ";
        }
        
        /* Selector para la página de demografía */
        section[data-testid="stSidebar"] a:contains("demografía")::before {
            content: "👥 ";
        }
        
        /* Selector para la página de presupuesto público */
        section[data-testid="stSidebar"] a:contains("presupuesto público")::before {
            content: "💰 ";
        }
        
        /* Selector para la página de plan de estudios */
        section[data-testid="stSidebar"] a:contains("plan de estudios")::before {
            content: "📚 ";
        }
        
        /* Selector para la página de servicios */
        section[data-testid="stSidebar"] a:contains("servicios")::before {
            content: "🔧 ";
        }
        
        /* Selector para la página de comentario */
        section[data-testid="stSidebar"] a:contains("comentario")::before {
            content: "💬 ";
        }
        
        /* Selector para la página de productos */
        section[data-testid="stSidebar"] a:contains("productos")::before {
            content: "📦 ";
        }
        
        /* Selector para la página de generador de informes */
        section[data-testid="stSidebar"] a:contains("generador de informes")::before {
            content: "📊 ";
        }
        
        /* Selector para la página de predictor inmobiliario */
        section[data-testid="stSidebar"] a:contains("predictor inmobiliario")::before {
            content: "🏘️ ";
        }
    </style>

    <script>
    // Código JavaScript para marcar la página actual como activa
    document.addEventListener('DOMContentLoaded', function() {
        const currentPath = window.location.pathname;
        const sidebarLinks = document.querySelectorAll('section[data-testid="stSidebar"] a');
        
        sidebarLinks.forEach(link => {
            const linkPath = link.getAttribute('href');
            if (linkPath === currentPath || 
                (currentPath === '/' && linkPath === './') || 
                (linkPath !== './' && currentPath.includes(linkPath))) {
                link.classList.add('active');
            }
        });
    });
    </script>
    """, unsafe_allow_html=True)
