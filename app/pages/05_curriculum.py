"""
Página de currículum vitae
"""
import streamlit as st
import sys
from pathlib import Path
import base64
import os
import json
from PIL import Image

# Importar configuración de página
parent_dir = Path(__file__).parent.parent
if str(parent_dir) not in sys.path:
    sys.path.append(str(parent_dir))

# Configurar directorios de datos
DATA_CACHE_DIR = parent_dir / "data" / "cache"
DATA_DIR = parent_dir / "data"

from utils.page_setup import setup_page, add_page_title, create_card

# Configurar página
st = setup_page(
    title="Currículum | Daniel Mardones",
    icon="📝"
)

# Título y descripción de la página
add_page_title(
    "Currículum Vitae",
    "Experiencia profesional, habilidades técnicas y proyectos destacados en Data Science y desarrollo de software.",
    "📝"
)

# Cargar estilos CSS específicos para el currículum
def load_cv_styles():
    st.markdown("""
    <style>
        /* Reducir espacio superior */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0 !important;
        }
        
        /* Ajustar espaciado del título principal */
        .stTitle {
            margin-bottom: 1rem !important;
            padding-bottom: 1rem !important;
        }
        
        /* Resto de estilos existentes */
        .cv-box {
            background: linear-gradient(135deg, #EBF8FF 0%, #BEE3F8 100%);
            border-left: 4px solid #3182CE;
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 0 8px 8px 0;
            transition: all 0.3s ease;
        }
        
        .cv-box:hover {
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(49, 130, 206, 0.2);
        }
        
        .cv-section {
            margin-bottom: 2rem;
            animation: fadeIn 0.6s ease-out;
        }
        
        .cv-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
        }
        
        .cv-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #2C5282;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .cv-text {
            color: #2D3748;
            line-height: 1.6;
        }
        
        .education-box {
            background: linear-gradient(135deg, #FEFCBF 0%, #F6E05E 100%);
            border-left: 4px solid #B7791F;
        }
        
        .experience-box {
            background: linear-gradient(135deg, #EBF4FF 0%, #C3DAFE 100%);
            border-left: 4px solid #4C51BF;
        }
        
        .skills-box {
            background: linear-gradient(135deg, #E6FFFA 0%, #B2F5EA 100%);
            border-left: 4px solid #319795;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @media (max-width: 768px) {
            .cv-grid {
                grid-template-columns: 1fr;
            }
        }

        .certificate-gallery {
            margin-top: 2rem;
        }

        .certificate-container {
            margin-bottom: 1.5rem;
            padding: 1rem;
            border: 1px solid #CBD5E0;
            border-radius: 8px;
            background-color: #F7FAFC;
            transition: transform 0.3s;
        }

        .certificate-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .certificate-title {
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: #2C5282;
        }

        .cv-download-button {
            display: inline-block;
            padding: 0.5rem 1rem;
            margin-top: 0.5rem;
            background-color: #3182CE;
            color: white;
            border-radius: 4px;
            text-align: center;
            transition: background-color 0.3s;
        }

        .cv-download-button:hover {
            background-color: #2B6CB0;
        }
    </style>
    """, unsafe_allow_html=True)

# Importaciones adicionales
import os
from PIL import Image
import io
import requests
from utils.contact_components import add_page_footer, add_sidebar_contact

def load_image(image_path, fallback_url=None, width=None):
    """
    Carga una imagen desde una ruta local o URL de fallback.
    """
    try:
        # Intentar cargar imagen local
        if os.path.exists(image_path):
            image = Image.open(image_path)
            if width:
                # Mantener la proporción al redimensionar
                aspect_ratio = image.height / image.width
                height = int(width * aspect_ratio)
                image = image.resize((width, height), Image.Resampling.LANCZOS)
            return image
        
        # Si no existe localmente, intentar fallback URL
        elif fallback_url:
            response = requests.get(fallback_url, timeout=5)
            if response.status_code == 200:
                image = Image.open(io.BytesIO(response.content))
                if width:
                    aspect_ratio = image.height / image.width
                    height = int(width * aspect_ratio)
                    image = image.resize((width, height), Image.Resampling.LANCZOS)
                return image
    except Exception as e:
        st.warning(f"No se pudo cargar la imagen: {str(e)}")
    
    return None

def load_cv_content():
    """Carga el contenido del CV desde el archivo markdown"""
    cv_path = Path(__file__).parent.parent.parent / "docs" / "curriculum.md"
    
    if cv_path.exists():
        return cv_path.read_text(encoding="utf-8")
    else:
        return """
# Daniel Andrés Mardones Sanhueza

## 📊 Data Science | 🔧 Mantenimiento Industrial

> Profesional con más de 10 años de experiencia en mantenimiento industrial,
> transitando hacia el análisis de datos y la ciencia de datos.

### 🎓 Formación

- **Data Science**, Academia Desafío Latam (2023-2024)

### 💼 Experiencia Profesional

#### Técnico de Mantenimiento Senior | Integral Service
*2015 - Presente*
- Optimización de procesos industriales
- Análisis de datos para mantenimiento predictivo
- Gestión de equipos técnicos

#### Jefe de mantenimiento | Nutraseed
*2013 - 2015*
- Implementación de programas de mantenimiento
- Mejora continua de procesos
- Supervisión de operaciones

### 🛠️ Habilidades Técnicas

#### Análisis de Datos
- Python, Pandas, NumPy
- SQL, BigQuery
- Visualización de datos (Plotly, Matplotlib)

#### Mantenimiento Industrial
- PLCs y Vdfs
- Automatización y control
- Análisis de datos para mantenimiento predictivo
- Mantenimiento preventivo y correctivo

### 📫 Contacto

- [LinkedIn](https://www.linkedin.com/in/daniel-andres-mardones-sanhueza-27b73777)
- [GitHub](https://github.com/Denniels)
- [Web](https://integralservicespa.cl)
"""

def load_certificates():
    """Carga los certificados desde la carpeta de certificados"""
    certificates_dir = Path(__file__).parent.parent / "static/images/certificados"
    certificates = []
    
    if certificates_dir.exists():
        # Buscar archivos de imagen y PDF
        for file in certificates_dir.glob("*.*"):
            if file.suffix.lower() in ['.jpg', '.jpeg', '.png', '.pdf']:
                cert_info = {
                    'name': file.stem.replace('_', ' ').title(),
                    'path': str(file),
                    'type': 'pdf' if file.suffix.lower() == '.pdf' else 'image',
                    'date': file.stat().st_mtime  # Usamos la fecha de modificación como fecha del certificado
                }
                certificates.append(cert_info)
    
    # Ordenar por fecha, más reciente primero
    certificates.sort(key=lambda x: x['date'], reverse=True)
    return certificates

def display_certificate_gallery():
    """Muestra la galería de certificados de manera interactiva"""
    st.markdown("""
    <div class="certificate-gallery">
        <h2 class="cv-title">🎓 Certificados y Logros</h2>
    """, unsafe_allow_html=True)
    
    certificates = load_certificates()
    
    if not certificates:
        st.info("No se encontraron certificados en la carpeta.")
        return
    
    # Crear pestañas para filtrar por tipo
    cert_types = list(set(cert['type'] for cert in certificates))
    tabs = st.tabs([type.title() for type in cert_types])
    
    for tab, cert_type in zip(tabs, cert_types):
        with tab:
            filtered_certs = [cert for cert in certificates if cert['type'] == cert_type]
            cols = st.columns(3)
            
            for i, cert in enumerate(filtered_certs):
                with cols[i % 3]:
                    if cert['type'] == 'image':
                        try:
                            image = Image.open(cert['path'])
                            st.image(image, caption=cert['name'], use_column_width=True)
                        except Exception as e:
                            st.error(f"Error al cargar la imagen: {cert['name']}")
                    else:  # PDF
                        # Crear un botón que abra el PDF en una nueva pestaña
                        with open(cert['path'], "rb") as pdf_file:
                            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
                            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="300" type="application/pdf"></iframe>'
                            st.markdown(f"""
                            <div class="certificate-container">
                                <div class="certificate-title">{cert['name']}</div>
                                {pdf_display}
                                <a href="data:application/pdf;base64,{base64_pdf}" download="{cert['name']}.pdf" 
                                   class="cv-download-button" style="margin-top: 1rem; display: block;">
                                   📥 Descargar PDF
                                </a>
                            </div>
                            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Cargar estilos CSS
    load_cv_styles()
    
    # Agregar enlaces de contacto al sidebar
    add_sidebar_contact()
    
    # Título y imagen de perfil
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("📄 Currículum Vitae")
        
        # Cargar imagen de perfil
        profile_image_path = os.path.join(os.path.dirname(__file__), "..", "static", "emoji_python_developer.png")
        profile_image = load_image(
            profile_image_path,
            fallback_url="https://via.placeholder.com/120x120/1f77b4/ffffff?text=👨‍💻",
            width=120
        )
        
        # Mostrar imagen centrada
        if profile_image:
            col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
            with col_img2:
                st.image(profile_image, width=120)
        else:
            st.markdown('<div style="font-size: 80px; text-align: center;">👨‍💻</div>', unsafe_allow_html=True)    # Perfil Profesional
    st.markdown("""
    <div class="cv-section">
        <div class="cv-grid">
            <div class="cv-box">
                <h3 class="cv-title">👨‍💻 Perfil Profesional</h3>
                <div class="cv-text">
                    Emprendedor con más de 10 años de experiencia en mantenimiento de equipos industriales,
                    transitando hacia el análisis de datos y la ciencia de datos. Combino
                    el conocimiento técnico industrial con habilidades analíticas modernas 
                    para optimizar procesos y extraer valor de los datos.
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)    # Sección de Formación
    st.markdown("""
    <div class="cv-section">
        <h2 class="cv-title">🎓 Formación Académica</h2>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">Data Science con Python</h3>
                <div class="cv-text">
                    <strong>Academia Desafío Latam</strong><br>
                    2023-2024<br>
                    • Especialización en análisis de datos<br>
                    • Machine learning y visualización<br>
                    • Proyectos prácticos guiados por expertos<br>
                    • 108 horas declases mas 192 horas de estudio.
                </div>
        </div>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">SQL PARA DATASCIENCE</h3>
                <div class="cv-text">
                    <strong>DATASCIENCE CON PYTHON</strong><br>
                    DIC 2022 A ENE 2023<br>
                    • 18 horas de clases y 18 horas de estudio<br>
                    • Proyectos prácticos guiados por expertos
                </div>
            </div>
        </div>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">MACHINE LEARNING</h3>
                <div class="cv-text">
                    <strong>DATASCIENCE CON PYTHON</strong><br>
                    NOV 2022 A DIC 2022<br>
                    • 48 horas de clases y 48 horas de estudio<br>
                    • Proyectos prácticos guiados por expertos
                </div>
            </div>
        </div>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">FUNDAMENTOS DE DATASCIENCE</h3>
                <div class="cv-text">
                    <strong>DATASCIENCE CON PYTHON</strong><br>
                    SEP 2022 A OCT 2023<br>
                    • 48 horas de clases y 48 horas de estudio<br>
                    • Proyectos prácticos guiados por expertos
                </div>
            </div>
        </div>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">PROGRAMACION CON PYTHON</h3>
                <div class="cv-text">
                    <strong>DATASCIENCE CON PYTHON</strong><br>
                    JUL 2022 A AGO 2023<br>
                    • 24 horas de clases y 24 horas de estudio<br>
                    • Proyectos prácticos guiados por expertos
                </div>
            </div>
        </div>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">INACAP</h3>
                <div class="cv-text">
                    <strong>PROGRAMACION DE PLC</strong><br>
                    MAY 2012 A JUL 2012<br>
                    • Programa académico contempla 40 horas de clases<br>
                    • Proyectos prácticos guiados por expertos
                </div>
            </div>
        </div>
        <div class="cv-grid">
            <div class="cv-box education-box">
                <h3 class="cv-title">SMC</h3>
                <div class="cv-text">
                    <strong>APLICACIÓN DE CONTROL ELECTRO NEUMATICO</strong><br>
                    MAY 2012 A JUL 2012<br>
                    •  30 horas de trabajo distribuidas en 50% teóricas y 50% prácticas.<br>
                    • Proyectos prácticos guiados por expertos
                </div>
            </div>
        </div>""", unsafe_allow_html=True)    

# Sección de Experiencia
    
    st.markdown("""
    <div class="cv-section">
        <h2 class="cv-title">💼 Experiencia Profesional</h2>
        <div class="cv-grid">
            <div class="cv-box experience-box">
                <h3 class="cv-title">Ingeniero de Mantenimiento Senior</h3>
                <div class="cv-text">
                    <strong>Integral Service</strong> | 2015 - Presente<br>
                    • Optimización de procesos industriales<br>
                    • Análisis de datos para mantenimiento predictivo<br>
                    • Gestión de equipos técnicos<br>
                    • Implementación de soluciones de automatización<br>
                    • Desarrollo de dashboards analíticos
                </div>
            </div>
            <div class="cv-box experience-box">
                <h3 class="cv-title">Ingeniero de Planta</h3>
                <div class="cv-text">
                    <strong>Nutraseed</strong> | 2013 - 2015<br>
                    • Implementación de programas de mantenimiento<br>
                    • Mejora continua de procesos<br>
                    • Supervisión de operaciones<br>
                    • Análisis y optimización de eficiencia<br>
                    • Gestión de indicadores KPI
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)    # Sección de Habilidades Técnicas
    st.markdown("""
    <div class="cv-section">
        <h2 class="cv-title">🛠️ Habilidades Técnicas</h2>
        <div class="cv-grid">
            <div class="cv-box skills-box">
                <h3 class="cv-title">Análisis de Datos</h3>
                <div class="cv-text">
                    • Python, Pandas, NumPy<br>
                    • SQL, BigQuery<br>
                    • Visualización (Plotly, Matplotlib)<br>
                    • Análisis estadístico<br>
                    • Machine Learning básico
                </div>
            </div>
            <div class="cv-box skills-box">
                <h3 class="cv-title">Mantenimiento Industrial</h3>
                <div class="cv-text">
                    • PLCs y automatización<br>
                    • Análisis de vibraciones<br>
                    • Mantenimiento predictivo<br>
                    • Gestión de activos<br>
                    • Optimización de procesos
                </div>
            </div>
            <div class="cv-box skills-box">
                <h3 class="cv-title">Herramientas y Tecnologías</h3>
                <div class="cv-text">
                    • Git y GitHub<br>
                    • Streamlit<br>
                    • Jupyter Notebooks<br>
                    • Power BI<br>
                    • APIs REST
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Agregar sección de certificados antes del botón de descarga del CV
    display_certificate_gallery()
    
    # Botón para descargar CV en PDF (simulado)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📄 Descargar CV en PDF", type="primary"):
            st.info("Funcionalidad de descarga en desarrollo. Por ahora puedes guardar esta página como PDF desde tu navegador.")
    
    # Enlaces de contacto en el footer
    add_page_footer()

if __name__ == "__main__":
    main()
