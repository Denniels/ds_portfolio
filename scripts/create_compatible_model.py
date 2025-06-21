"""
Script para crear modelo compatible con la versión específica de scikit-learn en Streamlit Cloud
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

def create_compatible_model():
    """
    Crea un modelo asegurando compatibilidad con la estructura de nodos esperada
    """
    # Datos de ejemplo para el mercado inmobiliario chileno
    np.random.seed(42)
    n_samples = 1000
    
    # Features con distribuciones más realistas
    data = {
        'metros_totales': np.random.normal(120, 40, n_samples).clip(30, 300),
        'metros_construidos': np.random.normal(100, 35, n_samples).clip(25, 250),
        'dormitorios': np.random.randint(1, 6, n_samples),
        'banos': np.random.randint(1, 5, n_samples),
        'estacionamientos': np.random.randint(0, 4, n_samples),
        'antiguedad_anos': np.random.exponential(10, n_samples).clip(0, 40),
        'comuna_valor': np.random.normal(50, 15, n_samples).clip(20, 100)  # Índice socioeconómico simulado
    }
    
    X = pd.DataFrame(data)
    
    # Precio base por metro cuadrado (UF) según comuna
    precio_base = data['comuna_valor'] * 2
    
    # Cálculo de precio más realista
    y = (
        precio_base * X['metros_construidos'] * 0.8 +  # Precio base por m²
        X['dormitorios'] * 500 +                       # Valor por dormitorio
        X['banos'] * 300 +                            # Valor por baño
        X['estacionamientos'] * 200 -                 # Valor por estacionamiento
        X['antiguedad_anos'] * 15 +                   # Depreciación por antigüedad
        np.random.normal(0, 500, n_samples)           # Variación aleatoria
    ).clip(1000, 20000)  # Rango realista de precios en UF
    
    # Normalizar features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Entrenar modelo con parámetros específicos para compatibilidad
    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1
    )
    
    # Entrenar con datos escalados
    model.fit(X_scaled, y)
    
    # Guardar también el scaler
    return model, scaler

def save_model():
    """Guarda el modelo y el scaler en las ubicaciones necesarias"""
    model, scaler = create_compatible_model()
    
    # Directorios donde guardar el modelo
    paths = [
        Path('app/models'),
        Path('app/data/processed'),
        Path('app/data/inmobiliario')
    ]
    
    # Crear directorios si no existen
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo y scaler
        joblib.dump(model, path / 'modelo_inmobiliario.pkl', compress=3)
        joblib.dump(scaler, path / 'scaler_inmobiliario.pkl', compress=3)
        
        print(f"✓ Modelo guardado en: {path / 'modelo_inmobiliario.pkl'}")
        print(f"✓ Scaler guardado en: {path / 'scaler_inmobiliario.pkl'}")

if __name__ == "__main__":
    print("🔄 Creando y guardando modelo compatible...")
    save_model()
    print("✨ ¡Proceso completado con éxito!")
