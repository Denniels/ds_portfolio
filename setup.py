from setuptools import setup, find_packages

setup(
    name="ds_portfolio",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.28.0",
        "pandas==2.0.3",
        "numpy==1.26.4",
        "scipy==1.11.4",
        "scikit-learn==1.7.0",
        "joblib==1.2.0",
        "threadpoolctl==3.2.0",
        "streamlit-folium==0.15.0",
        "folium==0.14.0",
    ],
    python_requires=">=3.9",
)
