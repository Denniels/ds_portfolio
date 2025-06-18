"""
Módulo de integración con APIs populares para el Generador de Reportes
Facilita la conexión con fuentes de datos comunes
"""
import requests
import pandas as pd
import json
from datetime import datetime, timedelta
import streamlit as st

class APIConnector:
    """Conector para APIs populares de datos de negocio"""
    
    @staticmethod
    def get_google_analytics_sample():
        """Simulación de datos de Google Analytics"""
        # En producción, esto se conectaría a la API real de GA
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = {
            'date': dates,
            'sessions': np.random.poisson(1000, len(dates)),
            'users': np.random.poisson(800, len(dates)),
            'pageviews': np.random.poisson(2500, len(dates)),
            'bounce_rate': np.random.uniform(0.3, 0.7, len(dates)),
            'avg_session_duration': np.random.uniform(120, 300, len(dates)),
            'conversions': np.random.poisson(50, len(dates))
        }
        return pd.DataFrame(data)
    
    @staticmethod
    def get_facebook_ads_sample():
        """Simulación de datos de Facebook Ads"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = {
            'date': dates,
            'impressions': np.random.poisson(10000, len(dates)),
            'clicks': np.random.poisson(200, len(dates)),
            'spend': np.random.uniform(50, 500, len(dates)),
            'cpm': np.random.uniform(5, 25, len(dates)),
            'ctr': np.random.uniform(1, 5, len(dates)),
            'conversions': np.random.poisson(10, len(dates))
        }
        df = pd.DataFrame(data)
        df['cpc'] = df['spend'] / df['clicks']
        df['conversion_rate'] = (df['conversions'] / df['clicks']) * 100
        return df
    
    @staticmethod
    def get_salesforce_sample():
        """Simulación de datos de Salesforce CRM"""
        data = {
            'opportunity_id': [f'OPP-{i:05d}' for i in range(1, 501)],
            'account_name': [f'Empresa {i}' for i in range(1, 501)],
            'stage': np.random.choice(['Prospecting', 'Qualification', 'Proposal', 'Closed Won', 'Closed Lost'], 500),
            'amount': np.random.uniform(5000, 100000, 500),
            'probability': np.random.uniform(10, 95, 500),
            'close_date': pd.date_range(start='2024-01-01', periods=500, freq='D'),
            'lead_source': np.random.choice(['Website', 'Referral', 'Cold Call', 'Trade Show'], 500),
            'industry': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Retail'], 500)
        }
        df = pd.DataFrame(data)
        df['expected_value'] = df['amount'] * (df['probability'] / 100)
        return df
    
    @staticmethod
    def get_stripe_sample():
        """Simulación de datos de pagos de Stripe"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='H')
        data = {
            'transaction_id': [f'ch_{i}' for i in range(len(dates))],
            'timestamp': dates,
            'amount': np.random.exponential(50, len(dates)),
            'currency': 'USD',
            'status': np.random.choice(['succeeded', 'failed', 'pending'], len(dates), p=[0.9, 0.05, 0.05]),
            'customer_id': [f'cus_{i%1000}' for i in range(len(dates))],
            'payment_method': np.random.choice(['card', 'bank_transfer', 'digital_wallet'], len(dates)),
            'country': np.random.choice(['CL', 'US', 'BR', 'AR', 'MX'], len(dates))
        }
        df = pd.DataFrame(data)
        df['fee'] = df['amount'] * 0.029 + 0.30  # Stripe fee structure
        df['net_amount'] = df['amount'] - df['fee']
        return df
    
    @staticmethod
    def get_hubspot_sample():
        """Simulación de datos de HubSpot marketing"""
        data = {
            'contact_id': range(1, 1001),
            'email': [f'user{i}@empresa{i%100}.com' for i in range(1, 1001)],
            'lifecycle_stage': np.random.choice(['subscriber', 'lead', 'mql', 'sql', 'customer'], 1000),
            'lead_score': np.random.randint(0, 100, 1000),
            'last_activity': pd.date_range(end='2024-12-31', periods=1000, freq='D'),
            'email_opens': np.random.poisson(5, 1000),
            'email_clicks': np.random.poisson(2, 1000),
            'page_views': np.random.poisson(10, 1000),
            'form_submissions': np.random.poisson(1, 1000),
            'deal_value': np.random.exponential(1000, 1000)
        }
        df = pd.DataFrame(data)
        df['engagement_score'] = (df['email_opens'] + df['email_clicks'] * 2 + df['page_views'] + df['form_submissions'] * 5)
        return df

class DataValidator:
    """Valida y limpia datos ingresados"""
    
    @staticmethod
    def validate_dataframe(df):
        """Valida que el DataFrame sea válido para análisis"""
        issues = []
        
        if df is None or df.empty:
            issues.append("❌ DataFrame está vacío")
            return False, issues
        
        # Verificar tamaño mínimo
        if len(df) < 2:
            issues.append("⚠️ Dataset muy pequeño (menos de 2 registros)")
        
        # Verificar si hay al menos una columna numérica
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            issues.append("⚠️ No se encontraron columnas numéricas para análisis")
        
        # Verificar porcentaje de valores faltantes
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        if missing_pct > 50:
            issues.append(f"⚠️ Alto porcentaje de valores faltantes ({missing_pct:.1f}%)")
        elif missing_pct > 20:
            issues.append(f"ℹ️ Porcentaje moderado de valores faltantes ({missing_pct:.1f}%)")
          # Verificar duplicados (solo en columnas hashables)
        try:
            duplicates = df.duplicated().sum()
            if duplicates > 0:
                issues.append(f"ℹ️ {duplicates} registros duplicados encontrados")
        except TypeError:
            # Si hay columnas no hashables, verificar solo columnas básicas
            try:
                hashable_cols = []
                for col in df.columns:
                    try:
                        # Intentar verificar si la columna es hashable
                        df[col].duplicated()
                        hashable_cols.append(col)
                    except TypeError:
                        continue
                
                if hashable_cols:
                    duplicates = df[hashable_cols].duplicated().sum()
                    if duplicates > 0:
                        issues.append(f"ℹ️ {duplicates} registros duplicados encontrados (columnas analizables)")
                else:
                    issues.append("ℹ️ No se pudo verificar duplicados (tipos de datos complejos)")
            except Exception:
                issues.append("ℹ️ No se pudo verificar duplicados (tipos de datos complejos)")
          # Verificar columnas con una sola valor único (solo en columnas hashables)
        try:
            single_value_cols = [col for col in df.columns if df[col].nunique() == 1]
            if single_value_cols:
                issues.append(f"ℹ️ Columnas con valor único: {', '.join(single_value_cols)}")
        except TypeError:
            # Si hay problemas con tipos no hashables, verificar columna por columna
            single_value_cols = []
            for col in df.columns:
                try:
                    if df[col].nunique() == 1:
                        single_value_cols.append(col)
                except (TypeError, ValueError):
                    continue
            if single_value_cols:
                issues.append(f"ℹ️ Columnas con valor único: {', '.join(single_value_cols)}")
        
        return True, issues
    
    @staticmethod
    def suggest_data_types(df):
        """Sugiere tipos de datos mejorados"""
        suggestions = []
        
        for col in df.columns:
            current_dtype = str(df[col].dtype)
            
            # Detectar fechas
            if df[col].dtype == 'object':
                # Intentar convertir a fecha
                try:
                    pd.to_datetime(df[col], errors='raise')
                    suggestions.append(f"📅 '{col}' parece ser una fecha")
                except:
                    pass
                  # Detectar booleanos (con manejo de tipos no hashables)
                try:
                    unique_vals = df[col].dropna().unique()
                    if len(unique_vals) == 2 and all(str(v).lower() in ['true', 'false', '1', '0', 'yes', 'no', 'si', 'no'] for v in unique_vals):
                        suggestions.append(f"✅ '{col}' parece ser booleano")
                except (TypeError, ValueError):
                    # No se puede obtener valores únicos para tipos no hashables
                    pass
                
                # Detectar categorías (con manejo de tipos no hashables)
                try:
                    unique_count = df[col].nunique()
                    if unique_count < 20 and unique_count > 2:
                        suggestions.append(f"🏷️ '{col}' podría ser categórica ({unique_count} valores únicos)")
                except (TypeError, ValueError):
                    # No se puede contar valores únicos para tipos no hashables
                    pass
              # Detectar IDs (con manejo de tipos no hashables)
            if col.lower() in ['id', 'index', 'key'] or 'id' in col.lower():
                try:
                    if df[col].nunique() == len(df):
                        suggestions.append(f"🆔 '{col}' parece ser un identificador único")
                except (TypeError, ValueError):
                    # No se puede verificar unicidad para tipos no hashables
                    pass
        
        return suggestions

class ReportTemplates:
    """Templates predefinidos para diferentes tipos de reportes"""
    
    @staticmethod
    def get_marketing_template():
        """Template para reportes de marketing"""
        return {
            "title": "📊 Reporte de Marketing Digital",
            "sections": [
                "Resumen Ejecutivo",
                "Métricas de Tráfico",
                "Conversiones y ROI",
                "Análisis de Canales",
                "Recomendaciones"
            ],
            "key_metrics": ["impressions", "clicks", "conversions", "spend", "ctr", "cpc"],
            "visualizations": ["time_series", "channel_comparison", "funnel"]
        }
    
    @staticmethod
    def get_sales_template():
        """Template para reportes de ventas"""
        return {
            "title": "💰 Reporte de Ventas",
            "sections": [
                "Resumen de Resultados",
                "Pipeline de Oportunidades",
                "Análisis por Vendedor",
                "Tendencias Temporales",
                "Proyecciones"
            ],
            "key_metrics": ["revenue", "deals_closed", "conversion_rate", "avg_deal_size"],
            "visualizations": ["revenue_trend", "pipeline_stages", "rep_performance"]
        }
    
    @staticmethod
    def get_financial_template():
        """Template para reportes financieros"""
        return {
            "title": "💵 Reporte Financiero",
            "sections": [
                "Estado de Resultados",
                "Flujo de Caja",
                "Análisis de Rentabilidad",
                "KPIs Financieros",
                "Variaciones vs Presupuesto"
            ],
            "key_metrics": ["revenue", "expenses", "profit", "roi", "cash_flow"],
            "visualizations": ["income_statement", "cash_flow", "profitability"]
        }
    
    @staticmethod
    def get_operations_template():
        """Template para reportes operacionales"""
        return {
            "title": "⚙️ Reporte Operacional",
            "sections": [
                "KPIs Operacionales",
                "Eficiencia de Procesos",
                "Calidad y Satisfacción",
                "Recursos y Capacidad",
                "Mejoras Propuestas"
            ],
            "key_metrics": ["efficiency", "quality_score", "capacity_utilization", "downtime"],
            "visualizations": ["efficiency_trends", "quality_metrics", "capacity_analysis"]
        }

# Importar numpy si no está disponible
try:
    import numpy as np
except ImportError:
    st.error("NumPy es requerido para generar datos demo. Instálalo con: pip install numpy")
    np = None
