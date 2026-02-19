"""
Script para regenerar modelos usando scikit-learn 1.3.2
"""
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import json

def generate_synthetic_data():
    """Genera datos sintéticos para el entrenamiento"""
    np.random.seed(42)
    n_samples = 1000

    # Características
    comunas = ['Las Condes', 'Providencia', 'Ñuñoa', 'Santiago Centro', 'Vitacura', 
              'La Reina', 'Maipú', 'La Florida', 'Puente Alto', 'Conchalí', 
              'Huechuraba', 'Independencia', 'Recoleta', 'Macul', 'San Miguel']

    tipos_propiedad = ['Casa', 'Departamento']

    data = {
        'comuna': np.random.choice(comunas, n_samples),
        'tipo_propiedad': np.random.choice(tipos_propiedad, n_samples),
        'metros_totales': np.random.normal(120, 50, n_samples).clip(30, 300),
        'metros_construidos': np.random.normal(90, 40, n_samples).clip(25, 250),
        'dormitorios': np.random.randint(1, 6, n_samples),
        'banos': np.random.randint(1, 5, n_samples),
        'estacionamientos': np.random.randint(0, 4, n_samples),
        'antiguedad_anos': np.random.randint(0, 40, n_samples),
        'piso': np.random.randint(1, 25, n_samples),
        'orientacion': np.random.choice(['Norte', 'Sur', 'Este', 'Oeste', 'Nororiente', 'Norponiente', 'Suroriente', 'Surponiente'], n_samples),
        'gastos_comunes': np.random.normal(120000, 50000, n_samples).clip(50000, 300000),
        'cercania_metro': np.random.choice([True, False], n_samples),
        'ascensor': np.random.choice([True, False], n_samples)
    }

    df = pd.DataFrame(data)

    # Ajustes de datos
    df['metros_construidos'] = df.apply(lambda x: min(x['metros_construidos'], x['metros_totales']), axis=1)
    df.loc[df['tipo_propiedad'] == 'Casa', 'piso'] = 1
    df.loc[df['tipo_propiedad'] == 'Casa', 'ascensor'] = False
    
    # Generar precios (variable objetivo)
    base_price = 3000  # UF por metro cuadrado base
    df['precio'] = df.apply(lambda x: calculate_price(x, base_price), axis=1)
    
    return df

def calculate_price(row, base_price):
    """Calcula el precio de una propiedad basado en sus características"""
    price = row['metros_construidos'] * base_price
    
    # Ajustes por comuna
    comuna_factors = {
        'Las Condes': 1.5, 'Vitacura': 1.6, 'Providencia': 1.4,
        'Ñuñoa': 1.2, 'La Reina': 1.3, 'Santiago Centro': 1.1,
        'Maipú': 0.8, 'La Florida': 0.9, 'Puente Alto': 0.7,
        'Conchalí': 0.7, 'Huechuraba': 0.9, 'Independencia': 0.8,
        'Recoleta': 0.8, 'Macul': 0.9, 'San Miguel': 1.0
    }
    price *= comuna_factors.get(row['comuna'], 1.0)
    
    # Otros ajustes
    if row['cercania_metro']:
        price *= 1.1
    if row['tipo_propiedad'] == 'Casa':
        price *= 1.2
    if row['ascensor']:
        price *= 1.05
    
    # Añadir algo de ruido aleatorio
    price *= np.random.normal(1, 0.1)
    
    return price

def prepare_features(df):
    """Prepara las características para el entrenamiento"""
    # One-hot encoding para variables categóricas
    df_encoded = pd.get_dummies(df, columns=['comuna', 'tipo_propiedad', 'orientacion'])
    
    # Convertir booleanos a int
    df_encoded['cercania_metro'] = df_encoded['cercania_metro'].astype(int)
    df_encoded['ascensor'] = df_encoded['ascensor'].astype(int)
    
    # Separar features y target
    y = df_encoded['precio']
    X = df_encoded.drop('precio', axis=1)
    
    return X, y

def train_and_save_models():
    """Entrena y guarda los modelos usando scikit-learn 1.3.2"""
    print("Cargando datos...")
    X, y = load_data()
    
    # Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print("Entrenando modelos...")
    
    # Entrenar StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Entrenar DecisionTreeRegressor
    dt_model = DecisionTreeRegressor(random_state=42)
    dt_model.fit(X_train_scaled, y_train)
    
    # Entrenar RandomForestRegressor
    rf_model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Calcular y guardar métricas
    dt_score = dt_model.score(X_test_scaled, y_test)
    rf_score = rf_model.score(X_test_scaled, y_test)
    
    # Crear directorio para modelos si no existe
    models_dir = Path(__file__).parent.parent / "app" / "data" / "modelos"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    print("Guardando modelos...")
    
    # Guardar modelos
    joblib.dump(dt_model, models_dir / "decision_tree.joblib")
    joblib.dump(rf_model, models_dir / "random_forest.joblib")
    joblib.dump(scaler, models_dir / "scaler.joblib")
    
    # Guardar información de versiones y métricas
    model_info = {
        "sklearn_version": "1.3.2",
        "metrics": {
            "decision_tree_r2": dt_score,
            "random_forest_r2": rf_score
        },
        "feature_names": list(X.columns),
        "training_date": pd.Timestamp.now().isoformat()
    }
    
    with open(models_dir / "model_info.json", "w") as f:
        json.dump(model_info, f, indent=2)
    
    print("Modelos guardados exitosamente!")
    print(f"DecisionTree R2 Score: {dt_score:.4f}")
    print(f"RandomForest R2 Score: {rf_score:.4f}")

if __name__ == "__main__":
    try:
        train_and_save_models()
    except Exception as e:
        print(f"Error al entrenar modelos: {str(e)}")
        raise
