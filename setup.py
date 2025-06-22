from setuptools import setup, find_packages

# Configuración optimizada para Streamlit Cloud
setup(
    name="ds_portfolio",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Dependencias core con rangos compatibles
        "streamlit>=1.28.0,<1.32.0",
        "pandas>=2.0.0,<2.1.0",
        "numpy>=1.22.0,<1.25.0",
        "scipy>=1.10.0,<1.11.0",
        "scikit-learn>=1.2.0,<1.4.0",
        "joblib>=1.1.0,<1.3.0",
        "threadpoolctl>=3.1.0",
        "streamlit-folium>=0.13.0",
        "folium>=0.13.0",
        
        # Garantizar disponibilidad de dependencias críticas
        "matplotlib>=3.7.0,<3.8.0",
        "plotly>=5.10.0",
        "cython>=0.29.30",
        "wheel>=0.37.0",
    ],
    python_requires=">=3.9,<3.11",
    # Configuración adicional para instalación
    zip_safe=False,
    include_package_data=True,
)
