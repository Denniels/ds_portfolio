"""
Script para regenerar el modelo de predicción inmobiliaria 
usando las versiones actuales de numpy y scikit-learn
"""
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def regenerate_model():
    # Usar datos sintéticos similares a los reales para el ejemplo
    np.random.seed(42)
    n_samples = 1000
    
    # Generar features sintéticos
    data = {
        'metros_totales': np.random.normal(100, 30, n_samples),
        'metros_utiles': np.random.normal(80, 25, n_samples),
        'dormitorios': np.random.randint(1, 5, n_samples),
        'banos': np.random.randint(1, 4, n_samples),
        'estacionamientos': np.random.randint(0, 3, n_samples),
        'comuna_score': np.random.uniform(0.3, 1.0, n_samples),
    }
    
    # Calcular precio sintético basado en los features
    precio_base = 3000  # UF por metro cuadrado base
    precios = []
    
    for i in range(n_samples):
        precio = (data['metros_totales'][i] * precio_base * 
                 (1 + data['comuna_score'][i]) * 
                 (1 + 0.1 * data['dormitorios'][i]) * 
                 (1 + 0.15 * data['banos'][i]) * 
                 (1 + 0.05 * data['estacionamientos'][i]))
        precios.append(precio * (1 + np.random.normal(0, 0.1)))  # Añadir ruido
    
    data['precio_uf'] = precios
    df = pd.DataFrame(data)
    
    # Separar features y target
    X = df.drop('precio_uf', axis=1)
    y = df['precio_uf']
    
    # Split train-test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar modelo
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Crear directorio si no existe
    model_dir = os.path.join('app', 'data', 'modelos')
    os.makedirs(model_dir, exist_ok=True)
    
    # Guardar modelo
    model_path = os.path.join(model_dir, 'modelo_ensemble.pkl')
    joblib.dump(model, model_path)
    print(f"Modelo regenerado y guardado en: {model_path}")
    print(f"Versiones utilizadas:")
    print(f"numpy: {np.__version__}")
    print(f"scikit-learn: {pd.__version__}")
    print(f"joblib: {joblib.__version__}")

if __name__ == "__main__":
    regenerate_model()
