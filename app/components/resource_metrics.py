"""
Componente para mostrar métricas de recursos y costos en la aplicación.
"""

import streamlit as st
import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar módulos locales
root_dir = Path(__file__).parent.parent.parent
sys.path.append(str(root_dir))

from utils.optimization import ResourceOptimizer, format_cost, format_resource

def display_resource_metrics():
    """Muestra las métricas de recursos en la interfaz"""
    optimizer = ResourceOptimizer()
    summary = optimizer.get_resource_summary()
    
    if not summary:
        st.warning("No hay datos de uso de recursos disponibles")
        return
    
    st.sidebar.markdown("### 📊 Métricas de Recursos")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        st.metric(
            "Costo Total Estimado",
            format_cost(summary.get('total_cost', 0))
        )
        st.metric(
            "CPU Total",
            format_resource(summary.get('total_cpu_seconds', 0), "vCPU-s")
        )
    
    with col2:
        st.metric(
            "Memoria Total",
            format_resource(summary.get('total_memory_gib_seconds', 0), "GiB-s")
        )
        st.metric(
            "Requests Totales",
            str(summary.get('total_requests', 0))
        )
    
    if st.sidebar.checkbox("Mostrar detalles de costos"):
        st.sidebar.markdown("#### Desglose de Costos")
        st.sidebar.markdown(f"""
        - Costo promedio por request: {format_cost(summary.get('average_cost_per_request', 0))}
        - Última actualización: {summary.get('last_updated', 'No disponible')}
        """)
        
        # Proyección a GCP
        st.sidebar.markdown("#### Proyección GCP")
        monthly_requests = summary.get('total_requests', 0) * 30  # estimación mensual
        st.sidebar.markdown(f"""
        Uso mensual estimado:
        - Requests: {monthly_requests:,}
        - % del límite gratuito: {(monthly_requests / 2_000_000) * 100:.2f}%
        """)

def track_page_view():
    """Registra una vista de página para métricas"""
    optimizer = ResourceOptimizer()
    optimizer.start_monitoring()
    return optimizer
