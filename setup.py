from setuptools import setup, find_packages

setup(
    name="ds_portfolio",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.28.0",
        "pandas==2.0.3",
        "numpy==1.24.3",
        "scipy==1.10.1",
        "scikit-learn==1.2.2",
        "joblib==1.2.0",
        "threadpoolctl==3.1.0",
    ],
    python_requires=">=3.9,<3.12",
)
