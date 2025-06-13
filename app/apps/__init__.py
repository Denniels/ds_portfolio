"""
Apps del Portafolio de Data Science
==================================

Este paquete contiene todas las aplicaciones individuales del portafolio.
"""

__version__ = "1.0.0"
__author__ = "Data Scientist"

# Importamos las clases principales de cada aplicación
try:
    from .feedback_system import FeedbackApp
except ImportError:
    pass

from .budget_analysis_app import BudgetAnalysisApp
from .water_quality_app import WaterQualityApp
from .co2_emissions_app import CO2EmissionsApp
from .demographics_app import DemographicsApp
