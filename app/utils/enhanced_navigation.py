"""
Componentes de navegación mejorados para la aplicación
"""
import streamlit as st
import base64
import os
from pathlib import Path

def add_navigation_menu():
    """Agrega el menú de navegación personalizado al sidebar"""
    st.markdown("""
        <style>
        /* Estilos del menú de navegación */
        .nav-container {
            background: linear-gradient(135deg,
                rgba(var(--primary-color-rgb), 0.05),
                rgba(var(--secondary-color-rgb), 0.05)
            );
            backdrop-filter: blur(10px);
            border: 1px solid rgba(var(--text-color-rgb), 0.1);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin: 1rem 0;
            transition: var(--transition);
        }
        
        .nav-header {
            color: var(--text-color);
            font-size: 1.2rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .nav-links {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .nav-link {
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            border-radius: var(--border-radius);
            color: var(--text-color);
            text-decoration: none;
            background: var(--surface-color);
            border: 1px solid rgba(var(--text-color-rgb), 0.1);
            transition: var(--transition);
            font-weight: 500;
            gap: 0.75rem;
        }
        
        .nav-link:hover {
            background: rgba(var(--primary-color-rgb), 0.1);
            transform: translateX(5px);
        }
        
        .nav-link.active {
            background: var(--primary-color);
            color: white;
            border: none;
        }
        
        .nav-link i {
            font-size: 1.2rem;
            opacity: 0.8;
        }
        
        .nav-section {
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid rgba(var(--text-color-rgb), 0.1);
        }
        
        .nav-section-title {
            color: var(--text-color-secondary);
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Animaciones */
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(-10px); }
            to { opacity: 1; transform: translateX(0); }
        }
        
        .nav-link {
            animation: slideIn 0.3s ease-out forwards;
        }
        </style>
        
        <div class="nav-container">
            <div class="nav-header">
                <span>🧭</span>
                <span>Navegación</span>
            </div>
            
            <nav class="nav-links">
                <a href="/" class="nav-link">
                    <i class="fas fa-home"></i>
                    <span>Inicio</span>
                </a>
                
                <div class="nav-section">
                    <div class="nav-section-title">Análisis</div>
                    <a href="/emisiones_co2" class="nav-link">
                        <i class="fas fa-chart-line"></i>
                        <span>Emisiones CO2</span>
                    </a>
                    <a href="/calidad_agua" class="nav-link">
                        <i class="fas fa-tint"></i>
                        <span>Calidad del Agua</span>
                    </a>
                    <a href="/demografia" class="nav-link">
                        <i class="fas fa-users"></i>
                        <span>Demografía</span>
                    </a>
                    <a href="/presupuesto" class="nav-link">
                        <i class="fas fa-money-bill-wave"></i>
                        <span>Presupuesto</span>
                    </a>
                </div>
                
                <div class="nav-section">
                    <div class="nav-section-title">Información</div>
                    <a href="/curriculum" class="nav-link">
                        <i class="fas fa-file-alt"></i>
                        <span>Currículum</span>
                    </a>
                    <a href="/servicios" class="nav-link">
                        <i class="fas fa-cogs"></i>
                        <span>Servicios</span>
                    </a>
                    <a href="/productos" class="nav-link">
                        <i class="fas fa-lightbulb"></i>
                        <span>Productos</span>
                    </a>
                </div>
            </nav>
        </div>
        
        <script>
        // Marcar enlace activo y manejar navegación
        (function() {
            const currentPath = window.location.pathname;
            
            // Marcar enlace activo
            document.querySelectorAll('.nav-link').forEach(link => {
                if (link.getAttribute('href') === currentPath) {
                    link.classList.add('active');
                }
                
                // Manejar navegación interna
                link.addEventListener('click', (e) => {
                    if (!link.hasAttribute('target')) {
                        e.preventDefault();
                        const path = link.getAttribute('href');
                        // Buscar el iframe principal
                        const mainFrame = window.parent.document.querySelector('iframe[title="streamlit_app"]') || 
                                        window.parent.document.querySelector('.main iframe');
                        if (mainFrame) {
                            window.parent.history.pushState({}, '', path);
                            mainFrame.contentWindow.location.replace(path);
                        } else {
                            window.location.href = path;
                        }
                    }
                });
            });
        })();
        </script>
    """, unsafe_allow_html=True)
