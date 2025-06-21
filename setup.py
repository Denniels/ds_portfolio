from setuptools import setup, find_packages

setup(
    name="ds_portfolio",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.28.0",
        "pandas>=2.1.0",
        "numpy>=1.26.0",
        "scipy>=1.11.0",
        "scikit-learn>=1.3.0",
        "joblib>=1.3.0",
        "threadpoolctl>=3.2.0",
    ],
    python_requires=">=3.9",
)
