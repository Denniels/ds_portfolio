"""
Script para crear un modelo compatible usando un enfoque diferente
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib

def create_compatible_model():
    """
    Crea un modelo asegurando compatibilidad
    """
    print("🔄 Generando datos de entrenamiento...")
    
    # Datos de ejemplo realistas
    np.random.seed(42)
    n_samples = 1000
    
    # Features con distribuciones realistas
    data = {
        'metros_totales': np.random.normal(120, 40, n_samples).clip(30, 300),
        'metros_construidos': np.random.normal(100, 35, n_samples).clip(25, 250),
        'dormitorios': np.random.randint(1, 6, n_samples),
        'banos': np.random.randint(1, 5, n_samples),
        'estacionamientos': np.random.randint(0, 4, n_samples),
        'antiguedad_anos': np.random.exponential(10, n_samples).clip(0, 40),
        'indice_ubicacion': np.random.normal(50, 15, n_samples).clip(20, 100)
    }
    
    X = pd.DataFrame(data)
    
    # Generar precios realistas (UF)
    precio_base = data['indice_ubicacion'] * 2
    y = (
        precio_base * X['metros_construidos'] * 0.8 +
        X['dormitorios'] * 500 +
        X['banos'] * 300 +
        X['estacionamientos'] * 200 -
        X['antiguedad_anos'] * 15 +
        np.random.normal(0, 500, n_samples)
    ).clip(1000, 20000)
    
    print("✓ Datos generados")
    
    # Preparar datos
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    print("🔄 Entrenando modelo...")
    
    # Usar configuración específica para compatibilidad
    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=4,
        random_state=42,
        bootstrap=True,
        n_jobs=1  # Importante para consistencia
    )
    
    model.fit(X_scaled, y)
    print("✓ Modelo entrenado")
    
    return model, scaler, X.columns.tolist()

def save_model_data(model, scaler, feature_names):
    """Guarda el modelo y datos relacionados"""
    save_paths = [
        Path('app/models'),
        Path('app/data/processed'),
        Path('app/data/inmobiliario')
    ]
    
    print("\n🔄 Guardando archivos...")
    
    model_info = {
        'feature_names': feature_names,
        'n_features': len(feature_names),
        'n_estimators': model.n_estimators,
        'max_depth': model.max_depth,
        'version': 'v2'
    }
    
    for path in save_paths:
        path.mkdir(parents=True, exist_ok=True)
        
        # Guardar modelo y scaler
        joblib.dump(model, path / 'modelo_inmobiliario.pkl', compress=3)
        joblib.dump(scaler, path / 'scaler_inmobiliario.pkl', compress=3)
        
        # Guardar información adicional
        with open(path / 'model_info.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(model_info, f, indent=2)
        
        print(f"✓ Archivos guardados en: {path}")
    
    return model_info

def test_model(model, scaler):
    """Prueba el modelo con algunos casos de uso"""
    print("\n🔄 Probando modelo...")
    
    test_cases = [
        {
            'metros_totales': 120,
            'metros_construidos': 100,
            'dormitorios': 3,
            'banos': 2,
            'estacionamientos': 1,
            'antiguedad_anos': 5,
            'indice_ubicacion': 60
        },
        {
            'metros_totales': 200,
            'metros_construidos': 180,
            'dormitorios': 4,
            'banos': 3,
            'estacionamientos': 2,
            'antiguedad_anos': 2,
            'indice_ubicacion': 80
        }
    ]
    
    for caso in test_cases:
        X_test = pd.DataFrame([caso])
        X_scaled = scaler.transform(X_test)
        prediction = model.predict(X_scaled)[0]
        
        print(f"\nCaso de prueba:")
        print(f"- {caso['metros_construidos']}m² construidos")
        print(f"- {caso['dormitorios']} dormitorios, {caso['banos']} baños")
        print(f"Precio predicho: {prediction:,.0f} UF")

if __name__ == "__main__":
    print("\n🚀 Iniciando proceso de creación de modelo...\n")
    
    model, scaler, feature_names = create_compatible_model()
    model_info = save_model_data(model, scaler, feature_names)
    test_model(model, scaler)
    
    print("\n✨ Proceso completado con éxito!")
