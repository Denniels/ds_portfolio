"""
Utilidades de seguridad para prevenir uso accidental de servicios cloud
"""
import json
from pathlib import Path
import streamlit as st

class SecurityManager:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config" / "environment.json"
        self.load_config()

    def load_config(self):
        """Carga la configuración del entorno"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            st.error(f"Error cargando configuración: {str(e)}")
            self.config = {"environment": "local", "gcp": {"enabled": False}}

    def prevent_cloud_services(self):
        """Previene el uso accidental de servicios cloud"""
        if self.config.get("security", {}).get("prevent_cloud_calls", True):
            import google.cloud
            def blocked_auth(*args, **kwargs):
                raise Exception(
                    "🚫 Acceso a servicios cloud bloqueado en modo local. " +
                    "Revisa la configuración en config/environment.json"
                )
            google.cloud.client.Client._credentials = property(blocked_auth)

    def is_cloud_allowed(self):
        """Verifica si se permiten llamadas a servicios cloud"""
        return not self.config.get("security", {}).get("local_only", True)

    def check_environment(self):
        """Muestra advertencia si se intenta usar servicios cloud en modo local"""
        if self.config["environment"] == "local":
            st.warning("""
            ⚠️ Ejecutando en modo local
            - Los servicios cloud están deshabilitados
            - Los datos se cargan desde archivos locales
            - Las llamadas a GCP están bloqueadas
            """)

# Uso:
# security = SecurityManager()
# security.prevent_cloud_services()
# security.check_environment()
