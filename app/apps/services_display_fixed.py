"""
Visualizador de Servicios Profesionales
=======================================
Muestra el catálogo de servicios profesionales disponibles
con sus respectivas tarifas en pesos chilenos y UF.
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path
import re
import sys

# Importar el componente de valor UF
components_dir = Path(__file__).parent / "components"
if str(components_dir) not in sys.path:
    sys.path.insert(0, str(components_dir))
try:
    from uf_value_component import get_uf_component
    UF_COMPONENT_AVAILABLE = True
except ImportError:
    UF_COMPONENT_AVAILABLE = False

class ServicesDisplay:
    def __init__(self):
        self.services_file = Path(__file__).parent.parent.parent / "SERVICIOS.md"
        
        # Inicializar variables de estado de sesión si no existen
        if 'show_price_justification' not in st.session_state:
            st.session_state.show_price_justification = False
        
    def _extract_tables_from_md(self, md_content):
        """Extrae las tablas de markdown y las convierte a DataFrames"""
        # Regex para encontrar secciones y tablas
        section_pattern = r'##\s+(.+?)\n\n\|\s+(.+?)\n\|[-\s\|]+\n((?:\|.+?\n)+)'
        sections = re.findall(section_pattern, md_content)
        
        tables = {}
        for section_name, header, rows in sections:
            # Limpiar el nombre de la sección
            clean_section = section_name.strip()
            if "📋" in clean_section or "🔍" in clean_section or "📞" in clean_section:
                continue  # Ignorar secciones que no son catálogos de servicios
                
            # Procesar encabezados
            headers = [h.strip() for h in header.split('|')]
            headers = [h for h in headers if h]  # Eliminar elementos vacíos
            
            # Procesar filas
            data = []
            for row in rows.strip().split('\n'):
                cols = [col.strip() for col in row.split('|')]
                cols = [col for col in cols if col]  # Eliminar elementos vacíos
                if cols:
                    data.append(cols)
            
            # Crear DataFrame
            try:
                tables[clean_section] = pd.DataFrame(data, columns=headers)
            except Exception as e:
                st.error(f"Error al procesar tabla {clean_section}: {str(e)}")
                continue
                
        return tables
        
    def read_services(self):
        """Lee el archivo de servicios y extrae la información"""
        try:
            if not self.services_file.exists():
                return None
                
            with open(self.services_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            return self._extract_tables_from_md(content)        
        except Exception as e:
            st.error(f"Error al leer el archivo de servicios: {str(e)}")
            return None
            
    def _convert_to_uf(self, clp_value, uf_value):
        """Convierte un valor en pesos chilenos a UF"""
        try:
            # Verificar si es un string con formato de moneda
            if isinstance(clp_value, str):
                # Eliminar símbolos de moneda y separadores
                clp_clean = clp_value.replace('$', '').replace('.', '').replace(',', '')
                clp_value = float(clp_clean)
            
            # Calcular valor en UF y formatear
            uf_result = clp_value / uf_value
            return f"{uf_result:.2f} UF"
        except Exception:
            return "N/A"
    
    def run(self):
        """Ejecuta la aplicación de visualización de servicios"""
        # Mostrar el componente UF en la barra lateral
        if UF_COMPONENT_AVAILABLE:
            try:
                uf_component = get_uf_component()
                uf_component.render_sidebar()
                uf_value = uf_component.get_uf_value()["valor"]
            except Exception as e:
                st.sidebar.warning(f"No se pudo cargar el valor de la UF: {str(e)}")
                uf_value = 39000  # Valor por defecto
        else:
            uf_value = 39000  # Valor por defecto
        
        st.markdown("""
        <div style='background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='color: white; text-align: center;'>💼 Servicios Profesionales</h1>
            <p style='color: white; text-align: center; font-size: 1.2rem;'>
                Catálogo de servicios disponibles con tarifas referenciales en pesos chilenos y UF
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Introducción
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            Este catálogo presenta los servicios profesionales basados en las habilidades y proyectos 
            demostrados en este portafolio. Las tarifas son referenciales para el mercado chileno (2025).
            
            Para solicitar una cotización personalizada o para discutir un proyecto específico, 
            por favor utiliza el formulario de contacto o escríbeme directamente.
            """)
            
            # Botón para ver justificación de precios
            if st.button("📋 Ver Justificación de Precios"):
                st.session_state.show_price_justification = True
            
        with col2:
            if UF_COMPONENT_AVAILABLE:
                try:
                    uf_component.render_compact()
                except:
                    st.info(f"UF: $39.000 (valor referencial)")
            else:
                st.info(f"UF: $39.000 (valor referencial)")
        
        # Mostrar justificación de precios si se ha solicitado
        if st.session_state.get("show_price_justification", False):
            st.markdown("---")
            st.markdown("## 📊 Justificación de Precios")
            
            # Botón para cerrar
            if st.button("✖️ Cerrar justificación", key="close_justification"):
                st.session_state.show_price_justification = False
                st.rerun()
                
            # Contenido de la justificación
            st.markdown("""
            ### 📝 Metodología de estimación de precios
            
            Los precios establecidos en el catálogo de servicios se basan en una combinación de los siguientes factores:
            
            #### 1. Investigación de mercado (Chile, 2025)
            
            - **Consultoras tecnológicas**: Tarifas promedio de empresas como Everis, Accenture, Bain & Company
            - **Freelancers especializados**: Rango de precios en plataformas como Workana y GetOnBoard
            - **Empresas de Data Science locales**: Cotizaciones referenciales para proyectos similares
            
            #### 2. Factores técnicos considerados
            
            - **Complejidad técnica**: Nivel de especialización y conocimientos avanzados requeridos
            - **Tiempo de desarrollo**: Horas-hombre estimadas para completar cada proyecto/servicio
            - **Recursos tecnológicos**: Costos asociados a infraestructura, licencias y herramientas
            - **Mantenimiento**: Esfuerzo post-implementación requerido
            
            #### 3. Valor comercial para el cliente
            
            - **ROI estimado**: Retorno sobre la inversión esperado para el cliente
            - **Criticidad**: Impacto del servicio en procesos clave del negocio
            - **Escalabilidad**: Capacidad de crecimiento de la solución implementada
            - **Ventaja competitiva**: Valor diferencial que aporta al negocio del cliente
            
            ### 💰 Referencias de mercado por categoría
            
            - **Dashboard y Visualización**: Entre $1.200.000 y $3.000.000 CLP para soluciones corporativas
            - **Análisis Geoespacial**: Entre $1.000.000 y $3.500.000 CLP según complejidad
            - **Análisis Sectorial**: Entre $2.200.000 y $3.500.000 CLP para estudios completos
            - **Machine Learning e IA**: Entre $2.500.000 y $5.000.000 CLP según complejidad
            - **Desarrollo e Implementación**: Entre $1.800.000 y $3.000.000 CLP para soluciones personalizadas
            - **Capacitación y Consultoría**: Entre $1.200.000 y $3.500.000 CLP según alcance y duración
            """)
            
            st.markdown("---")
        
        # Leer servicios
        services = self.read_services()
        
        if not services:
            st.warning("No se pudo cargar el catálogo de servicios. Por favor, inténtalo más tarde.")
            return
        
        # Checkbox para mostrar valores en UF
        show_uf_values = st.checkbox("Mostrar valores en UF", value=True)
        
        # Mostrar servicios por categoría
        for category, df in services.items():
            with st.expander(f"{category}", expanded=True):
                # Botón para abrir detalles completos
                if st.button(f"📋 Ver detalles de {category}", key=f"details_{category}"):
                    st.session_state[f"show_details_{category}"] = True
                
                # Si se ha solicitado ver detalles completos
                if st.session_state.get(f"show_details_{category}", False):
                    # Botón para cerrar detalles
                    if st.button(f"✖️ Cerrar detalles", key=f"close_{category}"):
                        st.session_state[f"show_details_{category}"] = False
                        st.rerun()
                
                # Crear una copia del dataframe para modificar
                display_df = df.copy()
                
                # Añadir columna de UF si es necesario
                if show_uf_values:
                    if 'Valor (CLP)' in df.columns:
                        # Convertir valores de pesos a UF
                        try:
                            # Extraer valores numéricos
                            display_df['Valor (UF)'] = display_df['Valor (CLP)'].apply(
                                lambda x: self._convert_to_uf(x, uf_value)
                            )
                            # Reordenar columnas para mostrar CLP y UF juntos
                            cols = list(display_df.columns)
                            clp_index = cols.index('Valor (CLP)')
                            cols.insert(clp_index + 1, cols.pop(-1))  # Mover 'Valor (UF)' después de 'Valor (CLP)'
                            display_df = display_df[cols]
                        except Exception as e:
                            st.warning(f"No se pudieron convertir los valores a UF: {str(e)}")
                    
                    elif 'Valor Desde (CLP)' in df.columns:
                        # Convertir valores de pesos a UF
                        try:
                            display_df['Valor Desde (UF)'] = display_df['Valor Desde (CLP)'].apply(
                                lambda x: self._convert_to_uf(x, uf_value)
                            )
                            # Reordenar columnas
                            cols = list(display_df.columns)
                            clp_index = cols.index('Valor Desde (CLP)')
                            cols.insert(clp_index + 1, cols.pop(-1))
                            display_df = display_df[cols]
                        except Exception as e:
                            st.warning(f"No se pudieron convertir los valores a UF: {str(e)}")
                
                # Mostrar la tabla
                st.table(display_df)
                
                # Si estamos mostrando detalles completos, agregamos información adicional
                if st.session_state.get(f"show_details_{category}", False):
                    st.markdown("### Detalles adicionales")
                    
                    if "📊 Análisis de Datos" in category:
                        st.markdown("""
                        #### Beneficios principales
                        - **Toma de decisiones basada en datos**: Visualización clara de KPIs y métricas clave
                        - **Acceso en tiempo real**: Información actualizada automáticamente cuando se necesita
                        - **Personalización completa**: Adaptado a las necesidades específicas de tu organización
                        
                        #### Proceso de trabajo
                        1. Reunión inicial para definición de necesidades y objetivos
                        2. Diseño de wireframes y maquetas de visualizaciones
                        3. Desarrollo del dashboard con revisiones periódicas
                        4. Pruebas y ajustes finales
                        5. Entrega con documentación y capacitación
                        
                        #### Tecnologías utilizadas
                        - Power BI, Tableau, o Streamlit según necesidades
                        - Conexiones API a múltiples fuentes de datos
                        - Alojamiento en la nube para acceso universal
                        """)
                    
                    elif "🌎 Análisis Geoespacial" in category:
                        st.markdown("""
                        #### Beneficios principales
                        - **Visualización territorial**: Comprensión clara de la distribución geográfica
                        - **Identificación de patrones espaciales**: Detección de clusters y correlaciones geográficas
                        - **Toma de decisiones territoriales**: Optimización de recursos por ubicación
                        
                        #### Proceso de trabajo
                        1. Análisis de datos georreferenciados disponibles
                        2. Limpieza y normalización de coordenadas
                        3. Desarrollo de visualizaciones interactivas
                        4. Análisis espacial avanzado según objetivos
                        5. Entrega con recomendaciones estratégicas
                        
                        #### Tecnologías utilizadas
                        - QGIS, ArcGIS, Folium, Leaflet
                        - Geocodificación avanzada
                        - Análisis espacial con GeoPandas y PostGIS
                        """)
                    
                    elif "🧠 Machine Learning" in category:
                        st.markdown("""
                        #### Beneficios principales
                        - **Predicciones precisas**: Modelos entrenados específicamente para tu negocio
                        - **Automatización de procesos analíticos**: Reducción de tiempo y errores humanos
                        - **Extracción de patrones ocultos**: Descubrimiento de relaciones no evidentes
                        
                        #### Proceso de trabajo
                        1. Exploración y preparación de datos
                        2. Feature engineering y selección de variables
                        3. Entrenamiento y validación de modelos
                        4. Optimización de hiperparámetros
                        5. Implementación en producción con monitoreo
                        
                        #### Tecnologías utilizadas
                        - Scikit-learn, TensorFlow, PyTorch
                        - MLflow para gestión del ciclo de vida
                        - Docker para despliegue
                        """)
                    
                    elif "🔍 Análisis Sectorial" in category:
                        st.markdown("""
                        #### Beneficios principales
                        - **Comprensión profunda del sector**: Análisis basado en datos oficiales y tendencias actuales
                        - **Benchmarking sectorial**: Posicionamiento relativo frente a estándares del sector
                        - **Identificación de oportunidades**: Detección de nichos y áreas de mejora
                        
                        #### Proceso de trabajo
                        1. Recopilación de datos públicos y privados del sector
                        2. Análisis comparativo y contextual
                        3. Modelado de escenarios y proyecciones
                        4. Desarrollo de visualizaciones específicas
                        5. Recomendaciones estratégicas documentadas
                        
                        #### Fuentes de datos utilizadas
                        - Registros gubernamentales (RETC, SISS, INE)
                        - APIs públicas nacionales e internacionales
                        - Bases de datos sectoriales especializadas
                        """)
                        
                    st.button(f"💬 Solicitar cotización para {category}", key=f"quote_{category}")
                    st.markdown("---")
        
        # Consideraciones
        st.markdown("""
        ### 🔍 Consideraciones
        
        - Los valores son referenciales para proyectos estándar y pueden ajustarse según requerimientos específicos.
        - Todos los servicios incluyen reuniones de levantamiento, informes de avance y documentación final.
        - Los precios no incluyen IVA ni otros impuestos aplicables.
        - Para proyectos que requieran licencias de software adicionales, estas se cotizarán por separado.
        - Disponible descuento por contratación de múltiples servicios o proyectos recurrentes.
        """)
        
        # Formulario de contacto
        st.markdown("---")
        st.markdown("### 📞 ¿Interesado en algún servicio?")
        
        with st.form("service_inquiry_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Nombre")
                email = st.text_input("Email")
                
            with col2:
                service_category = st.selectbox(
                    "Categoría de servicio",
                    options=list(services.keys())
                )
                
                if service_category and service_category in services:
                    service_options = services[service_category]["Servicio"].tolist() if "Servicio" in services[service_category].columns else ["Otro"]
                    service = st.selectbox("Servicio específico", options=service_options)
                
            message = st.text_area("Mensaje", placeholder="Describe brevemente tu proyecto o necesidad...")
            
            submit = st.form_submit_button("Enviar consulta")
            
            if submit:
                if name and email and message:
                    # Aquí podrías integrar con un sistema de CRM o simplemente enviar por email
                    st.success("¡Gracias por tu interés! Te contactaremos a la brevedad.")
                    # En una implementación real, aquí enviarías el formulario a un sistema de CRM o email
                else:
                    st.warning("Por favor completa todos los campos requeridos.")
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem; margin-top: 3rem;'>
            <p>Portafolio de Data Science © 2025</p>
            <p>Servicios profesionales actualizados: Junio 2025</p>
        </div>
        """, unsafe_allow_html=True)


# Crear instancia y ejecutar
def run():
    app = ServicesDisplay()
    app.run()
    
if __name__ == "__main__":
    run()
