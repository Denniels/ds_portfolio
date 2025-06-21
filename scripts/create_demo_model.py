"""
Script para reentrenar y guardar el modelo con la versión correcta de scikit-learn
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def crear_modelo_demo():
    """
    Crea un modelo de demostración simple compatible con la versión actual de scikit-learn
    """
    # Datos de ejemplo
    np.random.seed(42)
    n_samples = 1000
    
    # Características simuladas del mercado inmobiliario
    X = pd.DataFrame({
        'metros_totales': np.random.uniform(30, 300, n_samples),
        'metros_construidos': np.random.uniform(25, 250, n_samples),
        'dormitorios': np.random.randint(1, 6, n_samples),
        'banos': np.random.randint(1, 5, n_samples),
        'estacionamientos': np.random.randint(0, 4, n_samples),
        'antiguedad_anos': np.random.uniform(0, 40, n_samples)
    })
    
    # Precio simulado (UF)
    y = (X['metros_construidos'] * 50 + 
         X['dormitorios'] * 500 + 
         X['banos'] * 300 + 
         X['estacionamientos'] * 200 - 
         X['antiguedad_anos'] * 10 + 
         np.random.normal(0, 500, n_samples))
    
    # Entrenar modelo
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X, y)
    
    return model

def main():
    """Función principal"""
    # Crear y guardar modelo demo
    model = crear_modelo_demo()
    
    # Guardar en las ubicaciones necesarias
    model_paths = [
        Path(__file__).parent / 'app' / 'models' / 'modelo_demo.pkl',
        Path(__file__).parent / 'app' / 'data' / 'processed' / 'modelo_inmobiliario.pkl'
    ]
    
    for path in model_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, path)
        print(f"Modelo guardado en: {path}")

if __name__ == "__main__":
    main()
